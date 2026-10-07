from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE


# ============================================================
# ALMDP PRESENTATION CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "13_Presentation"
    / "ALMDP_Baseline_Assessment_Presentation_2026.pptx"
)
OUTPUT_DIR = OUTPUT_PATH.parent

REPORT_PDF = (
    PROJECT_ROOT
    / "10_Reporting"
    / "ALMDP_Baseline_Assessment_Report_2026.pdf"
)

REPORT_HTML = (
    PROJECT_ROOT
    / "10_Reporting"
    / "ALMDP_Baseline_Assessment_Report_2026.html"
)

PROJECT_NAME = (
    "Agricultural Livelihoods and MSME Development Project"
)

PROJECT_SHORT_NAME = "ALMDP"

LOCATION = "Kaduna State, Nigeria"

BASELINE_YEAR = "2026"

IMPLEMENTATION_PERIOD = "January 2027 - December 2030"

SYNTHETIC_NOTICE = (
    "SYNTHETIC / SIMULATED PORTFOLIO PROJECT - "
    "All project data and findings are simulated for demonstration "
    "and professional portfolio purposes."
)


# ============================================================
# PRESENTATION SIZE
# ============================================================

prs = Presentation()

# Widescreen 16:9
prs.slide_width = Inches(13.333333)
prs.slide_height = Inches(7.5)


# ============================================================
# DESIGN SYSTEM
# ============================================================

NAVY = RGBColor(20, 43, 74)
BLUE = RGBColor(42, 93, 140)
LIGHT_BLUE = RGBColor(221, 235, 247)

GREEN = RGBColor(47, 122, 82)
LIGHT_GREEN = RGBColor(226, 240, 231)

GOLD = RGBColor(201, 151, 48)
LIGHT_GOLD = RGBColor(247, 239, 215)

RED = RGBColor(176, 67, 67)
LIGHT_RED = RGBColor(248, 226, 226)

PURPLE = RGBColor(105, 78, 138)
LIGHT_PURPLE = RGBColor(235, 228, 244)

TEAL = RGBColor(42, 126, 133)
LIGHT_TEAL = RGBColor(224, 241, 242)

DARK = RGBColor(38, 43, 48)
MID = RGBColor(92, 101, 111)
LIGHT = RGBColor(242, 245, 247)
WHITE = RGBColor(255, 255, 255)
BORDER = RGBColor(211, 217, 223)


# ============================================================
# FONT SYSTEM
# ============================================================

FONT_HEAD = "Aptos Display"
FONT_BODY = "Aptos"
FONT_MONO = "Consolas"


# ============================================================
# SLIDE DIMENSIONS
# ============================================================

SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height


# ============================================================
# BASIC HELPERS
# ============================================================

def add_text(
    slide,
    text,
    left,
    top,
    width,
    height,
    font_size=20,
    bold=False,
    color=DARK,
    font_name=FONT_BODY,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
):
    """Add a formatted text box."""

    shape = slide.shapes.add_textbox(
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height),
    )

    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = valign

    p = tf.paragraphs[0]
    p.alignment = align

    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color

    return shape


def add_rect(
    slide,
    left,
    top,
    width,
    height,
    fill=WHITE,
    line=BORDER,
    radius=False,
):
    """Add a simple presentation panel."""

    shape_type = (
        MSO_SHAPE.ROUNDED_RECTANGLE
        if radius
        else MSO_SHAPE.RECTANGLE
    )

    shape = slide.shapes.add_shape(
        shape_type,
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height),
    )

    shape.fill.solid()
    shape.fill.fore_color.rgb = fill

    shape.line.color.rgb = line
    shape.line.width = Pt(1)

    return shape


def add_title(slide, title, subtitle=None):
    """Add consistent slide title."""

    add_text(
        slide,
        title,
        0.65,
        0.35,
        12.0,
        0.55,
        font_size=27,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    if subtitle:
        add_text(
            slide,
            subtitle,
            0.68,
            0.92,
            11.8,
            0.38,
            font_size=11,
            color=MID,
        )


def add_footer(slide, slide_number):
    """Add presentation footer."""

    add_text(
        slide,
        PROJECT_SHORT_NAME,
        0.65,
        7.12,
        2.0,
        0.2,
        font_size=8,
        bold=True,
        color=MID,
    )

    add_text(
        slide,
        "Synthetic / Simulated Portfolio Project",
        4.2,
        7.12,
        5.0,
        0.2,
        font_size=8,
        color=MID,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        str(slide_number),
        12.15,
        7.12,
        0.5,
        0.2,
        font_size=8,
        color=MID,
        align=PP_ALIGN.RIGHT,
    )


def add_bullet_list(
    slide,
    items,
    left,
    top,
    width,
    height,
    font_size=17,
    color=DARK,
):
    """Add a clean bullet list."""

    shape = slide.shapes.add_textbox(
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height),
    )

    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True

    for index, item in enumerate(items):
        p = (
            tf.paragraphs[0]
            if index == 0
            else tf.add_paragraph()
        )

        p.text = item
        p.font.name = FONT_BODY
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.space_after = Pt(8)
        p.level = 0
        p.text = f"â€¢ {item}"

    return shape


# ============================================================
# VALIDATION
# ============================================================

assert prs.slide_width == Inches(13.333333)
assert prs.slide_height == Inches(7.5)

print("PRESENTATION CONFIGURATION")
print("--------------------------")
print(f"Project: {PROJECT_NAME}")
print(f"Location: {LOCATION}")
print(f"Baseline year: {BASELINE_YEAR}")
print(f"Implementation: {IMPLEMENTATION_PERIOD}")
print(f"Output: {OUTPUT_PATH}")
print("Configuration: PASS")

# ============================================================
# ALMDP PRESENTATION DATA
# ============================================================

PROJECT_SCALE = {
    "beneficiaries": 10000,
    "farmers": 8000,
    "msmes": 2000,
    "lgas": 7,
    "value_chains": 8,
}

BASELINE_RESULTS = [
    {
        "id": "IMP-02",
        "label": "Economic resilience",
        "baseline": 30.60,
        "target": 65.00,
        "unit": "%",
        "direction": "higher",
    },
    {
        "id": "OUT-02",
        "label": "Practice adoption",
        "baseline": 67.81,
        "target": 65.00,
        "unit": "%",
        "direction": "higher",
    },
    {
        "id": "OUT-04",
        "label": "Structured markets",
        "baseline": 27.31,
        "target": 55.00,
        "unit": "%",
        "direction": "higher",
    },
    {
        "id": "OUT-05",
        "label": "Buyer access",
        "baseline": 30.00,
        "target": 70.00,
        "unit": "%",
        "direction": "higher",
    },
    {
        "id": "OUT-06",
        "label": "Post-harvest loss",
        "baseline": 17.33,
        "target": 12.00,
        "unit": "%",
        "direction": "lower",
    },
    {
        "id": "OUT-08",
        "label": "MSME annual profit",
        "baseline": 356839.05,
        "target": 550000,
        "unit": "NGN/year",
        "direction": "higher",
    },
    {
        "id": "OUT-09",
        "label": "Financial records",
        "baseline": 50.00,
        "target": 70.00,
        "unit": "%",
        "direction": "higher",
    },
    {
        "id": "OUT-10",
        "label": "Women beneficiaries",
        "baseline": 41.55,
        "target": 45.00,
        "unit": "%",
        "direction": "higher",
    },
    {
        "id": "OUT-11",
        "label": "Youth beneficiaries",
        "baseline": 30.17,
        "target": 35.00,
        "unit": "%",
        "direction": "higher",
    },
    {
        "id": "OUT-12",
        "label": "Women income improvement",
        "baseline": 29.12,
        "target": 60.00,
        "unit": "%",
        "direction": "higher",
    },
]

VALUE_CHAIN_RESULTS = [
    {
        "name": "Tomato",
        "beneficiaries": 155,
        "productivity": 5.42,
        "income": 3619051.36,
    },
    {
        "name": "Vegetables",
        "beneficiaries": 187,
        "productivity": 4.16,
        "income": 2500885.86,
    },
    {
        "name": "Ginger",
        "beneficiaries": 139,
        "productivity": 2.07,
        "income": 2412602.10,
    },
    {
        "name": "Rice",
        "beneficiaries": 296,
        "productivity": 1.97,
        "income": 1244835.43,
    },
    {
        "name": "Soybean",
        "beneficiaries": 219,
        "productivity": 1.90,
        "income": 1131995.25,
    },
    {
        "name": "Maize",
        "beneficiaries": 386,
        "productivity": 1.80,
        "income": 1039585.54,
    },
    {
        "name": "Sorghum",
        "beneficiaries": 135,
        "productivity": 1.50,
        "income": 1071684.97,
    },
    {
        "name": "Groundnut",
        "beneficiaries": 83,
        "productivity": 1.37,
        "income": 876346.91,
    },
]

PRACTICE_ADOPTION = [
    ("Fertilizer", 53.56),
    ("Improved seed", 45.44),
    ("Water management", 42.31),
    ("Storage", 38.63),
    ("IPM", 38.38),
    ("Climate-smart", 34.56),
    ("Conservation", 34.00),
    ("Soil testing", 27.06),
]

MARKET_RESULTS = [
    ("Regular buyer", 55.19),
    ("Market information", 46.94),
    ("Buyer access improved", 30.00),
    ("Structured markets", 27.31),
]

BENEFICIARY_PROFILE = {
    "farmers": {
        "count": 1600,
        "female": 41.94,
        "youth": 29.81,
        "average_age": 46.16,
        "average_income": 1626526.36,
    },
    "msmes": {
        "count": 400,
        "female": 40.00,
        "youth": 31.50,
        "average_age": 46.39,
        "average_income": 981668.74,
    },
}

