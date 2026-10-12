"""
TASK 3: DATA VISUALIZATION
==========================
CodeAlpha Data Analytics Internship

Loads dataset/books.csv and produces a set of charts that communicate the
insights discovered during EDA. Each figure is saved into the images/ folder.

Charts produced:
  1. Distribution of book prices (histogram + KDE)
  2. Average price by rating (bar chart)
  3. Top 10 categories by book count (horizontal bar)
  4. Price vs Rating (box plot)
  5. Rating distribution (count plot)
  6. Stock availability (pie chart)
  7. Combined insights dashboard
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

SCRIPT_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "dataset", "books.csv")
IMG_DIR = os.path.join(SCRIPT_DIR, "..", "images")
os.makedirs(IMG_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 120


def save(fig, name):
    path = os.path.join(IMG_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


def main():
    if not os.path.exists(DATA_FILE):
        raise SystemExit(
            f"Dataset not found at {DATA_FILE}.\n"
            "Run scripts/task1_web_scraping.py first."
        )

    df = pd.read_csv(DATA_FILE)

    # 1. Price distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["price"], kde=True, bins=30, ax=ax, color="#4C72B0")
    ax.set_title("Distribution of Book Prices")
    ax.set_xlabel("Price (GBP)")
    ax.set_ylabel("Number of Books")
    save(fig, "01_price_distribution.png")

    # 2. Average price by rating
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x="rating", y="price", estimator="mean",
                errorbar=None, ax=ax, hue="rating", legend=False, palette="crest")
    ax.set_title("Average Book Price by Rating")
    ax.set_xlabel("Rating (stars)")
    ax.set_ylabel("Average Price (GBP)")
    save(fig, "02_avg_price_by_rating.png")

    # 3. Top 10 categories
    fig, ax = plt.subplots(figsize=(9, 6))
    top = df["category"].value_counts().head(10)
    sns.barplot(x=top.values, y=top.index, ax=ax, hue=top.index, legend=False,
                palette="magma")
    ax.set_title("Top 10 Categories by Number of Books")
    ax.set_xlabel("Number of Books")
    ax.set_ylabel("")
    save(fig, "03_top_categories.png")

    # 4. Price vs Rating box plot
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="rating", y="price", ax=ax, hue="rating",
                legend=False, palette="Set2")
    ax.set_title("Price Distribution Across Ratings")
    ax.set_xlabel("Rating (stars)")
    ax.set_ylabel("Price (GBP)")
    save(fig, "04_price_vs_rating.png")

    # 5. Rating distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x="rating", ax=ax, hue="rating", legend=False,
                  palette="Blues")
    ax.set_title("Count of Books per Rating")
    ax.set_xlabel("Rating (stars)")
    ax.set_ylabel("Number of Books")
    save(fig, "05_rating_distribution.png")

    # 6. Stock availability pie
    fig, ax = plt.subplots(figsize=(6, 6))
    counts = df["in_stock"].value_counts()
    labels = ["In Stock" if v else "Out of Stock" for v in counts.index]
    ax.pie(counts.values, labels=labels, autopct="%1.1f%%",
           colors=["#55A868", "#C44E52"], startangle=90)
    ax.set_title("Stock Availability")
    save(fig, "06_stock_availability.png")

    # 7. Dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("CodeAlpha - Book Dataset Insights Dashboard",
                 fontsize=16, fontweight="bold")

    sns.histplot(df["price"], kde=True, bins=30, ax=axes[0, 0], color="#4C72B0")
    axes[0, 0].set_title("Price Distribution")
    axes[0, 0].set_xlabel("Price (GBP)")

    sns.countplot(data=df, x="rating", ax=axes[0, 1], hue="rating",
                  legend=False, palette="Blues")
    axes[0, 1].set_title("Books per Rating")
    axes[0, 1].set_xlabel("Rating (stars)")

    top10 = df["category"].value_counts().head(10)
    sns.barplot(x=top10.values, y=top10.index, ax=axes[1, 0],
                hue=top10.index, legend=False, palette="magma")
    axes[1, 0].set_title("Top 10 Categories")
    axes[1, 0].set_xlabel("Number of Books")

    cat_price = (df.groupby("category")["price"].mean()
                 .sort_values(ascending=False).head(10))
    sns.barplot(x=cat_price.values, y=cat_price.index, ax=axes[1, 1],
                hue=cat_price.index, legend=False, palette="viridis")
    axes[1, 1].set_title("Top 10 Categories by Avg Price")
    axes[1, 1].set_xlabel("Avg Price (GBP)")

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    save(fig, "07_dashboard.png")

    print("\nAll visualizations generated successfully.")


if __name__ == "__main__":
    main()
