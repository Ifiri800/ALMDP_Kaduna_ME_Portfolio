from pathlib import Path
import json
import re
import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image,
    KeepTogether,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

NOTEBOOK_PATH = (
    PROJECT_ROOT
    / "08_Analysis" 
    / "baseline_report_executed.ipynb"
)

OUTPUT_DIR = PROJECT_ROOT / "10_Reporting"

OUTPUT_PDF = (
    OUTPUT_DIR
    / "ALMDP_Baseline_Assessment_Report_2026.pdf"
)


# ============================================================
# REPORT METADATA
# ============================================================

REPORT_TITLE = (
    "Agricultural Livelihoods and MSME Development Project (ALMDP)"
)

REPORT_SUBTITLE = "Baseline Assessment Report"

LOCATION = "Kaduna State, Nigeria"

BASELINE_YEAR = "2026"

IMPLEMENTATION_PERIOD = (
    "January 2027 - December 2030"
)

BENEFICIARY_TARGET = "10,000"

FARMER_TARGET = "8,000"

MSME_TARGET = "2,000"


# ============================================================
# VALIDATE SOURCE NOTEBOOK
# ============================================================

if not NOTEBOOK_PATH.exists():
    raise FileNotFoundError(
        f"Source notebook not found: {NOTEBOOK_PATH}"
    )

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

with NOTEBOOK_PATH.open(
    "r",
    encoding="utf-8",
) as f:
    notebook = json.load(f)


# ============================================================
# REPORTLAB STYLES
# ============================================================

styles = getSampleStyleSheet()

styles.add(
    ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        alignment=TA_CENTER,
        spaceAfter=10 * mm,
    )
)

styles.add(
    ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Heading2"],
        fontName="Helvetica",
        fontSize=15,
        leading=19,
        alignment=TA_CENTER,
        spaceAfter=8 * mm,
    )
)

styles.add(
    ParagraphStyle(
        name="CoverText",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=4 * mm,
    )
)

styles.add(
    ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#17365D"),
        spaceBefore=5 * mm,
        spaceAfter=4 * mm,
        keepWithNext=True,
    )
)

styles.add(
    ParagraphStyle(
        name="SubHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#305496"),
        spaceBefore=3 * mm,
        spaceAfter=2 * mm,
        keepWithNext=True,
    )
)

styles.add(
    ParagraphStyle(
        name="BodyReport",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=3 * mm,
    )
)

styles.add(
    ParagraphStyle(
        name="BulletReport",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=13.5,
        leftIndent=6 * mm,
        firstLineIndent=-3 * mm,
        spaceAfter=1.5 * mm,
    )
)

styles.add(
    ParagraphStyle(
        name="SmallNote",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#555555"),
        spaceAfter=2 * mm,
    )
)

styles.add(
    ParagraphStyle(
        name="TableCell",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=9,
    )
)

styles.add(
    ParagraphStyle(
        name="TableHeader",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9,
        textColor=colors.white,
    )
)


# ============================================================
# BASIC MARKDOWN HELPERS
# ============================================================

def clean_markdown_text(text):
    """Convert basic Markdown formatting into ReportLab-safe text."""

    text = text.strip()

    if not text:
        return ""

    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        text,
    )

    text = re.sub(
        r"\*(.+?)\*",
        r"<i>\1</i>",
        text,
    )

    text = re.sub(
        r"`(.+?)`",
        r"<font name='Courier'>\1</font>",
        text,
    )

    text = text.replace(
        "&",
        "&amp;",
    )

    text = text.replace(
        "<b>",
        "___BOLD_OPEN___",
    )

    text = text.replace(
        "</b>",
        "___BOLD_CLOSE___",
    )

    text = text.replace(
        "<i>",
        "___ITALIC_OPEN___",
    )

    text = text.replace(
        "</i>",
        "___ITALIC_CLOSE___",
    )

    text = text.replace(
        "<font name='Courier'>",
        "___CODE_OPEN___",
    )

    text = text.replace(
        "</font>",
        "___CODE_CLOSE___",
    )

    text = text.replace(
        "<",
        "&lt;",
    )

    text = text.replace(
        ">",
        "&gt;",
    )

    text = text.replace(
        "___BOLD_OPEN___",
        "<b>",
    )

    text = text.replace(
        "___BOLD_CLOSE___",
        "</b>",
    )

    text = text.replace(
        "___ITALIC_OPEN___",
        "<i>",
    )

    text = text.replace(
        "___ITALIC_CLOSE___",
        "</i>",
    )

    text = text.replace(
        "___CODE_OPEN___",
        "<font name='Courier'>",
    )

    text = text.replace(
        "___CODE_CLOSE___",
        "</font>",
    )

    return text