MSME_RESULTS = {
    "count": 400,
    "annual_sales": 988565.44,
    "annual_cost": 631726.40,
    "annual_profit": 356839.05,
    "profit_target": 550000,
    "financial_records_3_plus": 50.00,
    "years_operation": 10.42,
    "employees": 15.84,
}

DQA_RESULTS = {
    "raw_duplicate_ids": 5,
    "raw_total_issues": 33,
    "raw_high_issues": 25,
    "raw_review_issues": 8,
    "clean_duplicate_ids": 0,
    "clean_invalid_ages": 0,
    "clean_invalid_farm_area": 0,
    "clean_logic_errors": 0,
    "indicator_checks": "24/24",
    "derived_variable_checks": "8/8",
}

STATUS_COUNTS = {
    "requires_improvement": 12,
    "not_measurable": 5,
    "pre_implementation": 5,
    "target_met_exceeded": 2,
}

PRIORITY_GAPS = [
    ("OUT-05", "Buyer access", 30.00, 70.00),
    ("IMP-02", "Economic resilience", 30.60, 65.00),
    ("OUT-12", "Women income", 29.12, 60.00),
    ("OUT-04", "Structured markets", 27.31, 55.00),
    ("OUT-08", "MSME profit", 356839.05, 550000),
    ("OUT-09", "Financial records", 50.00, 70.00),
    ("OUT-06", "Post-harvest loss", 17.33, 12.00),
]

MANAGEMENT_PRIORITIES = [
    "Strengthen market linkage and structured-market participation",
    "Improve buyer access and market information",
    "Reduce post-harvest losses across value chains",
    "Strengthen MSME financial management and profitability",
    "Prioritize women-focused economic outcomes",
    "Strengthen resilience programming",
    "Maintain rigorous M&E, DQA and indicator tracking",
]

RECOMMENDATIONS = [
    "Develop targeted market-linkage interventions for farmers and MSMEs.",
    "Strengthen buyer networks, aggregation and market information systems.",
    "Introduce value-chain-specific post-harvest loss reduction measures.",
    "Expand MSME financial-management and business-performance support.",
    "Use gender-responsive interventions to improve women's income outcomes.",
    "Embed resilience and climate-risk management into implementation.",
    "Maintain quarterly indicator review and evidence-based corrective action.",
]

OBJECTIVES = [
    (
        "01",
        "Productivity",
        "Increase adoption of improved agricultural practices and technologies.",
    ),
    (
        "02",
        "Market access",
        "Improve market participation and access to structured buyers.",
    ),
    (
        "03",
        "MSME performance",
        "Improve agricultural MSME business performance and management.",
    ),
    (
        "04",
        "Inclusion & resilience",
        "Increase inclusion and resilience of women and youth.",
    ),
]

COMPONENTS = [
    "Farmer Productivity & Climate-Smart Agriculture",
    "Market Access & Value-Chain Development",
    "Agricultural MSME Development",
    "Inclusion, Monitoring & Institutional Capacity",
]

VALUE_CHAINS = [
    "Maize",
    "Rice",
    "Soybean",
    "Ginger",
    "Tomato",
    "Vegetables",
    "Sorghum",
    "Groundnut",
]

LGAS = [
    "Chikun",
    "Igabi",
    "Kachia",
    "Kajuru",
    "Kaduna North",
    "Kaduna South",
    "Zaria",
]


print("Presentation data loaded")
print(f"Project beneficiaries: {PROJECT_SCALE['beneficiaries']:,}")
print(f"Value chains: {len(VALUE_CHAINS)}")
print(f"LGAs: {len(LGAS)}")
print(f"Baseline result indicators: {len(BASELINE_RESULTS)}")
print(f"Presentation data: PASS")

# ============================================================
# PRESENTATION BUILDING HELPERS
# ============================================================

def add_kpi_card(
    slide,
    left,
    top,
    width,
    height,
    value,
    label,
    accent=BLUE,
    value_size=28,
):
    """Add a polished KPI card."""

    add_rect(
        slide,
        left,
        top,
        width,
        height,
        fill=WHITE,
        line=BORDER,
        radius=True,
    )

    # Accent strip
    strip = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left),
        Inches(top),
        Inches(0.07),
        Inches(height),
    )
    strip.fill.solid()
    strip.fill.fore_color.rgb = accent
    strip.line.fill.background()

    add_text(
        slide,
        str(value),
        left + 0.22,
        top + 0.25,
        width - 0.4,
        0.55,
        font_size=value_size,
        bold=True,
        color=accent,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_text(
        slide,
        label,
        left + 0.2,
        top + 0.92,
        width - 0.4,
        height - 1.05,
        font_size=11,
        bold=True,
        color=MID,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.TOP,
    )


def add_section_label(slide, text, number):
    """Add a small section label."""

    add_rect(
        slide,
        0.68,
        1.22,
        0.58,
        0.36,
        fill=BLUE,
        line=BLUE,
        radius=True,
    )

    add_text(
        slide,
        number,
        0.68,
        1.25,
        0.58,
        0.22,
        font_size=9,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        text.upper(),
        1.38,
        1.23,
        5.0,
        0.28,
        font_size=9,
        bold=True,
        color=BLUE,
    )


def add_bar_chart(
    slide,
    items,
    left,
    top,
    width,
    height,
    max_value=None,
    bar_color=BLUE,
    value_suffix="",
    decimals=1,
    label_width=2.2,
):
    """Create a clean horizontal bar chart."""

    if not items:
        return

    if max_value is None:
        max_value = max(value for _, value in items)

    max_value = max(max_value, 1)

    row_height = height / len(items)

    chart_left = left + label_width
    chart_width = width - label_width - 0.65

    for i, (label, value) in enumerate(items):
        y = top + i * row_height

        add_text(
            slide,
            label,
            left,
            y + 0.05,
            label_width - 0.12,
            row_height - 0.08,
            font_size=10,
            color=DARK,
            valign=MSO_ANCHOR.MIDDLE,
        )

        # Background bar
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(chart_left),
            Inches(y + 0.13),
            Inches(chart_width),
            Inches(0.18),
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = LIGHT
        bg.line.fill.background()

        bar_width = max(0.02, chart_width * value / max_value)

        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(chart_left),
            Inches(y + 0.13),
            Inches(bar_width),
            Inches(0.18),
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = bar_color
        bar.line.fill.background()

        formatted = f"{value:.{decimals}f}{value_suffix}"

        add_text(
            slide,
            formatted,
            chart_left + chart_width + 0.05,
            y + 0.02,
            0.55,
            row_height - 0.05,
            font_size=9,
            bold=True,
            color=DARK,
            align=PP_ALIGN.RIGHT,
            valign=MSO_ANCHOR.MIDDLE,
        )


def add_grouped_bar_chart(
    slide,
    items,
    left,
    top,
    width,
    height,
    max_value=None,
    colors=None,
    value_suffix="%",
):
    """Create a two-series grouped horizontal bar chart."""

    if not items:
        return

    if colors is None:
        colors = [BLUE, GREEN]

    if max_value is None:
        max_value = max(
            max(item[1], item[2])
            for item in items
        )

    max_value = max(max_value, 1)

    row_height = height / len(items)

    label_width = 2.2
    chart_left = left + label_width
    chart_width = width - label_width - 0.65

    for i, item in enumerate(items):
        label, first, second = item

        y = top + i * row_height

        add_text(
            slide,
            label,
            left,
            y + 0.02,
            label_width - 0.1,
            row_height - 0.03,
            font_size=9,
            color=DARK,
            valign=MSO_ANCHOR.MIDDLE,
        )

        for j, value in enumerate([first, second]):
            bar_y = y + 0.05 + j * 0.23

            bg = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(chart_left),
                Inches(bar_y),
                Inches(chart_width),
                Inches(0.15),
            )
            bg.fill.solid()
            bg.fill.fore_color.rgb = LIGHT
            bg.line.fill.background()

            bar_width = max(
                0.02,
                chart_width * value / max_value,
            )

            bar = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(chart_left),
                Inches(bar_y),
                Inches(bar_width),
                Inches(0.15),
            )
            bar.fill.solid()
            bar.fill.fore_color.rgb = colors[j]
            bar.line.fill.background()

            add_text(
                slide,
                f"{value:.1f}{value_suffix}",
                chart_left + chart_width + 0.05,
                bar_y - 0.02,
                0.55,
                0.18,
                font_size=8,
                bold=True,
                color=DARK,
            )


def add_callout(
    slide,
    text,
    left,
    top,
    width,
    height,
    fill=LIGHT_BLUE,
    line=BLUE,
    text_color=NAVY,
    font_size=13,
):
    """Add a concise management callout."""

    add_rect(
        slide,
        left,
        top,
        width,
        height,
        fill=fill,
        line=line,
        radius=True,
    )

    add_text(
        slide,
        text,
        left + 0.18,
        top + 0.12,
        width - 0.36,
        height - 0.24,
        font_size=font_size,
        bold=True,
        color=text_color,
        valign=MSO_ANCHOR.MIDDLE,
    )


def add_flow_box(
    slide,
    text,
    left,
    top,
    width,
    height,
    fill=LIGHT_BLUE,
    line=BLUE,
    font_size=12,
):
    """Add a flow-diagram box."""

    add_rect(
        slide,
        left,
        top,
        width,
        height,
        fill=fill,
        line=line,
        radius=True,
    )

    add_text(
        slide,
        text,
        left + 0.12,
        top + 0.08,
        width - 0.24,
        height - 0.16,
        font_size=font_size,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )


def add_arrow(
    slide,
    x1,
    y1,
    x2,
    y2,
    color=MID,
    width=1.8,
):
    """Add a simple line arrow."""

    line = slide.shapes.add_connector(
        1,
        Inches(x1),
        Inches(y1),
        Inches(x2),
        Inches(y2),
    )

    line.line.color.rgb = color
    line.line.width = Pt(width)

    try:
        line.line.end_arrowhead = True
    except AttributeError:
        pass

    return line


