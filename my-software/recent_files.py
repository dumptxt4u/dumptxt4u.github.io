import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import threading

try:
    import humanize
    HAS_HUMANIZE = True
except ImportError:
    HAS_HUMANIZE = False

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RecentFilesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📁 Recent Files Explorer - Advanced")
        self.geometry("1400x820")
        self.minsize(1200, 700)
        
        self.current_dir = Path.home() / "Downloads"
        self.files_data = []
        self.sort_column = "modified"
        self.sort_ascending = False
        self.current_filter = None
        self.recursive = tk.BooleanVar(value=True)  # Default: Recursive ON
        
        self.build_ui()
        self.scan_directory()

    def build_ui(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="Recent Files Explorer", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Directory
        ctk.CTkLabel(self.sidebar, text="📂 Directory", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20,5))
        self.dir_label = ctk.CTkLabel(self.sidebar, text=str(self.current_dir), anchor="w", wraplength=240)
        self.dir_label.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="Change Directory", command=self.change_directory).pack(padx=20, pady=10, fill="x")

        # Recursive Option
        ctk.CTkCheckBox(self.sidebar, text="🔍 Recursive Search (include subfolders)", 
                       variable=self.recursive, command=self.scan_directory).pack(anchor="w", padx=20, pady=8)

        # ==================== TIME FILTERS ====================
        filter_frame = ctk.CTkFrame(self.sidebar)
        filter_frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(filter_frame, text="⏰ Time Filter", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(0,10))

        presets = ["Last 5 minutes", "Last 15 minutes", "Last 1 hour", "Last 6 hours", "Last 24 hours", "Last 7 days"]
        self.preset_var = ctk.StringVar(value="Last 1 hour")
        for p in presets:
            ctk.CTkRadioButton(filter_frame, text=p, variable=self.preset_var, value=p).pack(anchor="w", padx=10, pady=2)

        ctk.CTkLabel(filter_frame, text="Custom Range", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15,5))
        self.start_entry = ctk.CTkEntry(filter_frame, placeholder_text="Start: YYYY-MM-DD HH:MM")
        self.start_entry.pack(fill="x", padx=10, pady=2)
        self.end_entry = ctk.CTkEntry(filter_frame, placeholder_text="End: YYYY-MM-DD HH:MM")
        self.end_entry.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(filter_frame, text="Or since last X minutes", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(10,5))
        self.minutes_var = ctk.StringVar(value="60")
        self.minutes_entry = ctk.CTkEntry(filter_frame, textvariable=self.minutes_var, width=100)
        self.minutes_entry.pack(padx=10, pady=2)

        btn_frame = ctk.CTkFrame(filter_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="✅ Apply Time Filter", fg_color="green", command=self.apply_active_time_filter).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(btn_frame, text="Clear Filter", fg_color="red", command=self.clear_filter).pack(side="left", padx=5, expand=True, fill="x")

        # ==================== MAIN AREA ====================
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        toolbar = ctk.CTkFrame(main_frame, height=50)
        toolbar.pack(fill="x", pady=(0,10))

        ctk.CTkButton(toolbar, text="🔄 Refresh", width=120, command=self.scan_directory).pack(side="left", padx=10)
        ctk.CTkButton(toolbar, text="📂 Open Folder", width=140, command=self.open_nautilus).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="📊 Stats", command=self.show_stats).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="📄 Export PDF", width=130, fg_color="green", command=self.export_to_pdf).pack(side="left", padx=5)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, placeholder_text="Search filename...", textvariable=self.search_var)
        search_entry.pack(side="right", padx=10, fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda e: self.filter_files())

        # Treeview
        columns = ("name", "path", "size", "modified", "type")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=25)
        for col, text in zip(columns, ["File Name", "Full Path", "Size", "Modified", "Type"]):
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_tree(c))

        self.tree.column("name", width=280)
        self.tree.column("path", width=520)
        self.tree.column("size", width=110, anchor="e")
        self.tree.column("modified", width=170)
        self.tree.column("type", width=90)

        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Context Menu
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Open File", command=self.open_selected_file)
        self.context_menu.add_command(label="Open Containing Folder", command=self.open_nautilus_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy Path", command=self.copy_path)

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", lambda e: self.open_selected_file())

        self.status_bar = ctk.CTkLabel(main_frame, text="Ready | 0 files", anchor="w")
        self.status_bar.pack(fill="x", pady=5, padx=10)

    # ====================== RECURSIVE SCAN (NEW) ======================
    def scan_directory(self):
        def worker():
            self.files_data.clear()
            try:
                root_path = self.current_dir
                max_depth = 10 if self.recursive.get() else 1

                for dirpath, dirnames, filenames in os.walk(root_path):
                    # Skip hidden folders
                    dirnames[:] = [d for d in dirnames if not d.startswith('.')]
                    
                    # Depth control
                    depth = len(Path(dirpath).relative_to(root_path).parts)
                    if depth >= max_depth and self.recursive.get():
                        continue

                    for filename in filenames:
                        if filename.startswith('.'):  # Skip hidden files too
                            continue
                        filepath = Path(dirpath) / filename
                        try:
                            stat = filepath.stat()
                            mtime = datetime.fromtimestamp(stat.st_mtime)
                            self.files_data.append({
                                "name": filename,
                                "path": str(filepath),
                                "size": stat.st_size,
                                "modified": mtime,
                                "type": filepath.suffix.lower() or "file"
                            })
                        except:
                            continue  # Skip files we can't access
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
            
            self.after(0, lambda: self.refresh_tree())

        threading.Thread(target=worker, daemon=True).start()

    # ====================== FILTERS ======================
    def apply_active_time_filter(self):
        if self.start_entry.get().strip() or self.end_entry.get().strip():
            self.apply_custom_range()
        elif self.minutes_var.get().strip() not in ["", "60"]:
            self.apply_minutes_filter()
        else:
            self.on_preset_change()

    def apply_filter(self, filtered_data, filter_name=""):
        self.current_filter = filter_name
        self.refresh_tree(filtered_data)

    def clear_filter(self):
        self.current_filter = None
        self.refresh_tree()
        messagebox.showinfo("Filter", "All filters cleared.")

    def on_preset_change(self):
        preset = self.preset_var.get()
        now = datetime.now()
        if "5 minutes" in preset: cutoff = now - timedelta(minutes=5); name = "Last 5 min"
        elif "15 minutes" in preset: cutoff = now - timedelta(minutes=15); name = "Last 15 min"
        elif "1 hour" in preset: cutoff = now - timedelta(hours=1); name = "Last 1 hour"
        elif "6 hours" in preset: cutoff = now - timedelta(hours=6); name = "Last 6 hours"
        elif "24 hours" in preset: cutoff = now - timedelta(hours=24); name = "Last 24 hours"
        elif "7 days" in preset: cutoff = now - timedelta(days=7); name = "Last 7 days"
        else: return

        filtered = [f for f in self.files_data if f["modified"] >= cutoff]
        self.apply_filter(filtered, name)

    def apply_minutes_filter(self):
        try:
            minutes = int(self.minutes_var.get().strip())
            if minutes <= 0: raise ValueError
            cutoff = datetime.now() - timedelta(minutes=minutes)
            filtered = [f for f in self.files_data if f["modified"] >= cutoff]
            self.apply_filter(filtered, f"Last {minutes} min")
        except:
            messagebox.showerror("Error", "Please enter a valid positive number")

    def apply_custom_range(self):
        try:
            start_str = self.start_entry.get().strip()
            end_str = self.end_entry.get().strip()
            start = datetime.strptime(start_str, "%Y-%m-%d %H:%M") if start_str else datetime.min
            end = datetime.strptime(end_str, "%Y-%m-%d %H:%M") if end_str else datetime.max
            filtered = [f for f in self.files_data if start <= f["modified"] <= end]
            self.apply_filter(filtered, "Custom Range")
        except:
            messagebox.showerror("Error", "Invalid date format.\nUse: YYYY-MM-DD HH:MM")

    def refresh_tree(self, filtered_data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        data = filtered_data if filtered_data is not None else self.files_data

        for f in data:
            size_str = humanize.naturalsize(f["size"]) if HAS_HUMANIZE else f"{f['size']:,} bytes"
            mod_str = f["modified"].strftime("%Y-%m-%d %H:%M:%S")
            self.tree.insert("", "end", values=(f["name"], f["path"], size_str, mod_str, f["type"]))

        count = len(data)
        total_size = sum(f["size"] for f in data)
        size_str = humanize.naturalsize(total_size) if HAS_HUMANIZE else f"{total_size:,} bytes"
        
        status = f"Showing {count} files | Total size: {size_str}"
        if self.current_filter:
            status += f" | Filter: {self.current_filter}"
        if self.recursive.get():
            status += " | Recursive"
        self.status_bar.configure(text=status)

    # Other methods (unchanged from previous version)
    def change_directory(self):
        new_dir = filedialog.askdirectory(initialdir=self.current_dir)
        if new_dir:
            self.current_dir = Path(new_dir)
            self.dir_label.configure(text=str(self.current_dir))
            self.current_filter = None
            self.scan_directory()
    
    
    
    
    
    
    
    
    
    
    
    
    
    def export_to_pdf(self):
        if not self.tree.get_children():
            messagebox.showwarning("No Data", "No files to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"Recent_Files_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        if not file_path:
            return

        try:
            data = [self.tree.item(item)["values"] for item in self.tree.get_children()]

            doc = SimpleDocTemplate(
                file_path, 
                pagesize=A4,
                rightMargin=30, 
                leftMargin=30, 
                topMargin=40, 
                bottomMargin=40
            )
            
            styles = getSampleStyleSheet()
            elements = []

            # Title
            title = Paragraph(
                f"<font size=18><b>Recent Files Explorer Report</b></font><br/>"
                f"<font size=12>Directory: {self.current_dir}</font><br/>"
                f"<font size=11>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</font>",
                styles['Heading1']
            )
            elements.append(title)
            elements.append(Paragraph("<br/>", styles['Normal']))

            # Summary
            total_files = len(data)
            total_size = sum(int(''.join(filter(str.isdigit, str(row[2]).split()[0] or '0'))) for row in data)
            
            summary = Paragraph(
                f"<b>Summary</b><br/>"
                f"Total Files: <b>{total_files}</b><br/>"
                f"Total Size: <b>{humanize.naturalsize(total_size) if HAS_HUMANIZE else f'{total_size:,} bytes'}</b><br/>"
                f"Filter: <b>{self.current_filter if self.current_filter else 'None'}</b>",
                styles['Normal']
            )
            elements.append(summary)
            elements.append(Paragraph("<br/>", styles['Normal']))

            # Table Data
            table_data = [["File Name", "Full Path", "Size", "Modified", "Type"]] + data
            table = Table(table_data, repeatRows=1, colWidths=[130, 220, 70, 95, 55])

            # ==================== FIXED TABLE STYLE ====================
            style_list = [
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

                # Body
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (2, 1), (2, -1), 'RIGHT'),      # Size column
                ('ALIGN', (3, 1), (3, -1), 'CENTER'),     # Modified column
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]

            # Add alternate row colors properly
            for i in range(1, len(table_data)):
                if i % 2 == 0:
                    style_list.append(('BACKGROUND', (0, i), (-1, i), colors.lightgrey))

            table.setStyle(TableStyle(style_list))

            elements.append(table)
            elements.append(Paragraph("<br/><font size=9>This report was generated by Recent Files Explorer</font>", styles['Normal']))

            doc.build(elements)

            messagebox.showinfo(
                "✅ Success", 
                f"PDF exported successfully!\n\n"
                f"Total Files: {total_files}\n"
                f"Saved as: {file_path}"
            )

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to generate PDF:\n{str(e)}")
    
    

    def filter_files(self):
        term = self.search_var.get().lower().strip()
        if not term:
            self.refresh_tree()
            return
        filtered = [f for f in self.files_data if term in f["name"].lower()]
        self.refresh_tree(filtered)

    # ... (open_nautilus, open_selected_file, copy_path, show_context_menu, sort_tree, show_stats remain the same)
    def open_nautilus(self):
        try: subprocess.Popen(["nautilus", str(self.current_dir)])
        except: messagebox.showerror("Error", "Nautilus not found")

    def open_nautilus_selected(self):
        selected = self.tree.selection()
        if selected:
            path = self.tree.item(selected[0])["values"][1]
            try: subprocess.Popen(["nautilus", os.path.dirname(path)])
            except: pass

    def open_selected_file(self):
        selected = self.tree.selection()
        if selected:
            path = self.tree.item(selected[0])["values"][1]
            try: subprocess.Popen(["xdg-open", path])
            except: messagebox.showerror("Error", "Could not open file")

    def copy_path(self):
        selected = self.tree.selection()
        if selected:
            path = self.tree.item(selected[0])["values"][1]
            self.clipboard_clear()
            self.clipboard_append(path)
            messagebox.showinfo("Copied", "Path copied")

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def sort_tree(self, col):
        self.sort_ascending = not self.sort_ascending if self.sort_column == col else True
        self.sort_column = col
        def sort_key(item):
            val = self.tree.item(item)["values"]
            idx = ["name", "path", "size", "modified", "type"].index(col)
            v = val[idx]
            if col == "size":
                try: return int(''.join(filter(str.isdigit, str(v).split()[0] or "0")))
                except: return 0
            if col == "modified":
                try: return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                except: return datetime.min
            return str(v).lower()
        items = [(sort_key(item), item) for item in self.tree.get_children()]
        items.sort(reverse=not self.sort_ascending, key=lambda x: x[0])
        for i, (_, item) in enumerate(items):
            self.tree.move(item, "", i)

    def show_stats(self):
        if not self.files_data: return
        count = len(self.files_data)
        total = sum(f["size"] for f in self.files_data)
        msg = f"Files: {count}\nTotal Size: {humanize.naturalsize(total) if HAS_HUMANIZE else f'{total:,} bytes'}"
        messagebox.showinfo("Statistics", msg)


if __name__ == "__main__":
    if not HAS_HUMANIZE:
        print("💡 Tip: pip install humanize")
    app = RecentFilesApp()
    app.mainloop()
