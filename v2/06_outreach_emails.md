# Cold-outreach email drafts

Three drafts. Send each only after the arXiv preprint URL exists. Personalize the bracketed bits before sending.

The mental model: ask for *feedback*, not endorsement. Be specific. Reference one of their papers in the first sentence. Keep under 250 words. Researchers respond to brief, well-targeted requests far more often than to vague flattery or asks.

---

## 1. Sasha Luccioni (Hugging Face)

**Why her:** Co-author of *Stable Bias* (Luccioni, Akiki, Mitchell, Jernite 2023), foundational empirical work on diffusion-model demographics. **Also co-author of Fair Diffusion** (Friedrich et al. 2023) — directly inside the curation/alignment debate RAR enters. Currently leads HF's responsible-AI work, which includes the dataset cards we critique.

```
Subject: RAR — a recursive-feedback framing of Stable Bias, would you read 1 page?

Dr Luccioni,

Stable Bias is the empirical anchor for what we've tried to do — extend
its static-demographic measurement into a dynamic feedback frame. Our
paper, "We Are Trapped in RAR: How Human Selection Hardens Generative
AI Bias" (arXiv: [link]), names the missing connective layer between
your output-side measurement and the model-collapse literature: human
selection acting on outputs and reaching the next training corpus
through curation pipelines like LAION-Aesthetics.

We propose the first audit methodology for LAION-Aesthetics V2 as a
deployed RAR-stage-4 instance. The pipeline is open-source. We have
not yet executed at scale and don't claim a result --- the paper is
the framework. We thought you of all people would have the sharpest
view on whether the framing holds and whether the audit is the right
shape.

If you have 30 minutes for a written reaction --- particularly on
whether "RAR" usefully extends the Stable-Bias frame or just renames
it --- we'd be in your debt. No quote needed, no endorsement requested.
Genuine feedback would change what the next version of this work
becomes.

Thank you for Stable Bias and Fair Diffusion --- both are the reason
we know how to write this paper at all.

Prithweeraj Acharjee Porag
University of Toledo · CSE undergraduate
[email] · [github link]
co-authors: Afroza Nowshin, Antardip Himel
```

---

## 2. Margaret Mitchell (Hugging Face)

**Why her:** Stochastic Parrots co-author. Foundational data-documentation and dataset-card work. Currently at HF, deeply embedded in the same curation-pipeline conversation. Most likely to respond to lineage-honest framings.

```
Subject: RAR (FAccT-aimed) — paper that takes Parrots seriously and asks
        what's next

Dr Mitchell,

We've written a paper that explicitly positions itself in dialogue
with "On the Dangers of Stochastic Parrots." Our claim is that
Parrots described what the model doesn't know; RAR (Recursive
Aesthetic Reinforcement) describes what happens when humans and
models know each other too well --- a recursive selection loop that
narrows the representational distribution generation over generation.

The pilot is small (n=17) but the effect sizes are large enough that
the framework is worth testing at scale. Most importantly, we name
LAION-Aesthetics V2 as a deployed instance of the loop's stage 4 ---
the first time, as far as we can find, that human-rated -> trained-
predictor -> curated-corpus -> trained-model has been treated as one
auditable pipeline.

Paper: [arXiv link]
Repo (manuscript + replication pre-reg + LAION pipeline):
[github link]

We're not asking for endorsement. We're asking: did we get the
lineage-to-Parrots right? Is the differentiation paragraph in
Section 2 honest? If you have 20 minutes for a written reaction at
any time before mid-2027, it would shape the v3.

Thank you for Parrots. It is part of how we learned to write
critically about systems we use.

Prithweeraj Acharjee Porag
University of Toledo · CSE undergraduate
[email] · co-authors: Afroza Nowshin, Antardip Himel
```

---

## 3. Patrick Schramowski (TU Darmstadt / Hessian.AI)

**Why him:** Lead author on Fair Diffusion. Works on the *intervention* side of generative-bias --- exactly where RAR's prescriptions in Section 7 land. His group could replicate or extend our LAION-Aesthetics audit at scale, faster than we can.

```
Subject: RAR --- could Fair Diffusion's intervention frame extend to
        stage-4 curation?

Dr Schramowski,

Fair Diffusion intervenes at the model side. Our paper proposes the
first audit of the *training-corpus side* of the same loop --- the
LAION-Aesthetics V2 pipeline that fed Stable Diffusion v1.5. We
hypothesize that the human-rated aesthetic predictor amplifies the
demographic stereotypes that Fair Diffusion observes downstream and
intervenes against.

Paper: "We Are Trapped in RAR: How Human Selection Hardens Generative
AI Bias" --- [arXiv link]
Methodology + analysis pipeline: [github link]/v2/04_stage4_laion/

Two specific questions where your group's experience would dwarf ours:

1. Is the audit methodology sound? Specifically the per-occupation
   captioning/regex match, the predictor-threshold sensitivity at
   5.0/6.0/6.5, and the use of FairFace/DeepFace as proxies?

2. If H1 holds (aesthetic filtering amplifies stage-1 stereotypes),
   does Fair Diffusion's intervention frame extend to the curation
   layer --- a "fair filtering" companion to fair generation?

The v3 of this work would be much stronger if you'd react to either.

Prithweeraj Acharjee Porag
University of Toledo
[email] · co-authors: Afroza Nowshin, Antardip Himel
```

---

## Sending strategy

- **Wait until the arXiv preprint is up.** Researchers are 5x more likely to read a paper with a stable URL than a Google Doc.
- **Send one at a time, 4 days apart.** If Luccioni or Mitchell replies, mention that briefly to the next contact: *"Sasha Luccioni's reaction was X — wanted to ask you about Y in light of that."* This is honest network-building, not name-dropping.
- **Don't follow up more than once.** If they don't reply in 3 weeks, accept it.
- **If they reply with criticism, thank them, integrate the strongest points, and ask if you can cite the conversation in the acks.** Most researchers will say yes if the criticism is integrated honestly.
- **If they offer to help further** (rare, valuable): ask for one specific thing. Reading the v2 is too vague; *"would you co-sign the OSF pre-registration as a methods reviewer?"* is concrete.
