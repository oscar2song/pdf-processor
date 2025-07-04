# GitHub: https://github.com/oscar2song/pdf-processor

import fitz  # PyMuPDF
import os
import sys
from pathlib import Path
import argparse
from datetime import datetime
import json
import logging
from typing import List, Optional, Dict, Any
import shutil

# Third-party imports for advanced features
try:
    import mammoth  # for PDF to Word conversion

    MAMMOTH_AVAILABLE = True
except ImportError:
    MAMMOTH_AVAILABLE = False
    print("⚠️  mammoth not available. PDF to Word conversion will be limited.")

try:
    from pdf2docx import Converter  # Alternative PDF to Word

    PDF2DOCX_AVAILABLE = True
except ImportError:
    PDF2DOCX_AVAILABLE = False

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  reportlab not available. Some features may be limited.")


class PDFProcessor:
    """
    Comprehensive PDF processing toolkit
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO if self.verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('pdf_processor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_file_size_mb(self, file_path: str) -> float:
        """Get file size in MB"""
        return os.path.getsize(file_path) / (1024 * 1024)

    def log_print(self, message: str, level: str = "info"):
        """Print and log message"""
        if self.verbose:
            print(message)
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)

    # ========== OPTIMIZATION FUNCTIONS ==========

    def optimize_pdf(self, input_pdf_path: str, output_pdf_path: str,
                     target_dpi: int = 150, jpeg_quality: int = 70) -> bool:
        """
        Optimize a single PDF file
        """
        try:
            self.log_print(f"🔧 Optimizing: {input_pdf_path}")
            self.log_print(f"🎯 Target DPI: {target_dpi}, Quality: {jpeg_quality}%")

            # Create output directory
            output_dir = Path(output_pdf_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            input_doc = fitz.open(input_pdf_path)
            output_doc = fitz.open()

            for page_num in range(len(input_doc)):
                page = input_doc.load_page(page_num)
                page_rect = page.rect

                # Calculate scale factor
                scale_factor = target_dpi / 72.0
                matrix = fitz.Matrix(scale_factor, scale_factor)

                # Render page
                pix = page.get_pixmap(matrix=matrix, alpha=False)

                # Create new page
                new_page = output_doc.new_page(width=page_rect.width, height=page_rect.height)

                # Compress and insert
                img_data = pix.tobytes("jpeg", jpeg_quality)
                img_rect = fitz.Rect(0, 0, page_rect.width, page_rect.height)
                new_page.insert_image(img_rect, stream=img_data)

                pix = None

            # Save optimized PDF
            output_doc.save(
                output_pdf_path,
                garbage=4, clean=True, deflate=True,
                deflate_images=True, deflate_fonts=True
            )

            input_doc.close()
            output_doc.close()

            # Report results
            original_size = self.get_file_size_mb(input_pdf_path)
            final_size = self.get_file_size_mb(output_pdf_path)
            reduction = ((original_size - final_size) / original_size) * 100

            self.log_print(f"✅ Optimized: {original_size:.2f}MB → {final_size:.2f}MB ({reduction:.1f}% reduction)")
            return True

        except Exception as e:
            self.log_print(f"❌ Error optimizing {input_pdf_path}: {str(e)}", "error")
            return False

    def batch_optimize_pdfs(self, input_folder: str, output_folder: str,
                            optimization_type: str = "standard",
                            target_dpi: int = 150, jpeg_quality: int = 70,
                            max_file_size_mb: int = 100) -> Dict[str, Any]:
        """
        Batch optimize all PDF files in a folder
        """
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)

        # Find PDF files
        pdf_files = list(input_path.glob("*.pdf"))

        if not pdf_files:
            self.log_print(f"❌ No PDF files found in {input_folder}", "warning")
            return {"success": False, "message": "No PDF files found"}

        # Set optimization parameters
        if optimization_type == "aggressive":
            target_dpi, jpeg_quality = 100, 60
        elif optimization_type == "high_quality":
            target_dpi, jpeg_quality = 200, 80

        self.log_print(f"🔧 Batch Optimization ({optimization_type})")
        self.log_print(f"📁 Input: {input_folder} | Output: {output_folder}")
        self.log_print(f"📄 Found {len(pdf_files)} PDF files")
        self.log_print(f"🎯 Settings: {target_dpi} DPI, {jpeg_quality}% quality")

        # Statistics
        stats = {
            "processed": 0, "skipped": 0, "failed": 0,
            "total_original_size": 0, "total_final_size": 0,
            "files": []
        }

        for i, pdf_file in enumerate(pdf_files, 1):
            self.log_print(f"\n📄 Processing {i}/{len(pdf_files)}: {pdf_file.name}")

            file_size = self.get_file_size_mb(pdf_file)
            if file_size > max_file_size_mb:
                self.log_print(f"⏭️  Skipping - too large ({file_size:.2f}MB)")
                stats["skipped"] += 1
                continue

            output_filename = f"{pdf_file.stem}_optimized.pdf"
            output_file_path = output_path / output_filename

            success = self.optimize_pdf(str(pdf_file), str(output_file_path), target_dpi, jpeg_quality)

            if success:
                original_size = self.get_file_size_mb(pdf_file)
                final_size = self.get_file_size_mb(output_file_path)
                stats["total_original_size"] += original_size
                stats["total_final_size"] += final_size
                stats["processed"] += 1
                stats["files"].append({
                    "original": str(pdf_file),
                    "optimized": str(output_file_path),
                    "original_size": original_size,
                    "final_size": final_size
                })
            else:
                stats["failed"] += 1

        # Final report
        if stats["processed"] > 0:
            total_reduction = ((stats["total_original_size"] - stats["total_final_size"]) / stats[
                "total_original_size"]) * 100
            self.log_print(
                f"\n🎉 Batch Complete! Processed: {stats['processed']}, Skipped: {stats['skipped']}, Failed: {stats['failed']}")
            self.log_print(
                f"📊 Total: {stats['total_original_size']:.2f}MB → {stats['total_final_size']:.2f}MB ({total_reduction:.1f}% reduction)")

        return stats

    # ========== PAGINATION FUNCTIONS ==========

    def add_page_numbers(self, input_pdf_path: str, output_pdf_path: str,
                         position: str = "bottom-right", start_page: int = 1,
                         font_size: int = 12, margin: int = 50) -> bool:
        """
        Add page numbers to PDF
        """
        try:
            self.log_print(f"📄 Adding page numbers to: {input_pdf_path}")

            doc = fitz.open(input_pdf_path)
            total_pages = len(doc)

            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                page_rect = page.rect

                # Calculate position
                page_number = start_page + page_num
                text = f"{page_number}"

                if position == "bottom-right":
                    point = fitz.Point(page_rect.width - margin, page_rect.height - margin)
                elif position == "bottom-center":
                    point = fitz.Point(page_rect.width / 2, page_rect.height - margin)
                elif position == "bottom-left":
                    point = fitz.Point(margin, page_rect.height - margin)
                elif position == "top-right":
                    point = fitz.Point(page_rect.width - margin, margin)
                elif position == "top-center":
                    point = fitz.Point(page_rect.width / 2, margin)
                elif position == "top-left":
                    point = fitz.Point(margin, margin)
                else:
                    point = fitz.Point(page_rect.width - margin, page_rect.height - margin)

                # Insert text
                page.insert_text(point, text, fontsize=font_size, color=(0, 0, 0))

            # Save
            output_dir = Path(output_pdf_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            doc.save(output_pdf_path)
            doc.close()

            self.log_print(f"✅ Added page numbers to {total_pages} pages")
            return True

        except Exception as e:
            self.log_print(f"❌ Error adding page numbers: {str(e)}", "error")
            return False

    def batch_add_page_numbers(self, input_folder: str, output_folder: str,
                               position: str = "bottom-right", **kwargs) -> Dict[str, Any]:
        """
        Batch add page numbers to all PDFs in folder
        """
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)

        pdf_files = list(input_path.glob("*.pdf"))

        if not pdf_files:
            return {"success": False, "message": "No PDF files found"}

        self.log_print(f"📄 Adding page numbers to {len(pdf_files)} PDFs")

        stats = {"processed": 0, "failed": 0, "files": []}

        for pdf_file in pdf_files:
            output_filename = f"{pdf_file.stem}_numbered.pdf"
            output_file_path = output_path / output_filename

            success = self.add_page_numbers(str(pdf_file), str(output_file_path), position, **kwargs)

            if success:
                stats["processed"] += 1
                stats["files"].append(str(output_file_path))
            else:
                stats["failed"] += 1

        self.log_print(f"🎉 Batch numbering complete! Processed: {stats['processed']}, Failed: {stats['failed']}")
        return stats

    # ========== MERGE FUNCTIONS ==========

    def merge_pdfs(self, input_files: List[str], output_pdf_path: str,
                   add_bookmarks: bool = True) -> bool:
        """
        Merge multiple PDF files into one
        """
        try:
            self.log_print(f"🔗 Merging {len(input_files)} PDF files")

            output_doc = fitz.open()

            for i, pdf_file in enumerate(input_files):
                self.log_print(f"📄 Adding: {Path(pdf_file).name}")

                input_doc = fitz.open(pdf_file)
                output_doc.insert_pdf(input_doc)

                # Add bookmark
                if add_bookmarks:
                    bookmark_title = Path(pdf_file).stem
                    # Calculate page number where this PDF starts
                    page_num = sum(len(fitz.open(f)) for f in input_files[:i])
                    output_doc.set_toc_item(0, bookmark_title, page_num + 1)

                input_doc.close()

            # Save merged PDF
            output_dir = Path(output_pdf_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            output_doc.save(output_pdf_path)
            output_doc.close()

            final_size = self.get_file_size_mb(output_pdf_path)
            self.log_print(f"✅ Merged PDF saved: {output_pdf_path} ({final_size:.2f}MB)")
            return True

        except Exception as e:
            self.log_print(f"❌ Error merging PDFs: {str(e)}", "error")
            return False

    def merge_folder_pdfs(self, input_folder: str, output_pdf_path: str,
                          sort_by: str = "name", add_page_numbers: bool = False) -> bool:
        """
        Merge all PDFs in a folder
        """
        input_path = Path(input_folder)
        pdf_files = list(input_path.glob("*.pdf"))

        if not pdf_files:
            self.log_print(f"❌ No PDF files found in {input_folder}", "warning")
            return False

        # Sort files
        if sort_by == "name":
            pdf_files.sort(key=lambda x: x.name)
        elif sort_by == "date":
            pdf_files.sort(key=lambda x: x.stat().st_mtime)
        elif sort_by == "size":
            pdf_files.sort(key=lambda x: x.stat().st_size)

        self.log_print(f"📁 Merging {len(pdf_files)} PDFs from folder")

        # Merge
        success = self.merge_pdfs([str(f) for f in pdf_files], output_pdf_path)

        # Add page numbers if requested
        if success and add_page_numbers:
            temp_path = output_pdf_path.replace(".pdf", "_temp.pdf")
            shutil.move(output_pdf_path, temp_path)
            self.add_page_numbers(temp_path, output_pdf_path)
            os.remove(temp_path)

        return success

    # ========== CONVERSION FUNCTIONS ==========

    def pdf_to_word(self, input_pdf_path: str, output_word_path: str,
                    method: str = "auto") -> bool:
        """
        Convert PDF to Word document
        """
        try:
            self.log_print(f"📄➡️📝 Converting PDF to Word: {input_pdf_path}")

            output_dir = Path(output_word_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Method 1: pdf2docx (better layout preservation)
            if method == "pdf2docx" or (method == "auto" and PDF2DOCX_AVAILABLE):
                if PDF2DOCX_AVAILABLE:
                    cv = Converter(input_pdf_path)
                    cv.convert(output_word_path, start=0, end=None)
                    cv.close()
                    self.log_print("✅ Converted using pdf2docx")
                    return True
                else:
                    self.log_print("⚠️  pdf2docx not available, trying alternative method")

            # Method 2: PyMuPDF extraction + basic Word creation
            self.log_print("🔄 Using PyMuPDF extraction method...")

            doc = fitz.open(input_pdf_path)

            # Extract text with formatting
            full_text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                full_text += f"\n\n--- Page {page_num + 1} ---\n\n{text}"

            # Save as text file (basic approach)
            text_output = output_word_path.replace(".docx", ".txt")
            with open(text_output, 'w', encoding='utf-8') as f:
                f.write(full_text)

            doc.close()

            self.log_print(f"✅ Converted to text file: {text_output}")
            self.log_print("💡 For better Word conversion, install pdf2docx: pip install pdf2docx")
            return True

        except Exception as e:
            self.log_print(f"❌ Error converting PDF to Word: {str(e)}", "error")
            return False

    def batch_pdf_to_word(self, input_folder: str, output_folder: str,
                          method: str = "auto") -> Dict[str, Any]:
        """
        Batch convert PDFs to Word documents
        """
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)

        pdf_files = list(input_path.glob("*.pdf"))

        if not pdf_files:
            return {"success": False, "message": "No PDF files found"}

        self.log_print(f"📄➡️📝 Converting {len(pdf_files)} PDFs to Word")

        stats = {"processed": 0, "failed": 0, "files": []}

        for pdf_file in pdf_files:
            output_filename = f"{pdf_file.stem}.docx"
            output_file_path = output_path / output_filename

            success = self.pdf_to_word(str(pdf_file), str(output_file_path), method)

            if success:
                stats["processed"] += 1
                stats["files"].append(str(output_file_path))
            else:
                stats["failed"] += 1

        self.log_print(f"🎉 Batch conversion complete! Processed: {stats['processed']}, Failed: {stats['failed']}")
        return stats

    # ========== UTILITY FUNCTIONS ==========

    def analyze_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Analyze PDF file properties
        """
        try:
            doc = fitz.open(pdf_path)

            # Basic info
            info = {
                "filename": Path(pdf_path).name,
                "file_size_mb": self.get_file_size_mb(pdf_path),
                "total_pages": len(doc),
                "metadata": doc.metadata,
                "is_encrypted": doc.is_encrypted,
                "page_sizes": []
            }

            # Analyze first few pages
            for page_num in range(min(5, len(doc))):
                page = doc.load_page(page_num)
                rect = page.rect
                info["page_sizes"].append({
                    "page": page_num + 1,
                    "width": rect.width,
                    "height": rect.height,
                    "images": len(page.get_images())
                })

            doc.close()
            return info

        except Exception as e:
            return {"error": str(e)}

    def generate_report(self, stats: Dict[str, Any], output_path: str = None) -> str:
        """
        Generate processing report
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
PDF Processor Report
==================
Generated: {timestamp}

Summary:
- Processed: {stats.get('processed', 0)}
- Failed: {stats.get('failed', 0)}
- Skipped: {stats.get('skipped', 0)}
"""

        if 'total_original_size' in stats:
            report += f"""
File Size Statistics:
- Original Total: {stats['total_original_size']:.2f} MB
- Final Total: {stats['total_final_size']:.2f} MB
- Space Saved: {stats['total_original_size'] - stats['total_final_size']:.2f} MB
"""

        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            self.log_print(f"📊 Report saved to: {output_path}")

        return report


