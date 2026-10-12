"""
TASK 1: WEB SCRAPING
====================
CodeAlpha Data Analytics Internship

Scrapes book data from http://books.toscrape.com/ -- a website explicitly
built for scraping practice (safe & legal to scrape).

Extracts: title, price, rating, availability, category, stock count
Output  : dataset/books.csv
"""

import os
import re
import csv
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "books.csv")

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (CodeAlpha Internship Scraper)"}
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def parse_rating(class_attr):
    for cls in class_attr:
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    return None


def parse_stock(text):
    nums = re.findall(r"\d+", text)
    return int(nums[0]) if nums else 0


def scrape_category(category_url, category_name):
    """Walk through every page of one category and return book rows."""
    rows = []
    url = category_url
    page = 1
    while url:
        print(f"  Scraping {category_name} - page {page}: {url}")
        soup = get_soup(url)

        for article in soup.select("article.product_pod"):
            title = article.h3.a["title"]
            price = float(article.select_one("p.price_color").text.replace("£", ""))
            rating = parse_rating(article.select_one("p.star-rating")["class"])
            availability = article.select_one("p.instock.availability").text.strip()
            stock = parse_stock(availability)

            rows.append({
                "title": title,
                "price": price,
                "rating": rating,
                "in_stock": "In stock" in availability,
                "stock_count": stock,
                "category": category_name,
            })

        next_btn = soup.select_one("li.next > a")
        if next_btn:
            url = url.rsplit("/", 1)[0] + "/" + next_btn["href"]
            page += 1
            time.sleep(0.2)
        else:
            url = None
    return rows


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Fetching category list...")
    soup = get_soup(BASE_URL)

    categories = []
    for link in soup.select("div.side_categories ul li ul li a"):
        name = link.text.strip()
        href = link["href"].replace("catalogue/", "").replace("index.html", "")
        categories.append((name, BASE_URL + "catalogue/" + href))

    print(f"Found {len(categories)} categories.\n")

    all_rows = []
    for name, url in categories:
        all_rows.extend(scrape_category(url, name))

    fieldnames = ["title", "price", "rating", "in_stock", "stock_count", "category"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nDone. Scraped {len(all_rows)} books.")
    print(f"Saved to: {os.path.abspath(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
