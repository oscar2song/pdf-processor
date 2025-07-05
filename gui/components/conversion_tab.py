"""
Conversion Tab Component for PDF Processor GUI
==============================================

Tab for PDF to Word conversion functionality.
"""

import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab


class ConversionTab(BaseTab):
    """
    Conversion tab component
    """

    def create_widgets(self):
        """Create widgets for conversion tab"""
        # Create scrollable frame
        self.canvas, self.scrollbar, self.scrollable_frame = self.create_scrollable_frame(self.frame)

        # Create variables
        self.variables = {
            'input_path': tk.StringVar(),
            'output_path': tk.StringVar(),
            'conversion_method': tk.StringVar(value="auto")
        }

        # File selection frame
        self.file_frame = self.create_file_selection_frame(
            self.scrollable_frame,
            "Input Selection",
            self.variables['input_path'],
            self.variables['output_path'],
            self.browse_input_file_handler,
            self.browse_input_folder_handler,
            self.browse_output_handler
        )

        # Settings frame
        self.settings_frame = self.create_settings_frame()

        # Info frame
        self.info_frame = self.create_info_frame()

        # Action frame
        self.action_frame = self.create_action_frame(
            self.scrollable_frame,
            self.start_conversion,
            self.preview_settings
        )

    def create_settings_frame(self):
        """Create conversion settings frame"""
        settings_frame = ttk.LabelFrame(self.scrollable_frame, text="Conversion Settings", padding="10")

        # Conversion method selection
        method_options = [
            ("Auto (Use best available method)", "auto"),
            ("pdf2docx (Better layout preservation)", "pdf2docx"),
            ("PyMuPDF (Basic text extraction)", "pymupdf")
        ]

        self.create_radiobutton_group(
            settings_frame,
            "Conversion Method:",
            self.variables['conversion_method'],
            method_options,
            "auto"
        )

        return settings_frame

    def create_info_frame(self):
        """Create information frame with tips"""
        info_frame = ttk.LabelFrame(self.scrollable_frame, text="Conversion Tips", padding="10")

        # Info text widget
        info_text = tk.Text(info_frame, height=6, wrap=tk.WORD, font=('Arial', 9))
        info_text.pack(fill=tk.X)

        # Add tips text
        tips_text = """💡 Conversion Tips:

• For best results, install pdf2docx: pip install pdf2docx
• Auto method will use pdf2docx if available, otherwise PyMuPDF
• PyMuPDF method creates text files instead of Word documents
• pdf2docx preserves layout, images, and formatting better
• Complex layouts may not convert perfectly - manual adjustment may be needed
• Scanned PDFs require OCR for proper text extraction"""

        info_text.insert(tk.END, tips_text)
        info_text.configure(state='disabled')

        return info_frame

    def setup_layout(self):
        """Setup layout for conversion tab"""
        # Pack frames
        self.file_frame.pack(fill=tk.X, pady=(0, 10))
        self.settings_frame.pack(fill=tk.X, pady=(0, 10))
        self.info_frame.pack(fill=tk.X, pady=(0, 10))
        self.action_frame.pack(fill=tk.X, pady=(10, 0))

        # Pack scrollable frame
        self.pack_scrollable_frame(self.canvas, self.scrollbar)

    def get_settings(self):
        """Get conversion settings"""
        method = self.variables['conversion_method'].get()

        # Generate note based on method
        note = ""
        if method == "auto":
            note = "Will use pdf2docx if available, otherwise PyMuPDF"
        elif method == "pdf2docx":
            note = "Requires pdf2docx library for best results"
        elif method == "pymupdf":
            note = "Basic text extraction, creates .txt files"

        return {
            'input_path': self.variables['input_path'].get(),
            'output_path': self.variables['output_path'].get(),
            'method': method,
            'note': note
        }

    def browse_input_file_handler(self):
        """Handle browse input file"""
        self.browse_input_file(self.variables['input_path'])

    def browse_input_folder_handler(self):
        """Handle browse input folder"""
        self.browse_input_folder(self.variables['input_path'])

    def browse_output_handler(self):
        """Handle browse output with Word document support"""
        import os

        if self.variables['input_path'].get() and os.path.isfile(self.variables['input_path'].get()):
            # Single file - ask for output file
            self.browse_output_file(
                self.variables['output_path'],
                "Save Word document as",
                ".docx",
                [("Word documents", "*.docx"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
        else:
            # Folder - ask for output folder
            self.browse_output_folder(
                self.variables['output_path'],
                "Select output folder for converted documents"
            )

    def preview_settings(self):
        """Preview conversion settings"""
        settings = self.get_settings()

        # Add file type info
        import os
        if settings['input_path'] and os.path.isfile(settings['input_path']):
            settings['process_type'] = "Single file conversion"
        elif settings['input_path']:
            settings['process_type'] = "Batch conversion"
        else:
            settings['process_type'] = "No input selected"

        self.show_preview("Conversion", settings)

    def start_conversion(self):
        """Start conversion process"""
        self.start_processing(
            "conversion",
            self.processor_manager.process_conversion
        )
