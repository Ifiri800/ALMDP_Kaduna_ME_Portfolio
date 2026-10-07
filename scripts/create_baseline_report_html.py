from pathlib import Path
import base64
import html
import json
import re

import nbformat
import markdown


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

NOTEBOOK_PATH = (
    PROJECT_ROOT
    / "08_Analysis"
    / "baseline_report_executed.ipynb"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "10_Reporting"
    / "ALMDP_Baseline_Assessment_Report_2026.html"
)


# ============================================================
# CONFIGURATION
# ============================================================

REPORT_TITLE = (
    "Agricultural Livelihoods and MSME Development Project "
    "(ALMDP)"
)

REPORT_SUBTITLE = "Baseline Assessment Report"

REPORT_PERIOD = "2026"

PROJECT_LOCATION = "Kaduna State, Nigeria"

SYNTHETIC_NOTICE = (
    "This report presents a synthetic/simulated portfolio assessment "
    "developed for monitoring and evaluation demonstration and "
    "professional portfolio purposes. The dataset and findings do not "
    "represent actual donor-funded ALMDP implementation data."
)


# ============================================================
# HELPERS
# ============================================================

def image_to_data_uri(data: bytes, mime_type: str = "image/png") -> str:
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def clean_markdown(text: str) -> str:
    """
    Remove notebook-specific artifacts while retaining report content.
    """
    text = text.replace("\r\n", "\n")

    # Remove common notebook execution artifacts.
    text = re.sub(
        r"^\s*In\[\d+\]:\s*$",
        "",
        text,
        flags=re.MULTILINE,
    )

    return text.strip()


def markdown_to_html(text: str) -> str:
    text = clean_markdown(text)

    return markdown.markdown(
        text,
        extensions=[
            "tables",
            "fenced_code",
            "toc",
            "sane_lists",
        ],
        output_format="html5",
    )


def extract_heading(text: str):
    """
    Return the first Markdown heading and its level.
    """
    match = re.search(
        r"^\s*(#{1,6})\s+(.+?)\s*$",
        text,
        flags=re.MULTILINE,
    )

    if not match:
        return None, None

    level = len(match.group(1))
    title = re.sub(r"\s+#*\s*$", "", match.group(2)).strip()

    return level, title


def section_number_from_title(title: str):
    match = re.match(r"^\s*(\d+)\b", title)
    return match.group(1) if match else None


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def is_major_section(title: str) -> bool:
    number = section_number_from_title(title)
    if number is None:
        return False

    try:
        n = int(number)
        return 1 <= n <= 12
    except ValueError:
        return False


def safe_json_for_script(value) -> str:
    return json.dumps(value).replace("</", "<\\/")


# ============================================================
# NOTEBOOK EXTRACTION
# ============================================================

def extract_report_content():
    if not NOTEBOOK_PATH.exists():
        raise FileNotFoundError(
            f"Executed notebook not found: {NOTEBOOK_PATH}"
        )

    notebook = nbformat.read(
        NOTEBOOK_PATH,
        as_version=4,
    )

    content_blocks = []
    visual_count = 0
    markdown_count = 0
    code_count = 0

    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            source = cell.source.strip()

            if not source:
                continue

            level, title = extract_heading(source)

            content_blocks.append(
                {
                    "type": "markdown",
                    "source": source,
                    "heading_level": level,
                    "heading_title": title,
                }
            )

            markdown_count += 1

        elif cell.cell_type == "code":
            code_count += 1

            for output in cell.get("outputs", []):
                data = output.get("data", {})

                png = data.get("image/png")

                if png:
                    if isinstance(png, list):
                        png = "".join(png)

                    try:
                        image_bytes = base64.b64decode(png)
                    except Exception:
                        continue

                    visual_count += 1

                    content_blocks.append(
                        {
                            "type": "image",
                            "data_uri": image_to_data_uri(
                                image_bytes,
                                "image/png",
                            ),
                            "number": visual_count,
                        }
                    )

    return (
        content_blocks,
        markdown_count,
        code_count,
        visual_count,
    )


