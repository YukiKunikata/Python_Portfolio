import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
from cosme_scraper import scrape_ranking_pages
import pandas as pd

# -------------------------
# メインウィンドウ設定
# -------------------------
root = tk.Tk()
root.title("@コスメランキング取得アプリ")
root.geometry("520x360")
root.resizable(False, False)

# -------------------------
# 関数定義
# -------------------------
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_path_var.set(folder_path)

def start_scraping():
    category_url = url_var.get()
    output_folder = output_path_var.get()

    if not category_url:
        messagebox.showwarning("警告", "URLを入力してください。")
        return
    if not output_folder:
        messagebox.showwarning("警告", "出力フォルダを指定してください。")
        return

    try:
        df = scrape_ranking_pages(category_url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_folder, f"cosme_ranking_{timestamp}.xlsx")
        df.to_excel(output_file, index=False)

        messagebox.showinfo("完了", f"取得が完了しました！\n\n保存先:\n{output_file}")

    except Exception as e:
        messagebox.showerror("エラー", f"スクレイピング中にエラーが発生しました:\n{e}")

# -------------------------
# UI構成
# -------------------------
frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="@コスメランキングURL：").grid(row=0, column=0, sticky=tk.W)
url_var = tk.StringVar()
url_entry = ttk.Entry(frame, textvariable=url_var, width=60)
url_entry.grid(row=1, column=0, columnspan=2, pady=5)
url_var.set("https://www.cosme.net/categories/item/804/ranking/")

ttk.Label(frame, text="出力フォルダ：").grid(row=2, column=0, sticky=tk.W, pady=(15, 0))
output_path_var = tk.StringVar()
output_entry = ttk.Entry(frame, textvariable=output_path_var, width=45)
output_entry.grid(row=3, column=0, pady=5)
ttk.Button(frame, text="参照", command=select_folder).grid(row=3, column=1, padx=5)

ttk.Button(
    frame, text="取得開始 ▶", command=start_scraping
).grid(row=5, column=0, columnspan=2, pady=30, ipadx=30, ipady=10)

ttk.Label(frame, text="※上位100件をExcelに出力します", foreground="gray").grid(row=6, column=0, columnspan=2)

root.mainloop()