def add_note(
    slide,
    text,
    left=0.7,
    top=6.65,
    width=12,
):
    """Add a small methodological/reporting note."""

    add_text(
        slide,
        text,
        left,
        top,
        width,
        0.3,
        font_size=8,
        color=MID,
    )


def add_section_divider(
    slide,
    number,
    title,
    description,
):
    """Create a strong section divider."""

    # Full-width color block
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        SLIDE_W,
        SLIDE_H,
    )

    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    add_text(
        slide,
        number,
        0.85,
        1.35,
        2.0,
        1.2,
        font_size=54,
        bold=True,
        color=GOLD,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        title,
        0.85,
        2.55,
        10.8,
        1.0,
        font_size=35,
        bold=True,
        color=WHITE,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        description,
        0.9,
        3.7,
        9.8,
        0.8,
        font_size=17,
        color=LIGHT_BLUE,
    )

    add_text(
        slide,
        PROJECT_SHORT_NAME,
        0.9,
        6.45,
        3.0,
        0.35,
        font_size=11,
        bold=True,
        color=WHITE,
    )


print("Presentation helper functions loaded")
print("Presentation helpers: PASS")

# ============================================================
# SLIDE BUILDERS - PART 1
# ============================================================

def build_cover_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Background
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        SLIDE_W,
        SLIDE_H,
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    # Accent panel
    panel = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(8.9),
        0,
        Inches(4.433333),
        SLIDE_H,
    )
    panel.fill.solid()
    panel.fill.fore_color.rgb = BLUE
    panel.line.fill.background()

    # Gold accent
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(8.9),
        Inches(0.0),
        Inches(0.10),
        SLIDE_H,
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = GOLD
    accent.line.fill.background()

    add_text(
        slide,
        PROJECT_SHORT_NAME,
        0.85,
        0.85,
        2.2,
        0.45,
        font_size=18,
        bold=True,
        color=GOLD,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        "Baseline Assessment",
        0.85,
        1.65,
        7.3,
        0.7,
        font_size=34,
        bold=True,
        color=WHITE,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        PROJECT_NAME,
        0.88,
        2.48,
        7.35,
        1.2,
        font_size=21,
        bold=True,
        color=LIGHT_BLUE,
        font_name=FONT_BODY,
    )

    add_text(
        slide,
        LOCATION,
        0.88,
        3.88,
        5.5,
        0.4,
        font_size=16,
        color=WHITE,
    )

    add_text(
        slide,
        f"Baseline year: {BASELINE_YEAR}",
        0.88,
        4.38,
        4.0,
        0.35,
        font_size=13,
        color=LIGHT_BLUE,
    )

    add_text(
        slide,
        f"Implementation: {IMPLEMENTATION_PERIOD}",
        0.88,
        4.78,
        5.2,
        0.35,
        font_size=13,
        color=LIGHT_BLUE,
    )

    add_callout(
        slide,
        "SYNTHETIC / SIMULATED PORTFOLIO PROJECT",
        0.88,
        5.55,
        6.8,
        0.55,
        fill=LIGHT_GOLD,
        line=GOLD,
        text_color=NAVY,
        font_size=11,
    )

    # Right-side visual hierarchy
    add_text(
        slide,
        "10,000",
        9.55,
        1.45,
        2.8,
        0.8,
        font_size=38,
        bold=True,
        color=WHITE,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "Target beneficiaries",
        9.55,
        2.25,
        2.8,
        0.45,
        font_size=13,
        color=LIGHT_BLUE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "7",
        9.55,
        3.15,
        1.25,
        0.7,
        font_size=32,
        bold=True,
        color=GOLD,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "LGAs",
        9.55,
        3.82,
        1.25,
        0.35,
        font_size=11,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "8",
        11.0,
        3.15,
        1.25,
        0.7,
        font_size=32,
        bold=True,
        color=GOLD,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "Value chains",
        10.8,
        3.82,
        1.7,
        0.35,
        font_size=11,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "M&E Portfolio Demonstration",
        9.35,
        5.2,
        3.2,
        0.55,
        font_size=15,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "Results framework â€¢ Baseline â€¢ DQA â€¢ Analysis â€¢ Reporting",
        9.25,
        5.85,
        3.4,
        0.75,
        font_size=10,
        color=LIGHT_BLUE,
        align=PP_ALIGN.CENTER,
    )


def build_executive_summary_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Executive Summary",
        "Baseline evidence establishes the starting position for implementation and results tracking.",
    )
    add_section_label(slide, "Executive overview", "01")

    # Left: key message
    add_rect(
        slide,
        0.7,
        1.65,
        5.7,
        4.85,
        fill=LIGHT_BLUE,
        line=BLUE,
        radius=True,
    )

    add_text(
        slide,
        "Baseline message",
        1.0,
        1.98,
        4.8,
        0.4,
        font_size=19,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        (
            "The baseline indicates a mixed starting position: "
            "agricultural practice adoption and beneficiary income "
            "are relatively strong, while market access, economic "
            "resilience, women's economic outcomes and MSME "
            "performance require targeted implementation attention."
        ),
        1.0,
        2.55,
        4.95,
        2.05,
        font_size=15,
        color=DARK,
    )

    add_callout(
        slide,
        "2 indicators already meet or exceed their 2030 targets.",
        1.0,
        4.95,
        4.95,
        0.72,
        fill=LIGHT_GREEN,
        line=GREEN,
        text_color=GREEN,
        font_size=12,
    )

    add_callout(
        slide,
        "5 indicators were not measurable at baseline because implementation-dependent data were unavailable.",
        1.0,
        5.78,
        4.95,
        0.72,
        fill=LIGHT_GOLD,
        line=GOLD,
        text_color=NAVY,
        font_size=10,
    )

    # Right: KPI cards
    add_kpi_card(
        slide,
        6.75,
        1.75,
        2.75,
        1.65,
        "67.81%",
        "Farmers adopting 3+ recommended practices",
        accent=GREEN,
        value_size=24,
    )

    add_kpi_card(
        slide,
        9.75,
        1.75,
        2.75,
        1.65,
        "30.60%",
        "Beneficiaries reporting economic resilience",
        accent=RED,
        value_size=24,
    )

    add_kpi_card(
        slide,
        6.75,
        3.65,
        2.75,
        1.65,
        "27.31%",
        "Farmers selling through structured markets",
        accent=RED,
        value_size=24,
    )

    add_kpi_card(
        slide,
        9.75,
        3.65,
        2.75,
        1.65,
        "17.33%",
        "Average post-harvest loss rate",
        accent=GOLD,
        value_size=24,
    )

    add_callout(
        slide,
        "Priority management focus: market access + resilience + MSME performance + gender-responsive economic outcomes.",
        6.75,
        5.65,
        5.75,
        0.82,
        fill=LIGHT_PURPLE,
        line=PURPLE,
        text_color=PURPLE,
        font_size=11,
    )

    add_footer(slide, 2)


def build_project_scale_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Project Scale and Coverage",
        "The simulated programme is designed around 10,000 direct beneficiaries across seven LGAs and eight agricultural value chains.",
    )
    add_section_label(slide, "Project profile", "02")

    add_kpi_card(
        slide,
        0.75,
        1.65,
        2.25,
        1.75,
        "10,000",
        "Target beneficiaries",
        accent=NAVY,
        value_size=28,
    )

    add_kpi_card(
        slide,
        3.15,
        1.65,
        2.25,
        1.75,
        "8,000",
        "Smallholder farmers",
        accent=GREEN,
        value_size=28,
    )

    add_kpi_card(
        slide,
        5.55,
        1.65,
        2.25,
        1.75,
        "2,000",
        "Agricultural MSMEs",
        accent=BLUE,
        value_size=28,
    )

    add_kpi_card(
        slide,
        7.95,
        1.65,
        2.25,
        1.75,
        "7",
        "LGAs",
        accent=GOLD,
        value_size=30,
    )

    add_kpi_card(
        slide,
        10.35,
        1.65,
        2.25,
        1.75,
        "8",
        "Value chains",
        accent=PURPLE,
        value_size=30,
    )

    # Coverage panels
    add_rect(
        slide,
        0.75,
        3.75,
        5.8,
        2.55,
        fill=WHITE,
        line=BORDER,
        radius=True,
    )

    add_text(
        slide,
        "Geographic coverage",
        1.0,
        4.02,
        4.5,
        0.35,
        font_size=18,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    add_bullet_list(
        slide,
        [
            "Chikun",
            "Igabi",
            "Kachia",
            "Kajuru",
            "Kaduna North",
            "Kaduna South",
            "Zaria",
        ],
        1.05,
        4.55,
        4.9,
        1.45,
        font_size=11,
    )

    add_rect(
        slide,
        6.8,
        3.75,
        5.8,
        2.55,
        fill=WHITE,
        line=BORDER,
        radius=True,
    )

    add_text(
        slide,
        "Agricultural value chains",
        7.05,
        4.02,
        4.8,
        0.35,
        font_size=18,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    add_bullet_list(
        slide,
        [
            "Maize",
            "Rice",
            "Soybean",
            "Ginger",
            "Tomato",
            "Vegetables",
            "Sorghum",
            "Groundnut",
        ],
        7.1,
        4.55,
        4.9,
        1.45,
        font_size=11,
    )

    add_footer(slide, 3)


def build_objectives_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Project Objectives",
        "Four objectives define the results pathway from agricultural productivity to inclusive economic resilience.",
    )
    add_section_label(slide, "Results architecture", "03")

    positions = [
        (0.75, 1.75),
        (6.85, 1.75),
        (0.75, 4.15),
        (6.85, 4.15),
    ]

    colors = [GREEN, BLUE, PURPLE, GOLD]
    fills = [LIGHT_GREEN, LIGHT_BLUE, LIGHT_PURPLE, LIGHT_GOLD]

    for (number, title, description), (x, y), color, fill in zip(
        OBJECTIVES,
        positions,
        colors,
        fills,
    ):
        add_rect(
            slide,
            x,
            y,
            5.7,
            1.95,
            fill=fill,
            line=color,
            radius=True,
        )

        add_text(
            slide,
            number,
            x + 0.25,
            y + 0.25,
            0.65,
            0.55,
            font_size=22,
            bold=True,
            color=color,
            font_name=FONT_HEAD,
            align=PP_ALIGN.CENTER,
        )

        add_text(
            slide,
            title,
            x + 1.0,
            y + 0.25,
            4.25,
            0.4,
            font_size=18,
            bold=True,
            color=NAVY,
            font_name=FONT_HEAD,
        )

        add_text(
            slide,
            description,
            x + 1.0,
            y + 0.82,
            4.25,
            0.82,
            font_size=11,
            color=DARK,
        )

    add_footer(slide, 4)


def build_theory_of_change_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Theory of Change",
        "The programme links resources and implementation activities to outputs, outcomes and longer-term impact.",
    )
    add_section_label(slide, "Results pathway", "04")

    stages = [
        ("Inputs", "Resources\npeople â€¢ funds â€¢ systems", LIGHT_BLUE, BLUE),
        ("Activities", "Training\nmarket linkage\nMSME support", LIGHT_GREEN, GREEN),
        ("Outputs", "Farmers trained\nMSMEs supported\nevents delivered", LIGHT_GOLD, GOLD),
        ("Outcomes", "Adoption\nmarket access\nprofitability\nresilience", LIGHT_PURPLE, PURPLE),
        ("Impact", "Higher income\nand stronger\nlivelihood resilience", LIGHT_TEAL, TEAL),
    ]

    x_positions = [0.55, 3.05, 5.55, 8.05, 10.55]

    for i, (title, body, fill, color) in enumerate(stages):
        add_flow_box(
            slide,
            title,
            x_positions[i],
            2.05,
            2.05,
            0.65,
            fill=fill,
            line=color,
            font_size=15,
        )

        add_text(
            slide,
            body,
            x_positions[i] + 0.08,
            2.9,
            1.9,
            1.25,
            font_size=10,
            color=DARK,
            align=PP_ALIGN.CENTER,
        )

        if i < len(stages) - 1:
            add_arrow(
                slide,
                x_positions[i] + 2.08,
                2.38,
                x_positions[i + 1] - 0.08,
                2.38,
                color=MID,
            )

    add_callout(
        slide,
        "M&E implication: every major stage requires defined indicators, data sources, verification procedures and management use.",
        1.1,
        5.15,
        11.1,
        0.9,
        fill=LIGHT_BLUE,
        line=BLUE,
        text_color=NAVY,
        font_size=13,
    )

    add_footer(slide, 5)


