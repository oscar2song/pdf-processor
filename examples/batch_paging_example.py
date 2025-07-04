#!/usr/bin/env python3
"""
PDF Processor - Batch Paging Example
===================================

This example demonstrates the batch page numbering functionality
that keeps files separate (no merging).
"""

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import pdf_processor
sys.path.append(str(Path(__file__).parent.parent))

from pdf_processor import PDFProcessor


def main():
    """
    Example usage of batch page numbering
    """

    # Initialize processor
    processor = PDFProcessor(verbose=True)

    print("🔢 PDF Processor - Batch Page Numbering Example")
    print("=" * 60)

    # Create sample directories
    sample_dir = Path("sample_pdfs")
    output_dir = Path("numbered_pdfs")

    sample_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # Check if we have sample PDFs
    pdf_files = list(sample_dir.glob("*.pdf"))

    if not pdf_files:
        print("⚠️  No PDF files found in sample_pdfs/ folder.")
        print("💡 To test batch paging:")
        print("   1. Copy some PDF files to the 'sample_pdfs' folder")
        print("   2. Run this script again")
        return

    print(f"📄 Found {len(pdf_files)} PDF files:")
    for i, file in enumerate(pdf_files, 1):
        print(f"   {i}. {file.name}")

    # Example 1: Batch page numbering with separate numbering for each file
    print("\n📄 Example 1: Separate numbering for each file")
    print("-" * 50)

    separate_output = output_dir / "separate_numbering"
    stats = processor.batch_add_page_numbers(
        str(sample_dir),
        str(separate_output),
        position="bottom-right",
        start_page=1,
        font_size=12,
        continuous_numbering=False,  # Each file starts at page 1
        preserve_signatures=True
    )

    print(f"📊 Results: {stats['processed']} files processed, {stats['total_pages']} total pages")

    # Example 2: Batch page numbering with continuous numbering across files
    print("\n📄 Example 2: Continuous numbering across files")
    print("-" * 50)

    continuous_output = output_dir / "continuous_numbering"
    stats = processor.batch_add_page_numbers(
        str(sample_dir),
        str(continuous_output),
        position="bottom-center",
        start_page=1,
        font_size=14,
        continuous_numbering=True,  # Continue numbering across files
        preserve_signatures=True
    )

    print(f"📊 Results: {stats['processed']} files processed, {stats['total_pages']} total pages")

    # Example 3: Different positions
    print("\n📄 Example 3: Different positions")
    print("-" * 50)

    positions = ["top-left", "top-right", "bottom-left"]

    for position in positions:
        pos_output = output_dir / f"position_{position.replace('-', '_')}"
        stats = processor.batch_add_page_numbers(
            str(sample_dir),
            str(pos_output),
            position=position,
            start_page=1,
            font_size=10,
            continuous_numbering=False,
            preserve_signatures=True
        )

        print(f"   ✅ {position}: {stats['processed']} files processed")

    # Example 4: Command line equivalent
    print("\n💻 Command Line Equivalents:")
    print("-" * 50)
    print("# Separate numbering for each file:")
    print(
        f"python pdf_processor.py batch-paginate -i {sample_dir} -o {output_dir}/cli_separate --position bottom-right")
    print()
    print("# Continuous numbering across files:")
    print(
        f"python pdf_processor.py batch-paginate -i {sample_dir} -o {output_dir}/cli_continuous --position bottom-center --continuous")
    print()
    print("# With signature preservation disabled:")
    print(
        f"python pdf_processor.py batch-paginate -i {sample_dir} -o {output_dir}/cli_no_sigs --no-preserve-signatures")

    print(f"\n🎉 Examples completed!")
    print(f"📁 Check the '{output_dir}' folder for results")
    print(f"📄 Original files in '{sample_dir}' remain unchanged")

    # Show detailed stats
    if stats and stats.get('files'):
        print("\n📊 Detailed File Statistics:")
        print("-" * 30)
        for file_info in stats['files']:
            filename = Path(file_info['original']).name
            pages = file_info['pages']
            start_page = file_info['start_page']
            end_page = file_info['end_page']
            print(f"   {filename}: {pages} pages (numbered {start_page}-{end_page})")


if __name__ == "__main__":
    main()