# ============================================================
# BUILD REPORT BODY
# ============================================================

def build_report_body(content_blocks):
    body_parts = []

    current_section = None
    section_visual_count = {}

    for block in content_blocks:
        if block["type"] == "markdown":

            source = block["source"]
            title = block.get("heading_title")
            level = block.get("heading_level")

            if title and is_major_section(title):
                section_number = section_number_from_title(title)
                current_section = section_number

                section_visual_count.setdefault(
                    current_section,
                    0,
                )

                anchor = f"section-{section_number}"

                body_parts.append(
                    f"""
                    <section
                        class="report-section"
                        id="{anchor}"
                        data-section="{section_number}"
                    >
                    """
                )

            rendered = markdown_to_html(source)

            # Avoid duplicating the section heading because we use a
            # dedicated section heading element.
            if title and is_major_section(title):
                pattern = re.compile(
                    r"^\s*<h1[^>]*>.*?</h1>\s*",
                    flags=re.IGNORECASE | re.DOTALL,
                )

                rendered = pattern.sub("", rendered, count=1)

                body_parts.append(
                    f"""
                    <div class="section-heading">
                        <div class="section-kicker">
                            Section {html.escape(section_number)}
                        </div>
                        <h2>{html.escape(title)}</h2>
                    </div>
                    """
                )

            body_parts.append(
                f'<div class="markdown-content">{rendered}</div>'
            )

        elif block["type"] == "image":
            if current_section is not None:
                section_visual_count[current_section] = (
                    section_visual_count.get(current_section, 0) + 1
                )

            body_parts.append(
                f"""
                <figure class="report-figure">
                    <img
                        src="{block["data_uri"]}"
                        alt="ALMDP baseline assessment visual"
                        loading="lazy"
                    />
                    <figcaption>
                        ALMDP baseline assessment visual
                    </figcaption>
                </figure>
                """
            )

    if current_section is not None:
        body_parts.append("</section>")

    # The above can leave section boundaries open when another section
    # begins. Rebuild boundaries cleanly below.
    return rebuild_sections(content_blocks)


def rebuild_sections(content_blocks):
    """
    Reconstruct report sections cleanly so every Section 1-12 is an
    independent article.
    """

    output = []

    current_section = None
    open_section = False
    visual_number = 0

    for block in content_blocks:

        if block["type"] == "markdown":

            source = block["source"]
            level, title = extract_heading(source)

            is_section = (
                title is not None
                and is_major_section(title)
            )

            if is_section:

                if open_section:
                    output.append("</section>")

                section_number = section_number_from_title(title)
                current_section = section_number

                output.append(
                    f"""
                    <section
                        class="report-section"
                        id="section-{section_number}"
                        data-section="{section_number}"
                    >
                    <div class="section-heading">
                        <div class="section-kicker">
                            Section {html.escape(section_number)}
                        </div>
                        <h2>{html.escape(title)}</h2>
                    </div>
                    """
                )

                open_section = True

                # Remove first heading from rendered markdown.
                rendered = markdown_to_html(source)

                rendered = re.sub(
                    r"^\s*<h[1-6][^>]*>.*?</h[1-6]>\s*",
                    "",
                    rendered,
                    count=1,
                    flags=re.IGNORECASE | re.DOTALL,
                )

                if rendered.strip():
                    output.append(
                        f'<div class="markdown-content">{rendered}</div>'
                    )

            else:
                rendered = markdown_to_html(source)

                if rendered.strip():
                    output.append(
                        f'<div class="markdown-content">{rendered}</div>'
                    )

        elif block["type"] == "image":
            visual_number += 1

            output.append(
                f"""
                <figure class="report-figure">
                    <img
                        src="{block["data_uri"]}"
                        alt="ALMDP baseline assessment visual {visual_number}"
                        loading="lazy"
                    />
                    <figcaption>
                        Figure {visual_number}. ALMDP baseline assessment visual.
                    </figcaption>
                </figure>
                """
            )

    if open_section:
        output.append("</section>")

    return "\n".join(output)


