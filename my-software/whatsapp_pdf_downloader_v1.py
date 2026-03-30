import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ftplib
import os
import csv
import hashlib
import datetime
import threading
import queue
import webbrowser
from urllib.parse import unquote  # just in case

# ================== CONFIGURATION (You can change if needed) ==================
FTP_HOST = '192.168.1.38'
FTP_PORT = 8080
FTP_USER = 'android'
FTP_PASS = 'android'

LOCAL_BASE_DIR = "whatsapp_pdfs_downloads"          # Main folder on your PC
CSV_LOG_FILE = os.path.join(LOCAL_BASE_DIR, "pdfs_log.csv")

# Exact paths from your FTP URL (spaces are correct, not %20)
PATHS_TO_SCAN = {
    "WhatsApp": "/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Documents",
    "WhatsApp Business": "/Android/media/com.whatsapp.w4b/WhatsApp Business/Media/WhatsApp Business Documents"
}
# =============================================================================

class WhatsAppPDFDownloaderGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WhatsApp & WhatsApp Business PDF Downloader")
        self.geometry("1100x720")
        self.resizable(True, True)
        
        self.ftp = None
        self.queue = queue.Queue()
        self.new_pdfs = []          # List of PDFs to download (after scan)
        self.log_csv = {}           # In-memory cache of CSV: key = remote_path
        
        self.create_widgets()
        self.load_csv_log()
        
        # Auto-create base folder
        os.makedirs(LOCAL_BASE_DIR, exist_ok=True)

    def create_widgets(self):
        # ================== Top Frame - Connection ==================
        top_frame = ttk.LabelFrame(self, text="FTP Connection", padding=10)
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Host:").grid(row=0, column=0, sticky="w", padx=5)
        self.host_entry = ttk.Entry(top_frame, width=20)
        self.host_entry.insert(0, FTP_HOST)
        self.host_entry.grid(row=0, column=1, padx=5)

        ttk.Label(top_frame, text="Port:").grid(row=0, column=2, sticky="w", padx=5)
        self.port_entry = ttk.Entry(top_frame, width=8)
        self.port_entry.insert(0, str(FTP_PORT))
        self.port_entry.grid(row=0, column=3, padx=5)

        ttk.Label(top_frame, text="Username:").grid(row=0, column=4, sticky="w", padx=5)
        self.user_entry = ttk.Entry(top_frame, width=15)
        self.user_entry.insert(0, FTP_USER)
        self.user_entry.grid(row=0, column=5, padx=5)

        ttk.Label(top_frame, text="Password:").grid(row=0, column=6, sticky="w", padx=5)
        self.pass_entry = ttk.Entry(top_frame, width=15, show="•")
        self.pass_entry.insert(0, FTP_PASS)
        self.pass_entry.grid(row=0, column=7, padx=5)

        self.connect_btn = ttk.Button(top_frame, text="Connect to FTP", command=self.start_connect_thread)
        self.connect_btn.grid(row=0, column=8, padx=10)

        self.status_label = ttk.Label(top_frame, text="⛔ Disconnected", foreground="red")
        self.status_label.grid(row=0, column=9, padx=10)

        # ================== Scan Frame ==================
        scan_frame = ttk.LabelFrame(self, text="Scan for New PDFs", padding=10)
        scan_frame.pack(fill="x", padx=10, pady=5)

        self.scan_btn = ttk.Button(scan_frame, text="🔍 Scan Both WhatsApp Folders", command=self.start_scan_thread)
        self.scan_btn.pack(side="left", padx=5)

        self.progress_scan = ttk.Progressbar(scan_frame, mode="indeterminate")
        self.progress_scan.pack(side="left", fill="x", expand=True, padx=10)

        ttk.Button(scan_frame, text="Clear Log", command=self.clear_log).pack(side="right", padx=5)

        # ================== Results Frame ==================
        result_frame = ttk.LabelFrame(self, text="New PDFs Found (Ready to Download)", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_tree = ttk.Treeview(result_frame, columns=("App", "Filename", "Size (KB)", "Modified"), 
                                        show="headings", height=12)
        self.result_tree.heading("App", text="App")
        self.result_tree.heading("Filename", text="Filename")
        self.result_tree.heading("Size (KB)", text="Size (KB)")
        self.result_tree.heading("Modified", text="Modified")
        self.result_tree.column("App", width=120)
        self.result_tree.column("Filename", width=400)
        self.result_tree.column("Size (KB)", width=100)
        self.result_tree.column("Modified", width=140)
        self.result_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.result_tree.configure(yscrollcommand=tree_scroll.set)

        # ================== Download Frame ==================
        download_frame = ttk.LabelFrame(self, text="Download", padding=10)
        download_frame.pack(fill="x", padx=10, pady=5)

        self.download_btn = ttk.Button(download_frame, text="⬇️ Download All New PDFs", 
                                       command=self.start_download_thread, state="disabled")
        self.download_btn.pack(side="left", padx=10)

        self.progress_download = ttk.Progressbar(download_frame, mode="determinate")
        self.progress_download.pack(side="left", fill="x", expand=True, padx=10)

        self.download_status = ttk.Label(download_frame, text="0 new PDFs ready")
        self.download_status.pack(side="left", padx=10)

        # ================== Log Frame ==================
        log_frame = ttk.LabelFrame(self, text="Live Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state="disabled")
        self.log_text.pack(fill="both", expand=True)

        # ================== Bottom Buttons ==================
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="x", padx=10, pady=8)

        ttk.Button(bottom_frame, text="Open Download Folder", command=self.open_download_folder).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="View CSV Log", command=self.open_csv).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="Exit", command=self.quit).pack(side="right", padx=5)

        # Start polling queue for thread-safe updates
        self.after(100, self.process_queue)

    def log(self, message):
        """Thread-safe logging"""
        self.queue.put(("log", message))

    def process_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                if task[0] == "log":
                    self.log_text.configure(state="normal")
                    self.log_text.insert("end", f"{datetime.datetime.now().strftime('%H:%M:%S')} | {task[1]}\n")
                    self.log_text.see("end")
                    self.log_text.configure(state="disabled")
                elif task[0] == "status":
                    self.status_label.config(text=task[1], foreground=task[2])
                elif task[0] == "scan_done":
                    self.display_new_pdfs(task[1])
                elif task[0] == "download_progress":
                    self.progress_download["value"] = task[1]
                    self.download_status.config(text=task[2])
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def load_csv_log(self):
        """Load previous downloads from CSV for credible checking"""
        self.log_csv = {}
        if os.path.exists(CSV_LOG_FILE):
            try:
                with open(CSV_LOG_FILE, "r", encoding="utf-8", newline="") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.log_csv[row["remote_path"]] = {
                            "size": int(row["size"]),
                            "mtime": row["mtime"],
                            "md5": row.get("md5", "")
                        }
                self.log(f"Loaded {len(self.log_csv)} previous PDF records from CSV")
            except Exception as e:
                self.log(f"CSV load error: {e}")

    def save_to_csv(self, record):
        """Append or update CSV"""
        file_exists = os.path.exists(CSV_LOG_FILE)
        with open(CSV_LOG_FILE, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["app", "remote_path", "filename", "size", "mtime", "md5", "local_path", "download_date"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)

    def start_connect_thread(self):
        threading.Thread(target=self.connect_ftp, daemon=True).start()

    def connect_ftp(self):
        try:
            if self.ftp:
                self.ftp.quit()
            self.ftp = ftplib.FTP()
            self.ftp.connect(self.host_entry.get(), int(self.port_entry.get()))
            self.ftp.login(self.user_entry.get(), self.pass_entry.get())
            self.queue.put(("status", "✅ Connected", "green"))
            self.log("Successfully connected to FTP server")
            self.connect_btn.config(state="disabled")
        except Exception as e:
            self.queue.put(("status", f"❌ {str(e)}", "red"))
            self.log(f"Connection failed: {e}")

    def start_scan_thread(self):
        if not self.ftp:
            messagebox.showwarning("Not Connected", "Please connect to FTP first!")
            return
        self.scan_btn.config(state="disabled")
        self.progress_scan.start()
        self.log("Starting recursive scan of both folders...")
        threading.Thread(target=self.scan_both_folders, daemon=True).start()

    def is_pdf(self, name):
        return name.lower().endswith(".pdf")

    def get_file_info(self, ftp, path):
        """Get size and mtime reliably"""
        try:
            # Try MLSD first (best)
            for name, facts in ftp.mlsd(path, ["size", "modify"]):
                if self.is_pdf(name):
                    size = int(facts.get("size", 0))
                    mtime_str = facts.get("modify", "19700101000000")
                    return name, size, mtime_str
        except:
            pass
        
        # Fallback
        try:
            ftp.sendcmd(f"SIZE {path}")
            size = int(ftp.sendcmd(f"SIZE {path}").split()[1])
            mtime_str = ftp.sendcmd(f"MDTM {path}")[4:].strip()
            return os.path.basename(path), size, mtime_str
        except:
            return os.path.basename(path), 0, "19700101000000"

    def walk_ftp(self, ftp, base_path, app_name, pdf_list):
        """Recursive walk - returns list of dicts"""
        self.log(f"Scanning → {app_name}: {base_path}")
        try:
            ftp.cwd(base_path)
        except ftplib.error_perm:
            self.log(f"Path not found: {base_path}")
            return

        try:
            items = list(ftp.mlsd(base_path, ["type", "size", "modify"]))
            for name, facts in items:
                if name in (".", ".."):
                    continue
                full_path = f"{base_path}/{name}".replace("//", "/")
                item_type = facts.get("type", "file")

                if item_type == "dir":
                    self.walk_ftp(ftp, full_path, app_name, pdf_list)
                elif self.is_pdf(name):
                    size = int(facts.get("size", 0))
                    mtime_str = facts.get("modify", "19700101000000")
                    pdf_list.append({
                        "app": app_name,
                        "remote_path": full_path,
                        "filename": name,
                        "size": size,
                        "mtime": mtime_str
                    })
                    self.log(f"   Found PDF: {name} ({size//1024} KB)")
        except:
            # Very old FTP fallback
            ftp.cwd(base_path)
            for name in ftp.nlst():
                if name in (".", ".."):
                    continue
                full_path = f"{base_path}/{name}".replace("//", "/")
                if self.is_pdf(name):
                    try:
                        size = int(ftp.sendcmd(f"SIZE {full_path}").split()[1])
                        mtime_str = ftp.sendcmd(f"MDTM {full_path}")[4:].strip()
                    except:
                        size, mtime_str = 0, "19700101000000"
                    pdf_list.append({
                        "app": app_name,
                        "remote_path": full_path,
                        "filename": name,
                        "size": size,
                        "mtime": mtime_str
                    })
                    self.log(f"   Found PDF: {name} ({size//1024} KB)")

    def scan_both_folders(self):
        all_pdfs = []
        for app_name, path in PATHS_TO_SCAN.items():
            self.walk_ftp(self.ftp, path, app_name, all_pdfs)

        # Filter only NEW PDFs using credible check (remote_path + size + mtime)
        new_list = []
        for pdf in all_pdfs:
            key = pdf["remote_path"]
            stored = self.log_csv.get(key)

            is_new = False
            if not stored:
                is_new = True
            else:
                if pdf["size"] != stored["size"] or pdf["mtime"] > stored["mtime"]:
                    is_new = True

            if is_new:
                new_list.append(pdf)

        self.queue.put(("scan_done", new_list))
        self.progress_scan.stop()
        self.scan_btn.config(state="normal")

    def display_new_pdfs(self, new_list):
        # Clear previous results
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.new_pdfs = new_list

        if not new_list:
            self.log("No new PDFs found.")
            self.download_btn.config(state="disabled")
            self.download_status.config(text="0 new PDFs ready")
            messagebox.showinfo("Scan Complete", "No new PDFs found in WhatsApp or WhatsApp Business folders.")
            return

        for pdf in new_list:
            self.result_tree.insert("", "end", values=(
                pdf["app"],
                pdf["filename"],
                f"{pdf['size']//1024:,}",
                pdf["mtime"][0:4] + "-" + pdf["mtime"][4:6] + "-" + pdf["mtime"][6:8] + " " + pdf["mtime"][8:10] + ":" + pdf["mtime"][10:12]
            ))

        self.download_btn.config(state="normal")
        self.download_status.config(text=f"{len(new_list)} new PDFs ready")
        self.log(f"✅ Scan complete → {len(new_list)} new PDFs found")

    def start_download_thread(self):
        if not self.new_pdfs:
            return
        self.download_btn.config(state="disabled")
        threading.Thread(target=self.download_new_pdfs, daemon=True).start()

    def download_new_pdfs(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        date_folder = os.path.join(LOCAL_BASE_DIR, today)
        os.makedirs(date_folder, exist_ok=True)

        total = len(self.new_pdfs)
        downloaded = 0

        for i, pdf in enumerate(self.new_pdfs):
            app_folder = os.path.join(date_folder, pdf["app"].replace(" ", "_"))
            os.makedirs(app_folder, exist_ok=True)

            # Safe local filename (in case of rare name clash)
            local_name = pdf["filename"]
            local_path = os.path.join(app_folder, local_name)

            # Download
            self.log(f"Downloading ({i+1}/{total}): {pdf['filename']}")
            try:
                with open(local_path, "wb") as f:
                    self.ftp.retrbinary(f"RETR {pdf['remote_path']}", f.write)

                # Compute MD5 for credible future checking
                with open(local_path, "rb") as f:
                    md5_hash = hashlib.md5(f.read()).hexdigest()

                # Record in CSV
                record = {
                    "app": pdf["app"],
                    "remote_path": pdf["remote_path"],
                    "filename": pdf["filename"],
                    "size": pdf["size"],
                    "mtime": pdf["mtime"],
                    "md5": md5_hash,
                    "local_path": local_path,
                    "download_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.save_to_csv(record)
                self.log_csv[pdf["remote_path"]] = {"size": pdf["size"], "mtime": pdf["mtime"], "md5": md5_hash}

                downloaded += 1

                progress = int((i + 1) / total * 100)
                self.queue.put(("download_progress", progress, f"{downloaded}/{total} downloaded"))

            except Exception as e:
                self.log(f"Failed {pdf['filename']}: {e}")

        self.queue.put(("log", f"🎉 Download finished! {downloaded} new PDFs saved in folder: {today}"))
        self.queue.put(("download_progress", 100, f"Done – {downloaded} PDFs downloaded"))

        # Re-enable scan
        self.after(500, lambda: self.download_btn.config(state="normal"))
        messagebox.showinfo("Success", f"Download complete!\n{downloaded} new PDFs saved in:\n{date_folder}")

    def open_download_folder(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        path = os.path.join(LOCAL_BASE_DIR, today)
        if os.path.exists(path):
            webbrowser.open(f"file://{os.path.abspath(path)}")
        else:
            webbrowser.open(f"file://{os.path.abspath(LOCAL_BASE_DIR)}")

    def open_csv(self):
        if os.path.exists(CSV_LOG_FILE):
            webbrowser.open(f"file://{os.path.abspath(CSV_LOG_FILE)}")
        else:
            self.log("CSV log not created yet.")

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, "end")
        self.log_text.configure(state="disabled")

    def quit(self):
        if self.ftp:
            try:
                self.ftp.quit()
            except:
                pass
        self.destroy()


if __name__ == "__main__":
    app = WhatsAppPDFDownloaderGUI()
    app.mainloop()
