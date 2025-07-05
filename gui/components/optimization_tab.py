"""
Optimization Tab Component for PDF Processor GUI
===============================================

Tab for PDF optimization functionality.
"""

import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab


class OptimizationTab(BaseTab):
    """
    Optimization tab component
    """

    def create_widgets(self):
        """Create widgets for optimization tab"""
        # Create scrollable frame
        self.canvas, self.scrollbar, self.scrollable_frame = self.create_scrollable_frame(self.frame)

        # Create variables
        self.variables = {
            'input_path': tk.StringVar(),
            'output_path': tk.StringVar(),
            'optimization_type': tk.StringVar(value="aggressive"),
            'target_dpi': tk.IntVar(value=150),
            'jpeg_quality': tk.IntVar(value=70),
            'max_file_size_mb': tk.IntVar(value=100)
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

        # Action frame
        self.action_frame = self.create_action_frame(
            self.scrollable_frame,
            self.start_optimization,
            self.preview_settings
        )

    def create_settings_frame(self):
        """Create optimization settings frame"""
        settings_frame = ttk.LabelFrame(self.scrollable_frame, text="Optimization Settings", padding="10")

        # Optimization type selection
        optimization_options = [
            ("Standard (150 DPI, 70% quality)", "standard"),
            ("Aggressive (100 DPI, 60% quality)", "aggressive"),
            ("High Quality (200 DPI, 80% quality)", "high_quality"),
            ("Custom", "custom")
        ]

        self.create_radiobutton_group(
            settings_frame,
            "Optimization Type:",
            self.variables['optimization_type'],
            optimization_options,
            "aggressive"
        )

        # Custom settings
        custom_frame = ttk.Frame(settings_frame)
        custom_frame.pack(fill=tk.X, pady=(5, 10))

        # Target DPI
        self.create_spinbox_setting(
            custom_frame, "Target DPI:", self.variables['target_dpi'],
            50, 300, width=10, row=0, col=0
        )

        # JPEG Quality
        self.create_spinbox_setting(
            custom_frame, "JPEG Quality (0-100):", self.variables['jpeg_quality'],
            30, 100, width=10, row=0, col=2, padx=(20, 10)
        )

        # Max file size
        self.create_spinbox_setting(
            custom_frame, "Max File Size (MB):", self.variables['max_file_size_mb'],
            10, 1000, width=10, row=1, col=0, pady=(10, 0)
        )

        return settings_frame

    def setup_layout(self):
        """Setup layout for optimization tab"""
        # Pack frames
        self.file_frame.pack(fill=tk.X, pady=(0, 10))
        self.settings_frame.pack(fill=tk.X, pady=(0, 10))
        self.action_frame.pack(fill=tk.X, pady=(10, 0))

        # Pack scrollable frame
        self.pack_scrollable_frame(self.canvas, self.scrollbar)

    def get_settings(self):
        """Get optimization settings"""
        return {
            'input_path': self.variables['input_path'].get(),
            'output_path': self.variables['output_path'].get(),
            'optimization_type': self.variables['optimization_type'].get(),
            'target_dpi': self.variables['target_dpi'].get(),
            'jpeg_quality': self.variables['jpeg_quality'].get(),
            'max_file_size_mb': self.variables['max_file_size_mb'].get()
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
            "Save optimized PDF as",
            "Select output folder for optimized PDFs"
        )

    def preview_settings(self):
        """Preview optimization settings"""
        settings = self.get_settings()

        # Add estimated compression info
        if settings['optimization_type'] == 'aggressive':
            settings['estimated_compression'] = 'High'
        elif settings['optimization_type'] == 'standard':
            settings['estimated_compression'] = 'Medium'
        elif settings['optimization_type'] == 'high_quality':
            settings['estimated_compression'] = 'Low'
        else:
            settings['estimated_compression'] = 'Custom'

        self.show_preview("Optimization", settings)

    def start_optimization(self):
        """Start optimization process"""
        self.start_processing(
            "optimization",
            self.processor_manager.process_optimization
        )
