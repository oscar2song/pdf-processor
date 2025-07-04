#!/usr/bin/env python3
"""
PDF Processor - Example Usage
============================

This file demonstrates various ways to use the PDF Processor toolkit.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import pdf_processor
sys.path.append(str(Path(__file__).parent.parent))

from pdf_processor import PDFProcessor


def main():
    """
    Example usage of PDF Processor
    """

    # Initialize processor
    processor = PDFProcessor(verbose=True)

    print("🔧 PDF Processor - Example Usage")
    print("=" * 50)

    # Create sample directories
    sample_dir = Path("sample_pdfs")
    output_dir = Path("output")

    sample_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # Example 1: Analyze a PDF
    print("\n📊 Example 1: Analyze PDF")
    print("-" * 30)

    # Note: You'll need to add your own PDF files to the sample_pdfs folder
    sample_pdf = sample_dir / "sample.pdf"

    if sample_pdf.exists():
        analysis = processor.analyze_pdf(str(sample_pdf))
        print(f"📄 File: {analysis.get('filename', 'N/A')}")
        print(f"📏 Size: {analysis.get('file_size_mb', 0):.2f} MB")
        print(f"📖 Pages: {analysis.get('total_pages', 0)}")
        print(f"🔒 Encrypted: {analysis.get('is_encrypted', False)}")
    else:
        print("⚠️  No sample PDF found. Add a PDF to sample_pdfs/ folder to test.")

    # Example 2: Optimize PDF
    print("\n📉 Example 2: Optimize PDF")
    print("-" * 30)

    if sample_pdf.exists():
        optimized_pdf = output_dir / "optimized_sample.pdf"
        success = processor.optimize_pdf(
            str(sample_pdf),
            str(optimized_pdf),
            target_dpi=150,
            jpeg_quality=70
        )

        if success:
            print(f"✅ Optimized PDF saved to: {optimized_pdf}")
        else:
            print("❌ Optimization failed")

    # Example 3: Add Page Numbers
    print("\n📄 Example 3: Add Page Numbers")
    print("-" * 30)

    if sample_pdf.exists():
        numbered_pdf = output_dir / "numbered_sample.pdf"
        success = processor.add_page_numbers(
            str(sample_pdf),
            str(numbered_pdf),
            position="bottom-right",
            start_page=1,
            font_size=12
        )

        if success:
            print(f"✅ Numbered PDF saved to: {numbered_pdf}")
        else:
            print("❌ Page numbering failed")

    # Example 4: Batch Processing
    print("\n🔄 Example 4: Batch Processing")
    print("-" * 30)

    pdf_files = list(sample_dir.glob("*.pdf"))
    if pdf_files:
        batch_output = output_dir / "batch_optimized"
        stats = processor.batch_optimize_pdfs(
            str(sample_dir),
            str(batch_output),
            optimization_type="standard"
        )

        print(f"📊 Batch Results:")
        print(f"   Processed: {stats.get('processed', 0)}")
        print(f"   Failed: {stats.get('failed', 0)}")
        print(f"   Total Original: {stats.get('total_original_size', 0):.2f} MB")
        print(f"   Total Final: {stats.get('total_final_size', 0):.2f} MB")
    else:
        print("⚠️  No PDF files found for batch processing")

    # Example 5: Merge PDFs
    print("\n🔗 Example 5: Merge PDFs")
    print("-" * 30)

    if len(pdf_files) > 1:
        merged_pdf = output_dir / "merged_sample.pdf"
        success = processor.merge_folder_pdfs(
            str(sample_dir),
            str(merged_pdf),
            add_page_numbers=True
        )

        if success:
            print(f"✅ Merged PDF saved to: {merged_pdf}")
        else:
            print("❌ Merging failed")
    else:
        print("⚠️  Need at least 2 PDF files to demonstrate merging")

    # Example 6: Convert to Word
    print("\n📝 Example 6: Convert to Word")
    print("-" * 30)

    if sample_pdf.exists():
        word_doc = output_dir / "converted_sample.docx"
        success = processor.pdf_to_word(
            str(sample_pdf),
            str(word_doc)
        )

        if success:
            print(f"✅ Word document saved to: {word_doc}")
        else:
            print("❌ Conversion failed")

    print("\n🎉 Examples completed!")
    print(f"📁 Check the '{output_dir}' folder for results")
    print("\n💡 To add your own PDFs for testing:")
    print(f"   1. Copy PDF files to the '{sample_dir}' folder")
    print(f"   2. Run this script again")


if __name__ == "__main__":
    main()