# ========== COMMAND LINE INTERFACE ==========

def main():
    """
    Command line interface for PDF Processor
    """
    parser = argparse.ArgumentParser(description="PDF Processor - Comprehensive PDF toolkit")
    parser.add_argument("command", choices=[
        "optimize", "batch-optimize", "paginate", "batch-paginate",
        "merge", "merge-folder", "pdf-to-word", "batch-pdf-to-word",
        "analyze", "interactive"
    ], help="Command to execute")

    parser.add_argument("--input", "-i", required=False, help="Input file or folder")
    parser.add_argument("--output", "-o", required=False, help="Output file or folder")
    parser.add_argument("--dpi", type=int, default=150, help="Target DPI for optimization")
    parser.add_argument("--quality", type=int, default=70, help="JPEG quality (0-100)")
    parser.add_argument("--position", default="bottom-right", help="Page number position")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    processor = PDFProcessor(verbose=args.verbose)

    if args.command == "interactive":
        interactive_mode(processor)
    elif args.command == "optimize":
        if not args.input or not args.output:
            print("❌ --input and --output required for optimize command")
            return
        processor.optimize_pdf(args.input, args.output, args.dpi, args.quality)
    elif args.command == "batch-optimize":
        if not args.input or not args.output:
            print("❌ --input and --output required for batch-optimize command")
            return
        processor.batch_optimize_pdfs(args.input, args.output, target_dpi=args.dpi, jpeg_quality=args.quality)
    elif args.command == "analyze":
        if not args.input:
            print("❌ --input required for analyze command")
            return
        info = processor.analyze_pdf(args.input)
        print(json.dumps(info, indent=2))

    # Add more command implementations as needed


