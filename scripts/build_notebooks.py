"""Generates the three Jupyter notebooks for the CodeAlpha submission.

The notebooks are self-contained (paths are relative to the repository root)
so that they can be run top-to-bottom inside Jupyter.
"""

import os
import nbformat as nbf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def make_notebook(cells):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    return nb


# --------------------------------------------------------------------------
TASK1_MD = """# Task 1 - Web Scraping
**CodeAlpha Data Analytics Internship**

Goal: collect a real dataset from the web using Python.

* Website: `http://books.toscrape.com/` (a site built specifically for scraping practice)
* Library: `requests` + `BeautifulSoup`
* Fields extracted: title, price, rating, availability, stock count, category
* Output: `dataset/books.csv`
"""

TASK1_CODE = r'''
import os, re, time, csv
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"
OUTPUT_FILE = "dataset/books.csv"
os.makedirs("dataset", exist_ok=True)

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (CodeAlpha Internship Scraper)"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "html.parser")

def scrape_category(url, name):
    rows, page = [], 1
    while url:
        soup = get_soup(url)
        for a in soup.select("article.product_pod"):
            avail = a.select_one("p.instock.availability").text.strip()
            nums = re.findall(r"\d+", avail)
            rating = next((RATING_MAP[c] for c in a.select_one("p.star-rating")["class"] if c in RATING_MAP), None)
            rows.append({
                "title": a.h3.a["title"],
                "price": float(a.select_one("p.price_color").text.replace("\u00a3", "")),
                "rating": rating,
                "in_stock": "In stock" in avail,
                "stock_count": int(nums[0]) if nums else 0,
                "category": name,
            })
        nxt = soup.select_one("li.next > a")
        url = url.rsplit("/", 1)[0] + "/" + nxt["href"] if nxt else None
        page += 1
        time.sleep(0.1)
    return rows

soup = get_soup(BASE_URL)
categories = [(l.text.strip(), BASE_URL + "catalogue/" + l["href"].replace("catalogue/", "").replace("index.html", ""))
              for l in soup.select("div.side_categories ul li ul li a")]
print(f"Found {len(categories)} categories")

all_rows = []
for name, url in categories:
    all_rows.extend(scrape_category(url, name))

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["title", "price", "rating", "in_stock", "stock_count", "category"])
    w.writeheader()
    w.writerows(all_rows)

print(f"Scraped {len(all_rows)} books -> {OUTPUT_FILE}")
'''

TASK1_VERIFY = r'''
import pandas as pd
df = pd.read_csv("dataset/books.csv")
print("Shape:", df.shape)
df.head()
'''

# --------------------------------------------------------------------------
TASK2_MD = """# Task 2 - Exploratory Data Analysis (EDA)
**CodeAlpha Data Analytics Internship**

Questions asked before analysis:
1. What is the price distribution of books?
2. Do higher-rated books cost more?
3. Which categories have the most/expensive books?
4. Are there missing values, duplicates or outliers?

Techniques: structure inspection, summary statistics, distributions,
Pearson correlation, one-way ANOVA, IQR outlier detection.
"""

TASK2_CODE = r'''
import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv("dataset/books.csv")

print("Shape:", df.shape)
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicate titles:", df["title"].duplicated().sum())
print("\nSummary statistics:\n", df[["price", "rating", "stock_count"]].describe())
print("\nCategories:", df["category"].nunique())
print("In stock:", int(df["in_stock"].sum()), "/", len(df))
'''

TASK2_STATS = r'''
# H1: rating vs price
corr, p_corr = stats.pearsonr(df["rating"], df["price"])
print(f"H1 rating~price: Pearson r={corr:.4f}, p={p_corr:.4e}")

# H2: price across categories (ANOVA)
groups = [g["price"].values for _, g in df.groupby("category") if len(g) > 2]
f_stat, p_anova = stats.f_oneway(*groups)
print(f"H2 category price: ANOVA F={f_stat:.4f}, p={p_anova:.4e}")

# Outliers (IQR)
q1, q3 = df["price"].quantile([0.25, 0.75])
upper = q3 + 1.5*(q3-q1)
print(f"Price outliers: {(df['price'] > upper).sum()}")
print("\nMost expensive categories (avg):")
print(df.groupby("category")["price"].mean().sort_values(ascending=False).head())
'''

# --------------------------------------------------------------------------
TASK3_MD = """# Task 3 - Data Visualization
**CodeAlpha Data Analytics Internship**

Turns the EDA findings into clear visuals using Matplotlib & Seaborn.
All charts are saved to the `images/` folder.
"""

