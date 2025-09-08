
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import os
import threading
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path
import webbrowser
import json

class URLConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 All Video Downloader")
        self.root.geometry("1400x1000")
        self.root.minsize(1200, 800)
        self.root.resizable(True, True)
        
        # FFmpeg path
        self.ffmpeg_path = None
        self.is_downloading = False
        
        # Config file path
        self.config_file = os.path.join(os.path.expanduser("~"), ".urlconverter_config.json")
        
        # Modern Glassmorphic color scheme
        self.colors = {
            'primary': '#1E1E2E',      # Dark purple
            'secondary': '#2D2D44',    # Medium purple
            'accent': '#6366F1',       # Indigo
            'accent2': '#8B5CF6',      # Purple
            'accent3': '#06B6D4',      # Cyan
            'accent4': '#10B981',      # Emerald
            'success': '#10B981',      # Emerald
            'warning': '#F59E0B',      # Amber
            'error': '#EF4444',        # Red
            'text': '#F8FAFC',         # Light gray
            'text2': '#CBD5E1',        # Medium gray
            'bg': '#0F0F23',           # Very dark purple
            'glass': 'rgba(255, 255, 255, 0.1)',  # Glass effect
            'glass_dark': 'rgba(0, 0, 0, 0.2)',   # Dark glass
            'border': 'rgba(255, 255, 255, 0.2)', # Glass border
            'shadow': 'rgba(0, 0, 0, 0.3)'        # Shadow
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Variables
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp4")
        self.quality_var = tk.StringVar(value="4k")
        self.output_path = tk.StringVar()
        self.is_downloading = False
        self.advanced_mode = tk.BooleanVar(value=False)
        
        self.setup_ui()
        # Load saved settings
        self.load_config()
        # FFmpeg kontrolünü arka planda yap
        threading.Thread(target=self.check_ffmpeg_background, daemon=True).start()
        
    def setup_ui(self):
        # Configure styles
        self.setup_styles()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Main content area with proper scaling
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Configure grid weights for proper scaling
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel (inputs)
        left_panel = self.create_left_panel(content_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Right panel (preview and logs)
        right_panel = self.create_right_panel(content_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Set default output path
        self.output_path.set(os.path.join(os.path.expanduser("~"), "Downloads"))
        # Update path display
        self.update_path_display()
    
    def setup_styles(self):
        """Configure modern glassmorphic styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern button styles
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(20, 12),
                       borderwidth=0,
                       relief='flat')
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent2']),
                           ('pressed', self.colors['accent3'])])
        
        # Configure glass entry styles
        style.configure('Glass.TEntry',
                       fieldbackground=self.colors['secondary'],
                       foreground=self.colors['text'],
                       borderwidth=1,
                       relief='solid',
                       font=('Segoe UI', 11))
        
        # Configure modern label styles
        style.configure('Title.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text2'],
                       font=('Segoe UI', 12))
        
        style.configure('Info.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10))
        
        style.configure('Card.TLabel',
                       background=self.colors['secondary'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 11, 'bold'))
    
    def create_header(self, parent):
        """Create the modern header section with glassmorphic design"""
        # Main header card
        header_card = tk.Frame(parent, bg=self.colors['secondary'], relief='flat', bd=0)
        header_card.pack(fill=tk.X, pady=(0, 20))
        
        # Add rounded corners effect with padding
        header_content = tk.Frame(header_card, bg=self.colors['secondary'])
        header_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Title and icon row
        title_row = tk.Frame(header_content, bg=self.colors['secondary'])
        title_row.pack(fill=tk.X)
        
        # Icon
        icon_label = tk.Label(title_row, text="🎬", font=('Segoe UI', 20), 
                             bg=self.colors['secondary'], fg=self.colors['accent'])
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title
        title_label = tk.Label(title_row, text="All Video Downloader", 
                              font=('Segoe UI', 24, 'bold'), 
                              bg=self.colors['secondary'], fg=self.colors['text'])
        title_label.pack(side=tk.LEFT)
        
        # Help and Download buttons on the right
        button_frame = tk.Frame(title_row, bg=self.colors['secondary'])
        button_frame.pack(side=tk.RIGHT)
        
        # Download folder button
        folder_btn = tk.Button(button_frame, text="📁", font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['accent4'], fg='white', bd=0,
                              relief='flat', padx=12, pady=8,
                              command=self.browse_folder)
        folder_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add tooltip for folder button
        self.create_tooltip(folder_btn, "Select download folder")
        
        # Path display label next to folder button
        self.path_display = tk.Label(button_frame, text="📂 Downloads", 
                                   font=('Segoe UI', 10), 
                                   bg=self.colors['secondary'], fg=self.colors['text2'],
                                   wraplength=200, justify=tk.LEFT)
        self.path_display.pack(side=tk.LEFT, padx=(0, 10))
        
        # Download button
        download_btn = tk.Button(button_frame, text="📥 DOWNLOAD", font=('Segoe UI', 12, 'bold'),
                                bg=self.colors['accent'], fg='white', bd=0,
                                relief='flat', padx=20, pady=10,
                                command=self.start_download)
        download_btn.pack(side=tk.LEFT)
        
        # Progress bar
        progress_frame = tk.Frame(header_content, bg=self.colors['secondary'])
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Progress bar background
        progress_bg = tk.Frame(progress_frame, bg=self.colors['primary'], height=8)
        progress_bg.pack(fill=tk.X, pady=(5, 0))
        
        # Progress bar fill
        progress_fill = tk.Frame(progress_bg, bg=self.colors['accent'], height=8)
        progress_fill.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)
        
        # Storage info
        storage_label = tk.Label(progress_frame, text="60 GB free", 
                                font=('Segoe UI', 10), 
                                bg=self.colors['secondary'], fg=self.colors['text2'])
        storage_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Credits
        credits_label = tk.Label(header_content, text="Created by Mert Aydıngüneş", 
                                font=('Segoe UI', 9), 
                                bg=self.colors['secondary'], fg=self.colors['text2'])
        credits_label.pack(anchor=tk.E, pady=(10, 0))
    
    def create_left_panel(self, parent):
        """Create the modern left panel with glassmorphic cards"""
        panel = tk.Frame(parent, bg=self.colors['bg'])
        
        # URL input card
        url_card = tk.Frame(panel, bg=self.colors['secondary'], relief='flat', bd=0)
        url_card.pack(fill=tk.X, pady=(0, 15))
        
        url_content = tk.Frame(url_card, bg=self.colors['secondary'])
        url_content.pack(fill=tk.X, padx=15, pady=15)
        
        # URL label
        url_label = tk.Label(url_content, text="📎 Video URL", 
                            font=('Segoe UI', 12, 'bold'), 
                            bg=self.colors['secondary'], fg=self.colors['text'])
        url_label.pack(anchor=tk.W, pady=(0, 10))
        
        # URL entry with right-click context menu
        url_entry = tk.Entry(url_content, textvariable=self.url_var, 
                            font=('Segoe UI', 11), bg=self.colors['primary'], 
                            fg=self.colors['text'], bd=0, relief='flat',
                            insertbackground=self.colors['accent'])
        url_entry.pack(fill=tk.X, pady=(0, 10), ipady=12)
        
        # Add right-click context menu to URL entry
        self.create_context_menu(url_entry)
        
        # Format selection card
        format_card = tk.Frame(panel, bg=self.colors['secondary'], relief='flat', bd=0)
        format_card.pack(fill=tk.X, pady=(0, 15))
        
        format_content = tk.Frame(format_card, bg=self.colors['secondary'])
        format_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Format label
        format_label = tk.Label(format_content, text="🎵 Output Format", 
                               font=('Segoe UI', 12, 'bold'), 
                               bg=self.colors['secondary'], fg=self.colors['text'])
        format_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Format buttons
        format_buttons = tk.Frame(format_content, bg=self.colors['secondary'])
        format_buttons.pack(fill=tk.X)
        
        # Store format buttons for state management
        self.format_buttons = {}
        
        # MP4 button
        mp4_btn = tk.Button(format_buttons, text="🎬 MP4\nVideo + Audio", 
                           font=('Segoe UI', 10, 'bold'), 
                           bg=self.colors['accent'], fg='white', bd=0,
                           relief='flat', padx=20, pady=15,
                           command=lambda: self.select_format("mp4"))
        mp4_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        self.format_buttons["mp4"] = mp4_btn
        
        # MP3 button
        mp3_btn = tk.Button(format_buttons, text="🎵 MP3\nAudio Only", 
                           font=('Segoe UI', 10, 'bold'), 
                           bg=self.colors['accent3'], fg='white', bd=0,
                           relief='flat', padx=20, pady=15,
                           command=lambda: self.select_format("mp3"))
        mp3_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.format_buttons["mp3"] = mp3_btn
        
        # Set initial format selection (but don't call create_quality_buttons yet)
        self.format_var.set("mp4")  # Set default format
        
        # Quality selection card
        quality_card = tk.Frame(panel, bg=self.colors['secondary'], relief='flat', bd=0)
        quality_card.pack(fill=tk.X, pady=(0, 15))
        
        quality_content = tk.Frame(quality_card, bg=self.colors['secondary'])
        quality_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Quality label (will be updated dynamically)
        self.quality_label = tk.Label(quality_content, text="📺 Video Quality", 
                                     font=('Segoe UI', 12, 'bold'), 
                                     bg=self.colors['secondary'], fg=self.colors['text'])
        self.quality_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Quality buttons grid (will be updated dynamically)
        self.quality_grid = tk.Frame(quality_content, bg=self.colors['secondary'])
        self.quality_grid.pack(fill=tk.X)
        
        # Store quality buttons for state management
        self.quality_buttons = {}
        
        # Create initial quality buttons (after quality_grid is created)
        self.create_quality_buttons()
        
        # Set initial format selection with proper highlighting
        self.select_format("mp4")
        
        # Output path card
        output_card = tk.Frame(panel, bg=self.colors['secondary'], relief='flat', bd=0)
        output_card.pack(fill=tk.X, pady=(0, 15))
        
        output_content = tk.Frame(output_card, bg=self.colors['secondary'])
        output_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Output label
        output_label = tk.Label(output_content, text="📁 Save Location", 
                               font=('Segoe UI', 12, 'bold'), 
                               bg=self.colors['secondary'], fg=self.colors['text'])
        output_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Output entry and browse button
        output_row = tk.Frame(output_content, bg=self.colors['secondary'])
        output_row.pack(fill=tk.X)
        
        self.output_entry = tk.Entry(output_row, textvariable=self.output_path, 
                                    font=('Segoe UI', 11), bg=self.colors['primary'], 
                                    fg=self.colors['text'], bd=0, relief='flat',
                                    insertbackground=self.colors['accent'])
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=12)
        
        # Add context menu to output entry too
        self.create_context_menu(self.output_entry)
        
        # Folder selection button with file icon
        browse_btn = tk.Button(output_row, text="📁", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg=self.colors['accent4'], fg='white', bd=0,
                              relief='flat', padx=15, pady=12,
                              command=self.browse_folder)
        browse_btn.pack(side=tk.RIGHT)
        
        # Add tooltip for folder button
        self.create_tooltip(browse_btn, "Select download folder")
        
        # Download button
        self.download_btn = tk.Button(panel, text="🚀 Start Download", 
                                     font=('Segoe UI', 14, 'bold'), 
                                     bg=self.colors['accent'], fg='white', bd=0,
                                     relief='flat', padx=30, pady=20,
                                     command=self.start_download)
        self.download_btn.pack(fill=tk.X, pady=(20, 0))
        
        return panel
    
    def create_right_panel(self, parent):
        """Create the modern right panel with preview and logs"""
        panel = tk.Frame(parent, bg=self.colors['bg'])
        
        # Video info preview card
        preview_card = tk.Frame(panel, bg=self.colors['secondary'], relief='flat', bd=0)
        preview_card.pack(fill=tk.X, pady=(0, 15))
        
        preview_content = tk.Frame(preview_card, bg=self.colors['secondary'])
        preview_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Preview label
        preview_label = tk.Label(preview_content, text="📊 Video Information", 
                                font=('Segoe UI', 12, 'bold'), 
                                bg=self.colors['secondary'], fg=self.colors['text'])
        preview_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Video info text
        self.info_text = tk.Text(preview_content, height=8, wrap=tk.WORD, 
                                bg=self.colors['primary'], fg=self.colors['text'],
                                font=('Consolas', 9), state=tk.DISABLED,
                                insertbackground=self.colors['accent'], bd=0, relief='flat')
        self.info_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Progress section card
        progress_card = tk.Frame(panel, bg=self.colors['secondary'], relief='flat', bd=0)
        progress_card.pack(fill=tk.X, pady=(0, 15))
        
        progress_content = tk.Frame(progress_card, bg=self.colors['secondary'])
        progress_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Progress label
        progress_label = tk.Label(progress_content, text="📈 Download Progress", 
                                 font=('Segoe UI', 12, 'bold'), 
                                 bg=self.colors['secondary'], fg=self.colors['text'])
        progress_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_content, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(progress_content, text="Ready to download", 
                                    font=('Segoe UI', 10), 
                                    bg=self.colors['secondary'], fg=self.colors['text2'])
        self.status_label.pack(anchor=tk.W)
        
        # Log section card
        log_card = tk.Frame(panel, bg=self.colors['secondary'], relief='flat', bd=0)
        log_card.pack(fill=tk.BOTH, expand=True)
        
        log_content = tk.Frame(log_card, bg=self.colors['secondary'])
        log_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Log label
        log_label = tk.Label(log_content, text="📝 Download Log", 
                            font=('Segoe UI', 12, 'bold'), 
                            bg=self.colors['secondary'], fg=self.colors['text'])
        log_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Log text and scrollbar
        log_container = tk.Frame(log_content, bg=self.colors['secondary'])
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_container, wrap=tk.WORD, 
                               bg=self.colors['primary'], fg=self.colors['text'],
                               font=('Consolas', 9), bd=0, relief='flat',
                               insertbackground=self.colors['accent'])
        scrollbar = ttk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Add context menu to log text
        self.create_context_menu(self.log_text)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        return panel
    
    def toggle_advanced(self):
        """Toggle advanced settings visibility"""
        # This will be implemented to show/hide advanced options
        pass
    
    def create_context_menu(self, widget):
        """Create right-click context menu for text widgets"""
        context_menu = tk.Menu(widget, tearoff=0, bg=self.colors['secondary'], 
                              fg=self.colors['text'], font=('Segoe UI', 10))
        
        context_menu.add_command(label="📋 Paste", command=lambda: self.paste_text(widget))
        context_menu.add_command(label="✂️ Cut", command=lambda: self.cut_text(widget))
        context_menu.add_command(label="📄 Copy", command=lambda: self.copy_text(widget))
        context_menu.add_separator()
        context_menu.add_command(label="🗑️ Clear", command=lambda: self.clear_text(widget))
        context_menu.add_command(label="🔍 Select All", command=lambda: self.select_all_text(widget))
        
        def show_context_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
        
        widget.bind("<Button-3>", show_context_menu)  # Right-click
        widget.bind("<Control-v>", lambda e: self.paste_text(widget))  # Ctrl+V
        widget.bind("<Control-c>", lambda e: self.copy_text(widget))  # Ctrl+C
        widget.bind("<Control-x>", lambda e: self.cut_text(widget))  # Ctrl+X
        widget.bind("<Control-a>", lambda e: self.select_all_text(widget))  # Ctrl+A
    
    def paste_text(self, widget):
        """Paste text from clipboard"""
        try:
            widget.event_generate("<<Paste>>")
        except:
            pass
    
    def copy_text(self, widget):
        """Copy selected text to clipboard"""
        try:
            widget.event_generate("<<Copy>>")
        except:
            pass
    
    def cut_text(self, widget):
        """Cut selected text to clipboard"""
        try:
            widget.event_generate("<<Cut>>")
        except:
            pass
    
    def clear_text(self, widget):
        """Clear all text in widget"""
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, tk.Text):
            widget.delete(1.0, tk.END)
    
    def select_all_text(self, widget):
        """Select all text in widget"""
        if isinstance(widget, tk.Entry):
            widget.select_range(0, tk.END)
        elif isinstance(widget, tk.Text):
            widget.tag_add(tk.SEL, "1.0", tk.END)
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, 
                           bg=self.colors['primary'], fg=self.colors['text'],
                           font=('Segoe UI', 9), padx=8, pady=4,
                           relief='solid', bd=1)
            label.pack()
            
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def create_quality_buttons(self):
        """Create quality buttons based on current format"""
        # Clear existing buttons
        for widget in self.quality_grid.winfo_children():
            widget.destroy()
        self.quality_buttons.clear()
        
        # Get current format
        current_format = self.format_var.get()
        
        if current_format == "mp3":
            # Audio quality options
            self.quality_label.config(text="🎵 Audio Quality")
            qualities = [
                ("320 kbps", "320k", "High Quality", self.colors['accent']),
                ("256 kbps", "256k", "Good Quality", self.colors['accent2']),
                ("192 kbps", "192k", "Medium Quality", self.colors['accent3']),
                ("128 kbps", "128k", "Standard Quality", self.colors['accent4']),
                ("96 kbps", "96k", "Low Quality", self.colors['warning']),
                ("64 kbps", "64k", "Very Low Quality", self.colors['text2'])
            ]
        else:
            # Video quality options - All focused on 1920x1080 (Full HD)
            self.quality_label.config(text="📺 Video Quality (1920x1080)")
            qualities = [
                ("1080p 60fps", "1080p60", "1920x1080 60fps", self.colors['accent']),
                ("1080p FHD", "1080p", "1920x1080 30fps", self.colors['accent2']),
                ("1080p High", "1080p_high", "1920x1080 High", self.colors['accent3']),
                ("1080p Medium", "1080p_med", "1920x1080 Medium", self.colors['accent4']),
                ("1080p Low", "1080p_low", "1920x1080 Low", self.colors['warning']),
                ("1080p Auto", "1080p_auto", "1920x1080 Auto", self.colors['text2'])
            ]
        
        # Create buttons
        for i, (label, value, desc, color) in enumerate(qualities):
            row = i // 2
            col = i % 2
            
            quality_btn = tk.Button(self.quality_grid, text=f"{label}\n{desc}", 
                                  font=('Segoe UI', 8, 'bold'), 
                                  bg=color, fg='white', bd=0,
                                  relief='flat', padx=10, pady=8,
                                  command=lambda v=value: self.select_quality(v))
            quality_btn.grid(row=row, column=col, sticky=tk.W+tk.E, padx=(0, 8), pady=3)
            self.quality_grid.columnconfigure(col, weight=1)
            
            # Store button reference
            self.quality_buttons[value] = quality_btn
        
        # Set initial selection (default to first available quality)
        if self.quality_buttons:
            first_quality = list(self.quality_buttons.keys())[0]
            self.select_quality(first_quality)
    
    def select_format(self, format_type):
        """Select format and update button appearance"""
        self.format_var.set(format_type)
        
        # Reset all format buttons
        for format_name, button in self.format_buttons.items():
            if format_name == "mp4":
                button.config(bg=self.colors['accent'], relief='flat', bd=0, padx=20, pady=15)
            else:
                button.config(bg=self.colors['accent3'], relief='flat', bd=0, padx=20, pady=15)
        
        # Highlight selected format button with enhanced red styling
        if format_type in self.format_buttons:
            selected_button = self.format_buttons[format_type]
            selected_button.config(
                bg='#FF4444',  # Red background
                relief='solid', 
                bd=4,  # Thicker border
                highlightbackground='#FF4444',  # Bright red
                highlightcolor='#FF4444',  # Bright red
                highlightthickness=3,  # Thick highlight
                font=('Segoe UI', 11, 'bold'),  # Bolder font
                fg='white',  # White text
                padx=25,  # More padding
                pady=18   # More padding
            )
        
        # Update quality buttons based on format
        self.create_quality_buttons()
    
    def select_quality(self, quality):
        """Select quality and update button appearance"""
        self.quality_var.set(quality)
        
        # Define original colors for each quality (both video and audio)
        quality_colors = {
            # Video qualities - All 1920x1080 focused
            "1080p60": self.colors['accent'],
            "1080p": self.colors['accent2'],
            "1080p_high": self.colors['accent3'],
            "1080p_med": self.colors['accent4'],
            "1080p_low": self.colors['warning'],
            "1080p_auto": self.colors['text2'],
            # Audio qualities
            "320k": self.colors['accent'],
            "256k": self.colors['accent2'],
            "192k": self.colors['accent3'],
            "128k": self.colors['accent4'],
            "96k": self.colors['warning'],
            "64k": self.colors['text2']
        }
        
        # Reset all quality buttons
        for quality_name, button in self.quality_buttons.items():
            original_color = quality_colors.get(quality_name, self.colors['accent'])
            button.config(bg=original_color, relief='flat', bd=0, padx=10, pady=8)
        
        # Highlight selected quality button with enhanced red styling
        if quality in self.quality_buttons:
            selected_button = self.quality_buttons[quality]
            selected_button.config(
                bg='#FF4444',  # Red background
                relief='solid', 
                bd=4,  # Thicker border
                highlightbackground='#FF4444',  # Bright red
                highlightcolor='#FF4444',  # Bright red
                highlightthickness=3,  # Thick highlight
                font=('Segoe UI', 9, 'bold'),  # Bolder font
                fg='white',  # White text
                padx=12,  # More padding
                pady=10   # More padding
            )
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
🎬 All Video Downloader - Help

📎 Video URL:
• Paste any video URL from YouTube, Vimeo, Facebook, etc.
• The app will automatically detect the video source

🎵 Output Format:
• MP4: Download video with audio (recommended)
• MP3: Download only audio track

📺 Video Quality:
• 4K Ultra HD: Best quality (2160p)
• 1440p QHD: High quality (1440p)
• 1080p FHD: Full HD quality (1080p)
• 1080p 60fps: Full HD with 60fps
• 720p HD: HD quality (720p)
• 480p SD: Standard quality (480p)

📁 Save Location:
• Choose where to save downloaded files
• Default: Downloads folder

🚀 Start Download:
• Click to begin downloading
• Progress will be shown in the right panel

Created by Mert Aydıngüneş
        """
        
        # Create help window
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - All Video Downloader")
        help_window.geometry("500x600")
        help_window.configure(bg=self.colors['bg'])
        help_window.resizable(False, False)
        
        # Center the window
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Help content
        help_frame = tk.Frame(help_window, bg=self.colors['secondary'])
        help_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(help_frame, text="❓ Help", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg=self.colors['secondary'], fg=self.colors['text'])
        title_label.pack(pady=(0, 20))
        
        # Help text
        help_text_widget = tk.Text(help_frame, wrap=tk.WORD, 
                                  bg=self.colors['primary'], fg=self.colors['text'],
                                  font=('Segoe UI', 10), bd=0, relief='flat',
                                  state=tk.DISABLED)
        help_text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Insert help text
        help_text_widget.config(state=tk.NORMAL)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(help_frame, text="Close", 
                             font=('Segoe UI', 12, 'bold'), 
                             bg=self.colors['accent'], fg='white', bd=0,
                             relief='flat', padx=30, pady=10,
                             command=help_window.destroy)
        close_btn.pack()
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder:
            self.output_path.set(folder)
            self.update_path_display()
            self.save_config()  # Save the selected path
    
    def update_path_display(self):
        """Update the path display label with current download path"""
        current_path = self.output_path.get()
        if current_path:
            # Show only the last part of the path for space efficiency
            if len(current_path) > 30:
                display_text = f"📂 ...{current_path[-25:]}"
            else:
                display_text = f"📂 {current_path}"
            self.path_display.config(text=display_text)
        else:
            self.path_display.config(text="📂 Downloads")
    
    def load_config(self):
        """Load saved configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'output_path' in config:
                        self.output_path.set(config['output_path'])
                        self.update_path_display()
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            config = {
                'output_path': self.output_path.get()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_download(self):
        if self.is_downloading:
            return
            
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output folder")
            return
            
        # Start download in a separate thread
        self.is_downloading = True
        self.download_btn.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="Downloading...")
        
        thread = threading.Thread(target=self.download_video)
        thread.daemon = True
        thread.start()
    
    def progress_hook(self, d):
        """Progress callback for yt-dlp downloads"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / (1024 * 1024)
                    self.log_message(f"📥 Downloading: {percent:.1f}% - {speed_mb:.2f} MB/s")
                else:
                    self.log_message(f"📥 Downloading: {percent:.1f}%")
            elif 'total_bytes_estimate' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / (1024 * 1024)
                    self.log_message(f"📥 Downloading: ~{percent:.1f}% - {speed_mb:.2f} MB/s")
                else:
                    self.log_message(f"📥 Downloading: ~{percent:.1f}%")
        elif d['status'] == 'finished':
            self.log_message("✅ Download finished, processing...")

    def download_video(self):
        try:
            url = self.url_var.get().strip()
            output_format = self.format_var.get()
            quality = self.quality_var.get()
            output_dir = self.output_path.get()
            
            # Configure yt-dlp options for high quality
            ydl_opts = {
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'format': self.get_format_selector(output_format, quality),
                'writesubtitles': False,
                'writeautomaticsub': False,
                'extract_flat': False,
                'no_warnings': False,
                'ignoreerrors': False,
                'prefer_insecure': False,
                'geo_bypass': True,
                'geo_bypass_country': None,
                'geo_bypass_ip_block': None,
                'progress_hooks': [self.progress_hook],
            }
            
            if output_format == "mp3":
                # For MP3, try to find existing MP3 files first, then convert if needed
                ffmpeg_available = self.ffmpeg_path is not None
                ydl_opts.update({
                    'format': 'bestaudio[ext=mp3]/bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }] if ffmpeg_available else [],
                })
                
                if ffmpeg_available and self.ffmpeg_path != 'ffmpeg':
                    ydl_opts['ffmpeg_location'] = os.path.dirname(self.ffmpeg_path)
            else:
                # For video, get the best quality with FFmpeg if available
                ffmpeg_available = self.ffmpeg_path is not None
                ydl_opts.update({
                    'format': self.get_format_selector(output_format, quality),
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }] if ffmpeg_available else [],
                })
                
                if ffmpeg_available and self.ffmpeg_path != 'ffmpeg':
                    ydl_opts['ffmpeg_location'] = os.path.dirname(self.ffmpeg_path)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                self.log_message("🔍 Getting video information...")
                self.status_label.config(text="Analyzing video data...")
                
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                view_count = info.get('view_count', 0)
                upload_date = info.get('upload_date', 'Unknown')
                
                # Display video info
                self.display_video_info(info)
                
                self.log_message(f"📹 Title: {title}")
                self.log_message(f"👤 Uploader: {uploader}")
                self.log_message(f"⏱️ Duration: {duration // 60}:{duration % 60:02d}")
                self.log_message(f"👀 Views: {view_count:,}")
                self.log_message(f"📅 Upload Date: {upload_date}")
                self.log_message(f"🎯 Quality: {quality.upper()}")
                
                # Start download
                self.log_message("🚀 Starting download...")
                self.status_label.config(text="Downloading...")
                
                ydl.download([url])
                
            self.log_message("✅ Download completed successfully!")
            self.status_label.config(text="Download completed!")
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.log_message(error_msg)
            self.status_label.config(text="Download failed!")
            messagebox.showerror("Download Error", error_msg)
            
        finally:
            self.is_downloading = False
            self.download_btn.config(state="normal")
            self.progress.stop()
    
    def display_video_info(self, info):
        """Display modern video information in the preview panel"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        info_text = f"""📹 {info.get('title', 'Unknown')}
👤 {info.get('uploader', 'Unknown')}
⏱️ {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}
👀 {info.get('view_count', 0):,} views
📅 {info.get('upload_date', 'Unknown')}
🌐 {info.get('webpage_url', 'Unknown')}

Available formats:
"""
        
        # Get available formats with modern styling
        formats = info.get('formats', [])
        for fmt in formats[:10]:  # Show first 10 formats
            if fmt.get('vcodec') != 'none' or fmt.get('acodec') != 'none':
                height = fmt.get('height', 'Unknown')
                fps = fmt.get('fps', 'Unknown')
                ext = fmt.get('ext', 'Unknown')
                filesize = fmt.get('filesize', 0)
                if filesize:
                    size_mb = filesize / (1024 * 1024)
                    size_str = f"{size_mb:.1f}MB"
                else:
                    size_str = "Unknown"
                
                info_text += f"• {height}p {fps}fps {ext} ({size_str})\n"
        
        self.info_text.insert(1.0, info_text)
        self.info_text.config(state=tk.DISABLED)
    
    def get_format_selector(self, output_format, quality):
        if output_format == "mp3":
            return "bestaudio/best"
        
        # 1920x1080 (Full HD) focused format selectors - With FFmpeg support
        if self.ffmpeg_path:
            # High quality with FFmpeg available
            quality_selectors = {
                "1080p60": "bestvideo[height=1080][fps<=60]+bestaudio[ext=m4a]/bestvideo[height=1080]+bestaudio/best[height=1080][fps<=60]/best[height=1080]/best",
                "1080p": "bestvideo[height=1080]+bestaudio[ext=m4a]/bestvideo[height=1080]+bestaudio/best[height=1080]/best",
                "1080p_high": "bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height=1080]+bestaudio/best[height=1080][ext=mp4]/best[height=1080]/best",
                "1080p_med": "bestvideo[height=1080][filesize<500M]+bestaudio[ext=m4a]/bestvideo[height=1080]+bestaudio/best[height=1080]/best",
                "1080p_low": "bestvideo[height=1080][filesize<200M]+bestaudio[ext=m4a]/bestvideo[height=1080]+bestaudio/best[height=1080]/best",
                "1080p_auto": "bestvideo[height=1080]+bestaudio/best[height=1080]/best"
            }
        else:
            # Fallback without FFmpeg
            quality_selectors = {
                "1080p60": "best[height=1080][fps<=60]/best[height=1080]/best",
                "1080p": "best[height=1080]/best",
                "1080p_high": "best[height=1080][ext=mp4]/best[height=1080]/best",
                "1080p_med": "best[height=1080][filesize<500M]/best[height=1080]/best",
                "1080p_low": "best[height=1080][filesize<200M]/best[height=1080]/best",
                "1080p_auto": "best[height=1080]/best"
            }
        
        return quality_selectors.get(quality, "best[height=1080]/best")
    
    def check_ffmpeg_background(self):
        """Background FFmpeg check with downloading"""
        try:
            # Check if FFmpeg is in PATH
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                self.ffmpeg_path = 'ffmpeg'
                self.log_message("✅ FFmpeg bulundu ve hazır!")
                return True
        except:
            pass
        
        # Check if FFmpeg is in local directory
        local_ffmpeg = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
        if os.path.exists(local_ffmpeg):
            self.ffmpeg_path = local_ffmpeg
            self.log_message("✅ Yerel FFmpeg bulundu!")
            return True
        
        # FFmpeg not found, download it
        self.log_message("🔍 FFmpeg bulunamadı, otomatik indiriliyor...")
        self.download_ffmpeg_safe()
        return False
    
    def check_ffmpeg_simple(self):
        """Simple FFmpeg check without downloading"""
        try:
            # Check if FFmpeg is in PATH
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                self.ffmpeg_path = 'ffmpeg'
                self.log_message("✅ FFmpeg bulundu ve hazır!")
                return True
        except:
            pass
        
        # Check if FFmpeg is in local directory
        local_ffmpeg = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
        if os.path.exists(local_ffmpeg):
            self.ffmpeg_path = local_ffmpeg
            self.log_message("✅ Yerel FFmpeg bulundu!")
            return True
        
        # FFmpeg not found, but continue without it
        self.ffmpeg_path = None
        self.log_message("⚠️ FFmpeg bulunamadı, düşük kalite ile devam ediliyor.")
        return False
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available and download if needed"""
        try:
            # Check if FFmpeg is in PATH
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.ffmpeg_path = 'ffmpeg'
                print("✅ FFmpeg bulundu ve hazır!")
                return True
        except:
            pass
        
        # Check if FFmpeg is in local directory
        local_ffmpeg = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
        if os.path.exists(local_ffmpeg):
            self.ffmpeg_path = local_ffmpeg
            print("✅ Yerel FFmpeg bulundu!")
            return True
        
        # FFmpeg not found, download it
        print("🔍 FFmpeg bulunamadı, otomatik indiriliyor...")
        self.download_ffmpeg()
        return False
    
    def download_ffmpeg_safe(self):
        """Safe FFmpeg download with progress bar"""
        try:
            # Create ffmpeg directory
            ffmpeg_dir = os.path.join(os.path.dirname(__file__), 'ffmpeg')
            os.makedirs(ffmpeg_dir, exist_ok=True)
            
            # FFmpeg download URL (static build)
            ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            
            self.log_message("📥 FFmpeg indiriliyor... (Bu işlem 2-3 dakika sürebilir)")
            
            # Show progress bar
            self.show_ffmpeg_progress()
            
            # Download FFmpeg with progress
            zip_path = os.path.join(ffmpeg_dir, 'ffmpeg.zip')
            
            # Create request with timeout
            req = urllib.request.Request(ffmpeg_url)
            with urllib.request.urlopen(req, timeout=60) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                
                with open(zip_path, 'wb') as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            self.update_ffmpeg_progress(percent, downloaded, total_size)
            
            self.hide_ffmpeg_progress()
            self.log_message("📦 FFmpeg çıkarılıyor...")
            
            # Extract FFmpeg
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
            
            # Find ffmpeg.exe in extracted files
            for root, dirs, files in os.walk(ffmpeg_dir):
                if 'ffmpeg.exe' in files:
                    ffmpeg_exe = os.path.join(root, 'ffmpeg.exe')
                    # Move to ffmpeg directory
                    shutil.move(ffmpeg_exe, os.path.join(ffmpeg_dir, 'ffmpeg.exe'))
                    break
            
            # Clean up
            os.remove(zip_path)
            for root, dirs, files in os.walk(ffmpeg_dir):
                for dir_name in dirs:
                    if dir_name != 'ffmpeg':
                        shutil.rmtree(os.path.join(root, dir_name), ignore_errors=True)
            
            self.ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
            self.log_message("✅ FFmpeg başarıyla indirildi ve kuruldu!")
            self.log_message("🎯 Artık maksimum kalitede video indirebilirsiniz!")
            
        except Exception as e:
            self.hide_ffmpeg_progress()
            self.log_message(f"❌ FFmpeg indirme hatası: {str(e)}")
            self.log_message("⚠️ FFmpeg olmadan da çalışır, ancak kalite düşük olabilir.")
            self.ffmpeg_path = None
    
    def download_ffmpeg(self):
        """Download and extract FFmpeg automatically"""
        try:
            # Create ffmpeg directory
            ffmpeg_dir = os.path.join(os.path.dirname(__file__), 'ffmpeg')
            os.makedirs(ffmpeg_dir, exist_ok=True)
            
            # FFmpeg download URL (static build)
            ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            
            # UI'ye mesaj gönder
            if hasattr(self, 'log_text'):
                self.log_message("📥 FFmpeg indiriliyor...")
            
            # Download FFmpeg with timeout
            zip_path = os.path.join(ffmpeg_dir, 'ffmpeg.zip')
            urllib.request.urlretrieve(ffmpeg_url, zip_path)
            
            if hasattr(self, 'log_text'):
                self.log_message("📦 FFmpeg çıkarılıyor...")
            
            # Extract FFmpeg
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
            
            # Find ffmpeg.exe in extracted files
            for root, dirs, files in os.walk(ffmpeg_dir):
                if 'ffmpeg.exe' in files:
                    ffmpeg_exe = os.path.join(root, 'ffmpeg.exe')
                    # Move to ffmpeg directory
                    shutil.move(ffmpeg_exe, os.path.join(ffmpeg_dir, 'ffmpeg.exe'))
                    break
            
            # Clean up
            os.remove(zip_path)
            for root, dirs, files in os.walk(ffmpeg_dir):
                for dir_name in dirs:
                    if dir_name != 'ffmpeg':
                        shutil.rmtree(os.path.join(root, dir_name), ignore_errors=True)
            
            self.ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
            if hasattr(self, 'log_text'):
                self.log_message("✅ FFmpeg başarıyla indirildi ve kuruldu!")
            
        except Exception as e:
            if hasattr(self, 'log_text'):
                self.log_message(f"❌ FFmpeg indirme hatası: {str(e)}")
                self.log_message("⚠️ FFmpeg olmadan da çalışır, ancak kalite düşük olabilir.")
    
    def show_ffmpeg_progress(self):
        """Show FFmpeg download progress bar"""
        # Create progress window
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("FFmpeg İndiriliyor")
        self.progress_window.geometry("400x150")
        self.progress_window.resizable(False, False)
        self.progress_window.configure(bg=self.colors['bg'])
        
        # Center the window
        self.progress_window.transient(self.root)
        self.progress_window.grab_set()
        
        # Progress label
        self.progress_label = tk.Label(
            self.progress_window,
            text="📥 FFmpeg indiriliyor...",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        self.progress_label.pack(pady=20)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_window,
            mode='determinate',
            length=350,
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(pady=10)
        
        # Status label
        self.progress_status = tk.Label(
            self.progress_window,
            text="Hazırlanıyor...",
            font=('Segoe UI', 10),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        self.progress_status.pack(pady=5)
        
        # Configure progress bar style
        style = ttk.Style()
        style.configure('Custom.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['secondary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
    
    def update_ffmpeg_progress(self, percent, downloaded, total_size):
        """Update FFmpeg download progress"""
        if hasattr(self, 'progress_bar'):
            self.progress_bar['value'] = percent
            
            # Format file sizes
            downloaded_mb = downloaded / (1024 * 1024)
            total_mb = total_size / (1024 * 1024)
            
            status_text = f"İndiriliyor: {downloaded_mb:.1f} MB / {total_mb:.1f} MB ({percent:.1f}%)"
            self.progress_status.config(text=status_text)
            self.progress_window.update()
    
    def hide_ffmpeg_progress(self):
        """Hide FFmpeg download progress bar"""
        if hasattr(self, 'progress_window'):
            self.progress_window.destroy()
    
    def get_ffmpeg_path(self):
        """Get FFmpeg executable path"""
        return self.ffmpeg_path

def main():
    root = tk.Tk()
    app = URLConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