def paragraph_from_markdown(
    text,
    style=None,
):
    """Create a ReportLab Paragraph from simple Markdown."""

    if style is None:
        style = styles["BodyReport"]

    return Paragraph(
        clean_markdown_text(text),
        style,
    )


# ============================================================
# MARKDOWN TABLE DETECTION
# ============================================================

def is_table_separator(line):
    """
    Detect Markdown separator rows such as:

    |---|---|---|
    """

    stripped = line.strip()

    if not stripped.startswith("|"):
        return False

    cells = [
        cell.strip()
        for cell in stripped.strip("|").split("|")
    ]

    if not cells:
        return False

    return all(
        re.fullmatch(
            r":?-{3,}:?",
            cell,
        )
        for cell in cells
    )


def parse_markdown_table(lines):
    """
    Convert Markdown table lines into:
        headers, rows
    """

    table_lines = [
        line.strip()
        for line in lines
        if line.strip()
    ]

    if len(table_lines) < 2:
        return None

    if not table_lines[0].startswith("|"):
        return None

    if not is_table_separator(
        table_lines[1]
    ):
        return None

    def split_row(line):
        return [
            cell.strip()
            for cell in line.strip("|").split("|")
        ]

    headers = split_row(
        table_lines[0]
    )

    rows = [
        split_row(line)
        for line in table_lines[2:]
        if line.strip()
    ]

    return headers, rows


# ============================================================
# REPORT TABLE BUILDER
# ============================================================

def build_report_table(
    headers,
    rows,
):
    """Create a professional ReportLab table."""

    column_count = len(headers)

    normalized_rows = []

    for row in rows:
        row = list(row)

        if len(row) < column_count:
            row.extend(
                [""] * (
                    column_count - len(row)
                )
            )

        elif len(row) > column_count:
            row = row[:column_count]

        normalized_rows.append(row)

    table_data = [
        [
            Paragraph(
                clean_markdown_text(cell),
                styles["TableHeader"],
            )
            for cell in headers
        ]
    ]

    for row in normalized_rows:
        table_data.append(
            [
                Paragraph(
                    clean_markdown_text(cell),
                    styles["TableCell"],
                )
                for cell in row
            ]
        )

    available_width = (
        A4[0]
        - 30 * mm
    )

    col_width = (
        available_width
        / max(column_count, 1)
    )

    table = Table(
        table_data,
        colWidths=[
            col_width
            for _ in range(column_count)
        ],
        repeatRows=1,
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#17365D"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor(
                        "#B7C9D6"
                    ),
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor(
                            "#F4F7FA"
                        ),
                    ],
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
            ]
        )
    )

    return table


# ============================================================
# PAGE HEADER / FOOTER
# ============================================================

def draw_page_header_footer(
    canvas,
    document,
):
    canvas.saveState()

    width, height = A4

    # Header
    canvas.setStrokeColor(
        colors.HexColor("#B7C9D6")
    )

    canvas.setLineWidth(0.5)

    canvas.line(
        15 * mm,
        height - 12 * mm,
        width - 15 * mm,
        height - 12 * mm,
    )

    canvas.setFont(
        "Helvetica",
        7.5,
    )

    canvas.setFillColor(
        colors.HexColor("#5B6573")
    )

    canvas.drawString(
        15 * mm,
        height - 9 * mm,
        "ALMDP | Baseline Assessment Report | 2026",
    )

    # Footer
    canvas.line(
        15 * mm,
        12 * mm,
        width - 15 * mm,
        12 * mm,
    )

    canvas.drawString(
        15 * mm,
        8 * mm,
        "Synthetic/Simulated M&E Portfolio Project",
    )

    canvas.drawRightString(
        width - 15 * mm,
        8 * mm,
        f"Page {document.page}",
    )

    canvas.restoreState()


# ============================================================
# BASIC NOTEBOOK INSPECTION
# ============================================================

markdown_cells = [
    cell
    for cell in notebook.get("cells", [])
    if cell.get("cell_type") == "markdown"
]

code_cells = [
    cell
    for cell in notebook.get("cells", [])
    if cell.get("cell_type") == "code"
]

