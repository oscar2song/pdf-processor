"""
Base Tab Component for PDF Processor GUI
========================================

Base class for all tab components.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from abc import ABC, abstractmethod


class BaseTab(ABC):
    """
    Base class for all tab components
    """

    def __init__(self, parent, processor_manager):
        self.parent = parent
        self.processor_manager = processor_manager
        self.frame = None
        self.variables = {}
        self.widgets = {}

        # Create the tab frame
        self.create_frame()
        self.create_widgets()
        self.setup_layout()

    def create_frame(self):
        """Create the main frame for the tab"""
        self.frame = ttk.Frame(self.parent)

    def get_frame(self):
        """Get the frame for this tab"""
        return self.frame

    @abstractmethod
    def create_widgets(self):
        """Create widgets for this tab - must be implemented by subclasses"""
        pass

    @abstractmethod
    def setup_layout(self):
        """Setup layout for this tab - must be implemented by subclasses"""
        pass

    @abstractmethod
    def get_settings(self):
        """Get settings from this tab - must be implemented by subclasses"""
        pass

    def create_scrollable_frame(self, parent):
        """Create a scrollable frame"""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        return canvas, scrollbar, scrollable_frame

    def create_file_selection_frame(self, parent, title, input_var, output_var,
                                    browse_file_func=None, browse_folder_func=None,
                                    browse_output_func=None):
        """Create a standard file selection frame"""
        file_frame = ttk.LabelFrame(parent, text=title, padding="10")

        # Input selection
        ttk.Label(file_frame, text="Input (File or Folder):").pack(anchor=tk.W)
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=(5, 10))

        ttk.Entry(input_frame, textvariable=input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)

        if browse_file_func:
            ttk.Button(input_frame, text="Browse File", command=browse_file_func, style='Browse.TButton').pack(
                side=tk.RIGHT, padx=(5, 0))
        if browse_folder_func:
            ttk.Button(input_frame, text="Browse Folder", command=browse_folder_func, style='Browse.TButton').pack(
                side=tk.RIGHT, padx=(5, 0))

        # Output selection
        ttk.Label(file_frame, text="Output (File or Folder):").pack(anchor=tk.W)
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Entry(output_frame, textvariable=output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        if browse_output_func:
            ttk.Button(output_frame, text="Browse", command=browse_output_func, style='Browse.TButton').pack(
                side=tk.RIGHT, padx=(5, 0))

        return file_frame

    def create_action_frame(self, parent, start_func, preview_func=None):
        """Create a standard action frame with buttons"""
        action_frame = ttk.Frame(parent)

        if start_func:
            ttk.Button(action_frame, text="🚀 Start Processing", command=start_func, style='Action.TButton').pack(
                side=tk.RIGHT, padx=(5, 0))

        if preview_func:
            ttk.Button(action_frame, text="🔍 Preview Settings", command=preview_func, style='Preview.TButton').pack(
                side=tk.RIGHT)

        return action_frame

    def browse_input_file(self, var, title="Select PDF file", filetypes=None):
        """Browse for input file"""
        if filetypes is None:
            filetypes = [("PDF files", "*.pdf"), ("All files", "*.*")]

        filename = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if filename:
            var.set(filename)

    def browse_input_folder(self, var, title="Select folder containing PDFs"):
        """Browse for input folder"""
        folder = filedialog.askdirectory(title=title)
        if folder:
            var.set(folder)

    def browse_output_file(self, var, title="Save as", defaultextension=".pdf", filetypes=None):
        """Browse for output file"""
        if filetypes is None:
            filetypes = [("PDF files", "*.pdf"), ("All files", "*.*")]

        filename = filedialog.asksaveasfilename(
            title=title,
            defaultextension=defaultextension,
            filetypes=filetypes
        )
        if filename:
            var.set(filename)

    def browse_output_folder(self, var, title="Select output folder"):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title=title)
        if folder:
            var.set(folder)

    def browse_output_smart(self, input_var, output_var, file_title="Save as",
                            folder_title="Select output folder", defaultextension=".pdf",
                            filetypes=None):
        """Smart output browsing - file or folder based on input"""
        if input_var.get() and os.path.isfile(input_var.get()):
            # Single file - ask for output file
            self.browse_output_file(output_var, file_title, defaultextension, filetypes)
        else:
            # Folder - ask for output folder
            self.browse_output_folder(output_var, folder_title)

    def validate_inputs(self, input_path, output_path=None):
        """Validate input and output paths"""
        if not input_path:
            messagebox.showerror("Error", "Please select an input file or folder.")
            return False

        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input path does not exist.")
            return False

        if output_path and not output_path:
            messagebox.showerror("Error", "Please select an output path.")
            return False

        return True

    def show_preview(self, title, settings):
        """Show settings preview"""
        preview_text = f"{title} Settings Preview:\n\n"

        for key, value in settings.items():
            if isinstance(value, bool):
                value = "Yes" if value else "No"
            elif isinstance(value, list):
                value = f"{len(value)} items"

            # Format key name
            formatted_key = key.replace('_', ' ').title()
            preview_text += f"{formatted_key}: {value}\n"

        messagebox.showinfo(f"{title} Preview", preview_text)

    def start_processing(self, operation_name, process_func, settings=None):
        """Start processing with validation"""
        if settings is None:
            settings = self.get_settings()

        # Validate inputs
        if not self.validate_inputs(settings.get('input_path'), settings.get('output_path')):
            return

        # Start processing
        self.processor_manager.start_operation(operation_name, process_func, settings)

    def create_spinbox_setting(self, parent, label_text, variable, from_val, to_val,
                               width=10, row=0, col=0, padx=(0, 10), pady=(0, 0)):
        """Create a spinbox setting"""
        ttk.Label(parent, text=label_text).grid(row=row, column=col, sticky=tk.W, padx=padx, pady=pady)
        ttk.Spinbox(parent, from_=from_val, to=to_val, textvariable=variable, width=width).grid(row=row, column=col + 1,
                                                                                                sticky=tk.W, pady=pady)

    def create_radiobutton_group(self, parent, label_text, variable, options, default=None):
        """Create a group of radio buttons"""
        ttk.Label(parent, text=label_text).pack(anchor=tk.W)

        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=(5, 10))

        for i, (text, value) in enumerate(options):
            ttk.Radiobutton(frame, text=text, variable=variable, value=value).pack(anchor=tk.W)

        if default and hasattr(variable, 'set'):
            variable.set(default)

        return frame

    def create_checkbox_setting(self, parent, text, variable, default=False):
        """Create a checkbox setting"""
        if hasattr(variable, 'set'):
            variable.set(default)

        checkbox = ttk.Checkbutton(parent, text=text, variable=variable)
        checkbox.pack(anchor=tk.W)
        return checkbox

    def pack_scrollable_frame(self, canvas, scrollbar):
        """Pack scrollable frame components"""
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
