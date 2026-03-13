import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from converter import convert_timeline_to_kml


class TimelineToKmlApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("timeline2kml")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f1ea")

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status_text = tk.StringVar(value="請先選擇 Google Timeline 匯出的 JSON 檔案。")

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.root, padx=16, pady=16, bg="#f4f1ea")
        frame.grid(sticky="nsew")

        tk.Label(
            frame,
            text="Google Timeline JSON 轉 KML",
            font=("Microsoft JhengHei UI", 14, "bold"),
            bg="#f4f1ea",
            fg="#2f3b2f",
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        tk.Label(
            frame,
            text="把 Timeline JSON 轉成可匯入 Google My Maps 或 Google Earth 的 KML 檔。",
            bg="#f4f1ea",
            fg="#4f5d4f",
            justify="left",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 14))

        tk.Label(frame, text="1. 選擇輸入 JSON", bg="#f4f1ea", fg="#2f3b2f").grid(
            row=2, column=0, sticky="w", pady=(0, 6)
        )
        tk.Entry(frame, textvariable=self.input_path, width=54).grid(
            row=3, column=0, sticky="we", padx=(0, 8)
        )
        tk.Button(frame, text="瀏覽", command=self.select_input_file, width=10).grid(row=3, column=1)

        tk.Label(frame, text="2. 選擇輸出 KML", bg="#f4f1ea", fg="#2f3b2f").grid(
            row=4, column=0, sticky="w", pady=(14, 6)
        )
        tk.Entry(frame, textvariable=self.output_path, width=54).grid(
            row=5, column=0, sticky="we", padx=(0, 8)
        )
        tk.Button(frame, text="瀏覽", command=self.select_output_file, width=10).grid(row=5, column=1)

        tk.Button(
            frame,
            text="開始轉換",
            command=self.convert,
            bg="#2f6f4f",
            fg="white",
            activebackground="#255b40",
            activeforeground="white",
            pady=8,
        ).grid(row=6, column=0, columnspan=2, pady=(18, 10), sticky="we")

        tk.Button(frame, text="開啟輸出資料夾", command=self.open_output_folder, pady=6).grid(
            row=7, column=0, columnspan=2, sticky="we"
        )

        tk.Label(
            frame,
            textvariable=self.status_text,
            anchor="w",
            justify="left",
            wraplength=460,
            bg="#f4f1ea",
            fg="#4f5d4f",
        ).grid(row=8, column=0, columnspan=2, sticky="we", pady=(12, 0))

        tk.Label(
            frame,
            text="小提醒：如果你是從 Google Takeout 匯出的資料，先確認你選的是 Timeline JSON 檔。",
            bg="#f4f1ea",
            fg="#7a6f5a",
            justify="left",
            wraplength=460,
        ).grid(row=9, column=0, columnspan=2, sticky="we", pady=(8, 0))

        frame.columnconfigure(0, weight=1)

    def select_input_file(self):
        path = filedialog.askopenfilename(
            title="選擇 Timeline JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if path:
            self.input_path.set(path)
            self.output_path.set(str(Path(path).with_suffix(".kml")))
            self.status_text.set("已選擇輸入檔，接著可以直接按「開始轉換」。")

    def select_output_file(self):
        path = filedialog.asksaveasfilename(
            title="選擇 KML 輸出位置",
            defaultextension=".kml",
            filetypes=[("KML files", "*.kml"), ("All files", "*.*")],
        )
        if path:
            self.output_path.set(path)
            self.status_text.set("已設定輸出位置，可以開始轉換。")

    def open_output_folder(self):
        output_path = self.output_path.get().strip()
        if not output_path:
            messagebox.showinfo("timeline2kml", "請先選擇輸出 KML 路徑。")
            return

        output_dir = Path(output_path).expanduser().resolve().parent
        output_dir.mkdir(parents=True, exist_ok=True)
        os.startfile(str(output_dir))

    def convert(self):
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()

        if not input_path or not output_path:
            self.status_text.set("請先選擇輸入 JSON 與輸出 KML 路徑。")
            messagebox.showerror("timeline2kml", "請先選擇輸入 JSON 與輸出 KML 路徑。")
            return

        self.status_text.set("轉換中，請稍候...")
        self.root.update_idletasks()

        try:
            convert_timeline_to_kml(input_path, output_path)
        except Exception as exc:
            self.status_text.set(f"轉換失敗：{exc}")
            messagebox.showerror("timeline2kml", f"轉換失敗：\n{exc}")
            return

        self.status_text.set(f"轉換完成，KML 已儲存到：{output_path}")
        if messagebox.askyesno(
            "timeline2kml",
            f"KML 已儲存完成：\n{output_path}\n\n要現在打開輸出資料夾嗎？",
        ):
            os.startfile(str(Path(output_path).expanduser().resolve().parent))


def main():
    root = tk.Tk()
    TimelineToKmlApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
