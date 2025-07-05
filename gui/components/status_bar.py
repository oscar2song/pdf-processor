"""
Status Bar Component for PDF Processor GUI
==========================================

Status bar component for displaying current status and operation info.
"""

import tkinter as tk
from tkinter import ttk


class StatusBar:
    """
    Status bar component
    """

    def __init__(self, parent, processor_manager):
        self.parent = parent
        self.processor_manager = processor_manager
        self.status_var = tk.StringVar(value="Ready")

        # Set reference in processor manager
        self.processor_manager.set_status_bar(self)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        """Create status bar widgets"""
        # Status frame
        self.status_frame = ttk.Frame(self.parent)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))

        # Status label
        ttk.Label(self.status_frame, text="Status:", style='Status.TLabel').pack(side=tk.LEFT)
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))

        # Operation label (right side)
        self.operation_label = ttk.Label(self.status_frame, text="", style='Status.TLabel')
        self.operation_label.pack(side=tk.RIGHT)

    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        self.parent.update_idletasks()

    def update_operation(self, operation):
        """Update current operation"""
        self.operation_label.config(text=operation)
        self.parent.update_idletasks()

    def clear_operation(self):
        """Clear operation label"""
        self.operation_label.config(text="")
