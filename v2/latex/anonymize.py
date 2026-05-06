"""Produce a double-blind-anonymized copy of main.tex.

Run: python anonymize.py
Output: main_anonymized.tex (next to main.tex)

Why a script and not a hand-edited duplicate: every time you revise main.tex
you'd have to remember to re-strip in two places. This way the anonymous
version is regenerable from the canonical source.

What it strips:
  - \author{...} blocks (replaces with anonymous \author{Anonymous Authors})
  - \affiliation{...} blocks (replaces with anonymous institution)
  - \email{...} lines (removed)
  - \shortauthors (replaced with "Anonymous")
  - The "Author Contributions" section (kept but stripped of P.A.P. / A.N. / A.H. → "Author 1 / 2 / 3")
  - The acknowledgments section (replaced with placeholder)
  - First-person institutional self-references ("MGRS 2026", "University of Toledo")
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "main.tex"
DST = HERE / "main_anonymized.tex"


def anonymize(src: str) -> str:
    s = src

    # Replace the entire author block (\author through \shortauthors) with one
    # anonymous block. Match from the first \author{ to the \shortauthors line
    # inclusive.
    author_block = re.compile(
        r"\\author\{[^}]*\}.*?\\renewcommand\{\\shortauthors\}\{[^}]*\}",
        re.DOTALL,
    )
    s = author_block.sub(
        r"\\author{Anonymous Authors}\n"
        r"\\affiliation{%\n"
        r"  \\institution{Anonymous Institution}\n"
        r"  \\country{}\n"
        r"}\n"
        r"\\renewcommand{\\shortauthors}{Anonymous}",
        s,
    )

    # Strip CRediT roles down to anonymous
    s = re.sub(r"\\textbf\{P\.A\.P\.\}", r"\\textbf{Author 1}", s)
    s = re.sub(r"\\textbf\{A\.N\.\}", r"\\textbf{Author 2}", s)
    s = re.sub(r"\\textbf\{A\.H\.\}", r"\\textbf{Author 3}", s)
    s = re.sub(r"P\.A\.P\.", "Author 1", s)
    s = re.sub(r"A\.N\.", "Author 2", s)
    s = re.sub(r"A\.H\.", "Author 3", s)

    # Replace the acknowledgments block with an anonymized placeholder
    s = re.sub(
        r"\\begin\{acks\}.*?\\end\{acks\}",
        r"\\begin{acks}\n"
        r"Anonymized for double-blind review.\n"
        r"\\end{acks}",
        s,
        flags=re.DOTALL,
    )

    # Replace identifying institutional/event self-refs
    replacements = [
        (r"University of Toledo", r"[anonymized institution]"),
        (r"MGRS 2026", r"[prior venue, anonymized]"),
        (r"Midwest Graduate Research Symposium 2026", r"[prior venue, anonymized]"),
        (r"BAUST", r"[anonymized institution]"),
        (r"Dr\.~Fayeq Jeelani Syed", r"[anonymized advisor]"),
        (r"Dr\.\\ Fayeq Jeelani Syed", r"[anonymized advisor]"),
        (r"Dr\.~Abu Saleh Musa Miah", r"[anonymized advisor]"),
        (r"Dr\.\\ Abu Saleh Musa Miah", r"[anonymized advisor]"),
        (r"\(MGRS 2026\)", r"(prior venue, anonymized)"),
    ]
    for pat, repl in replacements:
        s = re.sub(pat, repl, s)

    # Hide the companion citation if it would dox us via repo URL
    s = re.sub(
        r"\\cite\{rar2026companion\}",
        r"\\cite{anonCompanion}",
        s,
    )

    # Drop first-person plural in the Author Contributions section header text
    # if needed (we keep the section structurally for word-count balance)

    # Add the obligatory anonymization-banner header comment
    banner = (
        "% ============================================================\n"
        "% ANONYMIZED FOR DOUBLE-BLIND REVIEW\n"
        "% This file is produced by anonymize.py from main.tex.\n"
        "% Do NOT submit main.tex to a double-blind venue. Submit this.\n"
        "% After acceptance, the camera-ready version reverts to main.tex.\n"
        "% ============================================================\n"
    )
    s = banner + s

    return s


def main() -> int:
    if not SRC.exists():
        sys.stderr.write(f"main.tex not found at {SRC}\n")
        return 1
    out = anonymize(SRC.read_text(encoding="utf-8"))
    DST.write_text(out, encoding="utf-8")
    print(f"wrote {DST.relative_to(HERE.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
