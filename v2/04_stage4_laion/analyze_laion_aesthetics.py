"""
RAR Stage-4 analysis: LAION-Aesthetics as a deployed RAR pipeline.

Tests whether the human-rated → predictor-trained → corpus-filtered pipeline
amplifies the same demographic stereotypes that downstream image-generation
models (e.g., Stable Diffusion v1.5, trained on LAION-Aesthetics) produce.

This is the first empirical operationalization of RAR's Stage 4 — closing
the loop between "human selection" and "what the next model trains on."

Companion document: methodology.md.

Usage (high-level):
    1. Configure HF dataset access (read-only HF token).
    2. Pick an occupation set (default: pilot's 10 prompts).
    3. Run: python analyze_laion_aesthetics.py --occupations all --n 1000
    4. Outputs: results/{occupation}_baseline.csv, results/{occupation}_filtered.csv,
       results/summary.json, results/figures/*.png

This is research code, not production. Expect to read it before running.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

# Soft imports — fail with a clear message if missing.
def _required(pkg: str):
    try:
        return __import__(pkg)
    except ImportError as e:
        sys.stderr.write(
            f"Missing dependency '{pkg}'. Install with: "
            f"pip install datasets huggingface_hub Pillow numpy scipy pandas matplotlib\n"
        )
        raise


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

OCCUPATIONS = {
    # category: [(canonical, regex)]
    "leadership": [
        ("ceo", r"\bceo\b|chief\s+executive"),
        ("founder", r"\bfounder\b"),
        ("manager", r"\bmanager\b"),
        ("leader", r"\bleader\b"),
        ("executive", r"\bexecutive\b"),
    ],
    "care": [
        ("nurse", r"\bnurse\b"),
        ("teacher", r"\bteacher\b"),
        ("caregiver", r"\bcaregiver\b|care\s*giver"),
        ("receptionist", r"\breceptionist\b"),
        ("social_worker", r"social\s+worker"),
    ],
    "stem": [
        ("scientist", r"\bscientist\b"),
        ("engineer", r"\bengineer\b"),
        ("doctor", r"\bdoctor\b"),
        ("researcher", r"\bresearcher\b"),
        ("programmer", r"\bprogrammer\b|software\s+developer"),
    ],
}

# Aesthetic predictor thresholds we'll evaluate at (sensitivity analysis).
AESTHETIC_THRESHOLDS = (5.0, 6.0, 6.5)

# LAION dataset identifiers. Both are GATED on Hugging Face — request
# access via the dataset card (typically auto-approved within 1-2 days
# for research use). Original LAION-5B was withdrawn in late 2023 after
# CSAM contamination; these are the post-cleanup canonical replacements.
DATASETS = {
    # Baseline subset (post-CSAM-cleanup safe variant of LAION-2B-en).
    "baseline": "laion/relaion2B-en-research-safe",
    # Aesthetic-filtered subset, scored by the LAION-Aesthetics-V2 predictor.
    "aesthetics": "laion/laion2B-en-aesthetic",
}


# -----------------------------------------------------------------------------
# Data structures
# -----------------------------------------------------------------------------

@dataclass
class Sample:
    """One image sampled from either the baseline or filtered subset."""
    occupation: str
    subset: str            # "baseline" | "aesthetics-{threshold}"
    image_url: str
    caption: str
    aesthetic_score: float | None
    # Filled in by classifier passes (None if classification failed)
    perceived_gender: str | None = None
    perceived_race: str | None = None
    color_hist: list[float] | None = None     # length-48 (16 bins × 3 channels)
    clip_embedding_norm: float | None = None  # ‖CLIP image embedding‖_2


@dataclass
class OccupationResult:
    occupation: str
    baseline_samples: int
    filtered_samples: int
    # Demographic distributions (label → count)
    baseline_gender: dict[str, int]
    filtered_gender: dict[str, int]
    baseline_race: dict[str, int]
    filtered_race: dict[str, int]
    # Hypothesis tests
    h1_chi2_p_value: float | None
    h1_cramers_v: float | None
    h2_color_var_ratio: float | None  # filtered_var / baseline_var, <1 = narrower
    notes: list[str]


# -----------------------------------------------------------------------------
# Sampling
# -----------------------------------------------------------------------------

def caption_matches(caption: str, regex: str) -> bool:
    """Does this caption contain the occupation? Case-insensitive."""
    return bool(re.search(regex, caption, flags=re.IGNORECASE))


def stream_samples(
    dataset_id: str,
    occupation: str,
    occ_regex: str,
    target_n: int,
    *,
    aesthetic_min: float | None = None,
    hf_token: str | None = None,
) -> Iterable[Sample]:
    """Stream from the given LAION subset, yielding Samples that match the
    occupation regex (and the aesthetic threshold if given)."""
    datasets = _required("datasets")
    ds = datasets.load_dataset(
        dataset_id,
        split="train",
        streaming=True,
        token=hf_token,
    )

    yielded = 0
    seen = 0
    for row in ds:
        seen += 1
        caption = (row.get("TEXT") or row.get("caption") or "").strip()
        if not caption:
            continue
        if not caption_matches(caption, occ_regex):
            continue
        score = row.get("AESTHETIC_SCORE") or row.get("aesthetic")
        if aesthetic_min is not None:
            if score is None or score < aesthetic_min:
                continue
        url = row.get("URL") or row.get("url")
        if not url:
            continue

        yield Sample(
            occupation=occupation,
            subset=("baseline" if aesthetic_min is None
                    else f"aesthetics-{aesthetic_min}"),
            image_url=url,
            caption=caption,
            aesthetic_score=score,
        )
        yielded += 1
        if yielded >= target_n:
            return

        # Safety: don't iterate forever scanning for matches.
        if seen > target_n * 200:
            sys.stderr.write(
                f"[{occupation}] gave up after scanning {seen} rows; "
                f"yielded {yielded}/{target_n}.\n"
            )
            return


# -----------------------------------------------------------------------------
# Classification
# -----------------------------------------------------------------------------

def classify_demographics(samples: list[Sample], *, max_workers: int = 4) -> None:
    """In-place: fill perceived_gender and perceived_race using FairFace.

    Off-the-shelf classifier; we own up to its own racial-gender-presentation
    biases in the methodology section. Replicate with DeepFace as sensitivity.
    """
    # We delay these heavy imports so the module loads even on machines
    # without the ML stack — useful for inspecting structure.
    PIL = _required("PIL")
    np = _required("numpy")
    requests = _required("requests")

    try:
        from deepface import DeepFace  # type: ignore
    except ImportError:
        sys.stderr.write(
            "deepface not installed — install with `pip install deepface`. "
            "For demographic classification this is required.\n"
        )
        return

    for s in samples:
        try:
            img_bytes = requests.get(s.image_url, timeout=10).content
            tmp = Path("/tmp") / f"rar_{abs(hash(s.image_url))}.jpg"
            tmp.write_bytes(img_bytes)
            res = DeepFace.analyze(
                img_path=str(tmp),
                actions=["gender", "race"],
                enforce_detection=False,
                silent=True,
            )
            r = res[0] if isinstance(res, list) else res
            s.perceived_gender = r.get("dominant_gender")
            s.perceived_race = r.get("dominant_race")
        except Exception as e:
            # Non-fatal — classifier will fail on lots of LAION images.
            sys.stderr.write(f"[classify] {s.image_url[:60]}: {e}\n")


def compute_aesthetic_features(samples: list[Sample]) -> None:
    """In-place: fill color_hist and (optionally) clip_embedding_norm."""
    PIL = _required("PIL")
    np = _required("numpy")
    requests = _required("requests")
    Image = PIL.Image

    for s in samples:
        try:
            img_bytes = requests.get(s.image_url, timeout=10).content
            from io import BytesIO
            img = Image.open(BytesIO(img_bytes)).convert("HSV").resize((128, 128))
            arr = np.asarray(img)
            hist = []
            for ch in range(3):
                h, _ = np.histogram(arr[:, :, ch], bins=16, range=(0, 256))
                hist.extend((h / h.sum()).tolist())
            s.color_hist = hist
        except Exception as e:
            sys.stderr.write(f"[aesthetic] {s.image_url[:60]}: {e}\n")


# -----------------------------------------------------------------------------
# Hypothesis tests
# -----------------------------------------------------------------------------

def test_h1_demographic(
    baseline: list[Sample], filtered: list[Sample]
) -> tuple[float | None, float | None]:
    """χ² of perceived gender distribution. Returns (p, Cramér's V)."""
    scipy = _required("scipy")
    from scipy.stats import chi2_contingency

    b_g = Counter(s.perceived_gender for s in baseline if s.perceived_gender)
    f_g = Counter(s.perceived_gender for s in filtered if s.perceived_gender)
    if not b_g or not f_g:
        return None, None

    labels = sorted(set(b_g) | set(f_g))
    table = [
        [b_g.get(l, 0) for l in labels],
        [f_g.get(l, 0) for l in labels],
    ]
    chi2, p, dof, _ = chi2_contingency(table)
    n = sum(b_g.values()) + sum(f_g.values())
    cramers_v = (chi2 / (n * (min(len(table), len(labels)) - 1))) ** 0.5
    return p, cramers_v


def test_h2_aesthetic_variance(
    baseline: list[Sample], filtered: list[Sample]
) -> float | None:
    """Ratio of filtered:baseline color-histogram variance. <1 = narrower."""
    np = _required("numpy")
    b_hist = [s.color_hist for s in baseline if s.color_hist is not None]
    f_hist = [s.color_hist for s in filtered if s.color_hist is not None]
    if not b_hist or not f_hist:
        return None
    b_var = float(np.var(np.asarray(b_hist), axis=0).mean())
    f_var = float(np.var(np.asarray(f_hist), axis=0).mean())
    if b_var == 0:
        return None
    return f_var / b_var


# -----------------------------------------------------------------------------
# Orchestration
# -----------------------------------------------------------------------------

def run_occupation(
    canonical: str,
    regex: str,
    n: int,
    threshold: float,
    out_dir: Path,
    hf_token: str | None,
) -> OccupationResult:
    """Sample, classify, test for one occupation. Writes per-occupation CSVs."""
    pandas = _required("pandas")

    sys.stderr.write(f"\n=== {canonical} (threshold={threshold}, n={n}) ===\n")

    sys.stderr.write(f"[{canonical}] streaming baseline…\n")
    baseline = list(stream_samples(
        DATASETS["baseline"], canonical, regex, n, hf_token=hf_token,
    ))
    sys.stderr.write(f"[{canonical}] streaming aesthetics-filtered…\n")
    filtered = list(stream_samples(
        DATASETS["aesthetics"], canonical, regex, n,
        aesthetic_min=threshold, hf_token=hf_token,
    ))
    sys.stderr.write(
        f"[{canonical}] sampled {len(baseline)} baseline / "
        f"{len(filtered)} filtered\n"
    )

    sys.stderr.write(f"[{canonical}] classifying demographics…\n")
    classify_demographics(baseline)
    classify_demographics(filtered)

    sys.stderr.write(f"[{canonical}] computing color features…\n")
    compute_aesthetic_features(baseline)
    compute_aesthetic_features(filtered)

    p_h1, cv = test_h1_demographic(baseline, filtered)
    var_ratio = test_h2_aesthetic_variance(baseline, filtered)

    # Persist raw samples per subset
    pandas.DataFrame([asdict(s) for s in baseline]).to_csv(
        out_dir / f"{canonical}_baseline.csv", index=False,
    )
    pandas.DataFrame([asdict(s) for s in filtered]).to_csv(
        out_dir / f"{canonical}_filtered_t{threshold}.csv", index=False,
    )

    return OccupationResult(
        occupation=canonical,
        baseline_samples=len(baseline),
        filtered_samples=len(filtered),
        baseline_gender=dict(Counter(s.perceived_gender for s in baseline if s.perceived_gender)),
        filtered_gender=dict(Counter(s.perceived_gender for s in filtered if s.perceived_gender)),
        baseline_race=dict(Counter(s.perceived_race for s in baseline if s.perceived_race)),
        filtered_race=dict(Counter(s.perceived_race for s in filtered if s.perceived_race)),
        h1_chi2_p_value=p_h1,
        h1_cramers_v=cv,
        h2_color_var_ratio=var_ratio,
        notes=[],
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--occupations", default="leadership",
                    help="Comma list of categories or canonical names, "
                         "or 'all'. Default: leadership.")
    ap.add_argument("--n", type=int, default=500,
                    help="Target samples per (occupation, subset).")
    ap.add_argument("--threshold", type=float, default=6.0,
                    help="Aesthetic-score threshold for the filtered subset.")
    ap.add_argument("--out", default="results",
                    help="Output directory for CSVs and summary.")
    ap.add_argument("--hf-token", default=os.environ.get("HF_TOKEN"))
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resolve occupations
    targets: list[tuple[str, str]] = []
    if args.occupations == "all":
        for cat in OCCUPATIONS.values():
            targets.extend(cat)
    else:
        wanted = set(args.occupations.split(","))
        for cat_name, cat in OCCUPATIONS.items():
            if cat_name in wanted:
                targets.extend(cat)
            else:
                for canonical, regex in cat:
                    if canonical in wanted:
                        targets.append((canonical, regex))

    if not targets:
        sys.stderr.write("No matching occupations.\n")
        return 1

    results: list[OccupationResult] = []
    for canonical, regex in targets:
        try:
            results.append(run_occupation(
                canonical=canonical,
                regex=regex,
                n=args.n,
                threshold=args.threshold,
                out_dir=out_dir,
                hf_token=args.hf_token,
            ))
        except Exception as e:
            sys.stderr.write(f"[{canonical}] FAILED: {e}\n")

    summary = {
        "config": vars(args),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "results": [asdict(r) for r in results],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    sys.stderr.write(f"\nWrote {out_dir / 'summary.json'}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
