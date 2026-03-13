import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from converter import convert_timeline_to_kml


class TimelineToKmlApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("timeline2kml")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status_text = tk.StringVar(value="Choose a Timeline JSON file to begin.")

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.grid(sticky="nsew")

        tk.Label(frame, text="Input JSON").grid(row=0, column=0, sticky="w", pady=(0, 6))
        tk.Entry(frame, textvariable=self.input_path, width=50).grid(
            row=1, column=0, sticky="we", padx=(0, 8)
        )
        tk.Button(frame, text="Browse", command=self.select_input_file).grid(row=1, column=1)

        tk.Label(frame, text="Output KML").grid(row=2, column=0, sticky="w", pady=(12, 6))
        tk.Entry(frame, textvariable=self.output_path, width=50).grid(
            row=3, column=0, sticky="we", padx=(0, 8)
        )
        tk.Button(frame, text="Browse", command=self.select_output_file).grid(row=3, column=1)

        tk.Button(frame, text="Convert", command=self.convert).grid(
            row=4, column=0, columnspan=2, pady=(16, 8), sticky="we"
        )

        tk.Label(frame, textvariable=self.status_text, anchor="w", justify="left").grid(
            row=5, column=0, columnspan=2, sticky="we"
        )

        frame.columnconfigure(0, weight=1)

    def select_input_file(self):
        path = filedialog.askopenfilename(
            title="Select Timeline JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if path:
            self.input_path.set(path)
            if not self.output_path.get():
                self.output_path.set(str(Path(path).with_suffix(".kml")))

    def select_output_file(self):
        path = filedialog.asksaveasfilename(
            title="Save KML As",
            defaultextension=".kml",
            filetypes=[("KML files", "*.kml"), ("All files", "*.*")],
        )
        if path:
            self.output_path.set(path)

    def convert(self):
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()

        if not input_path or not output_path:
            self.status_text.set("Select both an input JSON file and an output KML file.")
            messagebox.showerror("timeline2kml", "Select both input and output paths.")
            return

        try:
            convert_timeline_to_kml(input_path, output_path)
        except Exception as exc:
            self.status_text.set(f"Conversion failed: {exc}")
            messagebox.showerror("timeline2kml", f"Conversion failed:\n{exc}")
            return

        self.status_text.set(f"Saved KML to: {output_path}")
        messagebox.showinfo("timeline2kml", f"KML file saved to:\n{output_path}")


def main():
    root = tk.Tk()
    TimelineToKmlApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