print("Slide builders - Part 1 loaded")
print("Slide builders Part 1: PASS")

# ============================================================
# SLIDE BUILDERS - PART 2
# ============================================================

def build_me_architecture_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "M&E Architecture",
        "The portfolio connects programme design, indicator definitions, data collection, analysis and reporting.",
    )
    add_section_label(slide, "M&E system", "05")

    stages = [
        ("Results\nFramework", BLUE, LIGHT_BLUE),
        ("Indicators", GREEN, LIGHT_GREEN),
        ("Data\nRequirements", GOLD, LIGHT_GOLD),
        ("Collection\nTools", PURPLE, LIGHT_PURPLE),
        ("Dataset", TEAL, LIGHT_TEAL),
        ("Analysis", BLUE, LIGHT_BLUE),
        ("Dashboard /\nReport", GREEN, LIGHT_GREEN),
        ("Management\nDecision", GOLD, LIGHT_GOLD),
    ]

    start_x = 0.55
    box_w = 1.45
    gap = 0.12

    for i, (label, color, fill) in enumerate(stages):
        x = start_x + i * (box_w + gap)

        add_flow_box(
            slide,
            label,
            x,
            2.0,
            box_w,
            1.05,
            fill=fill,
            line=color,
            font_size=11,
        )

        if i < len(stages) - 1:
            add_arrow(
                slide,
                x + box_w,
                2.52,
                x + box_w + gap - 0.02,
                2.52,
                color=MID,
                width=1.2,
            )

    # Data-quality layer
    add_rect(
        slide,
        0.75,
        3.65,
        12.0,
        1.55,
        fill=LIGHT,
        line=BORDER,
        radius=True,
    )

    add_text(
        slide,
        "Cross-cutting M&E controls",
        1.05,
        3.92,
        3.0,
        0.35,
        font_size=17,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    controls = [
        "Data quality assurance",
        "Source verification",
        "Indicator calculation",
        "Disaggregation",
        "Timeliness monitoring",
        "Management action tracking",
    ]

    control_x = 1.05

    for i, control in enumerate(controls):
        x = control_x + (i % 3) * 3.75
        y = 4.42 + (i // 3) * 0.48

        add_text(
            slide,
            f"â€¢ {control}",
            x,
            y,
            3.35,
            0.3,
            font_size=10,
            color=DARK,
        )

    add_callout(
        slide,
        "Data flow: Field data â†’ validation â†’ clean dataset â†’ indicators â†’ dashboard/report â†’ management decision.",
        1.15,
        5.65,
        10.9,
        0.72,
        fill=LIGHT_BLUE,
        line=BLUE,
        text_color=NAVY,
        font_size=11,
    )

    add_footer(slide, 6)


def build_methodology_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Baseline Methodology",
        "A structured synthetic baseline was designed to demonstrate the full M&E data lifecycle.",
    )
    add_section_label(slide, "Methodology", "06")

    # Left methodology flow
    add_rect(
        slide,
        0.7,
        1.65,
        7.0,
        4.9,
        fill=WHITE,
        line=BORDER,
        radius=True,
    )

    add_text(
        slide,
        "Baseline data workflow",
        1.0,
        1.95,
        4.5,
        0.35,
        font_size=19,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    methodology = [
        ("1", "Synthetic baseline design"),
        ("2", "Respondent generation"),
        ("3", "Data profiling"),
        ("4", "Validation rules"),
        ("5", "Data cleaning"),
        ("6", "Indicator calculation"),
        ("7", "Disaggregation and analysis"),
        ("8", "Reporting and management use"),
    ]

    for i, (number, label) in enumerate(methodology):
        y = 2.48 + i * 0.47

        add_rect(
            slide,
            1.0,
            y,
            0.42,
            0.32,
            fill=BLUE,
            line=BLUE,
            radius=True,
        )

        add_text(
            slide,
            number,
            1.0,
            y + 0.04,
            0.42,
            0.18,
            font_size=8,
            bold=True,
            color=WHITE,
            align=PP_ALIGN.CENTER,
        )

        add_text(
            slide,
            label,
            1.58,
            y + 0.02,
            5.5,
            0.28,
            font_size=11,
            color=DARK,
        )

    # Right parameters
    add_rect(
        slide,
        7.95,
        1.65,
        4.65,
        4.9,
        fill=LIGHT_BLUE,
        line=BLUE,
        radius=True,
    )

    add_text(
        slide,
        "Baseline parameters",
        8.25,
        1.95,
        3.6,
        0.35,
        font_size=19,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    add_kpi_card(
        slide,
        8.25,
        2.55,
        1.85,
        1.35,
        "2,000",
        "Respondents",
        accent=BLUE,
        value_size=23,
    )

    add_kpi_card(
        slide,
        10.3,
        2.55,
        1.85,
        1.35,
        "109",
        "Variables",
        accent=GREEN,
        value_size=23,
    )

    add_kpi_card(
        slide,
        8.25,
        4.15,
        1.85,
        1.35,
        "7",
        "LGAs",
        accent=GOLD,
        value_size=27,
    )

    add_kpi_card(
        slide,
        10.3,
        4.15,
        1.85,
        1.35,
        "8",
        "Value chains",
        accent=PURPLE,
        value_size=27,
    )

    add_callout(
        slide,
        "Farmers: 1,600 | MSMEs: 400",
        8.25,
        5.72,
        3.9,
        0.48,
        fill=WHITE,
        line=BLUE,
        text_color=NAVY,
        font_size=10,
    )

    add_footer(slide, 7)


def build_dqa_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Data Quality Assurance",
        "The DQA process identified, documented and resolved baseline data-quality issues before indicator calculation.",
    )
    add_section_label(slide, "DQA", "07")

    # Before
    add_rect(
        slide,
        0.7,
        1.7,
        5.85,
        4.45,
        fill=LIGHT_RED,
        line=RED,
        radius=True,
    )

    add_text(
        slide,
        "Raw data review",
        1.0,
        2.0,
        3.8,
        0.35,
        font_size=20,
        bold=True,
        color=RED,
        font_name=FONT_HEAD,
    )

    raw_items = [
        ("Duplicate ID collisions", 5),
        ("Total issue instances", 33),
        ("High-priority issues", 25),
        ("Review issues", 8),
    ]

    add_bar_chart(
        slide,
        raw_items,
        1.0,
        2.65,
        4.95,
        1.8,
        max_value=35,
        bar_color=RED,
        decimals=0,
        label_width=2.5,
        value_suffix="",
    )

    add_callout(
        slide,
        "Issues were logged rather than silently overwritten.",
        1.0,
        5.15,
        4.9,
        0.58,
        fill=WHITE,
        line=RED,
        text_color=RED,
        font_size=10,
    )

    # After
    add_rect(
        slide,
        6.75,
        1.7,
        5.85,
        4.45,
        fill=LIGHT_GREEN,
        line=GREEN,
        radius=True,
    )

    add_text(
        slide,
        "Post-cleaning QA",
        7.05,
        2.0,
        3.8,
        0.35,
        font_size=20,
        bold=True,
        color=GREEN,
        font_name=FONT_HEAD,
    )

    clean_items = [
        ("Duplicate IDs", 0),
        ("Invalid ages", 0),
        ("Invalid farm area", 0),
        ("Logic errors", 0),
    ]

    add_bar_chart(
        slide,
        clean_items,
        7.05,
        2.65,
        4.95,
        1.8,
        max_value=1,
        bar_color=GREEN,
        decimals=0,
        label_width=2.5,
    )

    add_callout(
        slide,
        "8/8 derived-variable checks passed",
        7.05,
        4.72,
        2.35,
        0.65,
        fill=WHITE,
        line=GREEN,
        text_color=GREEN,
        font_size=10,
    )

    add_callout(
        slide,
        "24/24 indicators passed",
        9.65,
        4.72,
        2.35,
        0.65,
        fill=WHITE,
        line=GREEN,
        text_color=GREEN,
        font_size=10,
    )

    add_text(
        slide,
        "DQA dimensions: accuracy â€¢ completeness â€¢ consistency â€¢ timeliness â€¢ integrity",
        7.05,
        5.62,
        5.0,
        0.3,
        font_size=9,
        color=MID,
        align=PP_ALIGN.CENTER,
    )

    add_footer(slide, 8)


def build_beneficiary_profile_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Baseline Beneficiary Profile",
        "The synthetic baseline covers both smallholder farmers and agricultural MSMEs.",
    )
    add_section_label(slide, "Beneficiary profile", "08")

    # Farmers
    add_rect(
        slide,
        0.7,
        1.7,
        5.85,
        4.75,
        fill=LIGHT_GREEN,
        line=GREEN,
        radius=True,
    )

    add_text(
        slide,
        "Smallholder farmers",
        1.0,
        2.0,
        4.4,
        0.35,
        font_size=21,
        bold=True,
        color=GREEN,
        font_name=FONT_HEAD,
    )

    add_kpi_card(
        slide,
        1.0,
        2.6,
        2.15,
        1.45,
        "1,600",
        "Respondents",
        accent=GREEN,
        value_size=25,
    )

    add_kpi_card(
        slide,
        3.4,
        2.6,
        2.15,
        1.45,
        "41.94%",
        "Women",
        accent=PURPLE,
        value_size=22,
    )

    add_kpi_card(
        slide,
        1.0,
        4.3,
        2.15,
        1.45,
        "29.81%",
        "Youth (18-35)",
        accent=GOLD,
        value_size=22,
    )

    add_kpi_card(
        slide,
        3.4,
        4.3,
        2.15,
        1.45,
        "NGN 1.63M",
        "Average income",
        accent=BLUE,
        value_size=19,
    )

    # MSMEs
    add_rect(
        slide,
        6.75,
        1.7,
        5.85,
        4.75,
        fill=LIGHT_BLUE,
        line=BLUE,
        radius=True,
    )

    add_text(
        slide,
        "Agricultural MSMEs",
        7.05,
        2.0,
        4.4,
        0.35,
        font_size=21,
        bold=True,
        color=BLUE,
        font_name=FONT_HEAD,
    )

    add_kpi_card(
        slide,
        7.05,
        2.6,
        2.15,
        1.45,
        "400",
        "Respondents",
        accent=BLUE,
        value_size=27,
    )

    add_kpi_card(
        slide,
        9.45,
        2.6,
        2.15,
        1.45,
        "40.00%",
        "Women",
        accent=PURPLE,
        value_size=22,
    )

    add_kpi_card(
        slide,
        7.05,
        4.3,
        2.15,
        1.45,
        "31.50%",
        "Youth (18-35)",
        accent=GOLD,
        value_size=22,
    )

    add_kpi_card(
        slide,
        9.45,
        4.3,
        2.15,
        1.45,
        "NGN 0.98M",
        "Average income",
        accent=GREEN,
        value_size=19,
    )

    add_footer(slide, 9)


print("Slide builders - Part 2 loaded")
print("Slide builders Part 2: PASS")

# ============================================================
# SLIDE BUILDERS - PART 3
# ============================================================

def build_indicator_status_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Baseline Indicator Status",
        "The 24-indicator framework separates measurable baseline results from implementation-dependent indicators.",
    )
    add_section_label(slide, "Indicator status", "10")

    status_items = [
        ("Requires improvement", STATUS_COUNTS["requires_improvement"], RED),
        ("Not measurable", STATUS_COUNTS["not_measurable"], GOLD),
        ("Pre-implementation", STATUS_COUNTS["pre_implementation"], BLUE),
        ("Target met / exceeded", STATUS_COUNTS["target_met_exceeded"], GREEN),
    ]

    total = sum(value for _, value, _ in status_items)

    # Four status cards
    positions = [
        (0.75, 1.75),
        (3.95, 1.75),
        (7.15, 1.75),
        (10.35, 1.75),
    ]

    for (label, value, color), (x, y) in zip(
        status_items,
        positions,
    ):
        add_kpi_card(
            slide,
            x,
            y,
            2.45,
            1.7,
            str(value),
            label,
            accent=color,
            value_size=30,
        )

    # Visual summary
    add_rect(
        slide,
        0.75,
        3.9,
        7.1,
        2.3,
        fill=WHITE,
        line=BORDER,
        radius=True,
    )

    add_text(
        slide,
        "What the baseline tells management",
        1.05,
        4.18,
        5.5,
        0.35,
        font_size=19,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    add_bullet_list(
        slide,
        [
            "Half of the indicator set requires active performance improvement.",
            "Five indicators are implementation-dependent and should be tracked after programme activities begin.",
            "Two indicators already meet or exceed their 2030 targets and should be protected from deterioration.",
        ],
        1.05,
        4.72,
        6.2,
        1.2,
        font_size=11,
    )

    # Percentage composition
    add_rect(
        slide,
        8.15,
        3.9,
        4.45,
        2.3,
        fill=LIGHT_BLUE,
        line=BLUE,
        radius=True,
    )

    add_text(
        slide,
        "24 indicators",
        8.45,
        4.18,
        3.7,
        0.35,
        font_size=20,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "100% of the results framework reviewed",
        8.45,
        4.72,
        3.7,
        0.3,
        font_size=11,
        color=MID,
        align=PP_ALIGN.CENTER,
    )

    add_callout(
        slide,
        "Baseline analysis should drive implementation priorities, not simply describe starting values.",
        8.45,
        5.28,
        3.75,
        0.55,
        fill=WHITE,
        line=BLUE,
        text_color=NAVY,
        font_size=9,
    )

    add_footer(slide, 10)


def build_priority_gap_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Priority Baseline Gaps",
        "The largest management gaps are concentrated in market access, resilience, women's economic outcomes and MSME performance.",
    )
    add_section_label(slide, "Gap analysis", "11")

    gap_items = [
        ("Buyer access", 30.00, 70.00),
        ("Economic resilience", 30.60, 65.00),
        ("Women income", 29.12, 60.00),
        ("Structured markets", 27.31, 55.00),
        ("Financial records", 50.00, 70.00),
    ]

    add_text(
        slide,
        "Baseline",
        5.1,
        1.58,
        1.0,
        0.25,
        font_size=9,
        bold=True,
        color=BLUE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "2030 target",
        6.55,
        1.58,
        1.3,
        0.25,
        font_size=9,
        bold=True,
        color=GREEN,
        align=PP_ALIGN.CENTER,
    )

    grouped = [
        (label, baseline, target)
        for label, baseline, target in gap_items
    ]

    add_grouped_bar_chart(
        slide,
        grouped,
        0.8,
        1.95,
        7.2,
        3.8,
        max_value=75,
        colors=[BLUE, GREEN],
        value_suffix="%",
    )

    # Right management panel
    add_rect(
        slide,
        8.35,
        1.75,
        4.25,
        4.45,
        fill=LIGHT_RED,
        line=RED,
        radius=True,
    )

    add_text(
        slide,
        "Highest-priority gaps",
        8.65,
        2.05,
        3.5,
        0.35,
        font_size=20,
        bold=True,
        color=RED,
        font_name=FONT_HEAD,
    )

    add_bullet_list(
        slide,
        [
            "Buyer access: 30% vs 70% target.",
            "Economic resilience: 30.60% vs 65% target.",
            "Women income improvement: 29.12% vs 60% target.",
            "Structured markets: 27.31% vs 55% target.",
            "MSME profitability remains below the 2030 target.",
        ],
        8.65,
        2.65,
        3.45,
        2.55,
        font_size=11,
    )

    add_callout(
        slide,
        "Management implication: prioritize interventions where the baseline-target distance is largest and operationally actionable.",
        8.65,
        5.42,
        3.45,
        0.55,
        fill=WHITE,
        line=RED,
        text_color=RED,
        font_size=9,
    )

    add_footer(slide, 11)