def interactive_mode(processor: PDFProcessor):
    """
    Interactive mode for user-friendly operation
    """
    print("🔧 PDF Processor - Interactive Mode")
    print("=" * 50)

    while True:
        print("\n📋 Available Commands:")
        print("1. Optimize PDF(s)")
        print("2. Add Page Numbers")
        print("3. Merge PDFs")
        print("4. Convert PDF to Word")
        print("5. Analyze PDF")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            input_path = input("📁 Enter input file or folder: ").strip()
            output_path = input("📁 Enter output file or folder: ").strip()

            if Path(input_path).is_file():
                processor.optimize_pdf(input_path, output_path)
            else:
                processor.batch_optimize_pdfs(input_path, output_path, "aggressive")

        elif choice == "2":
            input_path = input("📁 Enter input file or folder: ").strip()
            output_path = input("📁 Enter output file or folder: ").strip()
            position = input("📄 Position (bottom-right/bottom-center/top-right): ").strip() or "bottom-right"

            if Path(input_path).is_file():
                processor.add_page_numbers(input_path, output_path, position)
            else:
                processor.batch_add_page_numbers(input_path, output_path, position)

        elif choice == "3":
            input_folder = input("📁 Enter folder with PDFs to merge: ").strip()
            output_file = input("📄 Enter output merged PDF path: ").strip()
            add_numbers = input("Add page numbers? (y/n): ").strip().lower() == 'y'

            processor.merge_folder_pdfs(input_folder, output_file, add_page_numbers=add_numbers)

        elif choice == "4":
            input_path = input("📁 Enter PDF file or folder: ").strip()
            output_path = input("📁 Enter output Word file or folder: ").strip()

            if Path(input_path).is_file():
                processor.pdf_to_word(input_path, output_path)
            else:
                processor.batch_pdf_to_word(input_path, output_path)

        elif choice == "5":
            input_file = input("📄 Enter PDF file to analyze: ").strip()
            info = processor.analyze_pdf(input_file)
            print(json.dumps(info, indent=2))

        elif choice == "6":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        processor = PDFProcessor()
        interactive_mode(processor)
    else:
        # Run with command line arguments
        main()
