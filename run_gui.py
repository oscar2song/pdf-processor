#!/usr/bin/env python3
"""
PDF Processor GUI Launcher
==========================

Launcher script for the PDF Processor GUI application.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from gui.main_window import main

    if __name__ == "__main__":
        print("🚀 Starting PDF Processor GUI...")
        main()

except ImportError as e:
    print(f"❌ Error importing GUI module: {e}")
    print("📋 Please ensure all dependencies are installed:")
    print("   pip install PyMuPDF pdf2docx reportlab")
    print("   and that pdf_processor.py is in the current directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting GUI: {e}")
    sys.exit(1)
