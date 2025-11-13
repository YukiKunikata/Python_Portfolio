import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_ranking_pages(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # ✅ ランキング部分（<div id="keyword-ranking-list">）を限定
    ranking_section = soup.find("div", id="keyword-ranking-list")
    if not ranking_section:
        raise ValueError("ランキング部分が見つかりません。HTML構造が変更された可能性があります。")

    # ✅ 「<h4>」タグ配下のリンクのみ抽出（XPathでいう //*[@id="keyword-ranking-list"]//h4）
    items = ranking_section.select("h4 a")
    
    data = []
    rank = 1

    for a in items:
        if not a.name == "a":
            continue
        name = a.get_text(strip=True)
        href = a.get("href")

        # 不要なリンクを除外
        if not href or not name or href.startswith("#"):
            continue

        # 相対パスを絶対URLに変換
        if href.startswith("/"):
            href = "https://www.cosme.net" + href

        data.append([rank, name, href])
        rank += 1
        if rank > 100:
            break

    df = pd.DataFrame(data, columns=["順位", "コスメ名", "URL"])
    return df