# ============================================================
# TABLE OF CONTENTS
# ============================================================

def build_toc():
    items = []

    for i in range(1, 13):
        items.append(
            f"""
            <a href="#section-{i}" class="toc-link">
                <span class="toc-number">{i:02d}</span>
                <span>Section {i}</span>
            </a>
            """
        )

    return "\n".join(items)


# ============================================================
# HTML TEMPLATE
# ============================================================

def build_html(report_body):
    toc = build_toc()

    synthetic_notice = html.escape(SYNTHETIC_NOTICE)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1"
>

<title>
    {html.escape(REPORT_TITLE)} -
    {html.escape(REPORT_SUBTITLE)}
</title>

<style>

:root {{
    --navy: #17324d;
    --blue: #246b9f;
    --blue-soft: #eaf3f8;
    --green: #2f6b4f;
    --green-soft: #edf6f0;
    --gold: #c3922e;
    --gold-soft: #fbf5e7;

    --text: #1f2933;
    --muted: #667085;
    --border: #d9e0e7;
    --surface: #ffffff;
    --background: #f4f6f8;

    --max-width: 1240px;
}}

* {{
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    margin: 0;
    background: var(--background);
    color: var(--text);

    font-family:
        "Segoe UI",
        Arial,
        Helvetica,
        sans-serif;

    line-height: 1.65;
}}

a {{
    color: var(--blue);
}}

.page-shell {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 28px 22px 60px;
}}

.cover {{
    min-height: 560px;

    background:
        linear-gradient(
            135deg,
            var(--navy),
            #244e6e 60%,
            #2f6b4f
        );

    color: white;

    border-radius: 18px;

    padding: 72px 64px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    box-shadow:
        0 18px 50px rgba(23, 50, 77, 0.18);

    margin-bottom: 28px;
}}

.cover-label {{
    display: inline-block;

    font-size: 13px;
    font-weight: 700;

    letter-spacing: 0.12em;
    text-transform: uppercase;

    opacity: 0.82;

    margin-bottom: 22px;
}}

.cover h1 {{
    max-width: 900px;

    font-size: clamp(34px, 5vw, 58px);
    line-height: 1.08;

    margin: 0 0 20px;

    font-weight: 750;
}}

.cover h2 {{
    font-size: 27px;
    font-weight: 500;

    margin: 0;

    opacity: 0.92;
}}

.cover-meta {{
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 16px;

    margin-top: 50px;
}}

.cover-meta-item {{
    padding: 18px 20px;

    border: 1px solid rgba(255,255,255,0.22);
    background: rgba(255,255,255,0.09);

    border-radius: 12px;
}}

.cover-meta-label {{
    display: block;

    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;

    opacity: 0.7;

    margin-bottom: 5px;
}}

.cover-meta-value {{
    font-size: 17px;
    font-weight: 650;
}}

.synthetic-notice {{
    background: var(--gold-soft);

    border-left: 5px solid var(--gold);

    padding: 18px 22px;

    border-radius: 10px;

    margin: 24px 0 32px;

    color: #5c481e;
}}

.layout {{
    display: grid;
    grid-template-columns: 245px minmax(0, 1fr);

    gap: 28px;

    align-items: start;
}}

.sidebar {{
    position: sticky;
    top: 20px;

    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 14px;

    padding: 20px;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.045);
}}

.sidebar-title {{
    font-size: 12px;
    font-weight: 750;

    text-transform: uppercase;
    letter-spacing: 0.1em;

    color: var(--muted);

    margin-bottom: 13px;
}}

.toc-link {{
    display: flex;
    align-items: center;
    gap: 10px;

    text-decoration: none;

    color: var(--text);

    font-size: 13px;

    padding: 7px 6px;

    border-radius: 7px;
}}

