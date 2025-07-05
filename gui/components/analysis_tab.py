"""
Analysis Tab Component for PDF Processor GUI
============================================

Tab for PDF analysis functionality.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
from .base_tab import BaseTab


class AnalysisTab(BaseTab):
    """
    Analysis tab component
    """

    def create_widgets(self):
        """Create widgets for analysis tab"""
        # Create variables
        self.variables = {
            'input_path': tk.StringVar()
        }

        # Store analysis results
        self.analysis_results = None

        # File selection frame
        self.file_frame = self.create_file_frame()

        # Results frame
        self.results_frame = self.create_results_frame()

    def create_file_frame(self):
        """Create file selection frame"""
        file_frame = ttk.LabelFrame(self.frame, text="File Selection", padding="10")

        # Input file selection
        ttk.Label(file_frame, text="PDF File to Analyze:").pack(anchor=tk.W)
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=(5, 10))

        ttk.Entry(input_frame, textvariable=self.variables['input_path'], width=50).pack(side=tk.LEFT, fill=tk.X,
                                                                                         expand=True)
        ttk.Button(input_frame, text="Browse", command=self.browse_input_file_handler, style='Browse.TButton').pack(
            side=tk.RIGHT, padx=(5, 0))

        # Action buttons
        action_frame = ttk.Frame(file_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(action_frame, text="🚀 Analyze PDF", command=self.start_analysis, style='Action.TButton').pack(
            side=tk.RIGHT, padx=(5, 0))
        ttk.Button(action_frame, text="💾 Save Report", command=self.save_analysis_report, style='Browse.TButton').pack(
            side=tk.RIGHT)

        return file_frame

    def create_results_frame(self):
        """Create results display frame"""
        results_frame = ttk.LabelFrame(self.frame, text="Analysis Results", padding="10")

        # Create text widget with scrollbar for results
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.analysis_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            height=20,
            font=('Consolas', 10)
        )
        self.analysis_text.pack(fill=tk.BOTH, expand=True)

        # Initially show placeholder text
        self.show_placeholder_text()

        return results_frame

    def show_placeholder_text(self):
        """Show placeholder text in results area"""
        placeholder_text = """📊 PDF Analysis Results will appear here

🔍 To analyze a PDF:
1. Select a PDF file using the Browse button
2. Click "🚀 Analyze PDF" to start analysis
3. Results will be displayed here with detailed information