def build_value_chain_productivity_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Agricultural Productivity by Value Chain",
        "Productivity varies substantially across value chains, creating opportunities for targeted technical support.",
    )
    add_section_label(slide, "Agricultural outcomes", "12")

    productivity_items = [
        (item["name"], item["productivity"])
        for item in VALUE_CHAIN_RESULTS
    ]

    add_bar_chart(
        slide,
        productivity_items,
        0.75,
        1.7,
        7.25,
        4.45,
        max_value=6,
        bar_color=GREEN,
        value_suffix=" t/ha",
        decimals=2,
        label_width=2.0,
    )

    # Right panel
    add_rect(
        slide,
        8.25,
        1.7,
        4.35,
        4.45,
        fill=LIGHT_GREEN,
        line=GREEN,
        radius=True,
    )

    add_text(
        slide,
        "Key findings",
        8.55,
        2.0,
        3.4,
        0.35,
        font_size=20,
        bold=True,
        color=GREEN,
        font_name=FONT_HEAD,
    )

    add_bullet_list(
        slide,
        [
            "Tomato has the highest baseline productivity at 5.42 t/ha.",
            "Vegetables follow at 4.16 t/ha.",
            "Groundnut has the lowest productivity at 1.37 t/ha.",
            "Maize, sorghum and groundnut require particular productivity attention.",
        ],
        8.55,
        2.58,
        3.4,
        2.25,
        font_size=11,
    )

    add_callout(
        slide,
        "Baseline productivity: 2.448 t/ha overall",
        8.55,
        5.25,
        3.45,
        0.62,
        fill=WHITE,
        line=GREEN,
        text_color=GREEN,
        font_size=10,
    )

    add_footer(slide, 12)