.toc-link:hover {{
    background: var(--blue-soft);
    color: var(--blue);
}}

.toc-number {{
    width: 24px;

    color: var(--muted);

    font-variant-numeric: tabular-nums;

    font-size: 11px;
    font-weight: 700;
}}

.report {{
    min-width: 0;
}}

.report-section {{
    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 16px;

    padding: 40px 44px;

    margin-bottom: 26px;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.035);

    scroll-margin-top: 24px;
}}

.section-heading {{
    border-bottom: 1px solid var(--border);

    padding-bottom: 18px;

    margin-bottom: 28px;
}}

.section-kicker {{
    color: var(--blue);

    font-size: 12px;
    font-weight: 750;

    letter-spacing: 0.11em;
    text-transform: uppercase;

    margin-bottom: 5px;
}}

.section-heading h2 {{
    color: var(--navy);

    font-size: clamp(26px, 3vw, 36px);

    line-height: 1.2;

    margin: 0;

    font-weight: 750;
}}

.markdown-content {{
    max-width: 100%;
}}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4 {{
    color: var(--navy);

    line-height: 1.3;

    margin-top: 30px;
    margin-bottom: 12px;
}}

.markdown-content h1 {{
    font-size: 30px;
}}

.markdown-content h2 {{
    font-size: 25px;
}}

.markdown-content h3 {{
    font-size: 20px;
}}

.markdown-content h4 {{
    font-size: 17px;
}}

.markdown-content p {{
    margin: 0 0 15px;
}}

.markdown-content ul,
.markdown-content ol {{
    padding-left: 26px;
}}

.markdown-content li {{
    margin-bottom: 6px;
}}

.markdown-content strong {{
    color: #162b3d;
}}

.markdown-content blockquote {{
    margin: 20px 0;

    padding: 14px 20px;

    border-left: 4px solid var(--blue);

    background: var(--blue-soft);

    border-radius: 8px;

    color: #334e68;
}}

.markdown-content code {{
    background: #f1f3f5;

    padding: 2px 5px;

    border-radius: 4px;

    font-family:
        Consolas,
        "Courier New",
        monospace;

    font-size: 0.9em;
}}

.markdown-content pre {{
    overflow-x: auto;

    background: #18232e;

    color: #f8fafc;

    padding: 18px;

    border-radius: 10px;
}}

.markdown-content table {{
    width: 100%;

    border-collapse: collapse;

    margin: 22px 0;

    font-size: 13px;

    display: block;

    overflow-x: auto;
}}

.markdown-content th {{
    background: var(--navy);

    color: white;

    font-weight: 700;

    text-align: left;
}}

.markdown-content th,
.markdown-content td {{
    padding: 9px 11px;

    border: 1px solid var(--border);

    vertical-align: top;
}}

.markdown-content tr:nth-child(even) td {{
    background: #fafbfc;
}}

.report-figure {{
    margin: 30px auto 34px;

    padding: 16px;

    border: 1px solid var(--border);

    border-radius: 12px;

    background: #fbfcfd;

    text-align: center;
}}

.report-figure img {{
    display: block;

    width: 100%;
    height: auto;

    max-width: 100%;

    margin: 0 auto;

    border-radius: 6px;
}}

.report-figure figcaption {{
    color: var(--muted);

    font-size: 12px;

    margin-top: 9px;
}}

.footer {{
    margin-top: 30px;

    padding: 24px;

    text-align: center;

    color: var(--muted);

    font-size: 12px;
}}

.footer strong {{
    color: var(--navy);
}}

@media (max-width: 900px) {{

    .layout {{
        grid-template-columns: 1fr;
    }}

    .sidebar {{
        position: static;
    }}

    .cover {{
        padding: 48px 34px;
        min-height: auto;
    }}

    .cover-meta {{
        grid-template-columns: 1fr;
        margin-top: 32px;
    }}

    .report-section {{
        padding: 30px 25px;
    }}
}}

