#!/usr/bin/env python3
"""
Test the compression functionality without GUI
"""

import os
import sys
from pathlib import Path

# Add the current directory to the path so we can import our compressor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our compressor class but we need to mock tkinter for testing
import unittest.mock

# Mock tkinter components for testing
with unittest.mock.patch('tkinter.Tk'), \
     unittest.mock.patch('tkinter.StringVar'), \
     unittest.mock.patch('tkinter.IntVar'):
    
    from compressor import FileCompressor

class TestCompressor:
    def __init__(self):
        # Mock the GUI components
        self.output_directory = unittest.mock.Mock()
        self.output_directory.get = lambda: "output"
        self.compression_quality = unittest.mock.Mock()
        self.compression_quality.get = lambda: 80
        self.pdf_compression_level = unittest.mock.Mock()
        self.pdf_compression_level.get = lambda: 2
        
    def log_message(self, message):
        print(f"LOG: {message}")
        
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
    
    def compress_pdf(self, input_path):
        """Compress PDF file"""
        try:
            output_path = os.path.join(
                self.output_directory.get(),
                f"compressed_{os.path.basename(input_path)}"
            )
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            import pypdf
            
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
            
            self.log_message(f"PDF Compression - Size reduction: {compression_ratio:.1f}% "
                           f"({self.format_file_size(original_size)} → {self.format_file_size(compressed_size)})")
            
            return True
            
        except Exception as e:
            self.log_message(f"PDF compression failed for {input_path}: {str(e)}")
            return False
            
    def compress_image(self, input_path):
        """Compress image file"""
        try:
            from PIL import Image, ImageOps
            
            output_filename = f"compressed_{os.path.basename(input_path)}"
            # Convert HEIC/HEIF to JPG for better compatibility
            if Path(input_path).suffix.lower() in ['.heic', '.heif']:
                output_filename = output_filename.replace('.heic', '.jpg').replace('.heif', '.jpg')
                
            output_path = os.path.join(self.output_directory.get(), output_filename)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Open and process image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary (for PNG with transparency, etc.)
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
            
            self.log_message(f"Image Compression - Size reduction: {compression_ratio:.1f}% "
                           f"({self.format_file_size(original_size)} → {self.format_file_size(compressed_size)})")
            
            return True
            
        except Exception as e:
            self.log_message(f"Image compression failed for {input_path}: {str(e)}")
            return False

def test_compression():
    """Test compression functionality"""
    print("Testing File Compression Functionality")
    print("=" * 40)
    
    compressor = TestCompressor()
    
    # Test files
    test_files = [
        "test_files/test_image.jpg",
        "test_files/test_image.png", 
        "test_files/test_document.pdf"
    ]
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\nTesting: {file_path}")
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.pdf':
                success = compressor.compress_pdf(file_path)
            elif file_ext in ['.jpg', '.jpeg', '.png', '.heic', '.heif', '.bmp', '.tiff', '.webp']:
                success = compressor.compress_image(file_path)
            else:
                print(f"Unsupported file type: {file_ext}")
                continue
                
            if success:
                print(f"✓ Successfully compressed {file_path}")
            else:
                print(f"✗ Failed to compress {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    print("\n" + "=" * 40)
    print("Compression test completed!")
    
    # List output files
    if os.path.exists("output"):
        output_files = os.listdir("output")
        if output_files:
            print(f"\nCompressed files created in 'output' directory:")
            for file in output_files:
                file_path = os.path.join("output", file)
                size = os.path.getsize(file_path)
                print(f"  - {file} ({compressor.format_file_size(size)})")
        else:
            print("\nNo compressed files were created.")

if __name__ == "__main__":
    test_compression()