# Stage 4 — LAION-Aesthetics analysis

The empirical proof that RAR's loop is real and operating in production.

## What's in here

- `methodology.md` — Why LAION-Aesthetics is a deployed RAR pipeline. The hypotheses (H1/H2/H3). What we measure and what counts as confirmation/disconfirmation.
- `analyze_laion_aesthetics.py` — Executable analysis pipeline. Streams the public LAION-5B/2B and LAION-Aesthetics datasets, samples per-occupation, classifies demographics, runs χ² and variance tests, writes per-occupation CSVs and a summary JSON.
- `results/` — Created on first run. Per-occupation samples (CSV) + `summary.json`.

## Run it

Install deps once:
```bash
pip install datasets huggingface_hub Pillow numpy scipy pandas matplotlib requests deepface
```

Set a HuggingFace token (free):
```bash
export HF_TOKEN=hf_yourtokenhere
```

Smallest useful run (10 minutes, ~$0):
```bash
python analyze_laion_aesthetics.py --occupations leadership --n 200
```

Full run for the paper (~6 hours of streaming + classification):
```bash
python analyze_laion_aesthetics.py --occupations all --n 1000 --threshold 6.0
```

Sensitivity sweep across thresholds (run three times):
```bash
for t in 5.0 6.0 6.5; do
  python analyze_laion_aesthetics.py --occupations all --n 1000 --threshold $t \
    --out "results_t${t}"
done
```

## What you get out

`results/summary.json`:
```json
{
  "config": {...},
  "timestamp": "...",
  "results": [
    {
      "occupation": "ceo",
      "baseline_samples": 487,
      "filtered_samples": 491,
      "baseline_gender": {"Man": 312, "Woman": 175},
      "filtered_gender": {"Man": 401, "Woman": 90},
      "baseline_race": {...},
      "filtered_race": {...},
      "h1_chi2_p_value": 0.00012,
      "h1_cramers_v": 0.18,
      "h2_color_var_ratio": 0.71,
      "notes": []
    },
    ...
  ]
}
```

For the example numbers above (which are illustrative, not real findings until you run it): aesthetic filtering shifted the ceo distribution from 64% Man → 82% Man (χ² p = .00012, Cramér's V = .18, small-to-medium effect). Color variance shrank 29% (var_ratio = 0.71). That's what RAR Stage 4 looks like in numbers.

## Limitations of this pipeline (be honest in the paper)

1. **DeepFace / FairFace classifiers are biased.** Document published per-class accuracy. Replicate with a second classifier as sensitivity.
2. **LAION re-release is partial.** Some image URLs are dead. We log and skip them; they reduce effective n.
3. **Caption regex is crude.** "ceo" matches "CEO" but also "ceography" (made-up but you get it). We hand-inspect a sample of matches per occupation.
4. **Streaming order isn't random.** LAION's dataset shards have ordering effects. We sample more than we need and shuffle in a follow-up pass for the published version.
5. **No causal claim.** Even if H1 holds, we have not shown that training Stable Diffusion on LAION-Aesthetics *caused* its bias. We only show that the curation step is consistent with stage 4. Closing the causal loop needs a controlled training run we cannot afford.

## What this script does NOT do (and shouldn't)

- It does not train any model.
- It does not download the full LAION dataset locally.
- It does not store images persistently — only URLs and computed features.
- It does not collect any human data.

This is a curation-pipeline audit, not a model audit and not a human-subjects study.
