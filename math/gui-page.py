import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from datetime import datetime

# ------------------- CustomTkinter Setup -------------------
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JSONtoWebpageApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JSON to Beautiful Webpage Generator")
        self.geometry("800x600")
        self.resizable(False, False)

        self.json_data = None
        self.json_path = None

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(self, text="JSON → Beautiful Webpage", 
                             font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=30)

        # Page Heading Input
        heading_frame = ctk.CTkFrame(self)
        heading_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(heading_frame, text="Page Heading:", 
                     font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=(10,5))
        
        self.heading_entry = ctk.CTkEntry(heading_frame, placeholder_text="e.g. Robotics & ROS Tutorials", 
                                          height=40, font=ctk.CTkFont(size=15))
        self.heading_entry.pack(padx=10, pady=5, fill="x")

        # Subtitle
        ctk.CTkLabel(heading_frame, text="Subtitle (optional):", 
                     font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=(10,5))
        
        self.subtitle_entry = ctk.CTkEntry(heading_frame, placeholder_text="Malayalam + English Tutorials", 
                                           height=40, font=ctk.CTkFont(size=15))
        self.subtitle_entry.pack(padx=10, pady=5, fill="x")

        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=30, padx=40, fill="x")

        self.select_btn = ctk.CTkButton(btn_frame, text="Select JSON File", 
                                        command=self.select_json, height=45, font=ctk.CTkFont(size=15))
        self.select_btn.pack(pady=8, fill="x")

        self.generate_btn = ctk.CTkButton(btn_frame, text="Generate Beautiful Webpage", 
                                          command=self.generate_html, height=50, 
                                          font=ctk.CTkFont(size=16, weight="bold"), 
                                          state="disabled")
        self.generate_btn.pack(pady=8, fill="x")

        # Status
        self.status_label = ctk.CTkLabel(self, text="No file selected", 
                                         text_color="gray")
        self.status_label.pack(pady=20)

    def select_json(self):
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.json_data = json.load(f)
                
                self.json_path = file_path
                filename = os.path.basename(file_path)
                
                self.status_label.configure(text=f"Loaded: {filename} | {len(self.get_videos())} videos", 
                                            text_color="lightgreen")
                self.generate_btn.configure(state="normal")
                
                # Auto-fill heading from project name if available
                if isinstance(self.json_data, dict) and 'project' in self.json_data:
                    proj = self.json_data['project']
                    self.heading_entry.delete(0, tk.END)
                    self.heading_entry.insert(0, proj.replace("_", " ").title() + " Tutorials")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON:\n{str(e)}")

    def get_videos(self):
        """Extract video list from different possible JSON structures"""
        if not self.json_data:
            return []
        
        if isinstance(self.json_data, dict):
            if 'videos' in self.json_data:
                return self.json_data['videos']
            elif 'project' in self.json_data and isinstance(self.json_data.get('videos'), list):
                return self.json_data['videos']
        
        # If it's a list directly
        if isinstance(self.json_data, list):
            return self.json_data
        
        return []

    def generate_html(self):
        if not self.json_data:
            messagebox.showwarning("Warning", "No JSON data loaded!")
            return

        heading = self.heading_entry.get().strip()
        subtitle = self.subtitle_entry.get().strip()

        if not heading:
            heading = "Robotics & ROS Video Library"

        videos = self.get_videos()
        if not videos:
            messagebox.showwarning("Warning", "No videos found in the JSON file!")
            return

        total_videos = len(videos)
        generated_date = datetime.now().strftime("%Y-%m-%d")

        html_content = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{heading} • Video Library</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
  <style>
    body {{ font-family: 'Inter', system-ui, sans-serif; }}
    .video-card {{
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .video-card:hover {{
      transform: translateY(-8px);
      box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
    }}
    .thumbnail-container {{ position: relative; }}
    .duration {{
      position: absolute; bottom: 8px; right: 8px;
      background: rgba(0, 0, 0, 0.85); color: white;
      font-size: 0.75rem; padding: 2px 6px; border-radius: 4px;
      font-weight: 600;
    }}
    .hero-bg {{ background: linear-gradient(135deg, #1e3a8a 0%, #312e81 100%); }}
  </style>
</head>
<body class="bg-zinc-950 text-zinc-100">
  <!-- HEADER -->
  <header class="hero-bg border-b border-zinc-800">
    <div class="max-w-7xl mx-auto px-6 py-8">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-x-4">
          <div class="w-14 h-14 bg-blue-600 rounded-3xl flex items-center justify-center text-4xl">
            🤖
          </div>
          <div>
            <h1 class="text-5xl font-bold tracking-tight">{heading}</h1>
            <p class="text-blue-300 text-xl">{subtitle if subtitle else "Curated Video Collection"}</p>
          </div>
        </div>
        <div class="flex items-center gap-x-6 text-sm">
          <div class="bg-zinc-900/70 px-5 py-3 rounded-3xl flex items-center gap-x-2">
            <span class="text-emerald-400 font-mono font-bold">{total_videos}</span>
            <span class="text-zinc-500">•</span>
            <span class="text-zinc-400">Videos</span>
          </div>
          <button onclick="alert('✅ Collection exported successfully!')" 
                  class="bg-white text-zinc-900 px-8 py-3 rounded-3xl font-semibold flex items-center gap-x-2 hover:bg-amber-300 transition">
            <i class="fa-solid fa-download"></i> Export
          </button>
        </div>
      </div>
    </div>
  </header>

  <div class="max-w-7xl mx-auto px-6 py-10">
    <!-- SEARCH -->
    <div class="flex flex-col md:flex-row gap-4 mb-12">
      <div class="flex-1 relative">
        <input id="searchInput" type="text" placeholder="Search videos by title..." 
               class="w-full bg-zinc-900 border border-zinc-700 rounded-3xl py-4 px-6 pl-14 focus:outline-none focus:border-blue-500 text-lg">
        <i class="fa-solid fa-magnifying-glass absolute left-6 top-1/2 -translate-y-1/2 text-zinc-500"></i>
      </div>
    </div>

    <!-- VIDEO GRID -->
    <div id="videoGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
      <!-- Populated by JS -->
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="bg-black py-12 border-t border-zinc-900 mt-20">
    <div class="max-w-7xl mx-auto px-6 text-center text-zinc-500 text-sm">
      <p>{heading} — Generated on {generated_date}</p>
      <p class="mt-2">Made with ❤️ using Python + Tailwind</p>
    </div>
  </footer>

  <script>
    const videos = {json.dumps(videos, ensure_ascii=False, indent=2)};

    function createVideoCard(video) {{
      const card = document.createElement('div');
      card.className = `video-card bg-zinc-900 rounded-3xl overflow-hidden border border-zinc-800`;
      card.innerHTML = `
        <div class="thumbnail-container">
          <img src="${{video.thumbnail}}" alt="${{video.title}}" 
               class="w-full aspect-video object-cover">
          <div class="duration">VIDEO</div>
        </div>
        <div class="p-6">
          <h3 class="font-semibold leading-tight line-clamp-3 mb-4 min-h-[3.75rem]">${{video.title}}</h3>
          <a href="${{video.url}}" target="_blank" 
             class="inline-flex items-center gap-x-2 text-blue-400 hover:text-blue-300 font-medium">
            <i class="fa-solid fa-play"></i>
            Watch on YouTube
          </a>
        </div>
      `;
      return card;
    }}

    function renderVideos(filteredVideos) {{
      const container = document.getElementById('videoGrid');
      container.innerHTML = '';
      filteredVideos.forEach(video => container.appendChild(createVideoCard(video)));
    }}

    // Search
    document.getElementById('searchInput').addEventListener('input', (e) => {{
      const term = e.target.value.toLowerCase();
      const filtered = videos.filter(v => 
        v.title.toLowerCase().includes(term)
      );
      renderVideos(filtered);
    }});

    // Initial render
    renderVideos(videos);

    // Keyboard shortcut
    document.addEventListener('keydown', e => {{
      if (e.key === '/' && document.getElementById('searchInput') !== document.activeElement) {{
        e.preventDefault();
        document.getElementById('searchInput').focus();
      }}
    }});
  </script>
</body>
</html>
"""

        # Save HTML file
        save_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")],
            initialfile=f"{heading.lower().replace(' ', '_')}_library.html"
        )

        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                messagebox.showinfo("Success", f"Beautiful webpage generated successfully!\n\nSaved as:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")


if __name__ == "__main__":
    app = JSONtoWebpageApp()
    app.mainloop()
