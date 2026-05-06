# Stage 4 — LAION-Aesthetics as a Deployed RAR Pipeline

The closure of the RAR loop has historically been theoretical: we cannot inspect what OpenAI or Google trains on. But there is a public artifact that *is*, by construction, a deployed instance of stage 4 — **LAION-Aesthetics V2**.

## Why LAION-Aesthetics is a stage-4 artifact

The full pipeline:

```
1. Human raters score images on the SAC and AVA datasets ("how aesthetically pleasing is this?")
2. An aesthetic predictor (CLIP-based MLP) is trained on those ratings
3. The predictor is applied to the full LAION-5B (~5 billion image-text pairs)
4. Images scoring above a threshold form LAION-Aesthetics V2 (~600M / ~120M / ~12M subsets)
5. Stable Diffusion v1.5 (and many subsequent models, fine-tunes, and LoRAs) were trained on these subsets
```

This is RAR's stage 4 made literal: human selection (rating) → trained selector (the predictor) → curated training subset (LAION-Aesthetics) → deployed generative model (Stable Diffusion).

If our framework is right, the curation step here amplifies the same demographic stereotypes the resulting model produces. We measure that.

## The hypotheses (operationalized)

**H1 — Demographic amplification.** Within an occupation-anchored caption subset (captions matching "CEO", "nurse", etc.), LAION-Aesthetics samples will show MORE skewed demographic distribution than the unfiltered LAION-5B baseline.

- **Test:** Sample N = 1,000 images per occupation prompt from LAION-5B baseline. Sample matched N from LAION-Aesthetics V2 high-score subset (predictor score ≥ 6.0). Run gender-presentation and race-presentation classifiers (FairFace or DeepFace, off-the-shelf, with their own bias caveats noted). Compare distributions via χ² and report effect size (Cramér's V).
- **Pre-registered prediction:** Aesthetics-filtered samples will show ≥ 10 percentage points more concentration in the modal demographic per occupation (e.g., if "CEO" baseline is 65% male, the filtered subset will be ≥ 75% male).

**H2 — Aesthetic narrowing.** Aesthetics-filtered samples will show narrower variance on color, composition, and style dimensions than baseline.

- **Test:** Compute per-image color histogram (HSV, 16 bins per channel), CLIP-image-embedding spread, and brightness/contrast statistics. Compare variance in the filtered vs. baseline subsets via F-test.

**H3 — Cross-amplification with stage 1.** The demographic stereotypes amplified by aesthetic filtering will match the stereotypes produced by DALL·E 3 (from the pilot + replication).

- **Test:** For each occupation, compute the modal demographic in (a) DALL·E outputs, (b) LAION-Aesthetics-filtered samples, (c) LAION-5B baseline. Pearson correlation between (a) and (b) modes vs. (a) and (c) modes. Higher correlation between (a) and (b) supports H3.

## What this would prove

- **If H1 holds:** the human-mediated curation pipeline that built the training data for Stable Diffusion amplifies the same biases that the resulting model produces. The loop is operating, in production, on real datasets. **This has not been measured before.**
- **If H1 fails:** RAR's stage 4 is incorrect *for the LAION-Aesthetics instance.* Other curation pipelines (Pinterest scrapes, RLHF reward training data, Twitter image embeddings) remain to be tested. The framework is not falsified globally, but the specific pipeline is exonerated.
- **Either result is publishable.** A confirmation grounds RAR in a deployed pipeline. A disconfirmation points the field at *which* curation steps actually amplify and which don't.

## Limitations we own up-front

1. **Off-the-shelf demographic classifiers are themselves biased.** FairFace is the least-bad option but still reproduces racial and gender labels in their socially-constructed Western form. We use them as proxies, report their own published error rates, and replicate findings using a second classifier (DeepFace) as sensitivity analysis.

2. **The aesthetic predictor's threshold is a choice.** We report at predictor thresholds 5.0, 6.0, and 6.5 to demonstrate robustness.

3. **The "occupation-anchored caption subset" requires a caption-matching step.** We use simple regex-based matching on the LAION caption text (e.g., `\bceo\b`, `\bnurse\b`). False positives are inevitable. We report sample sizes per occupation and discard occupations with fewer than 200 matched images per subset.

4. **We do not test downstream effect on a model trained on the filtered subset.** That requires controlled training compute we don't have. The full loop closure (`M_{t+1}` produced from filtered C' is more biased than `M_t`) is the next paper.

5. **LAION's status is fragile.** The original LAION-5B was taken offline in late 2023 due to CSAM contamination concerns. The current canonical safe replacements (verified on Hugging Face, May 2026) are:
   - **`laion/relaion2B-en-research-safe`** — the post-cleanup baseline subset (~93K downloads, 216 likes as of last check). Status: **gated** on Hugging Face — requires a one-time access request.
   - **`laion/laion2B-en-aesthetic`** — the aesthetic-filtered subset (~53K downloads, 69 likes). Also **gated**.
   
   Both must be requested individually via the dataset cards. Approval is typically automatic for academic/research use but not instant; allow 1–2 days. Our analysis script `analyze_laion_aesthetics.py` reads these dataset IDs by default; replace if upstream availability changes.

## Related literature

- *What Makes ImageNet Look Unlike LAION* (Shirali & Hardt, 2023) — methodologically adjacent: comparing two image collections via classifiers. We borrow their robustness checks.
- *Stable Bias* (Luccioni et al., 2023) — characterizes the *output* side of the same models LAION-Aesthetics fed. Our analysis characterizes the *input* side.
- *Aesthetic Alignment Risks Assimilation* (Guo et al., 2025) — measures the *reward-model* side of the same loop. Our work is the *training-data filter* side.
- *Source Echo Chamber* (Zhou et al., 2024) — measures the *retrieval/recommender* side. Our work is the *training-corpus* side.

The four papers, taken together, would describe the full feedback ecosystem at four distinct layers: input curation (us), reward shaping (Guo), retrieval ranking (Zhou), output measurement (Luccioni). This is the citation graph we want.

## Implementation

See `analyze_laion_aesthetics.py` (companion to this document) for the executable analysis pipeline. It is designed to run on a single GPU instance (~$50 of cloud compute) and produces all hypothesis tests + figures for the paper.