@media (max-width: 600px) {{

    .page-shell {{
        padding: 12px 10px 35px;
    }}

    .cover {{
        padding: 38px 25px;
        border-radius: 13px;
    }}

    .cover h1 {{
        font-size: 34px;
    }}

    .cover h2 {{
        font-size: 22px;
    }}

    .report-section {{
        padding: 24px 18px;
        border-radius: 12px;
    }}

    .section-heading h2 {{
        font-size: 27px;
    }}
}}

@media print {{

    body {{
        background: white;
    }}

    .page-shell {{
        max-width: none;
        padding: 0;
    }}

    .sidebar {{
        display: none;
    }}

    .layout {{
        display: block;
    }}

    .cover,
    .report-section {{
        box-shadow: none;
    }}

    .cover {{
        border-radius: 0;
        min-height: 100vh;
        page-break-after: always;
    }}

    .report-section {{
        border: none;
        page-break-before: always;
    }}

    .report-figure {{
        break-inside: avoid;
    }}

    a {{
        color: inherit;
        text-decoration: none;
    }}
}}

</style>
</head>

<body>

<div class="page-shell">

    <header class="cover">

        <div>
            <div class="cover-label">
                Monitoring &amp; Evaluation Portfolio
            </div>

            <h1>
                {html.escape(REPORT_TITLE)}
            </h1>

            <h2>
                {html.escape(REPORT_SUBTITLE)}
            </h2>
        </div>

        <div class="cover-meta">

            <div class="cover-meta-item">
                <span class="cover-meta-label">
                    Location
                </span>

                <span class="cover-meta-value">
                    {html.escape(PROJECT_LOCATION)}
                </span>
            </div>

            <div class="cover-meta-item">
                <span class="cover-meta-label">
                    Assessment
                </span>

                <span class="cover-meta-value">
                    Baseline Assessment
                </span>
            </div>

            <div class="cover-meta-item">
                <span class="cover-meta-label">
                    Report Year
                </span>

                <span class="cover-meta-value">
                    {html.escape(REPORT_PERIOD)}
                </span>
            </div>

        </div>

    </header>


    <div class="synthetic-notice">
        <strong>Synthetic / Simulated Portfolio Project:</strong>
        {synthetic_notice}
    </div>


    <div class="layout">

        <aside class="sidebar">

            <div class="sidebar-title">
                Report Contents
            </div>

            {toc}

        </aside>


        <main class="report">

            {report_body}

        </main>

    </div>


    <footer class="footer">

        <strong>
            ALMDP Baseline Assessment Report
        </strong>

        <br>

        Synthetic/simulated M&amp;E portfolio artifact |
        {html.escape(REPORT_PERIOD)}

    </footer>

</div>

</body>
</html>
"""


# ============================================================
# MAIN
# ============================================================

def main():

    print("ALMDP HTML REPORT GENERATOR")
    print("============================")

    print(f"Notebook: {NOTEBOOK_PATH}")
    print(f"Output:   {OUTPUT_PATH}")

    (
        content_blocks,
        markdown_count,
        code_count,
        visual_count,
    ) = extract_report_content()

    print()
    print("NOTEBOOK EXTRACTION")
    print("-------------------")
    print(f"Markdown cells: {markdown_count}")
    print(f"Code cells:     {code_count}")
    print(f"PNG visuals:    {visual_count}")

    if visual_count != 12:
        print(
            f"WARNING: Expected 12 final visuals, "
            f"found {visual_count}."
        )

    report_body = rebuild_sections(content_blocks)

    final_html = build_html(report_body)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        final_html,
        encoding="utf-8",
    )

    file_size = OUTPUT_PATH.stat().st_size

    print()
    print("HTML BUILD")
    print("----------")
    print("HTML file created: PASS")
    print(f"File size: {file_size:,} bytes")
    print(f"Visuals embedded: {visual_count}")
    print()
    print(f"Saved to: {OUTPUT_PATH}")
    print()
    print("HTML BUILD: PASS")


if __name__ == "__main__":
    main()