TASK3_CODE = r'''
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("images", exist_ok=True)
sns.set_theme(style="whitegrid", palette="viridis")
df = pd.read_csv("dataset/books.csv")

def save(fig, name):
    fig.savefig(f"images/{name}", bbox_inches="tight")
    plt.close(fig)

# 1. Price distribution
fig, ax = plt.subplots(figsize=(8,5))
sns.histplot(df["price"], kde=True, bins=30, ax=ax, color="#4C72B0")
ax.set_title("Distribution of Book Prices"); ax.set_xlabel("Price (GBP)")
save(fig, "01_price_distribution.png")

# 2. Average price by rating
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(data=df, x="rating", y="price", estimator="mean",
            errorbar=None, ax=ax, hue="rating", legend=False, palette="crest")
ax.set_title("Average Book Price by Rating"); ax.set_xlabel("Rating")
save(fig, "02_avg_price_by_rating.png")

# 3. Top 10 categories
fig, ax = plt.subplots(figsize=(9,6))
top = df["category"].value_counts().head(10)
sns.barplot(x=top.values, y=top.index, ax=ax, hue=top.index, legend=False, palette="magma")
ax.set_title("Top 10 Categories by Number of Books")
save(fig, "03_top_categories.png")

# 4. Price vs rating
fig, ax = plt.subplots(figsize=(8,5))
sns.boxplot(data=df, x="rating", y="price", ax=ax, hue="rating", legend=False, palette="Set2")
ax.set_title("Price Distribution Across Ratings")
save(fig, "04_price_vs_rating.png")

# 5. Rating distribution
fig, ax = plt.subplots(figsize=(8,5))
sns.countplot(data=df, x="rating", ax=ax, hue="rating", legend=False, palette="Blues")
ax.set_title("Count of Books per Rating")
save(fig, "05_rating_distribution.png")

# 6. Stock availability
fig, ax = plt.subplots(figsize=(6,6))
counts = df["in_stock"].value_counts()
ax.pie(counts.values, labels=["In Stock" if v else "Out of Stock" for v in counts.index],
       autopct="%1.1f%%", colors=["#55A868", "#C44E52"], startangle=90)
ax.set_title("Stock Availability")
save(fig, "06_stock_availability.png")

# 7. Dashboard
fig, axes = plt.subplots(2, 2, figsize=(14,10))
fig.suptitle("Book Dataset Insights Dashboard", fontsize=16, fontweight="bold")
sns.histplot(df["price"], kde=True, bins=30, ax=axes[0,0], color="#4C72B0")
axes[0,0].set_title("Price Distribution")
sns.countplot(data=df, x="rating", ax=axes[0,1], hue="rating", legend=False, palette="Blues")
axes[0,1].set_title("Books per Rating")
sns.barplot(x=top.values, y=top.index, ax=axes[1,0], hue=top.index, legend=False, palette="magma")
axes[1,0].set_title("Top 10 Categories")
cat_price = df.groupby("category")["price"].mean().sort_values(ascending=False).head(10)
sns.barplot(x=cat_price.values, y=cat_price.index, ax=axes[1,1], hue=cat_price.index, legend=False, palette="viridis")
axes[1,1].set_title("Top Categories by Avg Price")
fig.tight_layout(rect=[0,0,1,0.97])
save(fig, "07_dashboard.png")
print("Saved all charts to images/")
'''

for name, md, code in [
    ("CodeAlpha_Task1_WebScraping.ipynb", TASK1_MD, TASK1_CODE),
    ("CodeAlpha_Task2_EDA.ipynb", TASK2_MD, TASK2_CODE),
    ("CodeAlpha_Task3_Visualization.ipynb", TASK3_MD, TASK3_CODE),
]:
    cells = [nbf.v4.new_markdown_cell(md), nbf.v4.new_code_cell(code.strip())]
    if name.endswith("Task1_WebScraping.ipynb"):
        cells.append(nbf.v4.new_markdown_cell("### Verify the scraped dataset"))
        cells.append(nbf.v4.new_code_cell(TASK1_VERIFY.strip()))
    if name.endswith("Task2_EDA.ipynb"):
        cells.append(nbf.v4.new_markdown_cell("### Statistical tests & outliers"))
        cells.append(nbf.v4.new_code_cell(TASK2_STATS.strip()))
    path = os.path.join(ROOT, name)
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(make_notebook(cells), f)
    print("Created", path)
