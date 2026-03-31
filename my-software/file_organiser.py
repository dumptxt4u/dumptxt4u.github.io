import os
import shutil
import csv
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from pathlib import Path

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer Pro")
        self.root.geometry("1200x850")
        self.root.configure(bg="#0a0a0a")

        self.source_folder = None
        self.files = []
        self.hierarchy_entries = {}
        
        # History stack for Undo: stores (action_type, [(old_path, new_path), ...])
        self.history = []

        self.setup_ui()
        self.create_context_menu()

    def setup_ui(self):
        # ==================== TOP BAR ====================
        top_frame = tk.Frame(self.root, bg="#111111", height=70)
        top_frame.pack(fill="x", pady=(0, 5))

        tk.Label(top_frame, text="Smart File Organizer", 
                 font=("Segoe UI", 18, "bold"), bg="#111111", fg="#00d4ff").pack(side="left", padx=20)

        # Undo Button
        self.undo_btn = tk.Button(top_frame, text="⟲ Undo Last Task", command=self.undo_action, 
                                  bg="#444", fg="#888", font=("Arial", 10, "bold"), state="disabled", padx=15)
        self.undo_btn.pack(side="right", padx=20)

        tk.Button(top_frame, text="📂 Load Folder", command=self.load_folder, 
                  bg="#00d4ff", fg="black", font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=10)

        # ==================== MAIN CONTENT ====================
        main_pane = tk.PanedWindow(self.root, orient="horizontal", bg="#0a0a0a", sashwidth=6)
        main_pane.pack(fill="both", expand=True, padx=10, pady=5)

        # LEFT: File List
        left_frame = tk.Frame(main_pane, bg="#1a1a1a")
        main_pane.add(left_frame, width=450)

        tk.Label(left_frame, text="Right-click to Rename | Double-click to View", 
                 bg="#1a1a1a", fg="#00ffaa", font=("Arial", 9, "italic")).pack(pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1a1a1a", foreground="white", fieldbackground="#1a1a1a")
        
        self.file_list = ttk.Treeview(left_frame, columns=("name",), show="headings")
        self.file_list.heading("name", text="Filename")
        self.file_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        # BINDINGS
        self.file_list.bind("<Double-1>", self.open_file)
        # Right click (Button-3 is Windows/Linux, Button-2 is often macOS)
        self.file_list.bind("<Button-3>", self.show_context_menu)
        self.file_list.bind("<Button-2>", self.show_context_menu) 

        # RIGHT: Controls
        right_frame = tk.Frame(main_pane, bg="#0a0a0a")
        main_pane.add(right_frame)

        # --- Section 1: Batch Rename ---
        rename_frame = tk.LabelFrame(right_frame, text=" 1. Prefix & Tag Files ", bg="#1a1a1a", fg="#00d4ff", padx=15, pady=10)
        rename_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(rename_frame, text="Prefixes (e.g. Class, Subject):", bg="#1a1a1a", fg="white").pack(anchor="w")
        self.prefix_entry = tk.Entry(rename_frame, bg="#222", fg="white", insertbackground="white", font=("Consolas", 11))
        self.prefix_entry.pack(fill="x", pady=5)

        tk.Button(rename_frame, text="Apply Prefix to ALL", command=self.batch_rename, 
                  bg="#ffaa00", fg="black", font=("Arial", 9, "bold")).pack(fill="x", pady=10)

        # --- Section 2: Hierarchy ---
        move_frame = tk.LabelFrame(right_frame, text=" 2. Move to Folder Hierarchy ", bg="#1a1a1a", fg="#00d4ff", padx=15, pady=10)
        move_frame.pack(fill="x", padx=10, pady=5)

        levels = ["Class", "Board", "Subject", "Topic"]
        for lvl in levels:
            f = tk.Frame(move_frame, bg="#1a1a1a")
            f.pack(fill="x", pady=2)
            tk.Label(f, text=f"{lvl}:", bg="#1a1a1a", fg="white", width=10, anchor="w").pack(side="left")
            self.hierarchy_entries[lvl] = tk.Entry(f, bg="#222", fg="white", insertbackground="white")
            self.hierarchy_entries[lvl].pack(side="left", fill="x", expand=True)

        tk.Button(move_frame, text="🚀 Move Selected", command=lambda: self.move_files(True), 
                  bg="#00ff88", fg="black", font=("Arial", 10, "bold"), pady=8).pack(fill="x", pady=(10, 5))

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", bg="#111", fg="#888").pack(side="bottom", fill="x")

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#222", fg="white", activebackground="#00d4ff")
        self.context_menu.add_command(label="📄 Open File", command=lambda: self.open_file(None))
        self.context_menu.add_command(label="✏️ Rename File", command=self.rename_single_file_dialog)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Delete (Coming soon)", state="disabled")

    def show_context_menu(self, event):
        # Select the item under the mouse first
        item = self.file_list.identify_row(event.y)
        if item:
            self.file_list.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    # ====================== CORE LOGIC ======================

    def rename_single_file_dialog(self):
        selection = self.file_list.selection()
        if not selection: return
        
        old_name = self.file_list.item(selection[0])["values"][0]
        old_path = self.source_folder / old_name
        
        # Ask user for new name
        new_name = simpledialog.askstring("Rename File", f"Enter new name for:\n{old_name}", initialvalue=old_name)
        
        if new_name and new_name != old_name:
            new_path = self.source_folder / new_name
            try:
                old_path.rename(new_path)
                self.add_to_history("manual rename", [(new_path, old_path)])
                self.refresh_list()
                self.update_status(f"Renamed: {old_name} -> {new_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not rename file: {e}")

    def open_file(self, event):
        selection = self.file_list.selection()
        if not selection: return
        filename = self.file_list.item(selection[0])["values"][0]
        path = self.source_folder / filename
        webbrowser.open(str(path))

    def batch_rename(self):
        if not self.source_folder: return
        
        prefixes = [p.strip() for p in self.prefix_entry.get().split(",") if p.strip()]
        if not prefixes: return
        prefix_str = "___".join(prefixes) + "___"

        changes = []
        for f in self.files:
            if not f.name.startswith(prefix_str):
                new_path = f.with_name(f"{prefix_str}{f.name}")
                try:
                    f.rename(new_path)
                    changes.append((new_path, f))
                except: pass
        
        if changes:
            self.add_to_history("batch rename", changes)
            self.refresh_list()
            self.update_status(f"Batch renamed {len(changes)} files.")

    def move_files(self, selected_only):
        if not self.source_folder: return
        parts = [self.hierarchy_entries[k].get().strip().replace(" ", "-") for k in self.hierarchy_entries]
        parts = [p for p in parts if p]
        if not parts: return
        
        dest_dir = Path.home() / "Tuition_Organized" / Path(*parts)
        dest_dir.mkdir(parents=True, exist_ok=True)

        targets = [self.source_folder / self.file_list.item(i)["values"][0] for i in self.file_list.selection()] if selected_only else [self.source_folder / f.name for f in self.files]

        changes = []
        for f in targets:
            dest_path = dest_dir / f.name
            try:
                shutil.move(str(f), str(dest_path))
                changes.append((dest_path, f))
            except: pass

        if changes:
            self.add_to_history("move", changes)
            self.refresh_list()
            self.update_status(f"Moved {len(changes)} files.")

    # ====================== HELPERS ======================

    def add_to_history(self, action_type, changes):
        self.history.append((action_type, changes))
        self.undo_btn.config(state="normal", bg="#ff4444", fg="white")

    def undo_action(self):
        if not self.history: return
        action_type, changes = self.history.pop()
        count = 0
        for current_path, original_path in changes:
            try:
                if not original_path.parent.exists(): original_path.parent.mkdir(parents=True)
                shutil.move(str(current_path), str(original_path))
                count += 1
            except: pass
        if not self.history: self.undo_btn.config(state="disabled", bg="#444", fg="#888")
        self.refresh_list()
        self.update_status(f"Undid {action_type}: Restored {count} files.")

    def load_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_folder = Path(folder)
            self.refresh_list()
            self.update_status(f"Folder Loaded: {folder}")

    def refresh_list(self):
        if not self.source_folder: return
        self.file_list.delete(*self.file_list.get_children())
        self.files = sorted([f for f in self.source_folder.iterdir() if f.is_file()])
        for f in self.files:
            self.file_list.insert("", "end", values=(f.name,))

    def update_status(self, text):
        self.status_var.set(text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
