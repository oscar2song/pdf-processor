"""
Merging Tab Component for PDF Processor GUI
===========================================

Tab for PDF merging functionality.
"""

import tkinter as tk
from tkinter import ttk, filedialog
from .base_tab import BaseTab


class MergingTab(BaseTab):
    """
    Merging tab component
    """

    def create_widgets(self):
        """Create widgets for merging tab"""
        # Create scrollable frame
        self.canvas, self.scrollbar, self.scrollable_frame = self.create_scrollable_frame(self.frame)

        # Create variables
        self.variables = {
            'merge_method': tk.StringVar(value="folder"),
            'folder_path': tk.StringVar(),
            'output_path': tk.StringVar(),
            'add_page_numbers': tk.BooleanVar(value=True),
            'preserve_signatures': tk.BooleanVar(value=True),
            'font_size': tk.IntVar(value=12),
            'right_margin': tk.IntVar(value=72),
            'bottom_margin': tk.IntVar(value=54)
        }

        # Input selection frame
        self.input_frame = self.create_input_frame()

        # Settings frame
        self.settings_frame = self.create_settings_frame()

        # Action frame
        self.action_frame = self.create_action_frame(
            self.scrollable_frame,
            self.start_merging,
            self.preview_settings
        )

        # File list for specific files method
        self.file_list = []

    def create_input_frame(self):
        """Create input selection frame"""
        input_frame = ttk.LabelFrame(self.scrollable_frame, text="Input Selection", padding="10")

        # Method selection
        method_frame = ttk.Frame(input_frame)
        method_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Radiobutton(
            method_frame,
            text="Merge all PDFs in a folder",
            variable=self.variables['merge_method'],
            value="folder",
            command=self.update_merge_inputs
        ).pack(anchor=tk.W)

        ttk.Radiobutton(
            method_frame,
            text="Merge specific files",
            variable=self.variables['merge_method'],
            value="specific",
            command=self.update_merge_inputs
        ).pack(anchor=tk.W)

        # Folder input frame
        self.folder_frame = ttk.Frame(input_frame)
        self.folder_frame.pack(fill=tk.X, pady=(5, 10))

        ttk.Label(self.folder_frame, text="Input Folder:").pack(anchor=tk.W)
        folder_select_frame = ttk.Frame(self.folder_frame)
        folder_select_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Entry(folder_select_frame, textvariable=self.variables['folder_path'], width=50).pack(side=tk.LEFT,
                                                                                                  fill=tk.X,
                                                                                                  expand=True)
        ttk.Button(folder_select_frame, text="Browse", command=self.browse_folder, style='Browse.TButton').pack(
            side=tk.RIGHT, padx=(5, 0))

        # Specific files frame
        self.files_frame = ttk.Frame(input_frame)
        # Don't pack initially - will be shown when specific files is selected

        ttk.Label(self.files_frame, text="Selected Files:").pack(anchor=tk.W)

        # Listbox for files
        listbox_frame = ttk.Frame(self.files_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        self.files_listbox = tk.Listbox(listbox_frame, height=6)
        files_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=files_scrollbar.set)

        self.files_listbox.pack(side="left", fill="both", expand=True)
        files_scrollbar.pack(side="right", fill="y")

        # File management buttons
        files_btn_frame = ttk.Frame(self.files_frame)
        files_btn_frame.pack(fill=tk.X)

        ttk.Button(files_btn_frame, text="Add Files", command=self.add_files).pack(side=tk.LEFT)
        ttk.Button(files_btn_frame, text="Remove Selected", command=self.remove_files).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(files_btn_frame, text="Move Up", command=self.move_file_up).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(files_btn_frame, text="Move Down", command=self.move_file_down).pack(side=tk.LEFT, padx=(5, 0))

        # Output selection
        output_frame = ttk.Frame(input_frame)
        output_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(output_frame, text="Output File:").pack(anchor=tk.W)
        output_select_frame = ttk.Frame(output_frame)
        output_select_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Entry(output_select_frame, textvariable=self.variables['output_path'], width=50).pack(side=tk.LEFT,
                                                                                                  fill=tk.X,
                                                                                                  expand=True)
        ttk.Button(output_select_frame, text="Browse", command=self.browse_output, style='Browse.TButton').pack(
            side=tk.RIGHT, padx=(5, 0))

        # Initialize with folder method
        self.update_merge_inputs()

        return input_frame

    def create_settings_frame(self):
        """Create merge settings frame"""
        settings_frame = ttk.LabelFrame(self.scrollable_frame, text="Merge Settings", padding="10")

        # Page numbering options
        self.create_checkbox_setting(
            settings_frame,
            "Add page numbers to merged PDF",
            self.variables['add_page_numbers'],
            True
        )

        self.create_checkbox_setting(
            settings_frame,
            "Preserve digital signatures",
            self.variables['preserve_signatures'],
            True
        )

        # Page number settings for merged PDF
        page_frame = ttk.Frame(settings_frame)
        page_frame.pack(fill=tk.X, pady=(10, 0))

        # Font size
        self.create_spinbox_setting(
            page_frame, "Font Size:", self.variables['font_size'],
            8, 24, width=10, row=0, col=0
        )

        # Right margin
        self.create_spinbox_setting(
            page_frame, "Right Margin:", self.variables['right_margin'],
            20, 150, width=10, row=0, col=2, padx=(20, 10)
        )

        # Bottom margin
        self.create_spinbox_setting(
            page_frame, "Bottom Margin:", self.variables['bottom_margin'],
            20, 150, width=10, row=1, col=0, pady=(10, 0)
        )

        return settings_frame

    def setup_layout(self):
        """Setup layout for merging tab"""
        # Pack frames
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        self.settings_frame.pack(fill=tk.X, pady=(0, 10))
        self.action_frame.pack(fill=tk.X, pady=(10, 0))

        # Pack scrollable frame
        self.pack_scrollable_frame(self.canvas, self.scrollbar)

    def update_merge_inputs(self):
        """Update merge input widgets based on selected method"""
        if self.variables['merge_method'].get() == "folder":
            self.files_frame.pack_forget()
            self.folder_frame.pack(fill=tk.X, pady=(5, 10))
        else:
            self.folder_frame.pack_forget()
            self.files_frame.pack(fill=tk.X, pady=(5, 10))

    def browse_folder(self):
        """Browse for folder containing PDFs to merge"""
        folder = filedialog.askdirectory(title="Select folder containing PDFs to merge")
        if folder:
            self.variables['folder_path'].set(folder)

    def browse_output(self):
        """Browse for output file"""
        filename = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.variables['output_path'].set(filename)

    def add_files(self):
        """Add files to merge list"""
        filenames = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for filename in filenames:
            self.files_listbox.insert(tk.END, filename)
            self.file_list.append(filename)

    def remove_files(self):
        """Remove selected files from merge list"""
        selected_indices = self.files_listbox.curselection()
        for index in reversed(selected_indices):
            self.files_listbox.delete(index)
            del self.file_list[index]

    def move_file_up(self):
        """Move selected file up in the list"""
        selected_indices = self.files_listbox.curselection()
        if selected_indices and selected_indices[0] > 0:
            index = selected_indices[0]

            # Move in listbox
            item = self.files_listbox.get(index)
            self.files_listbox.delete(index)
            self.files_listbox.insert(index - 1, item)
            self.files_listbox.selection_set(index - 1)

            # Move in file list
            self.file_list[index], self.file_list[index - 1] = self.file_list[index - 1], self.file_list[index]

    def move_file_down(self):
        """Move selected file down in the list"""
        selected_indices = self.files_listbox.curselection()
        if selected_indices and selected_indices[0] < self.files_listbox.size() - 1:
            index = selected_indices[0]

            # Move in listbox
            item = self.files_listbox.get(index)
            self.files_listbox.delete(index)
            self.files_listbox.insert(index + 1, item)
            self.files_listbox.selection_set(index + 1)

            # Move in file list
            self.file_list[index], self.file_list[index + 1] = self.file_list[index + 1], self.file_list[index]

    def get_settings(self):
        """Get merge settings"""
        settings = {
            'method': self.variables['merge_method'].get(),
            'output_path': self.variables['output_path'].get(),
            'add_page_numbers': self.variables['add_page_numbers'].get(),
            'preserve_signatures': self.variables['preserve_signatures'].get(),
            'font_size': self.variables['font_size'].get(),
            'right_margin': self.variables['right_margin'].get(),
            'bottom_margin': self.variables['bottom_margin'].get()
        }

        if self.variables['merge_method'].get() == "folder":
            settings['input_path'] = self.variables['folder_path'].get()
        else:
            settings['input_path'] = "Selected files"
            settings['files'] = self.file_list.copy()

        return settings

    def validate_inputs(self, input_path, output_path=None):
        """Validate merge-specific inputs"""
        settings = self.get_settings()

        if not settings['output_path']:
            from tkinter import messagebox
            messagebox.showerror("Error", "Please select an output file.")
            return False

        if settings['method'] == "folder":
            if not settings['input_path']:
                from tkinter import messagebox
                messagebox.showerror("Error", "Please select an input folder.")
                return False
            import os
            if not os.path.exists(settings['input_path']):
                from tkinter import messagebox
                messagebox.showerror("Error", "Input folder does not exist.")
                return False
        else:
            if not settings.get('files'):
                from tkinter import messagebox
                messagebox.showerror("Error", "Please add files to merge.")
                return False

        return True

    def preview_settings(self):
        """Preview merge settings"""
        settings = self.get_settings()

        # Add file count info
        if settings['method'] == "folder":
            settings['files_info'] = f"All PDFs in folder"
        else:
            settings['files_info'] = f"{len(settings.get('files', []))} files selected"

        self.show_preview("Merge", settings)

    def start_merging(self):
        """Start merging process"""
        # Custom validation for merging
        settings = self.get_settings()
        if not self.validate_inputs(settings.get('input_path'), settings.get('output_path')):
            return

        self.start_processing(
            "merging",
            self.processor_manager.process_merging
        )
