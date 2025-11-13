import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def scrape_ranking_pages(start_url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    all_data = []
    visited_urls = set()
    next_urls = [start_url]

    while next_urls:
        url = next_urls.pop(0)
        if url in visited_urls:
            continue
        visited_urls.add(url)

        print(f"🔍 {url} を処理中...")

        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ ランキング部分の抽出
        ranking_section = soup.find("div", id="keyword-ranking-list")
        if not ranking_section:
            continue

        # ✅ 商品名とURLを抽出（XPath: //*[@id="keyword-ranking-list"]//h4）
        items = ranking_section.select("h4 a")

        rank = 1
        for a in items:
            name = a.get_text(strip=True)
            href = a.get("href")
            if not name or not href:
                continue
            href = urljoin("https://www.cosme.net", href)
            all_data.append([name, href, url, rank])
            rank += 1

        # ✅ 次のページリンク取得（XPath: //*[@id="keyword-ranking-footer"]//a）
        footer = soup.find("div", id="keyword-ranking-footer")
        if footer:
            footer_links = footer.select("a")
            for link in footer_links:
                next_href = link.get("href")
                if next_href:
                    next_url = urljoin(url, next_href)
                    if next_url not in visited_urls:
                        next_urls.append(next_url)

    df = pd.DataFrame(all_data, columns=["コスメ名", "URL", "取得元ページ", "順位"])
    return df


def save_to_excel(df, file_path):
    df.to_excel(file_path, index=False)
