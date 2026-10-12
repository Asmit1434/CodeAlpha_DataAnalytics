"""
TASK 2: EXPLORATORY DATA ANALYSIS (EDA)
=======================================
CodeAlpha Data Analytics Internship

Loads dataset/books.csv (produced by task1_web_scraping.py) and performs
a full exploratory analysis:

  * Structure & data types
  * Summary statistics
  * Missing values / duplicates
  * Distributions (price, rating, category)
  * Hypotheses tests (rating vs price, category price differences)
  * Detected anomalies / data issues

Prints a readable report to the console and writes dataset/eda_summary.txt
"""

import os
import numpy as np
import pandas as pd
from scipy import stats

SCRIPT_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "dataset", "books.csv")
REPORT_FILE = os.path.join(SCRIPT_DIR, "..", "dataset", "eda_summary.txt")

_out = []


def log(text=""):
    print(text)
    _out.append(str(text))


def section(title):
    log("")
    log("=" * 70)
    log(title)
    log("=" * 70)


def main():
    if not os.path.exists(DATA_FILE):
        raise SystemExit(
            f"Dataset not found at {DATA_FILE}.\n"
            "Run scripts/task1_web_scraping.py first."
        )

    df = pd.read_csv(DATA_FILE)

    # ---------------------------------------------------------------- 1
    section("1. DATASET STRUCTURE")
    log(f"Shape (rows, columns): {df.shape}")
    log("\nColumn names:")
    for c in df.columns:
        log(f"  - {c}")
    log("\nData types:")
    log(df.dtypes.to_string())
    log("\nFirst 5 rows:")
    log(df.head().to_string())

    # ---------------------------------------------------------------- 2
    section("2. DATA QUALITY: MISSING VALUES & DUPLICATES")
    log("Missing values per column:")
    log(df.isnull().sum().to_string())
    dup_titles = df["title"].duplicated().sum()
    log(f"\nDuplicate titles: {dup_titles}")

    # ---------------------------------------------------------------- 3
    section("3. SUMMARY STATISTICS (numeric)")
    log(df[["price", "rating", "stock_count"]].describe().to_string())

    # ---------------------------------------------------------------- 4
    section("4. CATEGORICAL OVERVIEW")
    log(f"Number of categories : {df['category'].nunique()}")
    log(f"Books in stock       : {int(df['in_stock'].sum())} / {len(df)}")
    log("\nTop 10 categories by number of books:")
    log(df["category"].value_counts().head(10).to_string())
    log("\nRating distribution:")
    log(df["rating"].value_counts().sort_index().to_string())

    # ---------------------------------------------------------------- 5
    section("5. HYPOTHESIS TESTS")

    # H1: Is price correlated with rating?
    corr, p_corr = stats.pearsonr(df["rating"], df["price"])
    log("\nH1: Does rating correlate with price?")
    log(f"    Pearson r = {corr:.4f}   p-value = {p_corr:.4e}")
    log("    -> " + ("SIGNIFICANT" if p_corr < 0.05 else "NOT significant")
        + " relationship.")

    # H2: Do categories differ in average price? (one-way ANOVA)
    groups = [g["price"].values for _, g in df.groupby("category") if len(g) > 2]
    f_stat, p_anova = stats.f_oneway(*groups)
    log("\nH2: Do book prices differ significantly across categories?")
    log(f"    One-way ANOVA F = {f_stat:.4f}   p-value = {p_anova:.4e}")
    log("    -> " + ("SIGNIFICANT" if p_anova < 0.05 else "NOT significant")
        + " difference between categories.")

    # ---------------------------------------------------------------- 6
    section("6. ANOMALIES & DATA ISSUES")
    q1, q3 = df["price"].quantile([0.25, 0.75])
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    outliers = df[df["price"] > upper]
    log(f"Price IQR: Q1={q1:.2f}, Q3={q3:.2f}, upper fence={upper:.2f}")
    log(f"Price outliers detected: {len(outliers)}")
    if len(outliers):
        log("\nTop 5 most expensive books:")
        log(outliers.sort_values("price", ascending=False)
            .head()[["title", "price", "category"]].to_string(index=False))

    log("\nMost expensive category (avg):")
    log(df.groupby("category")["price"].mean().sort_values(ascending=False)
        .head(5).to_string())

    # ---------------------------------------------------------------- 7
    section("7. KEY FINDINGS")
    log(f"* {df.shape[0]} books across {df['category'].nunique()} categories.")
    log(f"* Average book price: GBP {df['price'].mean():.2f} "
        f"(median {df['price'].median():.2f}).")
    log(f"* Average rating: {df['rating'].mean():.2f} / 5.")
    log(f"* Price-rating correlation is "
        f"{'weak/none' if abs(corr) < 0.3 else 'notable'} (r={corr:.3f}).")
    log("* Best-value categories identified (see findings above).")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(_out))
    print(f"\nReport saved to: {os.path.abspath(REPORT_FILE)}")


if __name__ == "__main__":
    main()
