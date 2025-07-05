# PDF Processor 📄

A comprehensive Python toolkit for PDF processing operations including optimization, pagination, merging, and conversion. Now with a **modern GUI interface**!

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/oscar2song/pdf-processor)](https://github.com/oscar2song/pdf-processor/issues)
[![GUI Available](https://img.shields.io/badge/GUI-Available-green.svg)](https://github.com/oscar2song/pdf-processor#gui-interface)

## 🚀 Features

- **📉 PDF Optimization**: Compress and optimize PDF files for smaller sizes (up to 90% reduction)
- **🔢 Page Numbering**: Add page numbers to PDFs in various positions
- **📄 Batch Page Numbering**: Add page numbers to multiple PDFs (keep files separate)
- **🔗 PDF Merging**: Merge multiple PDFs into one document with bookmarks
- **📝 PDF to Word**: Convert PDFs to Word documents with layout preservation
- **📊 PDF Analysis**: Analyze PDF properties, metadata, and structure
- **🔄 Batch Processing**: Process multiple files at once efficiently
- **🔒 Signature Preservation**: Preserve digital signatures and form data
- **🎨 Modern GUI**: User-friendly graphical interface (NEW!)
- **🎛️ Interactive Mode**: Command-line interface
- **🛠️ Command Line Tools**: Full CLI support for automation

## 📋 Requirements

- Python 3.8+
- PyMuPDF (fitz)
- pdf2docx (optional, for better PDF to Word conversion)
- reportlab (optional, for advanced features)
- tkinter (included with Python, for GUI)

## 🛠️ Installation

### Method 1: Clone from GitHub (Recommended)

```bash
git clone https://github.com/oscar2song/pdf-processor.git
cd pdf-processor
pip install -r requirements.txt
```

### Method 2: Install Dependencies Manually

```bash
pip install PyMuPDF pdf2docx reportlab
```

### For GUI Support

```bash
pip install -r requirements_gui.txt
```

## 🎯 Quick Start

### 🎨 **GUI Interface** (Recommended for beginners)

```bash
python run_gui.py
```

**Features:**
- **Modern tabbed interface** with 5 main sections
- **Real-time progress bars** and status updates
- **Drag & drop file selection** with browse buttons
- **Settings preview** before processing
- **Live logging** with collapsible log area
- **Error handling** with user-friendly messages

![GUI Screenshot](screenshots/gui_main.png)

### 🎛️ **Interactive Mode** (Command-line friendly)

```bash
python pdf_processor.py
```

This will launch an interactive menu where you can:
1. Optimize PDF(s)
2. Add Page Numbers (Keep Files Separate)
3. Merge PDFs
4. Convert PDF to Word
5. Analyze PDF

### 🛠️ **Command Line Usage** (For automation)

```bash
# Optimize a single PDF
python pdf_processor.py optimize -i input.pdf -o output.pdf --dpi 150 --quality 70

# Batch optimize PDFs (aggressive compression)
python pdf_processor.py batch-optimize -i input_folder -o output_folder

# Add page numbers to single PDF
python pdf_processor.py paginate -i input.pdf -o output.pdf --position bottom-right

# Batch add page numbers (keep files separate)
python pdf_processor.py batch-paginate -i input_folder -o output_folder --position bottom-center

# Batch add page numbers with continuous numbering across files
python pdf_processor.py batch-paginate -i input_folder -o output_folder --continuous

# Merge PDFs in a folder
python pdf_processor.py merge-folder -i pdf_folder -o merged.pdf

# Convert PDF to Word
python pdf_processor.py pdf-to-word -i input.pdf -o output.docx

# Analyze PDF properties
python pdf_processor.py analyze -i document.pdf
```

## 📖 Detailed Usage

### 1. PDF Optimization

Reduce PDF file sizes by compressing images and optimizing content:

```python
from pdf_processor import PDFProcessor

processor = PDFProcessor()

# Single file optimization
processor.optimize_pdf(
    "large.pdf", 
    "compressed.pdf", 
    target_dpi=150, 
    jpeg_quality=70
)

# Batch optimization
stats = processor.batch_optimize_pdfs(
    input_folder="input_pdfs",
    output_folder="optimized_pdfs",
    optimization_type="aggressive"
)

print(f"Processed: {stats['processed']}")
print(f"Total size reduction: {stats['total_original_size'] - stats['total_final_size']:.2f} MB")
```

**Optimization Types:**
- `standard`: 150 DPI, 70% quality - balanced approach
- `aggressive`: 100 DPI, 60% quality - maximum compression (up to 90% reduction)
- `high_quality`: 200 DPI, 80% quality - preserves detail

### 2. Page Numbering

Add page numbers to PDFs in various positions with signature preservation:

```python
# Add page numbers to single PDF
processor.add_page_numbers(
    "input.pdf", 
    "numbered.pdf", 
    position="bottom-right",
    start_page=1,
    font_size=12,
    margin=50,
    preserve_signatures=True
)

# Batch add page numbers (keep files separate)
stats = processor.batch_add_page_numbers(
    "input_folder", 
    "output_folder", 
    position="bottom-center",
    continuous_numbering=False,  # Each file starts at page 1
    preserve_signatures=True
)

# Batch add page numbers with continuous numbering across files
stats = processor.batch_add_page_numbers(
    "input_folder", 
    "output_folder", 
    position="bottom-right",
    continuous_numbering=True,  # Continue numbering across files
    preserve_signatures=True
)
```

**Available Positions:**
- `bottom-right`, `bottom-center`, `bottom-left`
- `top-right`, `top-center`, `top-left`

**Batch Options:**
- `continuous_numbering=False`: Each file starts at page 1 (default)
- `continuous_numbering=True`: Continue numbering across all files
- `preserve_signatures=True`: Preserve digital signatures (default)

### 3. PDF Merging

Merge multiple PDFs into one document with signature preservation:

```python
# Merge specific files
processor.merge_specific_files(
    ["file1.pdf", "file2.pdf", "file3.pdf"],
    "merged.pdf",
    add_page_numbers=True,
    preserve_signatures=True
)

# Merge all PDFs in a folder
processor.merge_folder_pdfs(
    "pdf_folder",
    "merged_output.pdf",
    add_page_numbers=True,
    preserve_signatures=True
)

# Advanced merging with custom settings
processor.merge_pdfs_with_page_numbers(
    "pdf_folder",  # or list of files
    "merged.pdf",
    add_page_numbers=True,
    font_size=12,
    right_margin=72,  # 1 inch from right
    bottom_margin=54,  # 0.75 inch from bottom
    preserve_signatures=True
)
```

### 4. PDF to Word Conversion

Convert PDFs to editable Word documents:

```python
# Single file conversion
processor.pdf_to_word("document.pdf", "document.docx")

# Batch conversion
stats = processor.batch_pdf_to_word(
    "pdf_folder",
    "word_folder",
    method="auto"  # Uses best available method
)
```

**Note**: For best results, install `pdf2docx`: `pip install pdf2docx`

### 5. PDF Analysis

Analyze PDF properties and structure:

```python
info = processor.analyze_pdf("document.pdf")
print(f"Pages: {info['total_pages']}")
print(f"Size: {info['file_size_mb']:.2f} MB")
print(f"Encrypted: {info['is_encrypted']}")
print(f"Metadata: {info['metadata']}")
```

## 🔧 Advanced Usage

### Custom Processing Pipeline

```python
processor = PDFProcessor(verbose=True)

# 1. Analyze first
info = processor.analyze_pdf("input.pdf")
print(f"Original size: {info['file_size_mb']:.2f} MB")

# 2. Optimize
processor.optimize_pdf("input.pdf", "temp.pdf", target_dpi=120, jpeg_quality=65)

# 3. Add page numbers
processor.add_page_numbers("temp.pdf", "final.pdf", position="bottom-center")

# 4. Clean up
os.remove("temp.pdf")
```

### Batch Processing with Custom Settings

```python
# Process large batches with custom settings
stats = processor.batch_optimize_pdfs(
    input_folder="large_pdfs",
    output_folder="compressed_pdfs",
    optimization_type="custom",
    target_dpi=100,
    jpeg_quality=60,
    max_file_size_mb=200  # Skip files larger than 200MB
)

# Generate report
report = processor.generate_report(stats, "processing_report.txt")
```

## 🎨 GUI Interface

### Launch GUI
```bash
python run_gui.py
```

### GUI Features
- **📉 Optimization Tab**: Visual PDF compression with preset and custom settings
- **📄 Page Numbers Tab**: Add page numbers with position control and batch options
- **🔗 Merge PDFs Tab**: Merge files with drag-and-drop reordering
- **📝 PDF to Word Tab**: Convert with multiple methods and batch processing
- **📊 Analysis Tab**: Comprehensive PDF analysis with formatted results

### GUI Benefits
- **No command-line knowledge required**
- **Real-time progress monitoring**
- **Settings preview before processing**
- **Professional error handling**
- **Batch processing with visual feedback**

For detailed GUI documentation, see [GUI_README.md](GUI_README.md).

## 📊 Examples

Check the `examples/` folder for detailed usage examples:

```bash
# Run examples
cd examples
python example_usage.py
python batch_paging_example.py
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- Uses [pdf2docx](https://github.com/dothinking/pdf2docx) for PDF to Word conversion
- GUI built with tkinter for cross-platform compatibility
- Inspired by the need for efficient PDF processing tools

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/oscar2song/pdf-processor/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/oscar2song/pdf-processor/issues)
- **Documentation**: [Wiki](https://github.com/oscar2song/pdf-processor/wiki)
- **GUI Issues**: Please include screenshots and system information

## 📈 Roadmap

- [x] **GUI interface with tkinter** ✅ **COMPLETED**
- [ ] Docker containerization
- [ ] OCR integration for scanned PDFs
- [ ] PDF form processing
- [ ] Digital signature support
- [ ] Cloud storage integration (AWS S3, Google Drive)
- [ ] Web interface option
- [ ] Mobile app version
- [ ] Plugin system for extensions

## 🎯 Use Cases

**Perfect for:**
- **Document management** - Organize and optimize PDF collections
- **Office workflows** - Batch process business documents
- **Academic research** - Prepare papers and references
- **Legal documents** - Merge and number legal filings
- **Publishing** - Optimize documents for web/print
- **Archives** - Compress old documents for storage

---

**Made with ❤️ by [Oscar Song](https://github.com/oscar2song)**

⭐ **If this project helped you, please give it a star!** ⭐

---

## 🚀 Quick Links

- [📖 Full Documentation](https://github.com/oscar2song/pdf-processor/wiki)
- [🎨 GUI Guide](GUI_README.md)
- [📊 Examples](examples/)
- [🐛 Report Issues](https://github.com/oscar2song/pdf-processor/issues)
- [💡 Feature Requests](https://github.com/oscar2song/pdf-processor/issues)
