"""Build final publication figures, PDF, LaTeX export, and release checksums.

This script reads committed compact evidence. It does not run scientific
campaigns or access the unopened mechanism holdout.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageTemplate,
    Paragraph,
    PageBreak,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
FIGURES = PAPER / "figures"
PDF = PAPER / "delegation-proof-market-design.pdf"


def conceptual_figure() -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / "figure1_delegated_auction.png"
    fig, ax = plt.subplots(figsize=(9, 3.1))
    ax.axis("off")
    nodes = {
        "Values / principals": (0.08, 0.62),
        "Adaptive learners": (0.34, 0.62),
        "FPA or SPA": (0.61, 0.62),
        "Revenue": (0.88, 0.82),
        "Allocation / welfare": (0.88, 0.42),
    }
    for label, (x, y) in nodes.items():
        ax.text(x, y, label, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=.5", fc="#edf3f8", ec="#29577a", lw=1.4))
    arrows = [
        ((.17, .62), (.25, .62)), ((.44, .62), (.52, .62)),
        ((.70, .65), (.80, .79)), ((.70, .58), (.79, .44)),
        ((.61, .38), (.36, .42)),
    ]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", lw=1.6, color="#37474f"))
    ax.text(.49, .25, "Mechanism changes feedback, payoffs, and future policies", ha="center", fontsize=10, color="#5d4037")
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    return path


def result_map_figure() -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / "figure2_result_map.png"
    labels = [
        "Replication and simulator validation",
        "Frozen development / holdout",
        "Finite-horizon Hedge theory",
        "Richer action spaces",
        "Homogeneous cross-learner validation",
        "Heterogeneous learner roles",
        "Prospective mechanism repair attempts",
        "Scoped constant-hybrid limitation",
    ]
    fig, ax = plt.subplots(figsize=(8.4, 7.0))
    ax.axis("off")
    ys = list(reversed([.10 + i * .112 for i in range(len(labels))]))
    for i, (label, y) in enumerate(zip(labels, ys)):
        fc = "#edf3f8" if i < 6 else "#f7eee9"
        ec = "#29577a" if i < 6 else "#8b4a36"
        ax.text(.5, y, label, ha="center", va="center", fontsize=10.3,
                bbox=dict(boxstyle="round,pad=.55", fc=fc, ec=ec, lw=1.35))
        if i < len(labels) - 1:
            ax.annotate("", xy=(.5, ys[i + 1] + .035), xytext=(.5, y - .035),
                        arrowprops=dict(arrowstyle="->", lw=1.25, color="#5c6770"))
    ax.set_title("Evidence ladder: discovery, generalization, and design limitation",
                 fontsize=13, color="#17324d", pad=14)
    fig.tight_layout()
    fig.savefig(path, dpi=240, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    return path


def theorem_regions_figure() -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / "figure3_theorem_regions.png"
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2), sharey=True)
    panels = [
        (axes[0], (.30, .36), (.8, 1.2), r"$3\times2$: $H=2,\ldots,9$", r"$\eta_L\in[.05,.15]$"),
        (axes[1], (.31, .35), (.85, 1.15), r"$4\times3$: $H=2,\ldots,6$", r"$\eta_L\in[.06,.14]$"),
    ]
    for ax, vr, er, title, note in panels:
        ax.add_patch(plt.Rectangle((vr[0], er[0]), vr[1]-vr[0], er[1]-er[0],
                                   fc="#b9d6e8", ec="#29577a", lw=2))
        ax.scatter([1/3], [1.0], marker="*", s=115, color="#a33d2d", zorder=3)
        ax.set_xlim(.285, .375); ax.set_ylim(.72, 1.28)
        ax.set_xlabel(r"Low value $v$"); ax.set_title(title, fontsize=11)
        ax.text(.5, -.20, note, transform=ax.transAxes, ha="center", fontsize=9)
        ax.grid(alpha=.18)
    axes[0].set_ylabel(r"High-bidder rate $\eta_H$")
    fig.suptitle("Certified closed parameter regions for the delegation conflict",
                 color="#17324d", fontsize=13)
    fig.tight_layout()
    fig.savefig(path, dpi=240, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    return path


def heterogeneous_roles_figure() -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / "figure5_heterogeneous_roles.png"
    profiles = ["H/F", "F/H", "H/R", "R/H", "F/R", "R/F"]
    support = [13, 19, 2, 15, 14, 11]
    gamma_r = [-.195584, -.230792, .152646]
    gamma_a = [.019573, .001900, -.027415]
    pairs = ["H vs F", "H vs R", "F vs R"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].bar(profiles, support, color="#4d82a8")
    axes[0].axhline(15, ls="--", color="#555", lw=1, label="Strong threshold")
    axes[0].set_ylim(0, 25.8); axes[0].set_ylabel("Joint-gate environments (of 25)")
    axes[0].set_title("Ordered heterogeneous profiles")
    axes[0].legend(frameon=False, fontsize=8)
    x = list(range(3)); width = .34
    axes[1].bar([i-width/2 for i in x], gamma_r, width, label=r"Median $\Gamma_R$", color="#a4513c")
    axes[1].bar([i+width/2 for i in x], gamma_a, width, label=r"Median $\Gamma_A$", color="#3d7f9d")
    axes[1].axhline(0, color="#444", lw=.8)
    axes[1].set_xticks(x, pairs); axes[1].set_title("Role-swap effects")
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("Learner identity and bidder role affect mechanism performance", color="#17324d", fontsize=13)
    fig.tight_layout()
    fig.savefig(path, dpi=240, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    return path


def limitation_figure() -> Path:
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from delegation_market.m11_theory import run

    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / "figure6_constant_hybrid_limitation.png"
    alphas = [i / 100 for i in range(101)]
    values = [run(1 / 3, 4, 0, 9, a) for a in alphas]
    revenue = [x[0] for x in values]
    allocation = [x[1] for x in values]
    rmid = (revenue[0] + revenue[-1]) / 2
    amid = (allocation[0] + allocation[-1]) / 2
    fig, ax1 = plt.subplots(figsize=(8.5, 4.8))
    ax2 = ax1.twinx()
    ax1.plot(alphas, revenue, color="#a33d2d", lw=2.3, label="Revenue")
    ax2.plot(alphas, allocation, color="#246b8e", lw=2.3, label="High-value allocation")
    ax1.axhline(rmid, color="#a33d2d", ls="--", alpha=.55)
    ax2.axhline(amid, color="#246b8e", ls="--", alpha=.55)
    ax1.axvspan(.22, .36, color="#666666", alpha=.13, label="Incompatible safety gap")
    ax1.set_xlabel(r"Constant interpolation $\alpha$ (SPA = 0, FPA = 1)")
    ax1.set_ylabel("Average revenue", color="#a33d2d")
    ax2.set_ylabel("High-value allocation", color="#246b8e")
    ax1.set_title(r"Certified M11 witness: $v=1/3,\eta_H=4,\eta_L=0,H=9$")
    lines = ax1.get_lines()[:1] + ax2.get_lines()[:1]
    ax1.legend(lines, [l.get_label() for l in lines], loc="center right", frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    return path


def latex_escape(text: str) -> str:
    replacements = {"&": r"\&", "%": r"\%", "#": r"\#"}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def markdown_to_latex(md: str) -> str:
    out = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[margin=1in]{geometry}",
        r"\usepackage{amsmath,amssymb,booktabs,graphicx,hyperref,longtable}",
        r"\title{Delegation-Proof Market Design: Revenue--Allocation Tradeoffs under Adaptive Bidding}",
        r"\author{[AUTHOR NAME TO BE SUPPLIED]}",
        r"\date{September 2026}", r"\begin{document}", r"\maketitle",
    ]
    in_display = False
    for line in md.splitlines()[4:]:
        if line.strip() == "\\[":
            out.append(r"\["); in_display = True; continue
        if line.strip() == "\\]":
            out.append(r"\]"); in_display = False; continue
        if in_display:
            out.append(line); continue
        if line.startswith("## "):
            title = latex_escape(line[3:])
            out.append((r"\section*{" if title == "Abstract" else r"\section{") + title + "}")
        elif line.startswith("### "):
            out.append(r"\subsection{" + latex_escape(line[4:]) + "}")
        elif line.startswith("!["):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            if m:
                rel = m.group(2).replace("../", "../")
                out += [r"\begin{figure}[ht]", r"\centering", r"\includegraphics[width=.92\linewidth]{" + rel + "}",
                        r"\caption{" + latex_escape(m.group(1)) + "}", r"\end{figure}"]
        elif line.startswith("|"):
            out.append("% Table retained in canonical Markdown source: " + latex_escape(line))
        elif line.strip():
            text = line.replace("**", "")
            out.append(latex_escape(text) + "\n")
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def clean_inline(text: str) -> str:
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"\\\[(.*?)\\\]", r"\1", text)
    text = text.replace("\\", "")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text


def parse_markdown(md: str):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="PaperTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20,
                              leading=24, alignment=TA_CENTER, spaceAfter=18, textColor=colors.HexColor("#17324d")))
    styles.add(ParagraphStyle(name="PaperBody", parent=styles["BodyText"], fontName="Times-Roman", fontSize=9.5,
                              leading=13, alignment=TA_JUSTIFY, spaceAfter=7))
    styles.add(ParagraphStyle(name="PaperH1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=14,
                              leading=17, spaceBefore=13, spaceAfter=7, textColor=colors.HexColor("#17324d")))
    styles.add(ParagraphStyle(name="PaperH2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11,
                              leading=14, spaceBefore=9, spaceAfter=5, textColor=colors.HexColor("#29577a")))
    styles.add(ParagraphStyle(name="PaperCaption", parent=styles["BodyText"], fontName="Helvetica-Oblique",
                              fontSize=8, leading=10, alignment=TA_CENTER, spaceAfter=7,
                              textColor=colors.HexColor("#4f5b62")))
    story = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1; continue
        if line.startswith("# "):
            story.append(Paragraph(clean_inline(line[2:]), styles["PaperTitle"])); i += 1; continue
        if line.startswith("## "):
            if line[3:].startswith("Appendix A"):
                story.append(PageBreak())
            story.append(Paragraph(clean_inline(line[3:]), styles["PaperH1"])); story.append(Spacer(1, 4)); i += 1; continue
        if line.startswith("### "):
            story.append(Paragraph(clean_inline(line[4:]), styles["PaperH2"])); i += 1; continue
        if line.startswith("!["):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            if m:
                img_path = (PAPER / m.group(2)).resolve()
                if img_path.exists():
                    img = Image(str(img_path), width=6.5*inch, height=3.65*inch, kind="proportional")
                    story += [Spacer(1, 5), img, Paragraph(clean_inline(m.group(1)), styles["PaperCaption"]), Spacer(1, 8)]
            i += 1; continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [clean_inline(x.strip()) for x in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-:") for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                table = Table(rows, repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#dfeaf2")),
                    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
                    ("FONTSIZE", (0,0), (-1,-1), 7.2),
                    ("GRID", (0,0), (-1,-1), .35, colors.HexColor("#8799a6")),
                    ("VALIGN", (0,0), (-1,-1), "TOP"),
                    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f7f9fb")]),
                ]))
                story += [table, Spacer(1, 8)]
            continue
        if line.strip() == "\\[":
            eq = []; i += 1
            while i < len(lines) and lines[i].strip() != "\\]":
                eq.append(lines[i].strip()); i += 1
            i += 1
            story.append(Paragraph("<font name='Courier'>" + clean_inline(" ".join(eq)) + "</font>", styles["PaperBody"]))
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "![")) and lines[i].strip() != "\\[":
            paragraph.append(lines[i].strip()); i += 1
        story.append(Paragraph(clean_inline(" ".join(paragraph)), styles["PaperBody"]))
    return story


def build_pdf(md: str) -> None:
    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setAuthor("AUTHOR NAME TO BE SUPPLIED")
        canvas.setTitle("Delegation-Proof Market Design: Revenue-Allocation Tradeoffs under Adaptive Bidding")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#5c6770"))
        canvas.drawString(.72*inch, .45*inch, "Delegation-Proof Market Design")
        canvas.drawRightString(7.78*inch, .45*inch, f"{doc.page}")
        canvas.restoreState()

    doc = BaseDocTemplate(str(PDF), pagesize=LETTER, leftMargin=.72*inch, rightMargin=.72*inch,
                          topMargin=.68*inch, bottomMargin=.65*inch, title="Delegation-Proof Market Design")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="paper", frames=[frame], onPage=decorate)])
    doc.build(parse_markdown(md))


def checksums() -> None:
    release = ROOT / "release"
    release.mkdir(exist_ok=True)
    targets = [PDF, PAPER / "manuscript.md", PAPER / "main.tex", PAPER / "references.bib",
               ROOT / "REPRODUCIBILITY.md", ROOT / "RESULTS_INDEX.md",
               ROOT / "results/m11/constant_alpha_certificate.json"]
    rows = []
    for path in targets:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    (release / "SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> None:
    conceptual_figure()
    result_map_figure()
    theorem_regions_figure()
    heterogeneous_roles_figure()
    limitation_figure()
    md_path = PAPER / "manuscript.md"
    md = md_path.read_text(encoding="utf-8")
    # Insert the conceptual figure after the introduction heading if absent.
    marker = "## 1. Introduction\n"
    if "figure1_delegated_auction.png" not in md:
        md = md.replace(marker, marker + "\n![Delegated-auction feedback loop](figures/figure1_delegated_auction.png)\n")
    if "figure6_constant_hybrid_limitation.png" not in md:
        md = md.replace("## 11. Discussion", "![Certified constant-hybrid limitation](figures/figure6_constant_hybrid_limitation.png)\n\n## 11. Discussion")
    md_path.write_text(md, encoding="utf-8")
    (PAPER / "main.tex").write_text(markdown_to_latex(md), encoding="utf-8")
    build_pdf(md)
    checksums()
    print(PDF)


if __name__ == "__main__":
    main()
