# @cosmeランキング自動取得アプリ

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10--3.13-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

@cosmeのランキングページから商品情報を自動取得し、Excelファイルに出力するWindowsアプリです。

**URLを入力してボタンを押すだけ**で、ランキング商品の情報を簡単に取得できます。

---

## 📌 できること

- @cosmeランキングページから**商品名**と**商品URL**を自動取得
- 取得した情報を**Excelファイル（.xlsx）**に自動出力
- ファイル名に**カテゴリ名と実行日時**を自動付与
- **GUI操作**で誰でも簡単に使える
- 実行中は**スピナー表示**で進捗が分かる

---

## 🎯 こんな方におすすめ

- @cosmeのランキング情報を定期的に調査したい方
- 商品リサーチを効率化したい方
- Pythonを使った自動化ツールを試してみたい方

---

## 🖥️ 動作環境

- **OS**: Windows 10 以上
- **Python**: 3.10 〜 3.13
- **インターネット接続**: 必須

> **Python未インストールの方へ**  
> Pythonの公式サイトからダウンロード・インストールしてください。  
> 👉 [Python公式サイト](https://www.python.org/downloads/)  
> インストール時は「**Add Python to PATH**」に必ずチェックを入れてください。

---

## 📥 インストール方法

### 1. このリポジトリをダウンロード

**方法A: Zipでダウンロード（初心者向け）**
1. 画面右上の緑色の「Code」ボタンをクリック
2. 「Download ZIP」を選択
3. ダウンロードしたZIPファイルを解凍

**方法B: Gitでクローン（開発者向け）**
```bash
git clone https://github.com/YukiKunikata/Python_Portfolio.git
cd Python_Portfolio/app_Python/@cosme_scraping_app/Ver1.0.0
```

---

## 🚀 使い方

### ステップ1: アプリを起動

`run_app.bat` をダブルクリックしてください。

> 初回起動時は、必要なライブラリが自動でインストールされます（1〜2分かかります）

### ステップ2: URLを入力

取得したい@cosmeランキングページのURLを入力欄に貼り付けます。

**例:**
```
https://www.cosme.net/ranking/category/skincare
```

### ステップ3: 保存先を選択

「フォルダ選択」ボタンを押して、Excelファイルの保存先フォルダを選びます。

### ステップ4: 取得開始

「開始」ボタンを押すと、自動で情報取得が始まります。

処理中は画面にスピナーが表示されます。

### ステップ5: 完了

取得が完了すると、指定したフォルダにExcelファイルが出力されます。

---

## 📄 出力ファイルについて

### ファイル名の形式
```
@コスメ_＜カテゴリ名＞_＜実行年月日時分＞.xlsx
```

**例:**
```
@コスメ_スキンケア_20260107_1430.xlsx
```

### ファイルの内容

| 列名 | 内容 |
|------|------|
| 商品名 | ランキング商品の名称 |
| 商品URL | 商品ページへのリンク |

### 取得件数

- 上位**最大100件**まで取得します
- 100件未満の場合は、掲載されている全件を取得します

---

## ⚠️ 注意事項

- このアプリは**個人利用・学習目的**で作成されています
- @cosmeの利用規約を遵守し、**節度ある利用**をお願いします
- サイトの仕様変更により、動作しなくなる可能性があります
- 大量アクセスや過度な連続実行は避けてください

---

## ❓ よくある質問・トラブルシューティング

### Q1. 「Pythonが見つかりません」と表示される

**A.** Pythonがインストールされていないか、PATHが通っていません。

1. [Python公式サイト](https://www.python.org/downloads/)からPythonをインストール
2. インストール時に「**Add Python to PATH**」にチェックを入れる
3. PCを再起動してから再度お試しください

### Q2. アプリが起動しない

**A.** 以下を確認してください。

- Windowsのセキュリティソフトがブロックしていないか
- フォルダ名に日本語や特殊文字が含まれていないか
- 管理者権限で実行してみる（`run_app.bat`を右クリック→「管理者として実行」）

### Q3. 「取得できませんでした」と表示される

**A.** 以下の原因が考えられます。

- URLが正しくない（@cosmeのランキングページURLか確認）
- インターネット接続が切れている
- @cosmeのサイト構造が変更された

---

## 🛠️ 開発者向け情報

### 技術スタック

- **Python**: 3.10+
- **GUI**: Tkinter
- **スクレイピング**: requests, BeautifulSoup4, lxml
- **データ処理**: pandas
- **Excel出力**: openpyxl

### 依存ライブラリ

以下のライブラリが`run_app.bat`実行時に自動インストールされます。

```
requests
beautifulsoup4
pandas
openpyxl
lxml
```

手動でインストールする場合:
```bash
pip install requests beautifulsoup4 pandas openpyxl lxml
```

### フォルダ構成

```
@cosme_scraping_app/
├── run_app.bat          # 起動用バッチファイル
├── main.py              # メインスクリプト
├── scraper.py           # スクレイピング処理
├── gui.py               # GUI処理
└── README.md            # このファイル
```

### カスタマイズ方法

取得件数や対象要素を変更したい場合は、`scraper.py`内のXPath設定を編集してください。

```python
# 例: 取得件数を変更
MAX_ITEMS = 100  # この値を変更
```

詳細な開発ドキュメントは、後日Wikiにて公開予定です。

---

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

個人利用・学習目的での使用を想定していますが、商用利用の際は@cosmeの利用規約を必ずご確認ください。

---

## 👤 開発者

**Yuki**

プログラマー / 業務自動化エンジニア / RPA・Python学習中

- GitHub: [@YukiKunikata](https://github.com/YukiKunikata)
- Note: [Yukiの学習ログ](https://note.com/)

---

## 🔄 更新履歴

### Ver 1.0.0（2026年1月7日）
- 初回リリース
- 基本的なスクレイピング機能実装
- GUI実装
- Excel自動出力機能

---

## 📮 フィードバック・バグ報告

不具合の報告や機能リクエストは、[Issues](https://github.com/YukiKunikata/Python_Portfolio/issues)からお願いします。

---

## 🙏 謝辞

このアプリは学習・実績づくりを目的に作成しました。

同じくPythonや業務自動化を学んでいる方の参考になれば幸いです。