def build_practice_adoption_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Agricultural Practice Adoption",
        "Adoption is comparatively strong overall, but specific practices still have substantial room for expansion.",
    )
    add_section_label(slide, "Agricultural practices", "13")

    adoption_items = PRACTICE_ADOPTION

    add_bar_chart(
        slide,
        adoption_items,
        0.75,
        1.65,
        7.6,
        4.65,
        max_value=70,
        bar_color=GREEN,
        value_suffix="%",
        decimals=1,
        label_width=2.35,
    )

    add_rect(
        slide,
        8.65,
        1.65,
        3.9,
        4.65,
        fill=LIGHT_GREEN,
        line=GREEN,
        radius=True,
    )

    add_text(
        slide,
        "Headline result",
        8.95,
        1.98,
        3.0,
        0.35,
        font_size=19,
        bold=True,
        color=GREEN,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        "67.81%",
        8.95,
        2.65,
        3.0,
        0.7,
        font_size=34,
        bold=True,
        color=GREEN,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "of farmers adopt at least three recommended practices",
        9.0,
        3.35,
        2.9,
        0.85,
        font_size=12,
        bold=True,
        color=DARK,
        align=PP_ALIGN.CENTER,
    )

    add_callout(
        slide,
        "This exceeds the 2030 target of 65%.",
        9.0,
        4.48,
        2.9,
        0.58,
        fill=WHITE,
        line=GREEN,
        text_color=GREEN,
        font_size=10,
    )

    add_text(
        slide,
        "Priority extension opportunities:\nsoil testing â€¢ conservation â€¢ climate-smart practices â€¢ IPM",
        9.0,
        5.28,
        3.0,
        0.7,
        font_size=10,
        color=MID,
        align=PP_ALIGN.CENTER,
    )

    add_footer(slide, 13)


def build_market_postharvest_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Market Access and Post-Harvest Loss",
        "Market participation remains a major constraint, while post-harvest loss is above the programme target.",
    )
    add_section_label(slide, "Market outcomes", "14")

    market_items = MARKET_RESULTS

    add_bar_chart(
        slide,
        market_items,
        0.7,
        1.7,
        6.25,
        3.1,
        max_value=60,
        bar_color=BLUE,
        value_suffix="%",
        decimals=1,
        label_width=2.25,
    )

    add_rect(
        slide,
        7.2,
        1.7,
        5.35,
        3.1,
        fill=LIGHT_RED,
        line=RED,
        radius=True,
    )

    add_text(
        slide,
        "Post-harvest loss",
        7.5,
        2.0,
        3.6,
        0.35,
        font_size=20,
        bold=True,
        color=RED,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        "17.33%",
        7.5,
        2.65,
        4.5,
        0.7,
        font_size=34,
        bold=True,
        color=RED,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "baseline average",
        7.5,
        3.35,
        4.5,
        0.3,
        font_size=11,
        color=MID,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "2030 target: 12%",
        7.5,
        3.78,
        4.5,
        0.35,
        font_size=14,
        bold=True,
        color=GREEN,
        align=PP_ALIGN.CENTER,
    )

    add_callout(
        slide,
        "Lower is better. The programme must reduce losses by strengthening handling, storage, aggregation and value-chain practices.",
        0.95,
        5.2,
        11.3,
        0.85,
        fill=LIGHT_GOLD,
        line=GOLD,
        text_color=NAVY,
        font_size=11,
    )

    add_footer(slide, 14)


def build_msme_performance_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Agricultural MSME Performance",
        "MSME profitability and financial management represent important areas for programme support.",
    )
    add_section_label(slide, "MSME outcomes", "15")

    add_kpi_card(
        slide,
        0.75,
        1.65,
        2.55,
        1.75,
        "NGN 356,839",
        "Average annual profit",
        accent=BLUE,
        value_size=21,
    )

    add_kpi_card(
        slide,
        3.5,
        1.65,
        2.55,
        1.75,
        "NGN 550,000",
        "2030 profit target",
        accent=GREEN,
        value_size=20,
    )

    add_kpi_card(
        slide,
        6.25,
        1.65,
        2.55,
        1.75,
        "50%",
        "Maintaining 3+ basic financial records",
        accent=GOLD,
        value_size=25,
    )

    add_kpi_card(
        slide,
        9.0,
        1.65,
        2.55,
        1.75,
        "15.84",
        "Average employees",
        accent=PURPLE,
        value_size=25,
    )

    # Performance bridge
    add_rect(
        slide,
        0.75,
        3.75,
        7.0,
        2.35,
        fill=LIGHT_BLUE,
        line=BLUE,
        radius=True,
    )

    add_text(
        slide,
        "MSME financial picture",
        1.05,
        4.03,
        4.5,
        0.35,
        font_size=19,
        bold=True,
        color=NAVY,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        "Annual sales",
        1.05,
        4.72,
        2.0,
        0.25,
        font_size=10,
        color=MID,
    )

    add_text(
        slide,
        "NGN 988,565",
        3.0,
        4.68,
        2.0,
        0.35,
        font_size=14,
        bold=True,
        color=BLUE,
    )

    add_text(
        slide,
        "Annual cost",
        1.05,
        5.18,
        2.0,
        0.25,
        font_size=10,
        color=MID,
    )

    add_text(
        slide,
        "NGN 631,726",
        3.0,
        5.14,
        2.0,
        0.35,
        font_size=14,
        bold=True,
        color=RED,
    )

    add_text(
        slide,
        "Annual profit",
        4.85,
        4.72,
        1.8,
        0.25,
        font_size=10,
        color=MID,
    )

    add_text(
        slide,
        "NGN 356,839",
        4.85,
        5.05,
        2.0,
        0.35,
        font_size=14,
        bold=True,
        color=GREEN,
    )

    # Management implication
    add_rect(
        slide,
        8.0,
        3.75,
        4.55,
        2.35,
        fill=LIGHT_PURPLE,
        line=PURPLE,
        radius=True,
    )

    add_text(
        slide,
        "Management implication",
        8.3,
        4.03,
        3.7,
        0.35,
        font_size=19,
        bold=True,
        color=PURPLE,
        font_name=FONT_HEAD,
    )

    add_bullet_list(
        slide,
        [
            "Strengthen financial-record keeping.",
            "Improve cost and margin management.",
            "Target business types with lower profitability.",
        ],
        8.3,
        4.68,
        3.55,
        1.0,
        font_size=10,
    )

    add_footer(slide, 15)


def build_gender_youth_resilience_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Gender, Youth and Economic Resilience",
        "Inclusion indicators are relatively close to their targets, but women's income outcomes and resilience require focused action.",
    )
    add_section_label(slide, "Inclusion & resilience", "16")

    # Gender
    add_rect(
        slide,
        0.7,
        1.7,
        3.85,
        4.55,
        fill=LIGHT_PURPLE,
        line=PURPLE,
        radius=True,
    )

    add_text(
        slide,
        "Women",
        1.0,
        2.0,
        2.8,
        0.35,
        font_size=20,
        bold=True,
        color=PURPLE,
        font_name=FONT_HEAD,
    )

    add_kpi_card(
        slide,
        1.0,
        2.65,
        3.0,
        1.25,
        "41.55%",
        "Direct beneficiaries",
        accent=PURPLE,
        value_size=23,
    )

    add_kpi_card(
        slide,
        1.0,
        4.15,
        3.0,
        1.25,
        "29.12%",
        "Women reporting increased income",
        accent=RED,
        value_size=23,
    )

    # Youth
    add_rect(
        slide,
        4.75,
        1.7,
        3.85,
        4.55,
        fill=LIGHT_GOLD,
        line=GOLD,
        radius=True,
    )

    add_text(
        slide,
        "Youth",
        5.05,
        2.0,
        2.8,
        0.35,
        font_size=20,
        bold=True,
        color=GOLD,
        font_name=FONT_HEAD,
    )

    add_kpi_card(
        slide,
        5.05,
        2.65,
        3.0,
        1.25,
        "30.17%",
        "Direct beneficiaries aged 18-35",
        accent=GOLD,
        value_size=23,
    )

    add_callout(
        slide,
        "2030 target: 35%",
        5.05,
        4.15,
        3.0,
        0.65,
        fill=WHITE,
        line=GOLD,
        text_color=GOLD,
        font_size=12,
    )

    # Resilience
    add_rect(
        slide,
        8.85,
        1.7,
        3.85,
        4.55,
        fill=LIGHT_RED,
        line=RED,
        radius=True,
    )

    add_text(
        slide,
        "Resilience",
        9.15,
        2.0,
        2.8,
        0.35,
        font_size=20,
        bold=True,
        color=RED,
        font_name=FONT_HEAD,
    )

    add_kpi_card(
        slide,
        9.15,
        2.65,
        3.0,
        1.25,
        "30.60%",
        "Economic resilience",
        accent=RED,
        value_size=23,
    )

    add_callout(
        slide,
        "2030 target: 65%",
        9.15,
        4.15,
        3.0,
        0.65,
        fill=WHITE,
        line=RED,
        text_color=RED,
        font_size=12,
    )

    add_text(
        slide,
        "Priority: combine gender-responsive programming with resilience and income-generation measures.",
        1.15,
        6.48,
        11.0,
        0.35,
        font_size=11,
        bold=True,
        color=NAVY,
        align=PP_ALIGN.CENTER,
    )

    add_footer(slide, 16)


