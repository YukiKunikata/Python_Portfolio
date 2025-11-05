# TkinterベースのGUI。
# 用途選択、URL手入力、出力フォルダ選択、ログ表示、取得ボタンを装備

# gui_app.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from cosme_scraper import scrape_ranking_pages, save_to_excel

# --- 初期の「用途→既定URL」マッピング（参考例） ---
# 実際の @cosme のURL構造は変わる可能性があるため、URLが不明でも
# 「ランキングページURLを直接貼る」方式も使えるようにしています。
PURPOSE_URL_MAP = {
    "スキンケア": "https://www.cosme.net/ranking/skincare",  # 例（実際に動かなければ手入力してください）
    "メイクアップ": "https://www.cosme.net/ranking/makeup",
    "ボディケア": "https://www.cosme.net/ranking/bodycare",
    "ヘアケア": "https://www.cosme.net/ranking/hair",
    "フレグランス": "https://www.cosme.net/ranking/fragrance",
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("@cosme ランキング取得アプリ")
        self.geometry("700x480")
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        # 用途選択
        ttk.Label(frm, text="用途を選択：").grid(row=0, column=0, sticky=tk.W)
        self.purpose_var = tk.StringVar()
        self.purpose_cb = ttk.Combobox(frm, textvariable=self.purpose_var, state="readonly")
        self.purpose_cb["values"] = list(PURPOSE_URL_MAP.keys())
        self.purpose_cb.grid(row=0, column=1, sticky=tk.W)
        self.purpose_cb.bind("<<ComboboxSelected>>", self.on_purpose_selected)

        # ランキングページURL（手入力可能）
        ttk.Label(frm, text="ランキングページのURL（任意で上書き）：").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(8,0))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(frm, textvariable=self.url_var, width=80)
        self.url_entry.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(2,8))

        # 出力フォルダ
        ttk.Label(frm, text="出力フォルダ：").grid(row=3, column=0, sticky=tk.W)
        self.folder_var = tk.StringVar(value=os.getcwd())
        self.folder_entry = ttk.Entry(frm, textvariable=self.folder_var, width=60)
        self.folder_entry.grid(row=3, column=1, sticky=tk.W)
        ttk.Button(frm, text="参照", command=self.browse_folder).grid(row=3, column=2, sticky=tk.W)

        # 取得開始ボタン
        self.start_btn = ttk.Button(frm, text="取得開始 ▶", command=self.on_start)
        self.start_btn.grid(row=4, column=0, columnspan=3, pady=(12, 12))

        # ログ表示
        ttk.Label(frm, text="ログ：").grid(row=5, column=0, sticky=tk.W)
        self.log_text = tk.Text(frm, height=18)
        self.log_text.grid(row=6, column=0, columnspan=3, sticky=tk.NSEW)
        frm.rowconfigure(6, weight=1)
        frm.columnconfigure(1, weight=1)

    def on_purpose_selected(self, event=None):
        p = self.purpose_var.get()
        url = PURPOSE_URL_MAP.get(p)
        if url:
            self.url_var.set(url)

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get() or os.getcwd())
        if folder:
            self.folder_var.set(folder)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.update_idletasks()

    def on_start(self):
        start_url = self.url_var.get().strip()
        purpose = self.purpose_var.get().strip() or "用途未指定"
        folder = self.folder_var.get().strip() or os.getcwd()

        if not start_url:
            # もしURLが空なら、用途から取得可能か試す
            if purpose in PURPOSE_URL_MAP:
                start_url = PURPOSE_URL_MAP[purpose]
                self.url_var.set(start_url)
            else:
                messagebox.showwarning("URLが必要です", "ランキングページのURLを入力するか、用途を選択してください。")
                return

        if not os.path.isdir(folder):
            messagebox.showerror("出力フォルダが見つかりません", "有効な出力フォルダを選択してください。")
            return

        # ボタン無効化してスレッドで処理
        self.start_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.run_scrape, args=(start_url, purpose, folder), daemon=True).start()

    def run_scrape(self, start_url, purpose, folder):
        try:
            self.log(f"開始: {purpose} → {start_url}")
            def logger(s):
                self.log(s)

            items = scrape_ranking_pages(start_url, max_items=100, delay=1.0, logger=logger)
            if not items:
                self.log("アイテムが取得できませんでした。ページ構造の変更やブロックの可能性があります。")
                messagebox.showwarning("取得できませんでした", "アイテムが取得できませんでした。ログを確認してください。")
                return
            path = save_to_excel(items, purpose, folder)
            self.log(f"保存完了: {path}")
            messagebox.showinfo("完了", f"スクレイピング完了しました。\n保存先:\n{path}")
        except Exception as e:
            self.log(f"エラー: {e}")
            messagebox.showerror("エラーが発生しました", str(e))
        finally:
            self.start_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = App()
    app.mainloop()
