#!/usr/bin/env python3
"""
File Compressor with Tkinter GUI
Supports compression of PDFs, JPGs, PNGs, HEIC and other image formats
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
import logging

# Import compression modules
from PIL import Image, ImageOps
import pypdf
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

class FileCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("File Compressor")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Variables
        self.selected_files = []
        self.output_directory = tk.StringVar()
        self.compression_quality = tk.IntVar(value=80)
        self.pdf_compression_level = tk.IntVar(value=1)
        
        # Setup logging
        self.setup_logging()
        
        # Create GUI
        self.create_widgets()
        
    def setup_logging(self):
        """Setup logging for the application"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="File Compressor", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Select Files", command=self.select_files).grid(row=0, column=0, padx=(0, 10))
        
        # File list
        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        ttk.Button(file_frame, text="Clear", command=self.clear_files).grid(row=0, column=3)
        
        # Output directory section
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Button(output_frame, text="Select Directory", command=self.select_output_directory).grid(row=0, column=0, padx=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_directory, state='readonly').grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Compression settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Compression Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Image compression quality
        ttk.Label(settings_frame, text="Image Quality:").grid(row=0, column=0, sticky=tk.W)
        quality_scale = ttk.Scale(settings_frame, from_=10, to=100, variable=self.compression_quality, orient=tk.HORIZONTAL)
        quality_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        ttk.Label(settings_frame, textvariable=self.compression_quality).grid(row=0, column=2)
        
        # PDF compression level
        ttk.Label(settings_frame, text="PDF Compression:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        pdf_frame = ttk.Frame(settings_frame)
        pdf_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Radiobutton(pdf_frame, text="Light", variable=self.pdf_compression_level, value=1).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(pdf_frame, text="Medium", variable=self.pdf_compression_level, value=2).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Radiobutton(pdf_frame, text="Heavy", variable=self.pdf_compression_level, value=3).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Compress button
        self.compress_button = ttk.Button(main_frame, text="Compress Files", command=self.start_compression)
        self.compress_button.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status text
        self.status_text = scrolledtext.ScrolledText(main_frame, height=8, width=80)
        self.status_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        main_frame.rowconfigure(6, weight=1)
        
    def select_files(self):
        """Open file dialog to select files for compression"""
        filetypes = [
            ('All supported', '*.pdf *.jpg *.jpeg *.png *.heic *.heif *.bmp *.tiff *.webp'),
            ('PDF files', '*.pdf'),
            ('Image files', '*.jpg *.jpeg *.png *.heic *.heif *.bmp *.tiff *.webp'),
            ('All files', '*.*')
        ]
        
        files = filedialog.askopenfilenames(
            title="Select files to compress",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files.extend(files)
            self.update_file_list()
            
    def clear_files(self):
        """Clear the selected files list"""
        self.selected_files.clear()
        self.update_file_list()
        
    def update_file_list(self):
        """Update the file listbox with selected files"""
        self.file_listbox.delete(0, tk.END)
        for file in self.selected_files:
            filename = os.path.basename(file)
            self.file_listbox.insert(tk.END, filename)
            
    def select_output_directory(self):
        """Select output directory for compressed files"""
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_directory.set(directory)
            
    def log_message(self, message):
        """Add message to status text widget"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_compression(self):
        """Start the compression process in a separate thread"""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files to compress.")
            return
            
        if not self.output_directory.get():
            messagebox.showwarning("No Output Directory", "Please select an output directory.")
            return
            
        # Disable compress button during compression
        self.compress_button.config(state='disabled')
        self.status_text.delete(1.0, tk.END)
        
        # Start compression in a separate thread
        thread = threading.Thread(target=self.compress_files)
        thread.daemon = True
        thread.start()
        
    def compress_files(self):
        """Main compression function"""
        total_files = len(self.selected_files)
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        self.log_message(f"Starting compression of {total_files} files...")
        
        compressed_count = 0
        failed_count = 0
        
        for i, file_path in enumerate(self.selected_files):
            try:
                filename = os.path.basename(file_path)
                self.log_message(f"Processing: {filename}")
                
                # Determine file type and compress accordingly
                file_ext = Path(file_path).suffix.lower()
                
                if file_ext == '.pdf':
                    success = self.compress_pdf(file_path)
                elif file_ext in ['.jpg', '.jpeg', '.png', '.heic', '.heif', '.bmp', '.tiff', '.webp']:
                    success = self.compress_image(file_path)
                else:
                    self.log_message(f"  Unsupported file type: {file_ext}")
                    failed_count += 1
                    continue
                    
                if success:
                    compressed_count += 1
                    self.log_message(f"  ✓ Compressed successfully")
                else:
                    failed_count += 1
                    self.log_message(f"  ✗ Compression failed")
                    
            except Exception as e:
                failed_count += 1
                self.log_message(f"  ✗ Error: {str(e)}")
                
            # Update progress
            self.progress['value'] = i + 1
            self.root.update_idletasks()
            
        # Show completion message
        self.log_message(f"\nCompression completed!")
        self.log_message(f"Successfully compressed: {compressed_count} files")
        self.log_message(f"Failed: {failed_count} files")
        
        # Re-enable compress button
        self.compress_button.config(state='normal')
        
        if compressed_count > 0:
            messagebox.showinfo("Compression Complete", 
                              f"Successfully compressed {compressed_count} files!\n"
                              f"Output directory: {self.output_directory.get()}")
        
    def compress_pdf(self, input_path):
        """Compress PDF file"""
        try:
            output_path = os.path.join(
                self.output_directory.get(),
                f"compressed_{os.path.basename(input_path)}"
            )
            
            with open(input_path, 'rb') as input_file:
                reader = pypdf.PdfReader(input_file)
                writer = pypdf.PdfWriter()
                
                # Copy pages and apply compression
                for page in reader.pages:
                    page.compress_content_streams()
                    writer.add_page(page)
                
                # Apply different compression levels based on setting
                if self.pdf_compression_level.get() >= 2:
                    writer.compress_identical_objects()
                    
                if self.pdf_compression_level.get() >= 3:
                    writer.remove_duplicates()
                
                # Write compressed PDF
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                    
            # Check if compression was effective
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            self.log_message(f"  Size reduction: {compression_ratio:.1f}% "
                           f"({self.format_file_size(original_size)} → {self.format_file_size(compressed_size)})")
            
            return True
            
        except Exception as e:
            self.logger.error(f"PDF compression failed for {input_path}: {str(e)}")
            return False
            
    def compress_image(self, input_path):
        """Compress image file"""
        try:
            output_filename = f"compressed_{os.path.basename(input_path)}"
            # Convert HEIC/HEIF to JPG for better compatibility
            if Path(input_path).suffix.lower() in ['.heic', '.heif']:
                output_filename = output_filename.replace('.heic', '.jpg').replace('.heif', '.jpg')
                
            output_path = os.path.join(self.output_directory.get(), output_filename)
            
            # Open and process image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary (for HEIC, PNG with transparency, etc.)
                if img.mode in ['RGBA', 'LA', 'P']:
                    # Create white background for transparent images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ['RGBA', 'LA'] else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Apply auto-orientation
                img = ImageOps.exif_transpose(img)
                
                # Determine output format and quality
                quality = self.compression_quality.get()
                
                # Save compressed image
                if output_filename.lower().endswith('.png'):
                    img.save(output_path, 'PNG', optimize=True)
                else:
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                    
            # Check compression results
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            self.log_message(f"  Size reduction: {compression_ratio:.1f}% "
                           f"({self.format_file_size(original_size)} → {self.format_file_size(compressed_size)})")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Image compression failed for {input_path}: {str(e)}")
            return False
            
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
            
        return f"{size_bytes:.1f} {size_names[i]}"

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = FileCompressor(root)
    root.mainloop()

if __name__ == "__main__":
    main()