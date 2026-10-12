"""
Builds the Industry Internship Summary Report as a .docx file,
following the SCSE internship report template.

Generates:
  - images/architecture.png  (general architecture)
  - images/dfd.png           (data flow diagram, level 0 + level 1)
  - images/uml_usecase.png   (UML use-case diagram)
  - Internship_Report_Asmit_Singh.docx

Run from the repository root:  python scripts/build_report.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Circle

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG = os.path.join(ROOT, "images")
OUT = os.path.join(ROOT, "Internship_Report_Asmit_Singh.docx")

STUDENT = "Asmit Singh"
ADMISSION = "<< Admission Number >>"
TITLE = "Exploratory Data Analysis and Visualization of Web-Scraped Book Market Data"


# ==========================================================================
# 1. DIAGRAMS
# ==========================================================================
def _box(ax, x, y, w, h, text, fc="#DCE6F1"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.03",
                 linewidth=1.2, edgecolor="#333333", facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=8.5, wrap=True)


def _arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=14, color="#333333", linewidth=1.1))


def generate_diagrams():
    os.makedirs(IMG, exist_ok=True)

    # ---- architecture ---------------------------------------------------
    fig, ax = plt.subplots(figsize=(9.5, 2.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 3); ax.axis("off")
    labels = ["Web Source\nbooks.toscrape.com", "Web Scraper\nrequests + BS4",
              "Dataset\nbooks.csv", "EDA\npandas + scipy",
              "Visualization\nMatplotlib / Seaborn", "Insights\n& Report"]
    n = len(labels); w = 1.55; h = 0.95
    gap = (12 - n * w) / (n + 1)
    for i, t in enumerate(labels):
        x = gap + i * (w + gap)
        _box(ax, x, 1.0, w, h, t, "#DCE6F1")
        if i < n - 1:
            _arrow(ax, x + w, 1.475, x + w + gap, 1.475)
    ax.set_title("System Architecture - Data Analytics Pipeline",
                 fontsize=11, fontweight="bold")
    fig.savefig(os.path.join(IMG, "architecture.png"),
                bbox_inches="tight", dpi=150)
    plt.close(fig)

    # ---- data flow diagram ---------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.4))
    for a in axes:
        a.set_xlim(0, 10); a.set_ylim(0, 4); a.axis("off")

    a0 = axes[0]
    a0.set_title("Level 0 DFD (Context Diagram)", fontsize=10, fontweight="bold")
    _box(a0, 0.3, 1.6, 2.2, 1.0, "External Entity\nWebsite", "#FDE9D9")
    _box(a0, 3.8, 1.4, 2.6, 1.4, "Process\nBook Data Analytics\nSystem", "#DCE6F1")
    _box(a0, 7.5, 1.6, 2.2, 1.0, "External Entity\nReviewer / Stakeholder", "#E2EFDA")
    _arrow(a0, 2.5, 2.1, 3.8, 2.1)
    _arrow(a0, 6.4, 2.1, 7.5, 2.1)

    a1 = axes[1]
    a1.set_title("Level 1 DFD", fontsize=10, fontweight="bold")
    _box(a1, 0.2, 2.6, 1.7, 0.9, "Website", "#FDE9D9")
    _box(a1, 2.4, 2.6, 1.9, 0.9, "1.0 Scrape\nBooks", "#DCE6F1")
    _box(a1, 4.9, 2.6, 1.9, 0.9, "2.0 Store\nDataset", "#DCE6F1")
    _box(a1, 7.4, 2.6, 2.2, 0.9, "D1 | books.csv", "#FFF2CC")
    _box(a1, 2.4, 0.7, 1.9, 0.9, "3.0 Explore\n(EDA)", "#DCE6F1")
    _box(a1, 4.9, 0.7, 1.9, 0.9, "4.0 Visualize", "#DCE6F1")
    _box(a1, 7.4, 0.7, 2.2, 0.9, "Stakeholder\nInsights", "#E2EFDA")
    _arrow(a1, 1.9, 3.05, 2.4, 3.05)
    _arrow(a1, 4.3, 3.05, 4.9, 3.05)
    _arrow(a1, 6.8, 3.05, 7.4, 3.05)
    _arrow(a1, 8.5, 2.6, 8.5, 1.6)
    _arrow(a1, 7.4, 1.15, 6.8, 1.15)
    _arrow(a1, 4.9, 1.15, 4.3, 1.15)
    _arrow(a1, 3.35, 2.6, 3.35, 1.6)

    fig.savefig(os.path.join(IMG, "dfd.png"), bbox_inches="tight", dpi=150)
    plt.close(fig)

    # ---- UML use case ---------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

    # actor
    ax.add_patch(Circle((1.0, 3.6), 0.28, facecolor="#FDE9D9", edgecolor="#333"))
    ax.plot([1.0, 1.0], [3.32, 2.4], color="#333", lw=1.2)
    ax.plot([0.6, 1.4], [3.05, 3.05], color="#333", lw=1.2)
    ax.plot([1.0, 0.6], [2.4, 1.7], color="#333", lw=1.2)
    ax.plot([1.0, 1.4], [2.4, 1.7], color="#333", lw=1.2)
    ax.text(1.0, 1.3, "Data Analyst\n(Intern)", ha="center", fontsize=9)

    # system boundary
    ax.add_patch(FancyBboxPatch((3.2, 0.4), 6.3, 5.2,
                 boxstyle="round,pad=0.03", linewidth=1.2,
                 edgecolor="#333", facecolor="#F2F2F2", linestyle="--"))
    ax.text(6.35, 5.35, "CodeAlpha Data Analytics System",
            ha="center", fontsize=9, style="italic")

    cases = ["Scrape Book Data", "Explore & Analyse Data (EDA)",
             "Generate Visualizations", "Interpret Insights"]
    ys = [4.4, 3.4, 2.4, 1.4]
    for c, y in zip(cases, ys):
        ax.add_patch(Ellipse((6.4, y), 4.6, 0.8, facecolor="#DCE6F1",
                     edgecolor="#333", linewidth=1.1))
        ax.text(6.4, y, c, ha="center", va="center", fontsize=9)
        ax.plot([1.35, 4.1], [3.05, y], color="#888", lw=0.9)
    ax.set_title("UML Use-Case Diagram", fontsize=11, fontweight="bold")
    fig.savefig(os.path.join(IMG, "uml_usecase.png"),
                bbox_inches="tight", dpi=150)
    plt.close(fig)

    print("Diagrams generated: architecture.png, dfd.png, uml_usecase.png")


# ==========================================================================
# 2. DOCX HELPERS
# ==========================================================================
def set_style_font(style, name="Times New Roman"):
    style.font.name = name
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)


def style_run(run, size=12, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Times New Roman")


def para(doc, text="", size=12, bold=False, italic=False,
         align="justify", space_after=6, line=1.5):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = line
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                   "center": WD_ALIGN_PARAGRAPH.CENTER,
                   "left": WD_ALIGN_PARAGRAPH.LEFT,
                   "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    run = p.add_run(text)
    style_run(run, size, bold, italic)
    return p


def bullet(doc, text, size=12):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    style_run(run, size)
    return p


def chapter_heading(doc, number, title):
    doc.add_page_break()
    para(doc, f"CHAPTER {number}", size=14, bold=True, align="center",
         space_after=2)
    para(doc, title.upper(), size=14, bold=True, align="center", space_after=12)


def section(doc, text, size=12):
    para(doc, text, size=size, bold=True, align="left", space_after=4)


def figure(doc, filename, number, caption, width=5.8):
    path = os.path.join(IMG, filename)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(path, width=Inches(width))
    para(doc, f"Figure {number}: {caption}", size=11, italic=True,
         align="center", space_after=12)


def table(doc, number, caption, headers, rows):
    para(doc, f"Table {number}: {caption}", size=11, italic=True,
         align="center", space_after=4)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
        style_run(run, 11, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(val))
            style_run(run, 11)
    doc.add_paragraph()
    return t


# ==========================================================================
# 3. BUILD DOCUMENT
# ==========================================================================
def build_docx():
    doc = Document()
    set_style_font(doc.styles["Normal"])
    doc.styles["Normal"].font.size = Pt(12)

    # ---------------- Title page ----------------
    para(doc, "INDUSTRY INTERNSHIP", size=18, bold=True, align="center",
         space_after=0, line=1.0)
    para(doc, "SUMMARY REPORT", size=18, bold=True, align="center",
         space_after=18, line=1.0)
    para(doc, TITLE, size=16, bold=True, align="center", space_after=24)
    para(doc, "BACHELOR OF TECHNOLOGY", size=16, bold=True, align="center",
         space_after=0)
    para(doc, "in", size=12, align="center", space_after=0)
    para(doc, "COMPUTER SCIENCE AND ENGINEERING", size=16, bold=True,
         align="center", space_after=0)
    para(doc, "(Specialization: Data Analytics)", size=12, align="center",
         space_after=24)
    para(doc, "Submitted by", size=12, align="center", space_after=0)
    para(doc, f"{STUDENT}  ({ADMISSION})", size=14, bold=True,
         align="center", space_after=24)
    para(doc, "SCHOOL OF COMPUTING SCIENCE AND ENGINEERING", size=16,
         bold=True, align="center", space_after=0)
    para(doc, "GREATER NOIDA, UTTAR PRADESH", size=14, align="center",
         space_after=0)
    para(doc, "SUMMER 2025-2026", size=14, bold=True, align="center")

    # ---------------- Bonafide certificate page ----------------
    doc.add_page_break()
    para(doc, "BONAFIDE CERTIFICATE", size=14, bold=True, align="center",
         space_after=12)
    para(doc, "[ Attach bonafide certificate here ]", size=12, italic=True,
         align="center")

    # ---------------- Internship certificate page ----------------
    doc.add_page_break()
    para(doc, "INTERNSHIP CERTIFICATE", size=14, bold=True, align="center",
         space_after=12)
    para(doc, "[ Attach internship certificate / offer letter here ]",
         size=12, italic=True, align="center")

    # ---------------- Table of contents ----------------
    doc.add_page_break()
    para(doc, "TABLE OF CONTENTS", size=14, bold=True, align="center",
         space_after=12)
    toc = [
        ("Abstract", ""), ("List of Figures", ""), ("List of Tables", ""),
        ("List of Abbreviations", ""),
        ("1  Introduction", ""),
        ("     1.1 Objective of the Internship", ""),
        ("     1.2 Problem Statement and Research Objectives", ""),
        ("     1.3 Description of Domain", ""),
        ("     1.4 A Brief Introduction about the Organization", ""),
        ("2  Technical Description", ""),
        ("3  System Design", ""),
        ("     3.1 General Architecture", ""),
        ("     3.2 Design Phase", ""),
        ("           3.2.1 Data Flow Diagram", ""),
        ("           3.2.2 UML Diagrams", ""),
        ("     3.3 Methodology", ""),
        ("4  System Implementation", ""),
        ("5  Results and Discussions", ""),
        ("6  Conclusion and Future Work", ""),
        ("7  Appendices", ""),
        ("     7.1 Source Code", ""),
        ("     7.2 Learning Experiences", ""),
        ("     7.3 SWOT Analysis", ""),
    ]
    for item, _ in toc:
        para(doc, item, size=12, align="left", space_after=2, line=1.5)

    # ---------------- Abstract ----------------
    doc.add_page_break()
    para(doc, "ABSTRACT", size=14, bold=True, align="center", space_after=12)
    para(doc, (
        "This report documents the Data Analytics internship carried out at "
        "CodeAlpha. The objective was to apply the complete data analytics "
        "lifecycle - from data acquisition to insight communication - using "
        "the Python ecosystem. Three tasks were completed. First, a custom "
        "dataset of 1,000 books spanning 50 categories was collected from the "
        "public website books.toscrape.com using the requests and "
        "BeautifulSoup libraries (Web Scraping). Second, the dataset was "
        "profiled and analysed to understand its structure, distributions and "
        "statistical relationships using pandas, NumPy and SciPy "
        "(Exploratory Data Analysis). Third, seven charts and a consolidated "
        "dashboard were produced with Matplotlib and Seaborn to communicate "
        "the findings visually (Data Visualization). The analysis revealed an "
        "average book price of GBP 35.07 with no statistically significant "
        "relationship between rating and price (Pearson r = 0.028, p = 0.37) "
        "and no significant difference in price across categories (one-way "
        "ANOVA, p = 0.74). The report presents the methodology, system design, "
        "implementation, results and the skills gained during the internship."),
        align="justify")

    # ---------------- List of figures ----------------
    doc.add_page_break()
    para(doc, "LIST OF FIGURES", size=14, bold=True, align="center",
         space_after=12)
    figs = [
        ("3.1", "System Architecture - Data Analytics Pipeline"),
        ("3.2", "Data Flow Diagram (Level 0 and Level 1)"),
        ("3.3", "UML Use-Case Diagram"),
        ("5.1", "Distribution of Book Prices"),
        ("5.2", "Average Book Price by Rating"),
        ("5.3", "Top 10 Categories by Number of Books"),
        ("5.4", "Price Distribution Across Ratings"),
        ("5.5", "Count of Books per Rating"),
        ("5.6", "Stock Availability"),
        ("5.7", "Consolidated Insights Dashboard"),
    ]
    for num, cap in figs:
        para(doc, f"Figure {num}:  {cap}", size=12, align="left",
             space_after=2)

    # ---------------- List of tables ----------------
    doc.add_page_break()
    para(doc, "LIST OF TABLES", size=14, bold=True, align="center",
         space_after=12)
    tabs = [
        ("1.1", "Tasks Completed"), ("2.1", "Tools and Libraries Used"),
        ("3.1", "Dataset Schema"), ("5.1", "Summary Statistics"),
        ("5.2", "Hypothesis Test Results"),
    ]
    for num, cap in tabs:
        para(doc, f"Table {num}:  {cap}", size=12, align="left", space_after=2)

    # ---------------- List of abbreviations ----------------
    doc.add_page_break()
    para(doc, "LIST OF ABBREVIATIONS", size=14, bold=True, align="center",
         space_after=12)
    abbrs = [
        ("API", "Application Programming Interface"),
        ("BS4", "BeautifulSoup 4 (HTML parsing library)"),
        ("CSV", "Comma-Separated Values"),
        ("DFD", "Data Flow Diagram"),
        ("EDA", "Exploratory Data Analysis"),
        ("HTML", "HyperText Markup Language"),
        ("IQR", "Interquartile Range"),
        ("NLP", "Natural Language Processing"),
        ("SCSE", "School of Computing Science and Engineering"),
        ("UML", "Unified Modeling Language"),
    ]
    for a, b in abbrs:
        para(doc, f"{a}  -  {b}", size=12, align="left", space_after=2)

    # ================= CHAPTER 1 =================
    chapter_heading(doc, "1", "Introduction")
    section(doc, "1.1  Objective of the Internship")
    para(doc, (
        "The objective of this internship was to gain practical, hands-on "
        "experience in the field of data analytics. Specifically, the "
        "internship aimed to: (i) acquire and prepare real-world data from "
        "public web sources; (ii) explore and validate that data using "
        "statistical techniques; and (iii) communicate the resulting insights "
        "through effective visualizations. The internship was designed to "
        "bridge the gap between the theoretical concepts learned in the "
        "classroom and their application in a professional setting."))
    section(doc, "1.2  Problem Statement and Research Objectives")
    para(doc, (
        "A large volume of useful information is available on the web in "
        "unstructured HTML form, which cannot be analysed directly. The "
        "problem addressed by this project is the extraction, cleaning, "
        "exploration and visualization of such data to support data-driven "
        "decision making. The research objectives were: (1) to build an "
        "automated pipeline that collects structured data from a website; "
        "(2) to perform an exploratory data analysis to identify trends, "
        "patterns and anomalies; and (3) to present those findings using "
        "clear, well-designed visualizations that support decision making."))
    section(doc, "1.3  Description of Domain")
    para(doc, (
        "The domain of this internship is Data Analytics, an "
        "interdisciplinary field that combines statistics, programming and "
        "domain knowledge to extract insights from data. Core sub-domains "
        "covered include: web scraping (data acquisition), data cleaning and "
        "wrangling, exploratory data analysis, statistical inference and data "
        "visualization. These techniques are widely applied in e-commerce, "
        "finance, healthcare, marketing and business intelligence."))
    section(doc, "1.4  A Brief Introduction about the Organization")
    para(doc, (
        "CodeAlpha is a software development and technology organization that "
        "specializes in data-driven decision making and business "
        "intelligence. The organization provides internship programs that "
        "give students practical exposure to modern tools such as Python, "
        "SQL and visualization libraries. Interns work on real-world projects "
        "in a collaborative environment, guided by experienced mentors, and "
        "develop the skills required to support data-driven strategies. The "
        "organization's activities span software development, analytics, "
        "reporting and business intelligence services."))

    # ================= CHAPTER 2 =================
    chapter_heading(doc, "2", "Technical Description")
    para(doc, (
        "The project was implemented entirely in Python 3.13 using the "
        "standard data analytics stack. Web scraping was performed with the "
        "requests library for HTTP communication and BeautifulSoup for HTML "
        "parsing. Data manipulation and aggregation were handled with pandas "
        "and NumPy, while statistical hypothesis testing was carried out with "
        "SciPy. Visualization was produced using Matplotlib and Seaborn. The "
        "complete pipeline was developed in Jupyter Notebook, and the source "
        "code is version-controlled with Git and hosted on GitHub."))
    table(doc, "2.1", "Tools and Libraries Used",
          ["Tool / Library", "Purpose"],
          [["Python 3.13", "Core programming language"],
           ["requests", "HTTP requests to fetch web pages"],
           ["BeautifulSoup4", "HTML parsing and data extraction"],
           ["pandas", "Tabular data manipulation and analysis"],
           ["NumPy", "Numerical computing"],
           ["SciPy", "Statistical tests (Pearson, ANOVA)"],
           ["Matplotlib", "Base plotting library"],
           ["Seaborn", "Statistical data visualization"],
           ["Jupyter Notebook", "Interactive development environment"],
           ["Git & GitHub", "Version control and code hosting"]])
    para(doc, (
        "Web scraping was implemented as an automated crawler that navigates "
        "the category tree of the target website, extracts the required "
        "fields from each product page, and handles pagination. The EDA "
        "module computes descriptive statistics, distribution profiles and "
        "inferential tests. The visualization module renders charts to PNG "
        "files and assembles a summary dashboard."))

    # ================= CHAPTER 3 =================
    chapter_heading(doc, "3", "System Design")
    section(doc, "3.1  General Architecture")
    para(doc, (
        "The system follows a linear, modular pipeline architecture. Each "
        "stage is independent and produces an artefact consumed by the next "
        "stage, which makes the system easy to test and extend."))
    figure(doc, "architecture.png", "3.1",
           "System Architecture - Data Analytics Pipeline")
    section(doc, "3.2  Design Phase")
    para(doc, (
        "The design phase decomposed the problem into four logical modules: "
        "data acquisition, data storage, data analysis and data "
        "presentation. The data flow and interaction between the user and "
        "the system were modelled using a Data Flow Diagram and a UML "
        "use-case diagram."))
    section(doc, "3.2.1  Data Flow Diagram")
    figure(doc, "dfd.png", "3.2",
           "Data Flow Diagram (Level 0 and Level 1)")
    section(doc, "3.2.2  UML Diagrams")
    para(doc, (
        "The use-case diagram below shows the primary actor (the data "
        "analyst/intern) and the use cases supported by the system, from "
        "scraping data through to interpreting insights."))
    figure(doc, "uml_usecase.png", "3.3", "UML Use-Case Diagram")
    section(doc, "3.3  Methodology")
    para(doc, (
        "The methodology followed the standard data analytics lifecycle: "
        "(1) Problem definition - the analytics questions were framed before "
        "any analysis; (2) Data acquisition - data was scraped from a public "
        "website; (3) Data preparation - the dataset was validated for "
        "missing values, duplicates and type consistency; (4) Exploratory "
        "analysis - descriptive statistics, distributions and correlations "
        "were examined and hypotheses were tested; (5) Visualization - charts "
        "and a dashboard were created to communicate findings; and "
        "(6) Reporting - results were documented and published to GitHub."))

    # ================= CHAPTER 4 =================
    chapter_heading(doc, "4", "System Implementation")
    para(doc, (
        "The pipeline was implemented as three independent Python scripts "
        "(also provided as Jupyter notebooks). The web scraping script "
        "crawls the target site, extracts title, price, rating, availability, "
        "stock count and category for each book, and writes the result to "
        "dataset/books.csv. The EDA script loads this CSV, prints and saves "
        "a structured report (dataset/eda_summary.txt), and runs hypothesis "
        "tests. The visualization script reads the CSV and saves seven charts "
        "to the images/ folder, including a consolidated dashboard."))
    table(doc, "3.1", "Dataset Schema",
          ["Field", "Type", "Description"],
          [["title", "string", "Name of the book"],
           ["price", "float", "Price in GBP"],
           ["rating", "int", "Star rating (1-5)"],
           ["in_stock", "bool", "Availability flag"],
           ["stock_count", "int", "Number of copies in stock"],
           ["category", "string", "Book category"]])
    para(doc, (
        "All modules are deterministic and re-runnable. The complete source "
        "code is available in the Appendices and on GitHub at "
        "https://github.com/Asmit1434/CodeAlpha_DataAnalytics."))

    # ================= CHAPTER 5 =================
    chapter_heading(doc, "5", "Results and Discussions")
    para(doc, (
        "The pipeline successfully scraped 1,000 books across 50 categories. "
        "The summary statistics below describe the quantitative variables."))
    table(doc, "5.1", "Summary Statistics",
          ["Statistic", "Price (GBP)", "Rating", "Stock Count"],
          [["Count", "1000", "1000", "1000"],
           ["Mean", "35.07", "2.92", "-"],
           ["Median", "35.98", "3.00", "-"],
           ["Min", "10.00", "1", "0"],
           ["Max", "59.99", "5", "-"]])
    para(doc, (
        "Two hypotheses were tested. The first examined whether the rating of "
        "a book is related to its price; the second examined whether prices "
        "differ significantly across categories."))
    table(doc, "5.2", "Hypothesis Test Results",
          ["Hypothesis", "Test", "Statistic", "p-value", "Conclusion"],
          [["Rating vs. Price", "Pearson correlation", "r = 0.028", "0.37",
            "Not significant"],
           ["Price across categories", "One-way ANOVA", "F = 0.839", "0.74",
            "Not significant"]])
    para(doc, (
        "No price outliers were detected using the IQR rule (upper fence = "
        "GBP 85.48). The most expensive categories on average were Suspense "
        "(58.33), Novels (54.81) and Politics (53.61). The following figures "
        "present the key visualizations."))
    figure(doc, "01_price_distribution.png", "5.1",
           "Distribution of Book Prices")
    figure(doc, "02_avg_price_by_rating.png", "5.2",
           "Average Book Price by Rating")
    figure(doc, "03_top_categories.png", "5.3",
           "Top 10 Categories by Number of Books")
    figure(doc, "04_price_vs_rating.png", "5.4",
           "Price Distribution Across Ratings")
    figure(doc, "05_rating_distribution.png", "5.5",
           "Count of Books per Rating")
    figure(doc, "06_stock_availability.png", "5.6", "Stock Availability")
    figure(doc, "07_dashboard.png", "5.7",
           "Consolidated Insights Dashboard", width=6.2)
    para(doc, (
        "Discussion: The absence of a strong rating-price correlation "
        "indicates that customer ratings are not driven by price, suggesting "
        "that quality perception is independent of cost in this market. The "
        "uniform distribution of ratings further implies a balanced product "
        "catalogue. From a business perspective, categories such as Suspense "
        "and Novels generate higher average revenue per unit and could be "
        "prioritized for marketing and inventory investment."))

    # ================= CHAPTER 6 =================
    chapter_heading(doc, "6", "Conclusion and Future Work")
    para(doc, (
        "This internship successfully demonstrated the complete data "
        "analytics lifecycle using Python. A custom dataset was acquired by "
        "web scraping, analysed statistically and presented through effective "
        "visualizations. The project reinforced core skills in data "
        "acquisition, cleaning, exploratory analysis, statistical inference, "
        "visualization and reporting. The findings provide actionable insight "
        "into the pricing and rating behaviour of the book market."))
    para(doc, (
        "Future work could extend the project by: (i) scraping additional "
        "attributes such as review text and publication date; (ii) applying "
        "sentiment analysis to customer reviews; (iii) automating the pipeline "
        "with a scheduler; and (iv) deploying the dashboard as an interactive "
        "web application using Plotly Dash or Streamlit."))

    # ================= CHAPTER 7 =================
    chapter_heading(doc, "7", "Appendices")
    section(doc, "7.1  Source Code")
    para(doc, "Excerpt - Task 1: Web Scraping (scripts/task1_web_scraping.py)",
         bold=True, align="left")
    code1 = (
        "def get_soup(url):\n"
        "    headers = {\"User-Agent\": \"Mozilla/5.0 (CodeAlpha Scraper)\"}\n"
        "    r = requests.get(url, headers=headers, timeout=20)\n"
        "    r.raise_for_status()\n"
        "    r.encoding = \"utf-8\"\n"
        "    return BeautifulSoup(r.text, \"html.parser\")\n\n"
        "def scrape_category(url, name):\n"
        "    rows = []\n"
        "    while url:\n"
        "        soup = get_soup(url)\n"
        "        for a in soup.select(\"article.product_pod\"):\n"
        "            avail = a.select_one(\"p.instock.availability\").text\n"
        "            nums = re.findall(r\"\\d+\", avail)\n"
        "            rows.append({\n"
        "                \"title\": a.h3.a[\"title\"],\n"
        "                \"price\": float(a.select_one(\"p.price_color\").text[1:]),\n"
        "                \"rating\": parse_rating(a.select_one(\"p.star-rating\")[\"class\"]),\n"
        "                \"in_stock\": \"In stock\" in avail,\n"
        "                \"stock_count\": int(nums[0]) if nums else 0,\n"
        "                \"category\": name,\n"
        "            })\n"
        "        nxt = soup.select_one(\"li.next > a\")\n"
        "        url = url.rsplit(\"/\", 1)[0] + \"/\" + nxt[\"href\"] if nxt else None\n"
        "    return rows")
    _code_block(doc, code1)

    para(doc, "Excerpt - Task 2: EDA (scripts/task2_eda.py)",
         bold=True, align="left")
    code2 = (
        "corr, p = stats.pearsonr(df[\"rating\"], df[\"price\"])\n"
        "groups = [g[\"price\"].values for _, g in df.groupby(\"category\")\n"
        "          if len(g) > 2]\n"
        "f_stat, p_anova = stats.f_oneway(*groups)\n"
        "q1, q3 = df[\"price\"].quantile([0.25, 0.75])\n"
        "upper = q3 + 1.5 * (q3 - q1)\n"
        "outliers = df[df[\"price\"] > upper]")
    _code_block(doc, code2)

    para(doc, "Excerpt - Task 3: Visualization (scripts/task3_visualization.py)",
         bold=True, align="left")
    code3 = (
        "sns.histplot(df[\"price\"], kde=True, bins=30)\n"
        "sns.barplot(data=df, x=\"rating\", y=\"price\", estimator=\"mean\")\n"
        "top = df[\"category\"].value_counts().head(10)\n"
        "sns.barplot(x=top.values, y=top.index)\n"
        "plt.savefig(\"images/chart.png\", bbox_inches=\"tight\")")
    _code_block(doc, code3)
    para(doc, "Full source code: https://github.com/Asmit1434/"
              "CodeAlpha_DataAnalytics", italic=True, align="left")

    section(doc, "7.2  Learning Experiences")
    para(doc, "Knowledge acquired:", bold=True, align="left")
    para(doc, (
        "I gained a clear understanding of the end-to-end data analytics "
        "workflow. This connected directly to coursework in Python "
        "programming, probability and statistics, and database systems. I "
        "learned how HTML documents are structured and how to navigate them "
        "programmatically, how to clean and reshape tabular data with pandas, "
        "and how to apply statistical tests such as Pearson correlation and "
        "one-way ANOVA."))
    para(doc, "Skills learned:", bold=True, align="left")
    para(doc, (
        "I developed practical skills in writing web scrapers, handling HTTP "
        "requests and pagination, and dealing with real-world data quality "
        "issues. I also strengthened my ability to interpret reports, "
        "translate raw numbers into business insights, and present findings "
        "visually. Version control with Git and documentation of a project "
        "were additional skills acquired."))
    para(doc, "Observed attitudes and gained values:", bold=True, align="left")
    para(doc, (
        "The internship reinforced the value of patience, attention to detail "
        "and dependability. Debugging scrapers and validating data required "
        "persistence, while meeting task deadlines required discipline and "
        "time management. I learned the importance of honesty in reporting "
        "results - including negative findings."))
    para(doc, "The most challenging task performed:", bold=True, align="left")
    para(doc, (
        "The most challenging task was building the web scraper to reliably "
        "handle pagination and inconsistent HTML. The site returned results "
        "across multiple pages and the availability text varied in format. I "
        "overcame this by inspecting the HTML structure, writing a reusable "
        "parsing function, and using regular expressions to extract "
        "numerical stock counts. Testing on a small subset before running the "
        "full crawl prevented large-scale errors."))

    section(doc, "7.3  SWOT Analysis")
    para(doc, (
        "The following SWOT analysis is presented for CodeAlpha, the "
        "organization where the internship was carried out."))
    para(doc, "Strengths:", bold=True, align="left")
    bullet(doc, "Focus on data-driven decision making and business "
                "intelligence.")
    bullet(doc, "Structured internship programs providing real-world project "
                "exposure.")
    bullet(doc, "Use of industry-standard tools (Python, SQL, BI libraries).")
    bullet(doc, "Mentorship and a collaborative learning environment.")
    para(doc, "Weaknesses:", bold=True, align="left")
    bullet(doc, "As a growing organization, brand recognition is lower than "
                "large established firms.")
    bullet(doc, "Internship tasks are time-constrained, limiting depth of "
                "exploration.")
    para(doc, "Opportunities:", bold=True, align="left")
    bullet(doc, "Rapidly growing demand for analytics and BI services.")
    bullet(doc, "Potential to expand into AI/ML and cloud-based analytics.")
    bullet(doc, "Strong pipeline of skilled interns as future talent.")
    para(doc, "Threats:", bold=True, align="left")
    bullet(doc, "Intense competition from larger analytics and consulting "
                "firms.")
    bullet(doc, "Rapidly changing technology requiring continuous upskilling.")
    bullet(doc, "Data privacy and compliance risks in data handling.")

    doc.save(OUT)
    print("Report saved to:", OUT)


def _code_block(doc, code):
    for line in code.split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(line if line.strip() else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(9)
        rpr = run._element.get_or_add_rPr()
        rfonts = rpr.get_or_add_rFonts()
        for attr in ("w:ascii", "w:hAnsi", "w:cs"):
            rfonts.set(qn(attr), "Consolas")
    doc.add_paragraph()


if __name__ == "__main__":
    generate_diagrams()
    build_docx()