print("Slide builders - Part 3 loaded")
print("Slide builders Part 3: PASS")

# ============================================================
# SLIDE BUILDERS - PART 4
# ============================================================

def build_key_findings_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Key Baseline Findings",
        "The baseline identifies clear strengths, constraints and evidence gaps for implementation planning.",
    )
    add_section_label(slide, "Findings", "17")

    findings = [
        (
            "01",
            "Strong practice adoption",
            "67.81% of farmers report adopting at least three recommended practices, exceeding the 65% target.",
            GREEN,
            LIGHT_GREEN,
        ),
        (
            "02",
            "Income already strong",
            "Average beneficiary income is above the programme's 2030 design target, requiring monitoring to protect gains.",
            BLUE,
            LIGHT_BLUE,
        ),
        (
            "03",
            "Market access is weak",
            "Only 27.31% of farmers sell through structured markets and 30% report improved buyer access.",
            RED,
            LIGHT_RED,
        ),
        (
            "04",
            "Resilience gap is substantial",
            "Economic resilience is 30.60%, compared with a 65% target.",
            GOLD,
            LIGHT_GOLD,
        ),
        (
            "05",
            "MSME performance needs support",
            "Average annual profit is NGN 356,839 against a 2030 target of NGN 550,000.",
            PURPLE,
            LIGHT_PURPLE,
        ),
        (
            "06",
            "Gender outcomes require attention",
            "Women represent 41.55% of beneficiaries, but only 29.12% report increased income.",
            TEAL,
            LIGHT_TEAL,
        ),
    ]

    positions = [
        (0.65, 1.55),
        (4.45, 1.55),
        (8.25, 1.55),
        (0.65, 4.05),
        (4.45, 4.05),
        (8.25, 4.05),
    ]

    for (
        (number, title, description, color, fill),
        (x, y),
    ) in zip(findings, positions):

        add_rect(
            slide,
            x,
            y,
            3.55,
            2.05,
            fill=fill,
            line=color,
            radius=True,
        )

        add_text(
            slide,
            number,
            x + 0.2,
            y + 0.18,
            0.5,
            0.4,
            font_size=15,
            bold=True,
            color=color,
            font_name=FONT_HEAD,
        )

        add_text(
            slide,
            title,
            x + 0.75,
            y + 0.2,
            2.55,
            0.42,
            font_size=14,
            bold=True,
            color=NAVY,
            font_name=FONT_HEAD,
        )

        add_text(
            slide,
            description,
            x + 0.25,
            y + 0.78,
            3.05,
            1.05,
            font_size=9.5,
            color=DARK,
        )

    add_footer(slide, 17)


def build_management_priorities_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Management Priorities",
        "Baseline evidence should translate directly into implementation priorities and corrective action.",
    )
    add_section_label(slide, "Management use", "18")

    priorities = [
        ("01", "Market access", "Strengthen buyer networks, structured markets and market information.", BLUE, LIGHT_BLUE),
        ("02", "Resilience", "Integrate climate and economic resilience into livelihood interventions.", RED, LIGHT_RED),
        ("03", "MSME performance", "Improve financial management, cost control and profitability.", PURPLE, LIGHT_PURPLE),
        ("04", "Post-harvest loss", "Target handling, storage, aggregation and value-chain bottlenecks.", GOLD, LIGHT_GOLD),
        ("05", "Women's outcomes", "Use gender-responsive approaches to improve income and enterprise outcomes.", TEAL, LIGHT_TEAL),
        ("06", "M&E discipline", "Maintain DQA, indicator review, verification and evidence-based decision-making.", GREEN, LIGHT_GREEN),
    ]

    positions = [
        (0.7, 1.6),
        (4.45, 1.6),
        (8.2, 1.6),
        (0.7, 4.0),
        (4.45, 4.0),
        (8.2, 4.0),
    ]

    for (
        (number, title, description, color, fill),
        (x, y),
    ) in zip(priorities, positions):

        add_rect(
            slide,
            x,
            y,
            3.5,
            1.95,
            fill=fill,
            line=color,
            radius=True,
        )

        add_text(
            slide,
            number,
            x + 0.22,
            y + 0.18,
            0.5,
            0.35,
            font_size=15,
            bold=True,
            color=color,
            font_name=FONT_HEAD,
        )

        add_text(
            slide,
            title,
            x + 0.78,
            y + 0.18,
            2.45,
            0.4,
            font_size=14,
            bold=True,
            color=NAVY,
            font_name=FONT_HEAD,
        )

        add_text(
            slide,
            description,
            x + 0.25,
            y + 0.75,
            3.0,
            0.9,
            font_size=9.5,
            color=DARK,
        )

    add_footer(slide, 18)


def build_recommendations_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Recommended Implementation Actions",
        "Priority recommendations are designed to convert baseline evidence into measurable programme action.",
    )
    add_section_label(slide, "Recommendations", "19")

    recommendation_groups = [
        (
            "Market systems",
            [
                "Strengthen buyer networks.",
                "Expand structured-market participation.",
                "Improve market information access.",
            ],
            BLUE,
            LIGHT_BLUE,
        ),
        (
            "Productivity & losses",
            [
                "Target low-productivity value chains.",
                "Reduce post-harvest losses.",
                "Expand practical climate-smart support.",
            ],
            GREEN,
            LIGHT_GREEN,
        ),
        (
            "MSME development",
            [
                "Improve financial-record keeping.",
                "Strengthen cost and margin management.",
                "Target lower-profitability businesses.",
            ],
            PURPLE,
            LIGHT_PURPLE,
        ),
        (
            "Inclusion & resilience",
            [
                "Strengthen women-focused income interventions.",
                "Increase youth participation.",
                "Embed resilience measures across components.",
            ],
            GOLD,
            LIGHT_GOLD,
        ),
    ]

    positions = [
        (0.7, 1.65),
        (6.75, 1.65),
        (0.7, 4.15),
        (6.75, 4.15),
    ]

    for (
        (title, items, color, fill),
        (x, y),
    ) in zip(recommendation_groups, positions):

        add_rect(
            slide,
            x,
            y,
            5.85,
            2.05,
            fill=fill,
            line=color,
            radius=True,
        )

        add_text(
            slide,
            title,
            x + 0.3,
            y + 0.25,
            4.7,
            0.38,
            font_size=18,
            bold=True,
            color=color,
            font_name=FONT_HEAD,
        )

        add_bullet_list(
            slide,
            items,
            x + 0.35,
            y + 0.82,
            5.05,
            1.05,
            font_size=10,
        )

    add_footer(slide, 19)


def build_me_implementation_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "M&E Implementation Priorities",
        "The M&E system should remain an active management tool throughout implementation.",
    )
    add_section_label(slide, "M&E priorities", "20")

    implementation_steps = [
        ("1", "Track baseline indicators", "Use the baseline as the reference point for quarterly and annual performance review."),
        ("2", "Strengthen data quality", "Maintain validation, DQA, source verification and back-checks."),
        ("3", "Disaggregate results", "Review results by LGA, value chain, sex, age and beneficiary type."),
        ("4", "Investigate variance", "Identify causes when performance deviates materially from targets."),
        ("5", "Document corrective action", "Assign responsibility, deadlines and evidence requirements."),
        ("6", "Use evidence for decisions", "Feed M&E findings into planning, resource allocation and adaptive management."),
    ]

    for i, (number, title, description) in enumerate(implementation_steps):
        y = 1.55 + i * 0.82

        add_rect(
            slide,
            0.75,
            y,
            0.55,
            0.55,
            fill=BLUE,
            line=BLUE,
            radius=True,
        )

        add_text(
            slide,
            number,
            0.75,
            y + 0.13,
            0.55,
            0.25,
            font_size=12,
            bold=True,
            color=WHITE,
            align=PP_ALIGN.CENTER,
        )

        add_text(
            slide,
            title,
            1.55,
            y + 0.02,
            3.25,
            0.3,
            font_size=14,
            bold=True,
            color=NAVY,
            font_name=FONT_HEAD,
        )

        add_text(
            slide,
            description,
            4.8,
            y,
            7.4,
            0.55,
            font_size=10,
            color=DARK,
        )

    add_callout(
        slide,
        "Management cycle: Identify variance â†’ investigate â†’ document evidence â†’ corrective action â†’ assign responsibility â†’ monitor.",
        1.1,
        6.45,
        11.1,
        0.55,
        fill=LIGHT_BLUE,
        line=BLUE,
        text_color=NAVY,
        font_size=10,
    )

    add_footer(slide, 20)