print("PDF GENERATOR FOUNDATION")
print("=========================")
print(f"Notebook: {NOTEBOOK_PATH}")
print(f"Markdown cells: {len(markdown_cells)}")
print(f"Code cells: {len(code_cells)}")
print(f"Output: {OUTPUT_PDF}")
print("Table parser: READY")
print("ReportLab styles: READY")
print("PDF foundation: READY")

# ============================================================
# MARKDOWN CELL TO REPORTLAB STORY
# ============================================================

def markdown_cell_to_story(
    markdown_text,
):
    """
    Convert one notebook Markdown cell into
    ReportLab flowables.

    Handles:
    - H1/H2/H3 headings
    - paragraphs
    - bullet lists
    - blockquotes
    - Markdown tables
    """

    story = []

    lines = markdown_text.splitlines()

    i = 0

    while i < len(lines):

        raw_line = lines[i]
        line = raw_line.strip()

        # ----------------------------------------------------
        # Empty line
        # ----------------------------------------------------

        if not line:
            story.append(
                Spacer(
                    1,
                    2 * mm,
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # Markdown table
        # ----------------------------------------------------

        if (
            line.startswith("|")
            and i + 1 < len(lines)
            and is_table_separator(
                lines[i + 1]
            )
        ):

            table_lines = []

            while (
                i < len(lines)
                and lines[i].strip().startswith("|")
            ):
                table_lines.append(
                    lines[i]
                )
                i += 1

            parsed = parse_markdown_table(
                table_lines
            )

            if parsed:

                headers, rows = parsed

                story.append(
                    Spacer(
                        1,
                        2 * mm,
                    )
                )

                story.append(
                    KeepTogether(
                        [
                            build_report_table(
                                headers,
                                rows,
                            ),
                            Spacer(
                                1,
                                3 * mm,
                            ),
                        ]
                    )
                )

            continue

        # ----------------------------------------------------
        # H1
        # ----------------------------------------------------

        if line.startswith("# "):

            heading = line[2:].strip()

            story.append(
                Paragraph(
                    clean_markdown_text(
                        heading
                    ),
                    styles["SectionHeading"],
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # H2
        # ----------------------------------------------------

        if line.startswith("## "):

            heading = line[3:].strip()

            story.append(
                Paragraph(
                    clean_markdown_text(
                        heading
                    ),
                    styles["SectionHeading"],
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # H3
        # ----------------------------------------------------

        if line.startswith("### "):

            heading = line[4:].strip()

            story.append(
                Paragraph(
                    clean_markdown_text(
                        heading
                    ),
                    styles["SubHeading"],
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # H4
        # ----------------------------------------------------

        if line.startswith("#### "):

            heading = line[5:].strip()

            story.append(
                Paragraph(
                    clean_markdown_text(
                        heading
                    ),
                    styles["SubHeading"],
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # Horizontal rule
        # ----------------------------------------------------

        if re.fullmatch(
            r"[-*_]{3,}",
            line,
        ):

            story.append(
                Spacer(
                    1,
                    2 * mm,
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # Blockquote
        # ----------------------------------------------------

        if line.startswith(">"):

            quote_text = line[1:].strip()

            story.append(
                Paragraph(
                    clean_markdown_text(
                        quote_text
                    ),
                    styles["SmallNote"],
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # Bullet list
        # ----------------------------------------------------

        if re.match(
            r"^[-*+]\s+",
            line,
        ):

            bullet_text = re.sub(
                r"^[-*+]\s+",
                "",
                line,
            )

            story.append(
                Paragraph(
                    "&#8226; "
                    + clean_markdown_text(
                        bullet_text
                    ),
                    styles["BulletReport"],
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # Numbered list
        # ----------------------------------------------------

        if re.match(
            r"^\d+\.\s+",
            line,
        ):

            match = re.match(
                r"^(\d+)\.\s+(.*)",
                line,
            )

            number = match.group(1)
            item_text = match.group(2)

            story.append(
                Paragraph(
                    f"{number}. "
                    + clean_markdown_text(
                        item_text
                    ),
                    styles["BulletReport"],
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # Standalone bold line
        # ----------------------------------------------------

        if (
            line.startswith("**")
            and line.endswith("**")
        ):

            heading = line[2:-2].strip()

            story.append(
                Paragraph(
                    f"<b>{clean_markdown_text(heading)}</b>",
                    styles["BodyReport"],
                )
            )

            i += 1
            continue

        # ----------------------------------------------------
        # Normal paragraph
        # ----------------------------------------------------

        paragraph_lines = [
            line
        ]

        i += 1

        while i < len(lines):

            next_line = lines[i].strip()

            if not next_line:
                break

            if next_line.startswith(
                (
                    "# ",
                    "## ",
                    "### ",
                    "#### ",
                    ">",
                    "|",
                    "- ",
                    "* ",
                    "+ ",
                )
            ):
                break

            if re.match(
                r"^\d+\.\s+",
                next_line,
            ):
                break

            paragraph_lines.append(
                next_line
            )

            i += 1

        paragraph_text = " ".join(
            paragraph_lines
        )

        story.append(
            paragraph_from_markdown(
                paragraph_text
            )
        )

    return story


# ============================================================
# TEST MARKDOWN PARSING
# ============================================================

markdown_test_count = 0
markdown_table_count = 0
markdown_flowable_count = 0

for cell in markdown_cells:

    source = "".join(
        cell.get(
            "source",
            [],
        )
    )

    if not source.strip():
        continue

    markdown_test_count += 1

    if "|" in source:

        lines = source.splitlines()

        for index in range(
            len(lines) - 1
        ):

            if (
                lines[index].strip().startswith("|")
                and is_table_separator(
                    lines[index + 1]
                )
            ):
                markdown_table_count += 1

    flowables = markdown_cell_to_story(
        source
    )

    markdown_flowable_count += len(
        flowables
    )


print()
print("MARKDOWN REPORT PARSER")
print("======================")
print(
    f"Markdown cells parsed: "
    f"{markdown_test_count}"
)
print(
    f"Markdown tables detected: "
    f"{markdown_table_count}"
)
print(
    f"ReportLab flowables generated: "
    f"{markdown_flowable_count}"
)
print("Markdown parser: PASS")

# ============================================================
# ============================================================
# FINAL REPORT VISUALS - SECTIONS 1 TO 12
# ============================================================

FINAL_VISUALS = {
    "Section 1 Visual": {
        "section": "1",
        "caption": "Figure 1. Executive summary: project scale and baseline performance.",
    },
    "Section 2 Visual": {
        "section": "2",
        "caption": "Figure 2. Project coverage and agricultural value-chain representation.",
    },
    "Section 3 Visual": {
        "section": "3",
        "caption": "Figure 3. Project objectives and component-to-result architecture.",
    },
    "Section 4 Visual": {
        "section": "4",
        "caption": "Figure 4. Results architecture and M&E data flow.",
    },
    "Section 5 Visual": {
        "section": "5",
        "caption": "Figure 5. Baseline design and data-processing workflow.",
    },
    "Section 6 Visual": {
        "section": "6",
        "caption": "Figure 6. Respondent profile and geographic/value-chain coverage.",
    },
    "Section 7 Visual": {
        "section": "7",
        "caption": "Figure 7. Data-quality issues before cleaning and validation status after cleaning.",
    },
    "Section 8 Visual": {
        "section": "8",
        "caption": "Figure 8. Baseline indicator status and priority gaps relative to 2030 targets.",
    },
    "Section 9 Visual": {
        "section": "9",
        "caption": "Figure 9. Disaggregated baseline findings across beneficiary groups, value chains, practices, and market access.",
    },
    "Section 10 Visual": {
        "section": "10",
        "caption": "Figure 10. Indicator priority classification and highest-priority baseline gaps.",
    },
    "Section 11 Visual": {
        "section": "11",
        "caption": "Figure 11. Principal finding themes and consolidated management priorities.",
    },
    "Section 12 Visual": {
        "section": "12",
        "caption": "Figure 12. Recommendations by priority and early implementation monitoring priorities.",
    },
}


def extract_final_visuals(notebook_data):
    """
    Extract the final PNG visual from each Section 1-12
    visualization cell.
    """

    extracted = {}

    for cell in notebook_data.get(
        "cells",
        [],
    ):

        if cell.get(
            "cell_type"
        ) != "code":
            continue

        source = "".join(
            cell.get(
                "source",
                [],
            )
        )

        matched_key = None

        for visual_key in FINAL_VISUALS:

            marker_pattern = (
                rf"^\s*#\s*{re.escape(visual_key)}(?!\d)"
            )

            if re.search(
                marker_pattern,
                source,
                flags=re.MULTILINE,
            ):
                matched_key = visual_key
                break

        if matched_key is None:
            continue

        outputs = cell.get(
            "outputs",
            [],
        )

        for output in outputs:

            data = output.get(
                "data",
                {},
            )

            image_data = data.get(
                "image/png"
            )

            if image_data is None:
                continue

            if isinstance(
                image_data,
                list,
            ):
                image_data = "".join(
                    image_data
                )

            try:
                image_bytes = (
                    __import__(
                        "base64"
                    )
                    .b64decode(
                        image_data
                    )
                )
            except Exception:
                continue

            extracted[
                matched_key
            ] = {
                "image": image_bytes,
                "section": FINAL_VISUALS[
                    matched_key
                ][
                    "section"
                ],
                "caption": FINAL_VISUALS[
                    matched_key
                ][
                    "caption"
                ],
            }

            break

    return extracted


final_visuals = (
    extract_final_visuals(
        notebook
    )
)


print()
print("FINAL REPORT VISUAL EXTRACTION")
print("==============================")

for title, info in (
    final_visuals.items()
):

    print(
        f"{title} | "
        f"section={info['section']} | "
        f"bytes={len(info['image'])}"
    )

print(
    f"Final visuals found: "
    f"{len(final_visuals)}/"
    f"{len(FINAL_VISUALS)}"
)

if (
    len(final_visuals)
    != len(FINAL_VISUALS)
):
    missing = [
        title
        for title in FINAL_VISUALS
        if title not in final_visuals
    ]

    raise RuntimeError(
        "Missing final visual(s): "
        + "; ".join(missing)
    )

print("Visual extraction: PASS")

# ============================================================
# SECTION-AWARE REPORT CONTENT
# ============================================================# SECTION-AWARE REPORT CONTENT
# ============================================================

def get_section_number(markdown_text):
    """
    Extract the report section number from a Markdown
    heading such as '# 9. Disaggregated Baseline Findings'.
    """

    match = re.search(
        r"^#\s+(\d+)\.",
        markdown_text,
        flags=re.MULTILINE,
    )

    if match:
        return match.group(1)

    return None


def get_visuals_for_section(
    section_number,
):
    """
    Return approved visuals belonging to
    a specific report section.
    """

    return [
        (
            title,
            info,
        )
        for title, info
        in final_visuals.items()
        if info["section"]
        == str(section_number)
    ]


def visual_flowable(
    image_bytes,
    caption,
):
    """
    Convert PNG bytes into a centered
    report figure with caption.
    """

    image_stream = io.BytesIO(
        image_bytes
    )

    image = Image(
        image_stream,
    )

    max_width = 165 * mm
    max_height = 105 * mm

    scale = min(
        max_width / image.imageWidth,
        max_height / image.imageHeight,
        1.0,
    )

    image.drawWidth = (
        image.imageWidth * scale
    )

    image.drawHeight = (
        image.imageHeight * scale
    )

    image.hAlign = "CENTER"

    return [
        Spacer(
            1,
            3 * mm,
        ),
        image,
        Spacer(
            1,
            2 * mm,
        ),
        Paragraph(
            caption,
            ParagraphStyle(
                "FigureCaptionTemp",
                parent=styles["SmallNote"],
                alignment=TA_CENTER,
                fontSize=8,
                leading=10,
                spaceAfter=4 * mm,
            ),
        ),
    ]


def build_report_story(
    notebook_data,
):
    """
    Build the complete ReportLab story.

    The notebook is used as the source document,
    but execution/QC cells are excluded from the
    professional PDF.
    """

    story = []

    cells = notebook_data.get(
        "cells",
        [],
    )

    # --------------------------------------------------------
    # COVER
    # --------------------------------------------------------

    story.extend(
        [
            Spacer(
                1,
                30 * mm,
            ),
            Paragraph(
                REPORT_TITLE,
                styles["ReportTitle"],
            ),
            Paragraph(
                REPORT_SUBTITLE,
                styles["ReportSubtitle"],
            ),
            Paragraph(
                LOCATION,
                styles["ReportSubtitle"],
            ),
            Spacer(
                1,
                12 * mm,
            ),
            Paragraph(
                "<b>Synthetic/Simulated "
                "Monitoring &amp; Evaluation "
                "Portfolio Project</b>",
                styles["CoverText"],
            ),
            Spacer(
                1,
                5 * mm,
            ),
            Paragraph(
                f"<b>Baseline Year:</b> "
                f"{BASELINE_YEAR}",
                styles["CoverText"],
            ),
            Paragraph(
                f"<b>Implementation Period:</b> "
                f"{IMPLEMENTATION_PERIOD}",
                styles["CoverText"],
            ),
            Paragraph(
                f"<b>Target Beneficiaries:</b> "
                f"{BENEFICIARY_TARGET}",
                styles["CoverText"],
            ),
            Paragraph(
                f"8,000 Smallholder Farmers | "
                f"2,000 Agricultural MSMEs",
                styles["CoverText"],
            ),
            Spacer(
                1,
                12 * mm,
            ),
            Paragraph(
                "<b>Important Note</b>",
                styles["SubHeading"],
            ),
            Paragraph(
                "This report is part of a "
                "synthetic/simulated Monitoring "
                "&amp; Evaluation portfolio project. "
                "The dataset, beneficiary records, "
                "baseline results, and findings "
                "presented in this report are simulated "
                "for professional demonstration and "
                "analytical learning purposes and do "
                "not represent actual ALMDP "
                "implementation data or actual "
                "Kaduna State beneficiary records.",
                styles["CoverText"],
            ),
            Spacer(
                1,
                15 * mm,
            ),
            Paragraph(
                "<b>Prepared as an M&amp;E "
                "Portfolio Demonstration</b>",
                styles["CoverText"],
            ),
            Paragraph(
                "Reporting Focus: Baseline Assessment, "
                "Results Measurement, Data Quality, "
                "Indicator Analysis, and Management Use",
                styles["CoverText"],
            ),
            PageBreak(),
        ]
    )

    # --------------------------------------------------------
    # PROCESS NOTEBOOK MARKDOWN CELLS
    # --------------------------------------------------------

    for cell in cells:

        if cell.get(
            "cell_type"
        ) != "markdown":
            continue

        source = "".join(
            cell.get(
                "source",
                [],
            )
        ).strip()

        if not source:
            continue

        # ----------------------------------------------------
        # Skip notebook cover because the professional
        # cover was already created above.
        # ----------------------------------------------------

        if source.startswith(
            "# Agricultural Livelihoods and "
            "MSME Development Project"
        ):
            continue

        # ----------------------------------------------------
        # Determine section.
        # ----------------------------------------------------

        section_number = (
            get_section_number(
                source
            )
        )

        # ----------------------------------------------------
        # Add Markdown content.
        # ----------------------------------------------------

        section_story = (
            markdown_cell_to_story(
                source
            )
        )

        story.extend(
            section_story
        )

        # ----------------------------------------------------
        # Insert approved visuals after their
        # corresponding analytical sections.
        #
        # Section 9:
        #   4 visuals
        #
        # Section 10:
        #   1 visual
        #
        # Section 11:
        #   1 visual
        #
        # Section 12:
        #   1 visual
        # ----------------------------------------------------

        if section_number in {
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        }:

            visuals = (
                get_visuals_for_section(
                    section_number
                )
            )

            for (
                title,
                info,
            ) in visuals:

                story.extend(
                    visual_flowable(
                        info["image"],
                        info["caption"],
                    )
                )

    return story


print()
print("SECTION-AWARE REPORT BUILDER")
print("============================")

preview_story = build_report_story(
    notebook
)

print(
    f"Total ReportLab flowables: "
    f"{len(preview_story)}"
)

print(
    "Section-aware content: PASS"
)

print(
    "Approved visuals positioned by section: PASS"
)

# ============================================================
# FINAL PDF BUILD
# ============================================================

print()
print("FINAL PDF BUILD")
print("================")

doc = SimpleDocTemplate(
    str(OUTPUT_PDF),
    pagesize=A4,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=18 * mm,
    bottomMargin=17 * mm,
    title=REPORT_SUBTITLE,
    author="ALMDP M&E Portfolio Demonstration",
    subject=(
        "Synthetic baseline assessment report "
        "for the ALMDP Monitoring & Evaluation "
        "portfolio project"
    ),
)

final_story = build_report_story(
    notebook
)

print(
    f"Final flowables: {len(final_story)}"
)

doc.build(
    final_story,
    onFirstPage=draw_page_header_footer,
    onLaterPages=draw_page_header_footer,
)

print(
    f"PDF created: {OUTPUT_PDF}"
)

print(
    f"PDF size: "
    f"{OUTPUT_PDF.stat().st_size:,} bytes"
)

print("PDF BUILD: PASS")



