import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict


BASE_URL = "https://www.scrapethissite.com/pages/forms/"
OUTPUT_DIR = "output"


def fetch_page(page_number: int) -> BeautifulSoup:
    """Fetch and parse a page"""
    url = f"{BASE_URL}?page_num={page_number}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_teams(soup: BeautifulSoup) -> List[Dict]:
    """Extract team data from page"""
    teams = []
    rows = soup.find_all("tr", class_="team")

    for row in rows:
        team = {
            "name": row.find("td", class_="name").text.strip(),
            "year": int(row.find("td", class_="year").text.strip()),
            "wins": int(row.find("td", class_="wins").text.strip()),
            "losses": int(row.find("td", class_="losses").text.strip()),
        }
        teams.append(team)

    return teams


def scrape_all_pages() -> pd.DataFrame:
    """Scrape all pages until no data is found"""
    page_number = 1
    all_data = []

    while True:
        print(f"🔍 Scraping page {page_number}...")

        soup = fetch_page(page_number)
        page_data = parse_teams(soup)

        if not page_data:
            print("✅ No more data found. Stopping.")
            break

        all_data.extend(page_data)
        page_number += 1

    return pd.DataFrame(all_data)


def save_outputs(df: pd.DataFrame) -> None:
    """Save DataFrame to Excel and CSV"""
    df.to_excel(f"{OUTPUT_DIR}/teams.xlsx", index=False)
    df.to_csv(f"{OUTPUT_DIR}/teams.csv", index=False, encoding="utf-8-sig")
    print("💾 Files saved successfully.")


def main():
    df = scrape_all_pages()
    save_outputs(df)


if __name__ == "__main__":
    main()
