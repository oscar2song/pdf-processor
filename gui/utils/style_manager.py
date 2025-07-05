"""
Style Manager for PDF Processor GUI
===================================

Manages all GUI styling and themes.
"""

from tkinter import ttk


class StyleManager:
    """
    Manages GUI styles and themes
    """

    def __init__(self):
        self.style = ttk.Style()

    def setup_styles(self):
        """Setup all custom styles"""
        self.setup_notebook_styles()
        self.setup_button_styles()
        self.setup_label_styles()
        self.setup_frame_styles()

    def setup_notebook_styles(self):
        """Setup notebook tab styles"""
        self.style.configure('TNotebook.Tab', padding=[20, 10])
        self.style.configure('TNotebook', tabposition='n')

    def setup_button_styles(self):
        """Setup button styles"""
        # Action buttons (main operation buttons)
        self.style.configure('Action.TButton',
                             font=('Arial', 10, 'bold'),
                             padding=[10, 5])

        # Browse buttons
        self.style.configure('Browse.TButton',
                             font=('Arial', 9),
                             padding=[8, 3])

        # Preview buttons
        self.style.configure('Preview.TButton',
                             font=('Arial', 9),
                             padding=[8, 3])

    def setup_label_styles(self):
        """Setup label styles"""
        # Title labels
        self.style.configure('Title.TLabel',
                             font=('Arial', 16, 'bold'),
                             foreground='#2c3e50')

        # Subtitle labels
        self.style.configure('Subtitle.TLabel',
                             font=('Arial', 11),
                             foreground='#7f8c8d')

        # Status labels
        self.style.configure('Status.TLabel',
                             font=('Arial', 9),
                             foreground='#34495e')

        # Section headers
        self.style.configure('SectionHeader.TLabel',
                             font=('Arial', 10, 'bold'),
                             foreground='#2c3e50')

    def setup_frame_styles(self):
        """Setup frame styles"""
        # Main frames
        self.style.configure('Main.TFrame', padding=[5, 5])

        # Section frames
        self.style.configure('Section.TFrame', padding=[10, 10])

        # Input frames
        self.style.configure('Input.TFrame', padding=[5, 5])

    def get_colors(self):
        """Get color scheme"""
        return {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'accent': '#e74c3c',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'gray': '#95a5a6',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c'
        }

    def apply_theme(self, theme_name='default'):
        """Apply a specific theme"""
        if theme_name == 'dark':
            self.apply_dark_theme()
        elif theme_name == 'light':
            self.apply_light_theme()
        else:
            self.apply_default_theme()

    def apply_default_theme(self):
        """Apply default theme"""
        colors = self.get_colors()

        # Update button colors
        self.style.map('Action.TButton',
                       background=[('active', colors['primary']),
                                   ('pressed', colors['dark'])])

        # Update label colors
        self.style.configure('Title.TLabel', foreground=colors['dark'])
        self.style.configure('Subtitle.TLabel', foreground=colors['gray'])

    def apply_dark_theme(self):
        """Apply dark theme (future implementation)"""
        # TODO: Implement dark theme
        pass

    def apply_light_theme(self):
        """Apply light theme (future implementation)"""
        # TODO: Implement light theme
        pass
