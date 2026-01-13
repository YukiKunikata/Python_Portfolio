import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cosme_scraper import scrape_ranking_pages, save_to_excel
import threading


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

def run_scraping():
    """別スレッドでスクレイピングする（GUIが固まらないように）"""
    try:
        url = url_entry.get()
        folder_path = folder_path_var.get()

        df, title = scrape_ranking_pages(url)
        output_path = save_to_excel(df, folder_path, title)

        progress_bar.stop()
        progress_bar.pack_forget()

        messagebox.showinfo("完了", f"Excelファイルを出力しました！\n\n{output_path}")
    except Exception as e:
        progress_bar.stop()
        progress_bar.pack_forget()
        messagebox.showerror("エラー", f"エラーが発生しました：\n{e}")

def start_scraping():
    """ボタン押下時の処理"""
    url = url_entry.get()
    folder_path = folder_path_var.get()

    if not url or not folder_path:
        messagebox.showwarning("警告", "URLと出力フォルダを指定してください。")
        return

    # 「ぐるぐる」を表示して回し始める
    progress_bar.pack(pady=10, anchor="w")
    progress_bar.start(15)

    # 別スレッドでスクレイピング実行
    thread = threading.Thread(target=run_scraping)
    thread.start()


# ==============================================
# GUI構築
# ==============================================
root = tk.Tk()
root.title("@コスメランキング取得アプリ")
root.geometry("600x300")

# 左寄せしたいので親Frameを左寄せ配置
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20, anchor="w")

# 出力フォルダ変数
folder_path_var = tk.StringVar()

# URL入力欄
tk.Label(main_frame, text="① 取得する@コスメランキングURLを入力：", anchor="w")\
    .pack(anchor="w")
url_entry = tk.Entry(main_frame, width=70)
url_entry.pack(anchor="w", pady=5)

# フォルダ選択
tk.Label(main_frame, text="② Excelファイル保存先フォルダ：", anchor="w")\
    .pack(anchor="w", pady=(10, 0))

folder_frame = tk.Frame(main_frame)
folder_frame.pack(anchor="w")

tk.Entry(folder_frame, textvariable=folder_path_var, width=50)\
    .pack(side="left", pady=5)
tk.Button(folder_frame, text="参照", command=browse_folder)\
    .pack(side="left", padx=5)

# 実行ボタン
tk.Label(main_frame, text="③ 取得を開始：", anchor="w")\
    .pack(anchor="w", pady=(15, 0))

tk.Button(
    main_frame,
    text="取得開始 ▶",
    command=start_scraping,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20
).pack(anchor="w", pady=5)

# ぐるぐる用プログレスバー（初期は非表示）
progress_bar = ttk.Progressbar(main_frame, mode="indeterminate", length=400)

root.mainloop()
