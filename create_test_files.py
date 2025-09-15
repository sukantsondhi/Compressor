#!/usr/bin/env python3
"""
Test script for the file compressor functionality
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw
import pypdf
from pypdf import PdfWriter, PdfReader
from io import BytesIO
import tempfile

def create_test_image(filename, size=(800, 600), format='JPEG'):
    """Create a test image file"""
    img = Image.new('RGB', size, color='red')
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes to make the image more realistic
    draw.rectangle([50, 50, 750, 550], fill='blue', outline='white', width=5)
    draw.ellipse([200, 200, 600, 400], fill='green', outline='yellow', width=3)
    draw.text((300, 300), "Test Image", fill='white')
    
    img.save(filename, format=format, quality=90)
    print(f"Created test image: {filename} ({os.path.getsize(filename)} bytes)")

def create_test_pdf(filename):
    """Create a test PDF file"""
    # Create a simple PDF using pypdf
    writer = PdfWriter()
    
    # Add multiple pages to make it larger
    for i in range(5):
        page = writer.add_blank_page(width=612, height=792)
    
    with open(filename, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"Created simple test PDF: {filename} ({os.path.getsize(filename)} bytes)")

def test_compression():
    """Test the compression functionality"""
    # Create test files
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create test images
    create_test_image(os.path.join(test_dir, "test_image.jpg"), format='JPEG')
    create_test_image(os.path.join(test_dir, "test_image.png"), format='PNG')
    
    # Create test PDF
    create_test_pdf(os.path.join(test_dir, "test_document.pdf"))
    
    print("\nTest files created successfully!")
    print("You can now test the compressor application with these files.")

if __name__ == "__main__":
    test_compression()