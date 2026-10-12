# CodeAlpha Data Analytics Internship

**Domain:** Data Analytics
**Tasks completed:** 3 of 4 (Web Scraping, EDA, Data Visualization)
**Author:** Asmit Singh

This repository contains a complete, end-to-end data analytics workflow:
**collect data (web scraping) -> understand it (EDA) -> communicate it (visualization)**.

---

## Tasks Covered

| # | Task | Deliverable | Status |
|---|------|-------------|--------|
| 1 | Web Scraping | `scripts/task1_web_scraping.py`, `CodeAlpha_Task1_WebScraping.ipynb`, `dataset/books.csv` | Done |
| 2 | Exploratory Data Analysis | `scripts/task2_eda.py`, `CodeAlpha_Task2_EDA.ipynb`, `dataset/eda_summary.txt` | Done |
| 3 | Data Visualization | `scripts/task3_visualization.py`, `CodeAlpha_Task3_Visualization.ipynb`, `images/` | Done |

---

## Dataset

Books were scraped from **books.toscrape.com**, a public website built for
scraping practice.

- **Records:** 1,000 books
- **Categories:** 50
- **Fields:** `title`, `price`, `rating`, `in_stock`, `stock_count`, `category`

---

## Tools & Libraries

`Python` · `pandas` · `numpy` · `scipy` · `matplotlib` · `seaborn` · `requests` · `BeautifulSoup`

---

## Key Insights (from EDA)

- **1,000 books** across **50 categories** were analysed.
- **Average price:** GBP 35.07 (median GBP 35.98).
- **Average rating:** 2.92 / 5.
- **Rating vs. price:** no significant relationship (Pearson r = 0.028, p = 0.37).
- **Price by category:** no statistically significant difference (one-way ANOVA, p = 0.74).
- **Outliers:** none above the IQR upper fence (GBP 85.48).
- **Most expensive categories (avg):** Suspense (58.33), Novels (54.81), Politics (53.61).

Full report: [`dataset/eda_summary.txt`](dataset/eda_summary.txt)

---

## Visualizations

| Chart | Preview |
|-------|---------|
| Price distribution | `images/01_price_distribution.png` |
| Average price by rating | `images/02_avg_price_by_rating.png` |
| Top 10 categories | `images/03_top_categories.png` |
| Price vs. rating | `images/04_price_vs_rating.png` |
| Rating distribution | `images/05_rating_distribution.png` |
| Stock availability | `images/06_stock_availability.png` |
| Insights dashboard | `images/07_dashboard.png` |

---

## How to Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the full pipeline (from the repository root):

   ```bash
   python scripts/task1_web_scraping.py
   python scripts/task2_eda.py
   python scripts/task3_visualization.py
   ```

   Or open the three notebooks (`CodeAlpha_Task*.ipynb`) and run all cells.

---

## Project Structure

```
CodeAlpha_DataAnalytics-EDA-Visualization/
+-- CodeAlpha_Task1_WebScraping.ipynb
+-- CodeAlpha_Task2_EDA.ipynb
+-- CodeAlpha_Task3_Visualization.ipynb
+-- dataset/
|   +-- books.csv
|   +-- eda_summary.txt
+-- images/
|   +-- 01_price_distribution.png ... 07_dashboard.png
+-- scripts/
|   +-- task1_web_scraping.py
|   +-- task2_eda.py
|   +-- task3_visualization.py
|   +-- build_notebooks.py
+-- README.md
+-- requirements.txt
```

---

## Note on Ethics

`books.toscrape.com` is a sandbox site explicitly created for scraping
practice. Always check a website's `robots.txt` and terms of service before
scraping real production sites.
