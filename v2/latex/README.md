# Overleaf-ready LaTeX project for "We Are Trapped in RAR"

This folder is the LaTeX twin of [`../01_paper_draft.md`](../01_paper_draft.md). Three files:

- **`main.tex`** — the manuscript. ACM SIGCONF format (the standard for FAccT, AIES, CHI alt.chi). Compiles standalone with pdflatex + bibtex.
- **`references.bib`** — BibTeX entries for every citation.
- **`README.md`** — this file.

## Three ways to get a PDF

### Option 1 — Overleaf (recommended; ~3 minutes)

1. Sign in to [overleaf.com](https://www.overleaf.com).
2. **New Project → Upload Project**.
3. Zip up *just this folder's contents* (`main.tex` + `references.bib` only — Overleaf doesn't need this README).
4. Upload the zip. Overleaf unpacks it and opens an editor.
5. **Menu → Compiler → pdfLaTeX**. Hit **Recompile**.
6. PDF appears in the right pane.

The first compile takes ~30 seconds because Overleaf needs to fetch the `acmart` class. Subsequent compiles are instant.

### Option 2 — Overleaf via GitHub (one-click after first setup)

If you push this repo to GitHub:

1. Overleaf → **New Project → Import from GitHub**.
2. Pick the repo, select the `latex/` subfolder as the root.
3. Compile. Done.

Subsequent edits in Overleaf → "Sync to GitHub" pushes back. Or edits in your local repo → Overleaf pulls. Two-way sync.

### Option 3 — Local pdflatex

If you have a TeX distribution installed (TeX Live, MiKTeX):

```bash
cd d:/rar/v2/latex
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The triple compile is normal — first pass writes `.aux`, bibtex resolves citations, second/third passes produce the final PDF with proper cross-references.

Output: `main.pdf` in the same folder.

If you don't have a TeX distribution: install **TeX Live** (https://www.tug.org/texlive/) on Linux/macOS or **MiKTeX** (https://miktex.org/) on Windows. ~3 GB download, one-time.

## What's in the manuscript

- 10-section ACM SIGCONF paper structure
- Title: *We Are Trapped in RAR: How Human Selection Hardens Generative AI Bias*
- Co-authored: Acharjee Porag, Nowshin & Himel
- Abstract leads with the visceral "every time you choose the AI's default, you cast a vote" framing
- Section 1 epigraph ("the model works exactly as intended, and what it does is shrink the space of seeable images")
- Sections 2–8 carry the framework + pilot data + LAION methodology
- Section 5 (`\label{sec:stage4}`) is the novel empirical-methodology contribution
- 21 references in `references.bib` covering the canon (Bender, Bianchi, Luccioni, Shumailov, Crawford, Buolamwini, D'Ignazio & Klein, Noble, Benjamin, Hovy) plus the 2024–2026 active literature (Zhou Echo Chamber, Qiu Lock-in, Adapala Anti-Ouroboros, Guo Aesthetic Assimilation)

## Things to do in Overleaf before submission

1. **Verify every reference.** I generated `references.bib` from real paper titles surfaced via Hugging Face's paper search and from training-data canon. Every page number, year, and venue must be re-checked against the publisher's site. Don't trust the bib unverified.
2. **Add Afroza's affiliation/email** if different from Toledo (she's on the Toledo CS resume so the default is fine, but confirm).
3. **Strip `[nonacm]`** from `\documentclass[sigconf,nonacm]{acmart}` when you're ready for actual ACM submission. That re-enables the copyright/CCS XML block. ACM's submission portal walks you through filling those in.
4. **Add a CCS Concepts block** when ACM-submitting — Overleaf's acmart documentation has the template.
5. **Anonymize for double-blind review.** Replace the `\author{...}` blocks and `\thanks` with anonymous placeholders if the venue is double-blind (FAccT main is). AIES is single-blind; CHI alt.chi is single-blind.
6. **Add figures.** The pilot's three charts (`d:/rar/assets/chart_active.png`, `chart_gender.png`, `chart_recognition.png`) belong in Sections 4 and 7. Add `\includegraphics{...}` calls when you upload them.

## Sanity-check the PDF

Before considering it "done":

- Title appears as written (no broken acronym)
- All 21 references render in the bibliography
- No `[?]` cite markers in the body (means a `\cite{key}` doesn't match any `references.bib` entry)
- Section labels and `\ref{}` cross-references resolve
- Author block formats correctly
- No raw LaTeX commands leaking into the typeset text
