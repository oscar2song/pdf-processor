"""
Log Area Component for PDF Processor GUI
========================================

Collapsible log area for displaying operation logs.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime


class LogArea:
    """
    Log area component with collapsible functionality
    """

    def __init__(self, parent):
        self.parent = parent
        self.log_visible = tk.BooleanVar(value=False)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        """Create log area widgets"""
        # Log toggle button
        self.log_toggle_btn = ttk.Button(
            self.parent,
            text="🔽 Show Log",
            command=self.toggle_log
        )
        self.log_toggle_btn.pack(anchor=tk.W, pady=(5, 0))

        # Log frame (initially hidden)
        self.log_frame = ttk.LabelFrame(self.parent, text="Operation Log", padding="5")

        # Log text widget
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            height=8,
            wrap=tk.WORD,
            font=('Consolas', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Clear button
        self.clear_btn = ttk.Button(
            self.log_frame,
            text="Clear Log",
            command=self.clear_log
        )
        self.clear_btn.pack(anchor=tk.E, pady=(5, 0))

    def toggle_log(self):
        """Toggle log visibility"""
        if self.log_visible.get():
            self.log_frame.pack_forget()
            self.log_toggle_btn.config(text="🔽 Show Log")
            self.log_visible.set(False)
        else:
            self.log_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
            self.log_toggle_btn.config(text="🔼 Hide Log")
            self.log_visible.set(True)

    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.parent.update_idletasks()

    def clear_log(self):
        """Clear all log messages"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared")

    def save_log(self, filename=None):
        """Save log to file"""
        if filename is None:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                title="Save log as",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message(f"Log saved to {filename}")
                return True
            except Exception as e:
                self.log_message(f"Error saving log: {str(e)}")
                return False
        return False
