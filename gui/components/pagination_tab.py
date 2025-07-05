"""
Pagination Tab Component for PDF Processor GUI
==============================================

Tab for PDF page numbering functionality.
"""

import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab


class PaginationTab(BaseTab):
    """
    Pagination tab component
    """

    def create_widgets(self):
        """Create widgets for pagination tab"""
        # Create scrollable frame
        self.canvas, self.scrollbar, self.scrollable_frame = self.create_scrollable_frame(self.frame)

        # Create variables
        self.variables = {
            'input_path': tk.StringVar(),
            'output_path': tk.StringVar(),
            'position': tk.StringVar(value="bottom-right"),
            'start_page': tk.IntVar(value=1),
            'font_size': tk.IntVar(value=12),
            'margin': tk.IntVar(value=50),
            'continuous_numbering': tk.BooleanVar(value=False),
            'preserve_signatures': tk.BooleanVar(value=True)
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

        # Batch options frame
        self.batch_frame = self.create_batch_frame()

        # Action frame
        self.action_frame = self.create_action_frame(
            self.scrollable_frame,
            self.start_pagination,
            self.preview_settings
        )

    def create_settings_frame(self):
        """Create page numbering settings frame"""
        settings_frame = ttk.LabelFrame(self.scrollable_frame, text="Page Numbering Settings", padding="10")

        # Position selection
        position_options = [
            ("Bottom Right", "bottom-right"),
            ("Bottom Center", "bottom-center"),
            ("Bottom Left", "bottom-left"),
            ("Top Right", "top-right"),
            ("Top Center", "top-center"),
            ("Top Left", "top-left")
        ]

        position_frame = self.create_radiobutton_group(
            settings_frame,
            "Position:",
            self.variables['position'],
            position_options,
            "bottom-right"
        )

        # Other settings in grid
        other_frame = ttk.Frame(settings_frame)
        other_frame.pack(fill=tk.X, pady=(10, 0))

        # Start page
        self.create_spinbox_setting(
            other_frame, "Start Page:", self.variables['start_page'],
            1, 9999, width=10, row=0, col=0
        )

        # Font size
        self.create_spinbox_setting(
            other_frame, "Font Size:", self.variables['font_size'],
            8, 24, width=10, row=0, col=2, padx=(20, 10)
        )

        # Margin
        self.create_spinbox_setting(
            other_frame, "Margin:", self.variables['margin'],
            20, 100, width=10, row=1, col=0, pady=(10, 0)
        )

        return settings_frame

    def create_batch_frame(self):
        """Create batch options frame"""
        batch_frame = ttk.LabelFrame(self.scrollable_frame, text="Batch Options", padding="10")

        # Continuous numbering checkbox
        self.create_checkbox_setting(
            batch_frame,
            "Continuous numbering across files",
            self.variables['continuous_numbering'],
            False
        )

        # Preserve signatures checkbox
        self.create_checkbox_setting(
            batch_frame,
            "Preserve digital signatures",
            self.variables['preserve_signatures'],
            True
        )

        return batch_frame

    def setup_layout(self):
        """Setup layout for pagination tab"""
        # Pack frames
        self.file_frame.pack(fill=tk.X, pady=(0, 10))
        self.settings_frame.pack(fill=tk.X, pady=(0, 10))
        self.batch_frame.pack(fill=tk.X, pady=(0, 10))
        self.action_frame.pack(fill=tk.X, pady=(10, 0))

        # Pack scrollable frame
        self.pack_scrollable_frame(self.canvas, self.scrollbar)

    def get_settings(self):
        """Get pagination settings"""
        return {
            'input_path': self.variables['input_path'].get(),
            'output_path': self.variables['output_path'].get(),
            'position': self.variables['position'].get(),
            'start_page': self.variables['start_page'].get(),
            'font_size': self.variables['font_size'].get(),
            'margin': self.variables['margin'].get(),
            'continuous_numbering': self.variables['continuous_numbering'].get(),
            'preserve_signatures': self.variables['preserve_signatures'].get()
        }

    def browse_input_file_handler(self):
        """Handle browse input file"""
        self.browse_input_file(self.variables['input_path'])

    def browse_input_folder_handler(self):
        """Handle browse input folder"""
        self.browse_input_folder(self.variables['input_path'])

    def browse_output_handler(self):
        """Handle browse output"""
        self.browse_output_smart(
            self.variables['input_path'],
            self.variables['output_path'],
            "Save numbered PDF as",
            "Select output folder for numbered PDFs"
        )

    def preview_settings(self):
        """Preview pagination settings"""
        settings = self.get_settings()
        self.show_preview("Page Numbering", settings)

    def start_pagination(self):
        """Start pagination process"""
        self.start_processing(
            "pagination",
            self.processor_manager.process_pagination
        )
