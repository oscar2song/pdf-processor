#!/usr/bin/env python3
"""
PDF Processor GUI - Main Application
====================================

Main GUI application that coordinates all components.
"""

import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from pdf_processor import PDFProcessor
except ImportError:
    print("Error: Could not import PDFProcessor. Make sure pdf_processor.py is in the parent directory.")
    sys.exit(1)

# Import GUI components
from .components.optimization_tab import OptimizationTab
from .components.pagination_tab import PaginationTab
from .components.merging_tab import MergingTab
from .components.conversion_tab import ConversionTab
from .components.analysis_tab import AnalysisTab
from .components.status_bar import StatusBar
from .components.log_area import LogArea
from .utils.processor_manager import ProcessorManager
from .utils.style_manager import StyleManager


class PDFProcessorGUI:
    """
    Main GUI application for PDF Processor
    """

    def __init__(self, root):
        self.root = root
        self.root.title("PDF Processor - Comprehensive PDF Toolkit")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # Initialize core components
        self.processor = PDFProcessor(verbose=False)
        self.style_manager = StyleManager()
        self.processor_manager = ProcessorManager(self.processor)

        # Setup GUI
        self.setup_gui()
        self.create_widgets()
        self.center_window()

        # Start processing monitor
        self.processor_manager.start_monitoring(self.root)

    def setup_gui(self):
        """Setup GUI styles and configuration"""
        self.style_manager.setup_styles()

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title section
        self.create_title_section(main_frame)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Create tabs
        self.create_tabs()

        # Status and progress section
        self.create_status_section(main_frame)

        # Log area
        self.create_log_section(main_frame)

    def create_title_section(self, parent):
        """Create title section"""
        title_label = ttk.Label(parent, text="PDF Processor", style='Title.TLabel')
        title_label.pack(pady=(0, 10))

        subtitle_label = ttk.Label(parent, text="Comprehensive PDF Processing Toolkit", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 20))

    def create_tabs(self):
        """Create all tabs"""
        # Optimization tab
        self.optimization_tab = OptimizationTab(self.notebook, self.processor_manager)
        self.notebook.add(self.optimization_tab.get_frame(), text="📉 Optimization")

        # Pagination tab
        self.pagination_tab = PaginationTab(self.notebook, self.processor_manager)
        self.notebook.add(self.pagination_tab.get_frame(), text="📄 Page Numbers")

        # Merging tab
        self.merging_tab = MergingTab(self.notebook, self.processor_manager)
        self.notebook.add(self.merging_tab.get_frame(), text="🔗 Merge PDFs")

        # Conversion tab
        self.conversion_tab = ConversionTab(self.notebook, self.processor_manager)
        self.notebook.add(self.conversion_tab.get_frame(), text="📝 PDF to Word")

        # Analysis tab
        self.analysis_tab = AnalysisTab(self.notebook, self.processor_manager)
        self.notebook.add(self.analysis_tab.get_frame(), text="📊 Analysis")

    def create_status_section(self, parent):
        """Create status bar and progress bar"""
        # Status bar
        self.status_bar = StatusBar(parent, self.processor_manager)

        # Progress bar
        self.progress_bar = ttk.Progressbar(parent, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))

        # Connect progress bar to processor manager
        self.processor_manager.set_progress_bar(self.progress_bar)

    def create_log_section(self, parent):
        """Create log area"""
        self.log_area = LogArea(parent)

        # Connect log area to processor manager
        self.processor_manager.set_log_area(self.log_area)

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = PDFProcessorGUI(root)

    # Handle window close
    def on_closing():
        if app.processor_manager.is_processing():
            from tkinter import messagebox
            result = messagebox.askquestion("Operation in Progress",
                                            "An operation is currently running. Do you want to force quit?",
                                            icon='warning')
            if result == 'yes':
                root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
