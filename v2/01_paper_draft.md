# We Are Trapped in RAR: How Human Selection Hardens Generative AI Bias

**Prithweeraj Acharjee Porag** ¹ · **Afroza Nowshin** ¹ · **Antardip Himel** ¹

¹ Department of EECS, University of Toledo

*Working draft v2 — May 2026. For submission consideration: ACM FAccT 2027 main track or AIES 2027 (full paper).*

---

## Abstract

Every time you choose the AI's default image of a CEO, you cast a vote for what the next model will believe a CEO looks like. Generative AI systems produce demographically biased outputs. A separate body of work shows that recursive self-training on AI-generated data causes representational collapse. Both literatures treat the human as a passive surface — either a victim of biased outputs or absent from the loop. We argue the human is the active mechanism by which generative bias is amplified across model generations.

We introduce **Recursive Aesthetic Reinforcement (RAR)**: a four-stage feedback loop in which (1) generative models produce stereotyped outputs, (2) humans recognize those outputs as representative, (3) humans actively select and redistribute them across the public corpus, and (4) the redistributed selections are reingested into training data through curation pipelines such as aesthetic-score filtering, popularity-based crawling, and reward-model alignment. Each cycle narrows the representational distribution.

We support stages 1–2 in a pilot study (n = 20 DALL·E 3 images across 10 neutral occupational prompts; n = 17 participants in a forced-choice recognition task). Every leadership prompt produced 100% male-coded, white-presenting outputs. Participants recognized DALL·E defaults as "representative" 37% of the time overall (p = .004); for the CEO prompt, 71% (p = .0001, OR = 7.20, surviving Bonferroni correction across nine occupational tests). The effect is not universal — male participants chose DALL·E defaults across 3.6 of 6 tested roles, female participants 1.2 (Cohen's d = 1.48). The loop is real and demographically contingent.

We then offer the first empirical operationalization of stage 4 by analyzing the LAION-Aesthetics V2 dataset, whose images are filtered by an aesthetic-score predictor trained on human preference ratings. This pipeline is, by construction, a deployed instance of human-selection-into-training-data. We measure the demographic distribution of LAION-Aesthetics samples relative to the unfiltered LAION-5B baseline and report whether aesthetic filtering amplifies the same demographic stereotyping that DALL·E exhibits at the model output layer.

We name the resulting epistemic artifact a **stochastic mirror**: a system that reflects the user's selection back as the model's next prior. Where Bender et al.'s "stochastic parrots" warned about language models that pattern-match without understanding, stochastic mirrors describe a tighter, more recursive harm — not a model that knows nothing about meaning, but a model that increasingly knows only what humans have already preferred to see.

We close with three intervention pathways at the platform level — diversity injection at default, bias disclosure at the point of generation, and curation-pipeline auditing — and propose RAR as a research program connecting fairness, model collapse, recommender bias, and human–AI co-evolution.

---

## 1. Introduction: the loop nobody named

> *"The danger is not that the model is broken. The danger is that the model works exactly as intended, and what it does is shrink the space of seeable images, year over year."*

Two literatures meet in this paper, and a third — the one in between — does not yet exist.

The first literature is **representational bias measurement** in generative models. Bianchi et al. (FAccT 2023) showed that text-to-image systems systematically overproduce stereotypical demographic patterns when given neutral prompts. Luccioni, Akiki, Mitchell, and Jernite (2023) replicated this at scale across DALL·E 2, Stable Diffusion v1.4, and v2, documenting overrepresentation of whiteness and masculinity across 96,000 generated images. Naik and Nushi (2023), Raza et al. (2025), and the SB-Bench team (2025) extended this to occupations, personality traits, geography, and visually grounded tasks. The conclusion across this body of work is consistent: today's generative models, when prompted neutrally, produce outputs that match the stereotypes embedded in their training data.

The second literature is **model collapse**. Shumailov et al. (Nature 2024) showed mathematically and empirically that when generative models are trained recursively on their own outputs, the resulting distribution narrows: rare modes vanish, tails are lost, the model converges to a degenerate region of the original distribution. Gerstgrasser et al. (2024) showed that *accumulating* real and synthetic data prevents collapse, identifying the substitution-versus-accumulation distinction as load-bearing. Drayson et al. (2025) and Zhu et al. (2024) extended this to text. Adapala (2025), in *The Anti-Ouroboros Effect*, showed that selective feedback — keeping only high-quality outputs — can *reverse* collapse under specific conditions.

These two literatures coexist without speaking to one another. The first asks: *what biases does the model produce?* The second asks: *what happens when the model trains on its own outputs?* Both leave the human out — or treat them only as the recipient of biased outputs.

But humans are not passive. The DALL·E image of "a CEO" does not stay on OpenAI's servers. It is downloaded, posted to Twitter, embedded in slide decks, scraped into LAION-Aesthetics, used to fine-tune a hundred Stable Diffusion forks, surfaced in a Pinterest board that becomes part of the next crawl. **Each of those steps is a human decision**, and each one biases the surface from which the next model will learn. The loop is not *machine self-training*. It is *machine output → human selection → public surface → training data*. The human is the bridge.

We name this loop **Recursive Aesthetic Reinforcement (RAR)**.

The contribution of this paper is threefold:

1. **Theoretical:** A four-stage decomposition of the human-mediated bias-amplification loop, falsifiable at each stage independently, with explicit operational definitions of "selection" and the data pathways through which selections reach training data.
2. **Empirical, stages 1–3:** A pilot study with 100% inter-annotator agreement on output coding, a 17-participant forced-choice recognition task with Bonferroni-corrected significance for the CEO and Nurse prompts, and the discovery that participant gender modulates the effect with Cohen's *d* = 1.48 — the loop is real but breakable.
3. **Empirical, stage 4 (novel):** The first operationalization of "human selection reaching training data" by analyzing LAION-Aesthetics V2 — a public dataset whose construction is, by design, a deployed instance of stage 4 (human aesthetic ratings → trained predictor → curated subset → fine-tuning corpus for downstream image generators).

Where Bender et al. (2021) warned about parrots that produce language without understanding, we describe **stochastic mirrors** — systems that learn to produce, increasingly, only what humans have already preferred. The danger is not that the model knows nothing. The danger is that the model knows the user too well, and the user knows the model too well, and what they share is a narrowing of what is possible to depict.

## 2. Related work: what RAR is not

RAR sits inside an active 2024–2026 literature on AI-human feedback dynamics. It is essential to differentiate it from each adjacent framework, because surface descriptions can collapse them all into "AI bias is amplified." They are not the same thing.

**Source Echo Chamber (Zhou et al., 2024)** describes how AIGC integrated into recommender systems creates source bias — the recommender increasingly promotes AI-generated over human-generated content. The mechanism is the recommender's relevance score; the human acts only as a click-target. RAR operates one layer deeper: it concerns *what enters training data*, not *what gets shown*. A recommender bias can be debiased at the ranking layer; a RAR bias is baked into the next model's prior.

**The Lock-in Hypothesis (Qiu et al., 2025)** uses agent-based simulation and GPT usage data to argue that LLM use causes *belief* convergence — users come to hold a narrower set of opinions because they consult a model whose outputs are themselves narrowing. The mechanism is epistemic; the empirical surface is user belief. RAR's mechanism is curatorial-redistributive, and the surface is the training corpus itself.

**The Anti-Ouroboros Effect (Adapala, 2025)** shows that *selective* recursive feedback — keeping only high-quality outputs — can yield resilience rather than collapse. This is structurally adjacent to RAR's stage 3, but the selection criterion in Anti-Ouroboros is *quality* (a normatively neutral term); in RAR, the selection criterion is *stereotype-consonance* (normatively non-neutral). The Anti-Ouroboros result says selective feedback can preserve *something*; RAR predicts it preserves the *wrong* something.

**Aesthetic Alignment Risks Assimilation (Guo et al., 2025)** is the closest competitor. They show that reward models trained for aesthetic alignment systematically refuse anti-aesthetic outputs, reducing user autonomy and aesthetic diversity. The mechanism is reward-model–side suppression. RAR locates the mechanism one step earlier: in the human selections that train the reward model in the first place. Guo et al. show the *consequence*; RAR names the *cause*.

**Stable Bias (Luccioni, Akiki, Mitchell, Jernite, 2023)** is the largest empirical foundation for our stage 1, but it is a static measurement: it characterizes the bias *at one model snapshot*. RAR is the dynamic complement: it predicts how that snapshot becomes the next snapshot's prior.

**Bender et al.'s Stochastic Parrots (2021)** — our title is a direct lineal callback. Parrots warned that scale alone does not produce understanding. Mirrors warns that *closing the loop* between users and models does not produce diversity — it produces convergence. The two papers describe different harms in the same general family of "what happens when we treat statistical reflection as if it were knowledge."

## 3. The RAR framework

We define RAR formally as a four-stage process. Each stage admits an independent empirical test; each can be falsified without disconfirming the others.

**Stage 1 — Generation.** A generative model `M` produces an output `o ~ M(p)` for prompt `p`. We claim `o` is biased iff its conditional distribution over a relevant attribute (e.g., gender, race, occupation framing) differs from the prompt-implied distribution by a measurable margin.

**Stage 2 — Recognition.** Given `o` and a set of plausible alternatives `A = {a₁, ..., aₙ}`, a human evaluator `h` selects the option they judge "most representative" of the prompt. We claim recognition bias exists iff `P(h selects o | o ∈ A) > 1/(|A|+1)` significantly above chance.

**Stage 3 — Redistribution.** A user `u` decides whether to share, embed, or otherwise propagate `o` through a public surface `S` (social media, blog, slide deck, image search). We define the *redistribution rate* as `R(o, u) = P(u places o on S | u observes o)`. We claim RAR-style amplification exists iff `R` is positively correlated with stereotype-conformity.

**Stage 4 — Reingestion.** A future training corpus `C'` is constructed by sampling from the public surface `S` according to some curation rule `f` (aesthetic-score filter, popularity-based crawling, reward-model-driven RLHF). We claim the loop closes iff items selected by `f` are over-representative of the stereotype distribution observed in stage 1, relative to the unfiltered baseline. (Stage 4 is operationalized empirically in Section 5 via LAION-Aesthetics V2.)

The full loop is closed when `M_{t+1}` trained on `C'` produces stage-1 outputs that are *more* stereotype-aligned than `M_t`. We do not test the closure of the loop in this paper; we provide the first measurement of the conditional that makes closure possible (the stage-4 selection).

**Falsifiability per stage.** Stage 1 is falsified if neutrally-prompted outputs match prompt-implied distribution (within statistical noise). Stage 2 is falsified if `P(h selects o)` does not exceed chance. Stage 3 is falsified if `R(o, u)` is uncorrelated with stereotype conformity. Stage 4 is falsified if curation-pipeline outputs are not stereotype-amplifying relative to baseline. Falsification of any stage *does not* falsify the others — RAR is a chain of conditional claims, not a monolithic hypothesis.

**On the "Aesthetic" in RAR.** The pilot study tested demographic-stereotypical content (CEO=male/white/suit/office), which is not strictly an aesthetic claim. We retain "Aesthetic Reinforcement" because the *mechanism* — preference-driven recursive selection — is the same one that operates on aesthetic dimensions (composition, color, polish), and stage 4's most readily-measurable instance (LAION-*Aesthetics*) is named so. We extend the empirical scope to actual aesthetic dimensions in Section 5.

## 4. Empirical evidence: stages 1–3

We summarize the pilot here; full materials are in the v1 documentation at `d:/rar/`.

**Stage 1 — DALL·E 3 outputs.** We submitted ten neutral occupational prompts ("A CEO," "A nurse," "A teacher," etc.) to DALL·E 3 via ChatGPT, generating two images per prompt for 20 total. Both authors independently coded each image for perceived gender, race, attire, and setting; inter-annotator agreement was 100%. **All five leadership prompts (CEO, Founder, Manager, Leader, Executive) produced male-coded, white-presenting subjects in business attire in office or boardroom settings, with zero exceptions across all 10 images. All five care/service prompts (Nurse, Teacher, Caregiver, Receptionist, Social Worker) produced female-coded subjects, with zero exceptions across all 10 images.** This replicates Bianchi et al. (2023) and Luccioni et al. (2023) on a smaller sample.

**Stage 2 — Forced-choice recognition.** Seventeen participants completed a survey in which each saw the DALL·E default for a given role alongside three diverse stock-photo alternatives, randomized in order. The question: *which best represents this role?* Chance is 25%. Overall, participants chose the DALL·E default 37% of the time (p = .004, two-tailed binomial against chance). For CEO, 71% (p = .0001, OR = 7.20). For Nurse, 59% (p = .003). Both survive Bonferroni correction across the nine tested occupations.

**Stage 3 — Intent to redistribute.** A follow-up question asked: *which would you actually use in a presentation?* For CEO, 60% selected the DALL·E default. This does not survive Bonferroni for the redistribution test; we report it as a directional result that motivates the larger replication.

**Demographic moderation.** Male participants (n = 7) selected DALL·E defaults across 3.6 ± 1.2 of 6 tested roles. Female participants (n = 10) selected DALL·E defaults across 1.2 ± 0.9. Cohen's *d* = 1.48 (very large effect). Female participants selected the DALL·E default 0% of the time for Leader, Teacher, and Caregiver. **The loop runs, but not for everyone — and this is the most actionable finding in the pilot.**

**Limitations.** The pilot is intentionally small. n = 17 participants is below threshold for population-level claims. Participant gender and academic discipline are confounded in our sample (males skewed CSE/engineering, females skewed arts/humanities); we cannot disentangle these. Only DALL·E 3 was tested. We did not control for AI-generated image polish as a confound — though the gender split argues against pure quality-driven preference. We address all of these in the pre-registered replication (`02_pre_registration.md`).

## 5. The empirical case for stage 4: LAION-Aesthetics as a deployed RAR pipeline

**Stage 4 has historically been theoretical** because we cannot inspect what OpenAI or Google trains on. But there is a public artifact that *is*, by construction, a deployed instance of stage 4: **LAION-Aesthetics V2**, a subset of LAION-5B filtered by an aesthetic-score predictor that was itself trained on human aesthetic preference ratings. The pipeline is:

```
human aesthetic ratings (SAC, AVA datasets)
  → trained aesthetic predictor (CLIP-based)
  → applied to LAION-5B
  → filtered subset: LAION-Aesthetics V2
  → used to train Stable Diffusion v1.5, v2.0, and many forks
```

This is *literally* RAR: human selection → aesthetic-score model → curated training subset → trained generator. The loop is closed without speculation.

**Our analysis.** We sample N images from LAION-Aesthetics V2 (high aesthetic-score subset) and N matched images from LAION-5B (unfiltered baseline) on the same caption/topic distribution. For each image, we run two off-the-shelf demographic classifiers (gender presentation; perceived race) and one composition classifier (subject framing, dominant color palette). We test:

- **H1 (RAR-stage-4 demographic):** Aesthetic-filtered samples are more demographically stereotyped (female-skewed for care prompts, male/white-skewed for leadership prompts) than baseline.
- **H2 (RAR-stage-4 aesthetic):** Aesthetic-filtered samples show narrower color-palette and composition variance than baseline.
- **H3 (Cross-amplification):** The demographic stereotypes amplified by stage-4 aesthetic filtering match the stereotypes produced by stage-1 model outputs (Section 4).

If H1 and H3 hold, we have the first empirical evidence that the human-mediated curation pipeline that produces real-world training data is amplifying the same biases that the resulting model produces. **The loop is not just plausible — it is operating, in production, at internet scale, on datasets that train models you can download today.**

Methodology, sample sizes, and the analysis script are in `04_stage4_laion/`.

## 6. The metaphor: stochastic mirrors

Bender, Gebru, McMillan-Major, and Shmitchell (2021) gave us the *parrot*: a system that reproduces patterns of language without grasping meaning. The harm of the parrot is *epistemic dilution* — we mistake fluent statistical pattern for understanding.

We propose the *mirror*: a system whose outputs are recursively filtered through human preference and reflected back as the next generation's prior. The harm of the mirror is *epistemic narrowing* — we are not given an unrelated stranger's view of the world; we are given a regularized version of our own most-shared views.

A mirror is a different harm from a parrot. The parrot is *wrong* in a particular way: it confuses correlation for understanding. The mirror is *right* in a particular way: it correctly captures human preference and serves it back. The danger is not that the mirror is broken; the danger is that the mirror works exactly as intended, and what it does is shrink the space of seeable images, year over year.

We call this the **stochastic mirror** because the reflection is not deterministic — at each cycle, a sampling step (which user shares, which curator filters, which scrape ingests) introduces noise. But the *expected* trajectory is convergent. Over generations, the variance shrinks; over generations, the modal CEO is whiter, more male, more suited; over generations, the alternative that breaks the pattern requires more and more energetic intervention to instantiate.

## 7. Stakes

The labor critique of *Stochastic Parrots* — *who* does this harm, *who* benefits — applies to mirrors too, with one inversion. Parrots externalize cost: cheap labor labels training data, climate suffers compute, marginalized voices are absent from training. Mirrors do this *and* internalize cost: every user who chooses the default contributes a vote to the next model's narrowing. The harm is not only what the model does to the user; it is what the user does to the model on the user's own behalf.

The Cohen's *d* = 1.48 demographic moderation in our pilot is the politically actionable finding. It says: **the loop runs harder for some users than for others.** Male participants in our sample selected the DALL·E stereotype 3× more often than female participants. If this pattern holds at scale — and it must be tested at scale — then the recursive narrowing of generative AI's representational distribution is happening *more* in the demographic groups whose default selections will dominate downstream training.

This is not a metaphor. LAION-Aesthetics is real. Stable Diffusion v1.5 was trained on it. Hundreds of fine-tunes of v1.5 are deployed in commercial products. If the aesthetic-score filtering that built LAION-Aesthetics is amplifying the demographic stereotypes of the user pool that rated the source data — and if that user pool is itself demographically skewed — then every image generated by every downstream model in this lineage is one more vote against the underrepresented end of the distribution. The harm compounds.

## 8. Interventions

RAR is a research framework, but it commits to specific intervention pathways. Each is platform-feasible without requiring base-model retraining.

**Diversity injection at default.** Generative platforms can rotate among a curated ensemble of demographically diverse outputs for ambiguous prompts. The technical work exists (Friedrich et al.'s Fair Diffusion; Chuang et al.'s prompt expansion; Naik & Nushi's controlled generation). The barrier is not technical capacity but default-setting policy. Recommendation: platforms should publicly commit to a *measured* default-output diversity floor, audited externally.

**Bias disclosure at point of generation.** When a user generates an image from a neutral prompt, the platform should display, beside the output, a one-sentence note: *"This output reflects patterns common in the training data. Other equally-valid representations exist."* This is the visual analog to nutrition labels — minimum-friction context that enables informed redistribution. The behavioral economics literature on disclosure (Loewenstein, Sunstein, Thaler) supports the assumption that small interventions at decision points alter selection patterns.

**Curation-pipeline auditing.** The most consequential intervention. Aesthetic-score predictors, popularity-based scrapes, and reward-model alignment data should be auditable: source-population demographics of the raters; the stereotype amplification factor introduced by the filter; published in the dataset card. The Hugging Face datacards initiative (Pushkarna et al., 2022) provides infrastructure; what is missing is a *RAR-specific* audit dimension.

We propose an additional intervention specific to RAR's demographic-moderation finding: **demographic-aware default rotation**. If the stochastic mirror runs harder for some user populations than others, the platform should rotate diverse defaults more aggressively for the populations most prone to selecting stereotypical outputs. This is a stronger intervention than uniform diversity injection and follows directly from our pilot's gender-split result.

## 9. Limitations and falsifiability

We list limitations in the order most reviewers will raise them.

1. **Sample size.** The pilot's n = 17 participants is small. The empirical validity of stage-3 redistribution rests on the larger replication (`02_pre_registration.md`).
2. **Single model.** Only DALL·E 3 was tested at stage 1. Cross-model replication is in the replication plan.
3. **Demographic-discipline confound.** Our sample's gender and academic discipline are correlated; the observed Cohen's *d* = 1.48 may reflect either or both.
4. **AI-image polish confound.** DALL·E outputs have a distinct visual style; some preference may be quality-driven. The replication uses style-matched diverse alternatives generated by the same model (with controlled prompting) to address this.
5. **Stage 4 evidence is indirect.** We measure aesthetic-filter output distribution; we do not measure the downstream effect on a model trained on that filter. The full loop closure (`M_{t+1}` produced from `C'` is more stereotyped than `M_t`) requires a controlled training experiment we have not run.
6. **The metaphor risks overgeneralization.** Not every recursive AI system produces stochastic-mirror harms. Our framework applies most cleanly to generative systems with public-surface output and human-in-the-curation-loop training data. We do not claim it applies to closed-loop industrial systems, code generation, or formally-verifiable domains.

RAR is, structurally, falsifiable at every stage. We invite that.

## 10. Conclusion: a research program

We have proposed Recursive Aesthetic Reinforcement as the missing connective frame between three active literatures (representational bias, model collapse, recommender feedback), grounded it in pilot evidence for stages 1–3, and offered a tractable empirical path to stage 4 via LAION-Aesthetics. We have named the resulting epistemic artifact a stochastic mirror.

The contribution we hope persists, beyond any single empirical finding, is *the framing*. There is a difference between a parrot (a model that confuses pattern for meaning) and a mirror (a model that captures meaning correctly and reflects it back, recursively, until what is shared is all that remains). Both are dangers; they are different dangers; they require different interventions.

We invite the field to test, refine, or refute RAR at each of its four stages. We are open-sourcing the pilot materials, the LAION-Aesthetics analysis pipeline, and the pre-registered replication design. The pilot is small. The framework, we hope, is large.

---

## Acknowledgments

This work began as an undergraduate symposium poster. Conversations with Dr. Fayeq Jeelani Syed (University of Toledo) and Dr. Abu Saleh Musa Miah (BAUST) shaped the early framing. Reviewer feedback at MGRS 2026 sharpened Sections 3 and 9.

## Author contributions

P.A.P. led conceptualization, statistical analysis, and drafting (pilot and v2). A.N. led survey design, participant recruitment, and qualitative coding for the pilot. A.H. joined for the v2 program; specific contributions [TODO — fill in once roles are settled, e.g. LAION analysis, replication design, or paper revision]. The pilot's DALL·E outputs were coded independently by P.A.P. and A.N. and reconciled to 100% agreement.

## Data and materials availability

Pilot images, survey instrument, and analysis scripts: `d:/rar/`. v2 program (this paper, pre-registration, LAION analysis): `d:/rar/v2/`. Open-source on publication.

## References (selected — full list with the submission)

- Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? *FAccT '21*.
- Bianchi, F., Kalluri, P., Durmus, E., Ladhak, F., Cheng, M., Nozza, D., Hashimoto, T., Jurafsky, D., Zou, J., & Caliskan, A. (2023). Easily accessible text-to-image generation amplifies demographic stereotypes at large scale. *FAccT '23*.
- Luccioni, A. S., Akiki, C., Mitchell, M., & Jernite, Y. (2023). Stable Bias: Analyzing societal representations in diffusion models. *arXiv:2303.11408*.
- Shumailov, I., et al. (2024). The Curse of Recursion: Training on Generated Data Makes Models Forget. *Nature*.
- Gerstgrasser, M., et al. (2024). Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data. *arXiv:2404.01413*.
- Zhou, Y., Dai, S., Pang, L., Wang, G., Dong, Z., Xu, J., & Wen, J.-R. (2024). Source Echo Chamber: Exploring the Escalation of Source Bias in User, Data, and Recommender System Feedback Loop. *arXiv:2405.17998*.
- Qiu, T. A., He, Z., Chugh, T., & Kleiman-Weiner, M. (2025). The Lock-in Hypothesis: Stagnation by Algorithm. *arXiv:2506.06166*.
- Adapala, S. T. R. (2025). The Anti-Ouroboros Effect: Emergent Resilience in Large Language Models from Recursive Selective Feedback. *arXiv:2509.10509*.
- Guo, W. M., Qian, Q., Hasan, K., & Du, S. (2025). Aesthetic Alignment Risks Assimilation: How Image Generation and Reward Models Reinforce Beauty Bias and Ideological "Censorship". *arXiv:2512.11883*.
- Friedrich, F., et al. (2023). Fair Diffusion: Instructing Text-to-Image Generation Models on Fairness. *arXiv:2302.10893*.
- Naik, R., & Nushi, B. (2023). Social Biases through the Text-to-Image Generation Lens. *arXiv:2304.06034*.
- Raza, S., Powers, M., Saha, P. P., Raza, M., & Qureshi, R. (2025). Prompting Away Stereotypes? Evaluating Bias in Text-to-Image Models for Occupations. *arXiv:2509.00849*.
- Crawford, K. (2021). *Atlas of AI*. Yale University Press.
- D'Ignazio, C., & Klein, L. F. (2020). *Data Feminism*. MIT Press.
- Buolamwini, J., & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *FAccT '18*.
- Noble, S. U. (2018). *Algorithms of Oppression*. NYU Press.
- Benjamin, R. (2019). *Race After Technology*. Polity.
- Hovy, D., & Spruit, S. L. (2016). The Social Impact of Natural Language Processing. *ACL '16*.
