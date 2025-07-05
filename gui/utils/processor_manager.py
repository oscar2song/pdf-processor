"""
Processor Manager for PDF Processor GUI
=======================================

Manages PDF processing operations and threading.
"""

import threading
import queue
from tkinter import messagebox
from typing import Dict, Any, Optional, Callable


class ProcessorManager:
    """
    Manages PDF processing operations and threading
    """

    def __init__(self, processor):
        self.processor = processor
        self.result_queue = queue.Queue()
        self.current_operation = None
        self.progress_bar = None
        self.log_area = None
        self.status_bar = None

        # Callbacks for result handling
        self.result_handlers = {
            'optimization': self.handle_optimization_result,
            'pagination': self.handle_pagination_result,
            'merging': self.handle_merging_result,
            'conversion': self.handle_conversion_result,
            'analysis': self.handle_analysis_result
        }

    def set_progress_bar(self, progress_bar):
        """Set progress bar reference"""
        self.progress_bar = progress_bar

    def set_log_area(self, log_area):
        """Set log area reference"""
        self.log_area = log_area

    def set_status_bar(self, status_bar):
        """Set status bar reference"""
        self.status_bar = status_bar

    def is_processing(self):
        """Check if currently processing"""
        return self.current_operation is not None

    def start_monitoring(self, root):
        """Start monitoring processing results"""
        self.root = root
        self.monitor_results()

    def monitor_results(self):
        """Monitor processing results"""
        try:
            while True:
                result = self.result_queue.get_nowait()
                self.handle_result(result)
        except queue.Empty:
            pass

        # Schedule next check
        self.root.after(100, self.monitor_results)

    def handle_result(self, result):
        """Handle processing result"""
        operation = result.get('operation')
        success = result.get('success', False)
        message = result.get('message', '')
        data = result.get('data', {})

        # Call specific handler
        if operation in self.result_handlers:
            self.result_handlers[operation](success, message, data)

        # Update UI
        self.stop_operation()

        if success:
            self.update_status("Operation completed successfully")
            messagebox.showinfo("Success", message)
        else:
            self.update_status("Operation failed")
            messagebox.showerror("Error", message)

    def start_operation(self, operation_name, operation_func, *args):
        """Start a processing operation"""
        if self.is_processing():
            messagebox.showwarning("Operation in Progress",
                                   "Another operation is currently running. Please wait for it to complete.")
            return False

        self.current_operation = operation_name
        self.start_progress()
        self.update_status(f"Starting {operation_name}...")
        self.log_message(f"Starting {operation_name}")

        # Start processing in separate thread
        thread = threading.Thread(target=operation_func, args=args)
        thread.daemon = True
        thread.start()

        return True

    def stop_operation(self):
        """Stop current operation"""
        self.current_operation = None
        self.stop_progress()

    def start_progress(self):
        """Start progress bar"""
        if self.progress_bar:
            self.progress_bar.start()

    def stop_progress(self):
        """Stop progress bar"""
        if self.progress_bar:
            self.progress_bar.stop()

    def update_status(self, message):
        """Update status bar"""
        if self.status_bar:
            self.status_bar.update_status(message)

    def log_message(self, message):
        """Log a message"""
        if self.log_area:
            self.log_area.log_message(message)

    def put_result(self, result):
        """Put result in queue"""
        self.result_queue.put(result)

    # ==================================================
    # PROCESSING FUNCTIONS
    # ==================================================

    def process_optimization(self, settings):
        """Process optimization in separate thread"""
        try:
            input_path = settings['input_path']
            output_path = settings['output_path']

            if input_path and output_path:
                import os
                if os.path.isfile(input_path):
                    # Single file optimization
                    success = self.processor.optimize_pdf(
                        input_path,
                        output_path,
                        target_dpi=settings['target_dpi'],
                        jpeg_quality=settings['jpeg_quality']
                    )

                    if success:
                        message = f"Successfully optimized PDF: {os.path.basename(input_path)}"
                        data = {'files_processed': 1}
                    else:
                        message = "Failed to optimize PDF"
                        data = {}
                else:
                    # Batch optimization
                    stats = self.processor.batch_optimize_pdfs(
                        input_path,
                        output_path,
                        optimization_type=settings['optimization_type'],
                        target_dpi=settings['target_dpi'],
                        jpeg_quality=settings['jpeg_quality'],
                        max_file_size_mb=settings['max_file_size_mb']
                    )

                    success = stats['processed'] > 0
                    if success:
                        reduction = ((stats['total_original_size'] - stats['total_final_size']) / stats[
                            'total_original_size']) * 100 if stats['total_original_size'] > 0 else 0
                        message = f"Successfully optimized {stats['processed']} files\nSize reduction: {reduction:.1f}%\nSpace saved: {stats['total_original_size'] - stats['total_final_size']:.2f} MB"
                        data = stats
                    else:
                        message = "No files were optimized"
                        data = stats

                self.put_result({
                    'operation': 'optimization',
                    'success': success,
                    'message': message,
                    'data': data
                })
            else:
                self.put_result({
                    'operation': 'optimization',
                    'success': False,
                    'message': "Invalid input or output path",
                    'data': {}
                })

        except Exception as e:
            self.put_result({
                'operation': 'optimization',
                'success': False,
                'message': f"Error during optimization: {str(e)}",
                'data': {}
            })

    def process_pagination(self, settings):
        """Process pagination in separate thread"""
        try:
            input_path = settings['input_path']
            output_path = settings['output_path']

            import os
            if os.path.isfile(input_path):
                # Single file pagination
                success = self.processor.add_page_numbers(
                    input_path,
                    output_path,
                    position=settings['position'],
                    start_page=settings['start_page'],
                    font_size=settings['font_size'],
                    margin=settings['margin'],
                    preserve_signatures=settings['preserve_signatures']
                )

                if success:
                    message = f"Successfully added page numbers to: {os.path.basename(input_path)}"
                    data = {'files_processed': 1}
                else:
                    message = "Failed to add page numbers"
                    data = {}
            else:
                # Batch pagination
                stats = self.processor.batch_add_page_numbers(
                    input_path,
                    output_path,
                    position=settings['position'],
                    start_page=settings['start_page'],
                    font_size=settings['font_size'],
                    margin=settings['margin'],
                    preserve_signatures=settings['preserve_signatures'],
                    continuous_numbering=settings['continuous_numbering']
                )

                success = stats['processed'] > 0
                if success:
                    message = f"Successfully added page numbers to {stats['processed']} files\nTotal pages numbered: {stats['total_pages']}"
                    data = stats
                else:
                    message = "No files were processed"
                    data = stats

            self.put_result({
                'operation': 'pagination',
                'success': success,
                'message': message,
                'data': data
            })

        except Exception as e:
            self.put_result({
                'operation': 'pagination',
                'success': False,
                'message': f"Error during page numbering: {str(e)}",
                'data': {}
            })

    def process_merging(self, settings):
        """Process merging in separate thread"""
        try:
            if settings['method'] == "folder":
                # Merge folder
                success = self.processor.merge_folder_pdfs(
                    settings['input_path'],
                    settings['output_path'],
                    add_page_numbers=settings['add_page_numbers'],
                    preserve_signatures=settings['preserve_signatures']
                )
            else:
                # Merge specific files
                success = self.processor.merge_specific_files(
                    settings['files'],
                    settings['output_path'],
                    add_page_numbers=settings['add_page_numbers'],
                    preserve_signatures=settings['preserve_signatures']
                )

            if success:
                import os
                message = f"Successfully merged PDFs to: {os.path.basename(settings['output_path'])}"
                data = {'output_file': settings['output_path']}
            else:
                message = "Failed to merge PDFs"
                data = {}

            self.put_result({
                'operation': 'merging',
                'success': success,
                'message': message,
                'data': data
            })

        except Exception as e:
            self.put_result({
                'operation': 'merging',
                'success': False,
                'message': f"Error during merging: {str(e)}",
                'data': {}
            })

    def process_conversion(self, settings):
        """Process conversion in separate thread"""
        try:
            input_path = settings['input_path']
            output_path = settings['output_path']

            import os
            if os.path.isfile(input_path):
                # Single file conversion
                success = self.processor.pdf_to_word(
                    input_path,
                    output_path,
                    method=settings['method']
                )

                if success:
                    message = f"Successfully converted: {os.path.basename(input_path)}"
                    data = {'files_processed': 1}
                else:
                    message = "Failed to convert PDF"
                    data = {}
            else:
                # Batch conversion
                stats = self.processor.batch_pdf_to_word(
                    input_path,
                    output_path,
                    method=settings['method']
                )

                success = stats['processed'] > 0
                if success:
                    message = f"Successfully converted {stats['processed']} files"
                    data = stats
                else:
                    message = "No files were converted"
                    data = stats

            self.put_result({
                'operation': 'conversion',
                'success': success,
                'message': message,
                'data': data
            })

        except Exception as e:
            self.put_result({
                'operation': 'conversion',
                'success': False,
                'message': f"Error during conversion: {str(e)}",
                'data': {}
            })

    def process_analysis(self, input_path):
        """Process analysis in separate thread"""
        try:
            results = self.processor.analyze_pdf(input_path)

            if 'error' not in results:
                import os
                success = True
                message = f"Successfully analyzed: {os.path.basename(input_path)}"
                data = results
            else:
                success = False
                message = f"Failed to analyze PDF: {results['error']}"
                data = {}

            self.put_result({
                'operation': 'analysis',
                'success': success,
                'message': message,
                'data': data
            })

        except Exception as e:
            self.put_result({
                'operation': 'analysis',
                'success': False,
                'message': f"Error during analysis: {str(e)}",
                'data': {}
            })

    # ==================================================
    # RESULT HANDLERS
    # ==================================================

    def handle_optimization_result(self, success, message, data):
        """Handle optimization result"""
        self.log_message(f"Optimization completed: {message}")

        if success and data:
            if 'files_processed' in data:
                self.log_message(f"Files processed: {data['files_processed']}")
            if 'total_original_size' in data:
                self.log_message(f"Original size: {data['total_original_size']:.2f} MB")
                self.log_message(f"Final size: {data['total_final_size']:.2f} MB")
                reduction = ((data['total_original_size'] - data['total_final_size']) / data[
                    'total_original_size']) * 100
                self.log_message(f"Size reduction: {reduction:.1f}%")

    def handle_pagination_result(self, success, message, data):
        """Handle pagination result"""
        self.log_message(f"Page numbering completed: {message}")

        if success and data:
            if 'files_processed' in data:
                self.log_message(f"Files processed: {data['files_processed']}")
            if 'total_pages' in data:
                self.log_message(f"Total pages numbered: {data['total_pages']}")

    def handle_merging_result(self, success, message, data):
        """Handle merging result"""
        self.log_message(f"Merging completed: {message}")

        if success and data:
            if 'output_file' in data:
                self.log_message(f"Output file: {data['output_file']}")

    def handle_conversion_result(self, success, message, data):
        """Handle conversion result"""
        self.log_message(f"Conversion completed: {message}")

        if success and data:
            if 'files_processed' in data:
                self.log_message(f"Files processed: {data['files_processed']}")
            elif 'processed' in data:
                self.log_message(f"Files processed: {data['processed']}")

    def handle_analysis_result(self, success, message, data):
        """Handle analysis result"""
        self.log_message(f"Analysis completed: {message}")

        if success and data:
            # Analysis results are handled by the analysis tab directly
            pass