def build_conclusion_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(
        slide,
        "Conclusion",
        "The baseline provides a structured evidence base for implementation planning, performance monitoring and adaptive management.",
    )
    add_section_label(slide, "Conclusion", "21")

    add_rect(
        slide,
        0.75,
        1.7,
        12.0,
        1.25,
        fill=NAVY,
        line=NAVY,
        radius=True,
    )

    add_text(
        slide,
        (
            "The programme starts from a mixed baseline: strong agricultural practice adoption "
            "and beneficiary income coexist with important gaps in market access, resilience, "
            "MSME performance and women's economic outcomes."
        ),
        1.05,
        2.0,
        11.4,
        0.7,
        font_size=17,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    conclusion_points = [
        ("Strengths", "Practice adoption and income provide a strong platform for implementation.", GREEN, LIGHT_GREEN),
        ("Priority gaps", "Market access, resilience, MSME profitability and women's income require targeted action.", RED, LIGHT_RED),
        ("M&E role", "Regular indicator review and DQA will support adaptive management and accountability.", BLUE, LIGHT_BLUE),
    ]

    positions = [
        (0.75, 3.45),
        (4.75, 3.45),
        (8.75, 3.45),
    ]

    for (
        (title, text, color, fill),
        (x, y),
    ) in zip(conclusion_points, positions):

        add_rect(
            slide,
            x,
            y,
            3.55,
            2.0,
            fill=fill,
            line=color,
            radius=True,
        )

        add_text(
            slide,
            title,
            x + 0.25,
            y + 0.28,
            3.0,
            0.4,
            font_size=17,
            bold=True,
            color=color,
            font_name=FONT_HEAD,
            align=PP_ALIGN.CENTER,
        )

        add_text(
            slide,
            text,
            x + 0.3,
            y + 0.88,
            2.95,
            0.8,
            font_size=10,
            color=DARK,
            align=PP_ALIGN.CENTER,
        )

    add_callout(
        slide,
        "Next step: translate the baseline findings into an implementation-linked performance monitoring plan.",
        1.6,
        5.95,
        10.1,
        0.65,
        fill=LIGHT_GOLD,
        line=GOLD,
        text_color=NAVY,
        font_size=12,
    )

    add_footer(slide, 21)


def build_closing_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        SLIDE_W,
        SLIDE_H,
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    add_text(
        slide,
        "ALMDP",
        0.9,
        1.15,
        3.0,
        0.6,
        font_size=28,
        bold=True,
        color=GOLD,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        "Baseline Assessment",
        0.9,
        2.0,
        7.5,
        0.75,
        font_size=35,
        bold=True,
        color=WHITE,
        font_name=FONT_HEAD,
    )

    add_text(
        slide,
        "Evidence for implementation, learning and adaptive management",
        0.92,
        2.95,
        8.3,
        0.6,
        font_size=18,
        color=LIGHT_BLUE,
    )

    add_callout(
        slide,
        "SYNTHETIC / SIMULATED PORTFOLIO PROJECT",
        0.92,
        4.1,
        5.4,
        0.62,
        fill=LIGHT_GOLD,
        line=GOLD,
        text_color=NAVY,
        font_size=11,
    )

    add_text(
        slide,
        "Agricultural Livelihoods and MSME Development Project",
        0.92,
        5.15,
        7.8,
        0.45,
        font_size=14,
        bold=True,
        color=WHITE,
    )

    add_text(
        slide,
        "Kaduna State, Nigeria | Baseline 2026",
        0.92,
        5.62,
        6.0,
        0.35,
        font_size=12,
        color=LIGHT_BLUE,
    )

    # Right-side closing metrics
    add_text(
        slide,
        "10,000",
        9.4,
        1.55,
        2.8,
        0.7,
        font_size=34,
        bold=True,
        color=WHITE,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "beneficiaries",
        9.4,
        2.25,
        2.8,
        0.3,
        font_size=11,
        color=LIGHT_BLUE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "24",
        9.4,
        3.15,
        1.25,
        0.6,
        font_size=30,
        bold=True,
        color=GOLD,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "indicators",
        9.4,
        3.75,
        1.25,
        0.3,
        font_size=10,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "12",
        10.95,
        3.15,
        1.25,
        0.6,
        font_size=30,
        bold=True,
        color=GOLD,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "report visuals",
        10.65,
        3.75,
        1.9,
        0.3,
        font_size=10,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "M&E Portfolio",
        9.3,
        5.05,
        3.2,
        0.45,
        font_size=17,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "Results â€¢ Data Quality â€¢ Analysis â€¢ Reporting",
        9.0,
        5.58,
        3.8,
        0.4,
        font_size=10,
        color=LIGHT_BLUE,
        align=PP_ALIGN.CENTER,
    )


print("Slide builders - Part 4 loaded")
print("Slide builders Part 4: PASS")


def build_thank_you_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        SLIDE_W,
        SLIDE_H,
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    add_text(
        slide,
        "THANK YOU",
        1.0,
        2.05,
        11.3,
        1.0,
        font_size=42,
        bold=True,
        color=WHITE,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "Agricultural Livelihoods and MSME Development Project",
        1.3,
        3.25,
        10.7,
        0.5,
        font_size=17,
        color=LIGHT_BLUE,
        align=PP_ALIGN.CENTER,
    )

    add_text(
        slide,
        "Baseline Assessment | Kaduna State, Nigeria | 2026",
        1.5,
        3.85,
        10.0,
        0.4,
        font_size=12,
        color=GOLD,
        align=PP_ALIGN.CENTER,
    )

    add_callout(
        slide,
        "SYNTHETIC / SIMULATED PORTFOLIO PROJECT",
        3.45,
        5.05,
        6.45,
        0.62,
        fill=LIGHT_GOLD,
        line=GOLD,
        text_color=NAVY,
        font_size=11,
    )

    add_text(
        slide,
        "M&E | Data Quality | Analysis | Reporting",
        2.5,
        6.0,
        8.0,
        0.35,
        font_size=10,
        color=LIGHT_BLUE,
        align=PP_ALIGN.CENTER,
    )

# ============================================================
# FINAL PRESENTATION ASSEMBLY AND VALIDATION
# ============================================================

def build_presentation():
    print()
    print("=" * 60)
    print("ALMDP BASELINE ASSESSMENT PRESENTATION")
    print("=" * 60)

    # Build slides in final presentation order.
    build_cover_slide()                         # 1
    build_executive_summary_slide()             # 2
    build_project_scale_slide()                 # 3
    build_objectives_slide()                    # 4
    build_theory_of_change_slide()              # 5
    build_me_architecture_slide()               # 6
    build_methodology_slide()                   # 7
    build_dqa_slide()                           # 8
    build_beneficiary_profile_slide()           # 9
    build_indicator_status_slide()               # 10
    build_priority_gap_slide()                  # 11
    build_value_chain_productivity_slide()      # 12
    build_practice_adoption_slide()             # 13
    build_market_postharvest_slide()            # 14
    build_msme_performance_slide()              # 15
    build_gender_youth_resilience_slide()       # 16
    build_key_findings_slide()                  # 17
    build_management_priorities_slide()         # 18
    build_recommendations_slide()               # 19
    build_me_implementation_slide()             # 20
    build_conclusion_slide()                    # 21
    build_closing_slide()                       # 22
    build_thank_you_slide()                     # 23

    # Create output directory.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save presentation.
    prs.save(OUTPUT_PATH)

    print()
    print("PRESENTATION BUILD")
    print("------------------")
    print(f"Slides created: {len(prs.slides)}")
    print(f"Expected slides: 23")
    print(f"Output: {OUTPUT_PATH}")

    # --------------------------------------------------------
    # Automated validation
    # --------------------------------------------------------

    validation_pass = True

    if len(prs.slides) != 23:
        print("SLIDE COUNT CHECK: FAIL")
        validation_pass = False
    else:
        print("SLIDE COUNT CHECK: PASS")

    if not OUTPUT_PATH.exists():
        print("FILE EXISTENCE CHECK: FAIL")
        validation_pass = False
    else:
        print("FILE EXISTENCE CHECK: PASS")

        file_size = OUTPUT_PATH.stat().st_size

        if file_size <= 10000:
            print(f"FILE SIZE CHECK: FAIL ({file_size:,} bytes)")
            validation_pass = False
        else:
            print(f"FILE SIZE CHECK: PASS ({file_size:,} bytes)")

    # Validate that every slide contains at least one shape.
    empty_slides = []

    for index, slide in enumerate(prs.slides, start=1):
        if len(slide.shapes) == 0:
            empty_slides.append(index)

    if empty_slides:
        print(f"EMPTY SLIDE CHECK: FAIL - {empty_slides}")
        validation_pass = False
    else:
        print("EMPTY SLIDE CHECK: PASS")

    # Validate slide titles.
    title_check_failures = []

    expected_title_keywords = [
        "Agricultural Livelihoods",
        "Executive Summary",
        "Project Scale",
        "Project Objectives",
        "Theory of Change",
        "M&E Architecture",
        "Baseline Methodology",
        "Data Quality Assurance",
        "Beneficiary Profile",
        "Indicator Status",
        "Priority Baseline Gaps",
        "Agricultural Productivity by Value Chain",
        "Agricultural Practice Adoption",
        "Market Access",
        "MSME Performance",
        "Gender, Youth",
        "Key Baseline Findings",
        "Management Priorities",
        "Recommended Implementation Actions",
        "M&E Implementation Priorities",
        "Conclusion",
        "ALMDP",
    ]

    for index, keyword in enumerate(expected_title_keywords, start=1):
        slide = prs.slides[index - 1]

        slide_text = " ".join(
            shape.text
            for shape in slide.shapes
            if hasattr(shape, "text")
        )

        if keyword.lower() not in slide_text.lower():
            title_check_failures.append((index, keyword))

    if title_check_failures:
        print("TITLE CONTENT CHECK: FAIL")
        for item in title_check_failures:
            print(f"  Slide {item[0]} missing: {item[1]}")
        validation_pass = False
    else:
        print("TITLE CONTENT CHECK: PASS")

    # Validate synthetic-project disclosure appears in the presentation.
    all_text = "\n".join(
        shape.text
        for slide in prs.slides
        for shape in slide.shapes
        if hasattr(shape, "text")
    )

    disclosure_terms = [
        "SYNTHETIC",
        "SIMULATED",
    ]

    if all(term in all_text.upper() for term in disclosure_terms):
        print("SYNTHETIC DISCLOSURE CHECK: PASS")
    else:
        print("SYNTHETIC DISCLOSURE CHECK: FAIL")
        validation_pass = False

    # Final result.
    print()

    if validation_pass:
        print("PRESENTATION VALIDATION: PASS")
        print(f"Saved successfully to:")
        print(OUTPUT_PATH)
    else:
        print("PRESENTATION VALIDATION: FAIL")

    print("=" * 60)

    return validation_pass


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    build_presentation()






