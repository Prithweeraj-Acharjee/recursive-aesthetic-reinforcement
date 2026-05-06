# RAR v2 — *We Are Trapped in RAR*

A research program. Not a paper.

## What this is

The pilot study at `d:\rar\` proposed **Recursive Aesthetic Reinforcement (RAR)** — a 4-stage feedback loop in which generative AI's biased outputs are recognized, redistributed, and reingested by humans, hardening the bias each cycle. The pilot proved stages 1 and 2 with statistical rigor (n=20 images, n=17 participants, CEO recognition at p=.0001, OR=7.20). It did not prove the loop.

This v2 program turns RAR from a pilot framework into a **publishable theory at the level of "On the Dangers of Stochastic Parrots"** (Bender, Gebru, McMillan-Major, Shmitchell, FAccT 2021). That bar is intentional. The pieces:

| File | Role | Status |
|---|---|---|
| `01_paper_draft.md` | The main paper. Title: *"We Are Trapped in RAR: How Human Selection Hardens Generative AI Bias."* Synthesis-heavy, framework-first, declarative-condition framing. | drafted |
| `02_pre_registration.md` | OSF-compatible pre-registration for the n=400 image / n=100+ participant replication. | drafted |
| `03_methods_replication.md` | Full empirical methodology — sampling, instruments, analysis, IRB. | drafted |
| `04_stage4_laion/` | The empirical Stage-4 evidence. Methodology + Python analysis pipeline. | drafted |
| `05_publication_plan.md` | Where to submit, when, with what scope. | drafted |

## The lineage we're entering

The literature already has adjacent work. We must **claim our differentiator explicitly, in the first paragraph of the paper**, or reviewers will say "isn't this just X?":

- **Source Echo Chamber** — Zhou et al. 2024 — recommender-AIGC feedback. *Differentiator:* recommender layer, not training-data layer.
- **Lock-in Hypothesis** — Qiu et al. 2025 — LLM-belief reinforcement via agent simulation. *Differentiator:* belief stagnation, not representational collapse.
- **Anti-Ouroboros** — Adapala 2025 — selective feedback can *reverse* collapse. *Differentiator:* mathematical resilience, not human selection mechanism.
- **Aesthetic Assimilation** — Guo et al. 2025 — reward models enforce conventional aesthetics. *Differentiator:* reward-model side, not user-selection side. RAR sits one layer earlier in the pipeline.
- **Stable Bias** — Luccioni, Akiki, Mitchell, Jernite 2023 — Hugging Face team's 96K-image study. *Differentiator:* static measurement of bias, not dynamic feedback dynamics.
- **Model Collapse** — Shumailov 2024 (Nature) — *Differentiator:* Shumailov is *pure* self-training collapse; RAR predicts qualitatively different *representational narrowing* through *partial* human-curated reingestion.

**RAR's unique claim is the human bridge.** Echo Chamber, Lock-in, Anti-Ouroboros all model the loop with no human in it (or only a passive consumer). RAR is the only framework that says: the human is an *active selector*, and that selection is what makes the loop run.

## What "parrot-level" requires

Stochastic Parrots became canonical because it had:

1. **A creature/metaphor that became vocabulary.** "Stochastic parrots" is now everyday speech.
2. **Synthesis over empirics.** The paper's contribution was framing, not new datasets.
3. **Political/stakes claim.** Labor, climate, marginalization. It said *who* gets hurt and *how*.
4. **Differentiation from incumbents.** It explicitly named what bigger LMs do that smaller ones don't.
5. **Action items.** Documentation, energy budgets, slowing down.
6. **Authoritative reading list.** Cited semiotics, linguistics, philosophy — not just NLP.
7. **Right timing.** GPT-3 had just dropped. Climate of concern.
8. **Got the authors fired.** Controversy amplified citations. (Don't aim for this.)

RAR v2 hits 1 ("Stochastic Mirrors"), 2 (synthesis-heavy), 3 (the demographic moderation makes the stakes claim concrete), 4 (the lineage paragraph above), 5 (Section 7), 6 (we cite Crawford, Buolamwini, D'Ignazio & Klein, Noble, Benjamin alongside the bias-measurement canon), 7 (generative AI bias is the single hottest critical-AI topic of 2026).

We don't need 8.

## Author posture

This work is **co-authored with Afroza Nowshin**. The draft paper preserves that. Both names appear on every artifact in this folder.

## Reading order

If you have one hour and want to know what we're doing:
1. `01_paper_draft.md` — read the abstract + Section 1 + Section 5.
2. `04_stage4_laion/methodology.md` — read the framing.

If you have a week and want to execute:
1. `02_pre_registration.md` — file it on OSF this week.
2. `04_stage4_laion/analyze_laion_aesthetics.py` — run it locally with a LAION subset.
3. `05_publication_plan.md` — book the submission deadline.

## Honest accounting

- The pilot is solid for what it is. The replication is what makes RAR citable.
- The Stage-4 analysis is novel and tractable. We're the first to operationalize "human selection → training data" using LAION-Aesthetics as the measurable artifact.
- Parrot-level isn't guaranteed. Many good papers don't reach it. But the *shape* of RAR — synthesis + empirics + political stakes + lineage hook — is structurally the right shape. That's necessary, not sufficient.
