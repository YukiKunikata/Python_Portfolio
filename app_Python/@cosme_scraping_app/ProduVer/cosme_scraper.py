import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from datetime import datetime
import re
import os

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
    page_title = "ランキング"  # デフォルトタイトル

    while next_urls:
        url = next_urls.pop(0)
        if url in visited_urls:
            continue
        visited_urls.add(url)

        print(f"🔍 {url} を処理中...")

        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ 初回のみタイトル取得
        if page_title == "ランキング":
            title_elem = soup.select_one("#keyword-sp-ttl > div:nth-of-type(2) > h2")
            if title_elem:
                page_title = title_elem.get_text(strip=True)
                # ファイル名に使えない文字を除去（例：/ \ : * ? " < > |）
                page_title = re.sub(r'[\\/:*?"<>|]', '', page_title)

        # ✅ ランキング部分の抽出
        ranking_section = soup.find("div", id="keyword-ranking-list")
        if not ranking_section:
            continue

        # ✅ 商品名とURLを抽出
        items = ranking_section.select("h4 a")

        for a in items:
            name = a.get_text(strip=True)
            href = a.get("href")
            if not name or not href:
                continue
            href = urljoin("https://www.cosme.net", href)
            all_data.append([name, href, url])

        # ✅ フッター内のリンクを巡回
        footer = soup.find("div", id="keyword-ranking-footer")
        if footer:
            footer_links = footer.select("a")
            for link in footer_links:
                next_href = link.get("href")
                if next_href:
                    next_url = urljoin(url, next_href)
                    if next_url not in visited_urls:
                        next_urls.append(next_url)

    # ✅ DataFrame作成
    df = pd.DataFrame(all_data, columns=["コスメ名", "URL", "取得元ページ"])
    df.insert(0, "No", range(1, len(df) + 1))

    return df, page_title


def save_to_excel(df, folder_path, title):
    # ✅ タイトルと日時を含めたファイル名を生成
    now = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"@コスメ_{title}_{now}.xlsx"

    # ✅ 保存先パスを結合
    file_path = os.path.join(folder_path, file_name)

    df.to_excel(file_path, index=False)
    return file_path
