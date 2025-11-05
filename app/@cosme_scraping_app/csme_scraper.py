# スクレイピングとExcel 出力をメイン処理とする。
# cosme_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; cosme-scraper/1.0; +https://example.com/)"
}

def fetch_page(url, timeout=10):
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def extract_items_from_soup(soup, base_url):
    """
    汎用的に「商品名」と「リンク」を抽出するためのロジック：
    ページ中のランキングリストの中にある <a> 要素を幅広く探し、
    テキストとhrefを取り出す。重複を除外して返す。
    """
    items = []
    seen = set()

    # まずはランキングリストっぽい領域を探す（class 名などで絞る試み）
    possible_containers = []
    # よくあるクラス名を幾つか試す
    for cls in ["ranking_list", "rankingItem", "rank_list", "c-ranking", "itemList", "product-list"]:
        possible_containers += soup.select(f".{cls}")

    # もし見つからなければ body を使う（汎用フォールバック）
    containers = possible_containers or [soup.body]

    for container in containers:
        for a in container.select("a[href]"):
            text = a.get_text(strip=True)
            href = a.get("href")
            if not text:
                continue
            # フルURLにする
            full_url = urljoin(base_url, href)
            key = (text, full_url)
            if key in seen:
                continue
            seen.add(key)
            items.append({"name": text, "url": full_url})

    return items

def find_next_page_url(soup, base_url):
    """
    次ページへのリンクを汎用的に探す。
    '次へ'や 'next' のテキスト、rel=next、pageパラメータなどをチェック。
    """
    # rel="next"
    link = soup.find("link", rel="next")
    if link and link.get("href"):
        return urljoin(base_url, link.get("href"))

    # anchorで next / 次へ
    a = soup.find("a", string=lambda s: s and ("次へ" in s or "Next" in s or "next" in s))
    if a and a.get("href"):
        return urljoin(base_url, a.get("href"))

    # ページ番号リンク（2,3...） の中で現在より大きいものを探す（汎用だが完全ではない）
    for a in soup.select("a[href]"):
        txt = a.get_text(strip=True)
        if txt.isdigit():
            # choose a digit > 1 as candidate
            if int(txt) >= 2:
                return urljoin(base_url, a.get("href"))

    return None

def scrape_ranking_pages(start_url, max_items=100, delay=1.0, logger=None):
    """
    start_url から始め、最大 max_items 件取得する汎用的なループ。
    delay は各ページのリクエスト間の待機秒数（サイト負担軽減のため）。
    logger(optional) は関数にステータス文字列を送るコールバック。
    """
    collected = []
    visited_urls = set()
    url = start_url

    while url and len(collected) < max_items:
        if url in visited_urls:
            if logger:
                logger(f"ループ検出: {url} は既に訪問済みです。終了します。")
            break
        visited_urls.add(url)

        try:
            if logger:
                logger(f"ページ取得: {url}")
            html = fetch_page(url)
        except Exception as e:
            if logger:
                logger(f"ページ取得失敗: {e}")
            break

        soup = BeautifulSoup(html, "html.parser")
        items = extract_items_from_soup(soup, base_url=start_url)
        if not items:
            if logger:
                logger("このページからアイテムを抽出できませんでした（セレクタ調整が必要かもしれません）。")
        else:
            # items がランキング順である保証はないため、重複チェックしつつ追加
            for it in items:
                if len(collected) >= max_items:
                    break
                # 重複 URL または同名URL があればスキップ
                key = (it["name"], it["url"])
                if key in {(c["name"], c["url"]) for c in collected}:
                    continue
                collected.append({"name": it["name"], "url": it["url"]})

            if logger:
                logger(f"合計取得数: {len(collected)} 件")

        # 次ページを探す
        next_url = find_next_page_url(soup, base_url=start_url)
        if not next_url:
            if logger:
                logger("次ページが見つかりませんでした。ページネーションが無いか、別の方式で分割されています。")
            break

        if logger:
            logger(f"次ページ: {next_url} を取得します（{delay}s 待機）")
        time.sleep(delay)
        url = next_url

    # 最終的に ranking を付与して返す（取得順で）
    results = []
    for i, it in enumerate(collected[:max_items], start=1):
        results.append({"rank": i, "name": it["name"], "url": it["url"]})
    return results

def save_to_excel(items, purpose_label, folder_path):
    """
    items: list of dicts with keys 'rank','name','url'
    folder_path: 保存先フォルダ（文字列）
    """
    df = pd.DataFrame(items, columns=["rank", "name", "url"])
    date_s = datetime.now().strftime("%Y%m%d")
    safe_label = "".join(c if c.isalnum() or c in "_-" else "_" for c in purpose_label)
    filename = f"cosme_ranking_{safe_label}_{date_s}.xlsx"
    path = f"{folder_path.rstrip('/')}/{filename}"
    df.columns = ["ランキング", "コスメ名", "専用ページURL"]
    df.to_excel(path, index=False, engine="openpyxl")
    return path
