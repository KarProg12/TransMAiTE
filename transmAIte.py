# Uproszczone GUI - ttk
# Nic nie trzeba instalowac - ttk jest w Pythonie
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from converter import Converter as CNV


class TransMAiTE:
    def __init__(self):
        # Kolory z ikony aplikacji: ciemne tlo + zielen z ikony
        self.BG_DARK = "#232323"
        self.CARD_DARK = "#2E2E2E"
        self.BORDER_DARK = "#3A3A3A"
        self.GREEN_DARK = "#18863F"
        self.GREEN_MAIN = "#5ABC6F"
        self.GREEN_LIGHT = "#2A3D30"

        self.root_win = tk.Tk()
        self.root_win.title("TransMAiTE")
        self.root_win.geometry("694x510")
        self.root_win.configure(bg=self.BG_DARK)

        # Style ttk - kolory ustawiamy RAZ tutaj, widgety tylko wybieraja styl
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Top.TFrame", background=self.GREEN_DARK)
        self.style.configure("Top.TLabel", background=self.GREEN_DARK, foreground="white", font=("Segoe UI", 14, "bold"))
        self.style.configure("TopSmall.TLabel", background=self.GREEN_DARK, foreground="#D6F5DD", font=("Segoe UI", 9))
        self.style.configure("Card.TFrame", background=self.CARD_DARK, bordercolor=self.BORDER_DARK, borderwidth=1, relief="solid")
        self.style.configure("Body.TFrame", background=self.CARD_DARK)
        self.style.configure("Title.TLabel", background=self.GREEN_MAIN, foreground="black", font=("Segoe UI", 10, "bold"))
        self.style.configure("Row.TLabel", background=self.CARD_DARK, foreground="white", font=("Segoe UI", 9))
        self.style.configure("TEntry", fieldbackground=self.BG_DARK, foreground="white", insertcolor="white", font=("Segoe UI", 9), padding=3)
        self.style.configure("Green.TButton", background=self.GREEN_MAIN, foreground="black", font=("Segoe UI", 9, "bold"), padding=3)
        self.style.map("Green.TButton", background=[("active", self.GREEN_DARK), ("pressed", self.GREEN_DARK)])
        self.style.configure("BigGreen.TButton", background=self.GREEN_MAIN, foreground="black", font=("Segoe UI", 10, "bold"), padding=4)
        self.style.map("BigGreen.TButton", background=[("active", self.GREEN_DARK), ("pressed", self.GREEN_DARK)])
        self.style.configure("Status.TFrame", background=self.GREEN_LIGHT)
        self.style.configure("Status.TLabel", background=self.GREEN_LIGHT, foreground="white", font=("Segoe UI", 9))

        # Gorny pasek
        top = ttk.Frame(self.root_win, style="Top.TFrame", height=40)
        top.pack(fill="x")
        top.pack_propagate(False)
        ttk.Label(top, text="  TransMAiTE", style="Top.TLabel").pack(side="left")

        # Lista wybranych plikow .sdlxliff
        self.selected_files = []

        # Sciezki
        self.paths = {}
        for path_key in ["export_files_display", "export_folder", "import_json", "txt_to_import"]:
            self.paths[path_key] = tk.StringVar()

        self.status = tk.StringVar(value="Ready.")

        self.build_ui()
        self.converter = CNV()

    def choose_path(self, path_variable, choice_type):
        if choice_type == "files":
            files = filedialog.askopenfilenames(filetypes=[("SDLXLIFF files", "*.sdlxliff"), ("All files", "*.*")])
            if files:
                self.selected_files = [f.replace("\\", "/") for f in files]
                first_file = self.selected_files[0]
                folder = first_file.rsplit("/", 1)[0]

                if len(self.selected_files) == 1:
                    path_variable.set(first_file)
                    name = first_file.rsplit("/", 1)[-1].rsplit(".", 1)[0]
                    project_folder = folder + "/" + name
                else:
                    path_variable.set(f"[{len(self.selected_files)} files selected] in {folder}")
                    project_folder = folder + "/_TransMAiTE_batch"

                self.paths["export_folder"].set(project_folder)
                self.paths["import_json"].set(project_folder + "/export.json")
                self.paths["txt_to_import"].set(project_folder + "/target.txt")

        elif choice_type == "file":
            chosen = filedialog.askopenfilename()
            if chosen:
                path_variable.set(chosen.replace("\\", "/"))

        elif choice_type == "folder":
            chosen = filedialog.askdirectory()
            if chosen:
                chosen = chosen.replace("\\", "/")
                path_variable.set(chosen)
                if path_variable is self.paths["export_folder"]:
                    self.paths["import_json"].set(chosen + "/export.json")
                    self.paths["txt_to_import"].set(chosen + "/target.txt")

    def section(self, title):
        outer = ttk.Frame(self.root_win, style="Card.TFrame")
        outer.pack(fill="x", padx=12, pady=(12, 4))
        ttk.Label(outer, text="  " + title, style="Title.TLabel", anchor="w").pack(fill="x", ipady=8)
        body = ttk.Frame(outer, style="Body.TFrame")
        body.pack(fill="x", padx=10, pady=10)
        return body

    def row(self, frame, row_number, label, path_variable, choice_type):
        ttk.Label(frame, text=label, style="Row.TLabel").grid(row=row_number, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=path_variable).grid(row=row_number, column=1, sticky="ew", padx=8, pady=4)
        ttk.Button(frame, text="Browse...", style="Green.TButton", command=lambda: self.choose_path(path_variable, choice_type)).grid(row=row_number, column=2, pady=4)
        frame.grid_columnconfigure(1, weight=1)

    def button(self, frame, text, command):
        return ttk.Button(frame, text=text, style="BigGreen.TButton", command=command)

    def on_export_click(self):
        out_folder = self.paths["export_folder"].get()
        if not self.selected_files or not out_folder:
            messagebox.showwarning("Missing data", "Select SDLXLIFF file(s) and output folder.")
            return
        try:
            count = self.converter.export_many(self.selected_files, out_folder)
            message = f"Export done. Exported {count} unique segments from {len(self.selected_files)} file(s)."
            messagebox.showinfo("Done", message)
            self.status.set(message)
        except Exception as error:
            self.status.set("ERROR: " + str(error))
            messagebox.showerror("Error", str(error))

    def on_import_click(self):
        txt_file = self.paths["txt_to_import"].get()
        json_file = self.paths["import_json"].get()
        if not txt_file or not json_file:
            messagebox.showwarning("Missing data", "Select Project JSON and Translated TXT.")
            return
        try:
            count = self.converter.import_many(txt_file, json_file)
            if count == 0:
                message = "WARNING: Line count mismatch or no target translations found."
                messagebox.showwarning("Warning", message)
            else:
                message = f"Import done. Inserted {count} segments across files."
                messagebox.showinfo("Done", message)
            self.status.set(message)
        except Exception as error:
            self.status.set("ERROR: " + str(error))
            messagebox.showerror("Error", str(error))

    def build_ui(self):
        # Sekcja Export
        export_frame = self.section(">> Export << .sdlxliff(s) ==> single export.json & source.txt, target.txt:\n  exports only segments without statuses:\n"
                                    "    Translated, ApprovedTranslation, ApprovedSignOff, RejectedTranslation, RejectedSignOff, locked='true'\n  Deduplicates repetitions across all selected files into one source.txt")
        self.row(export_frame, 0, "SDLXLIFF file(s):", self.paths["export_files_display"], "files")
        self.row(export_frame, 1, "Output folder:", self.paths["export_folder"], "folder")
        self.button(export_frame, "Create folder and export .sdlxliff(s) to single export.json & 2x .txt", self.on_export_click).grid(row=2, column=0, columnspan=3, sticky="ew", pady=(8, 0))

        # Sekcja Import
        import_frame = self.section(">> Import << target.txt & export.json ==> all .sdlxliff files:\n  imports targets from target.txt via export.json back into original .sdlxliff files")
        self.row(import_frame, 0, "Project JSON:", self.paths["import_json"], "file")
        self.row(import_frame, 1, "Translated TXT:", self.paths["txt_to_import"], "file")
        self.button(import_frame, "Import target.txt back to .sdlxliff files", self.on_import_click).grid(row=2, column=0, columnspan=3, sticky="ew", pady=(8, 0))

        # Status
        status_bar = ttk.Frame(self.root_win, style="Status.TFrame", height=32)
        status_bar.pack(fill="x", side="bottom")
        ttk.Label(status_bar, textvariable=self.status, style="Status.TLabel").pack(anchor="w", padx=14, pady=5)

    def run(self):
        self.root_win.mainloop()


if __name__ == "__main__":
    plugin = TransMAiTE()
    plugin.run()
