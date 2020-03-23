import os,sys,time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import h5py
import pathlib
import csv
import numpy as np

selected_filepath = ""

def select_clicked():
    filetype = [("","*.go")]
    filepath = filedialog.askopenfilename(filetypes=filetype)
    selected_filepath.set(filepath)

def export_clicked():
    filepath = entry1.get()
    if(len(filepath) == 0):
        return 0

    print(filepath)
    try:
        # HDFファイルを開いてみる
        with h5py.File(filepath, mode="r") as fileobj:
            parent_dir = pathlib.Path(filepath).parent / "csv"

            # __video__グループを除く全グループ名を取得
            top_group_keys = [t for t in fileobj.keys() if t != "__video__"]
            for t in top_group_keys:
                top_dir = parent_dir / t
                # グループ名のフォルダを作成
                top_dir.mkdir(parents=True, exist_ok=True)
                data_group_key = t + "/data"
                data_group = fileobj[data_group_key]
                for side in data_group:
                    # csvのヘッダを用意
                    side_group_key = data_group_key + "/" + side
                    csv_header = [x for x in fileobj[side_group_key].keys()]

                    # データを格納
                    row = len(fileobj[side_group_key])
                    column = len(fileobj[side_group_key]["time"])
                    data_mat_trans = np.zeros((row, column))
                    for i in range(row):
                        earray_key = side_group_key + "/" + csv_header[i]
                        data_mat_trans[i] = fileobj[earray_key]
                    data_mat = data_mat_trans.transpose()

                    # csvに出力
                    csvfilepath = top_dir / (side + ".csv")
                    with csvfilepath.open(mode='w+t', encoding="utf-8", newline="") as f:
                        writer = csv.writer(f, delimiter=',')
                        writer.writerow(csv_header)
                        writer.writerows(data_mat.tolist())

            messagebox.showinfo(message="csvへの出力が完了しました")

    except OSError as e:
        messagebox.showerror(message="選択したファイルが開けないか存在しません")



def exit_clicked():
    sys.exit(0)

if __name__ == "__main__":
    root_window = tk.Tk()
    root_window.resizable(False, False)
    root_window.title("Moticon Exporter")

    frame1 = tk.Frame(root_window, borderwidth=5)
    frame1.pack()

    frame2 = tk.Frame(root_window, borderwidth=5)
    frame2.pack()

    label1 = ttk.Label(frame1, text="ソースファイル")
    label1.grid(row=0, column=0)

    selected_filepath = tk.StringVar()
    entry1 = ttk.Entry(frame1, textvariable=selected_filepath, width=50)
    entry1.grid(row=0, column=1)

    select_button = tk.Button(frame1, text="参照", command=select_clicked)
    select_button.grid(row=0, column=2)

    export_button = tk.Button(frame2, text="エクスポート", command=export_clicked)
    export_button.grid(row=0, column=0)

    exit_button = tk.Button(frame2, text="終了", command=exit_clicked)
    exit_button.grid(row=0, column=1)

    root_window.mainloop()
