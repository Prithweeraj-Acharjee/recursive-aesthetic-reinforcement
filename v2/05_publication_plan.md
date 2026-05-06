# Publication Plan — RAR v2

This document fixes *where* the work lands and *when*. Every other artifact in this folder is in service of these targets.

## The three-paper play

| # | Paper | Venue (target) | Submission window | Status |
|---|---|---|---|---|
| **P1** | *Stochastic Mirrors* — framework + pilot + LAION stage-4 | **AIES 2027** (deadline ~Jan 2027) OR **arXiv-as-position-paper** (any time) | Q4 2026 | drafted (`01_paper_draft.md`) |
| **P2** | Pre-registered RAR replication (n=120, 3 models, behavioral intent) | **ACM FAccT 2027** main track (deadline ~Sep 2026 for 2027 cycle) | Q3 2026 | pre-registered (`02_pre_registration.md`); needs IRB + data |
| **P3** | RAR generalization beyond images (LLM completions, recsys curation, code) | **ACM FAccT 2028** OR **CHI 2028** | Q4 2027 | sketched only |

## Why this ordering

P1 is **synthesis-heavy and empirics-light** — it can ship as soon as the LAION-Aesthetics analysis returns results. It doesn't need the n=120 replication, because its empirical contribution is the LAION analysis; it cites the pilot. This means **P1 can be on arXiv by November 2026**, claiming the framework before competitors do.

P2 is the **rigorous empirical anchor**. It refers back to P1 for the framework. Submitting P2 to FAccT main is the play that turns "framework paper" into "validated framework with replication."

P3 generalizes. Cannot be written until P1 has had time to be cited and refined.

## Backup venues

If primary venues reject:

| Primary | Backup A | Backup B |
|---|---|---|
| FAccT 2027 | AIES 2027 | EAAMO 2027 |
| AIES 2027 | NeurIPS Workshop on Algorithmic Fairness | CHI 2027 alt.chi |
| arXiv | (already on arXiv) | Patterns (Cell Press, fast review) |

Workshops also work — NeurIPS workshops on bias/fairness/responsible-AI are excellent first homes for early framings, often citation-heavy.

## Submission checklist (per paper)

- [ ] Camera-ready manuscript (anonymized for double-blind)
- [ ] Supplementary materials (data, code, OSF-pre-registration link)
- [ ] Ethics statement (FAccT requires explicit, AIES recommends)
- [ ] Conflict-of-interest disclosure
- [ ] Author photographs/bios for accepted-paper page
- [ ] arXiv preprint (after acceptance OR with venue's preprint policy)
- [ ] Twitter/Bluesky thread, 6 tweets max, lead with the metaphor + the gender finding
- [ ] Email the authors of papers we cite (Bender, Luccioni, Qiu, Adapala, Guo) with a paragraph + the PDF
- [ ] Submit to *Tech Policy Press* / *Ground Truths* / *The Verge* if the framing has policy hooks

## Promotion plan (post-acceptance)

The Stochastic Parrots template:
1. Strong title + lead-in metaphor → headlines write themselves.
2. One concrete number lay-readers can hold ("for CEO, 71% chose the AI default — for women, that dropped to 25%").
3. Co-authored thread → both authors retweet, multiplies reach.
4. Op-ed pitch to a non-academic outlet (Tech Policy Press, MIT Tech Review, The Atlantic Tech).
5. Speak at one workshop or panel within 6 months of publication.
6. Maintain the v2 GitHub repo as the canonical artifact. Pin releases.

## Co-author and advisor strategy

- **Afroza Nowshin** and **Antardip Himel** are co-authors on the v2 program. Co-author order is currently: Acharjee Porag (first), Nowshin (second), Himel (third). Decide co-first-author conventions per paper based on contribution. Default for P1: keep the current order. For P2 and P3, revisit based on who carries which workstream (replication recruitment + analysis vs. LAION pipeline vs. theory drafting).
- **Recommended faculty co-author for P2/P3:** approach Dr. Fayeq Jeelani Syed (UToledo) and/or Dr. Abu Saleh Musa Miah (BAUST) — both already cited as research mentors on Porag's resume. Faculty co-authorship (a) helps with venue acceptance, (b) provides IRB cover, (c) opens grant routes.
- **Cold outreach (post-arXiv preprint of P1):** send a 4-paragraph email to Sasha Luccioni (HF, Stable Bias author), Margaret Mitchell (HF, foundational bias work), Patrick Schramowski (Fair Diffusion). Ask for *feedback*, not endorsement. Researchers respond to specific, non-flattering, non-asking emails.

## Realistic timeline (concrete dates)

- **2026-05-15:** OSF pre-registration filed for P2.
- **2026-06-01:** IRB submission for P2.
- **2026-07-01:** Faculty co-author confirmed for P2.
- **2026-07-15:** LAION Stage-4 analysis run completed (P1 has its empirical anchor).
- **2026-08-01:** P1 draft circulated to two trusted readers (one technical, one critical-AI scholar).
- **2026-08-15:** P1 submitted to arXiv. Twitter thread.
- **2026-08-30:** IRB approved → start P2 data collection.
- **2026-09-15:** FAccT 2027 abstract deadline.
- **2026-10-15:** P2 data collection complete; analysis begins.
- **2026-11-15:** P2 manuscript draft.
- **2026-12-01:** FAccT 2027 full paper deadline.
- **2027-01-15:** AIES 2027 deadline (P1 submission).
- **2027 spring:** Notification cycle; revise + resubmit as needed.
- **2027 summer:** Begin P3 (generalization paper).

## Budget for the publication phase

| Line item | Cost |
|---|---|
| OSF storage upgrade | free tier ok |
| arXiv submission | free |
| FAccT registration (1 author, virtual) | $200 |
| AIES registration (1 author, virtual) | $200 |
| Travel if accepted in-person | $1,500–$3,000 (try for student rate + travel grant) |
| Open-access fees (FAccT and AIES are typically OA without fees) | $0 |
| **Promotion / blog post / newsletter** | $0 |

Total publication budget on top of the $2,000–$3,000 for the empirical work: **~$2,000 if virtual, ~$5,000 if travel is feasible.**

## What doing this well looks like, 18 months out

- P1 on arXiv with > 100 citations.
- P2 published at FAccT or AIES.
- "Stochastic mirrors" used as vocabulary in at least 5 other papers.
- One major-press feature mentioning the work.
- Porag and Nowshin both have a publication that helps with grad school / industry interviews.
- The framework is cited by 2+ unrelated research threads in adjacent fields (recsys, HCI, alignment) — independent uptake, not self-cite.

That's the bar. It's achievable. None of it requires luck — only the work shipping.
