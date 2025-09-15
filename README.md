# File Compressor

A Python application with Tkinter GUI for compressing various file formats including PDFs, JPEGs, PNGs, HEIC files, and other image formats.

## Features

- **Multi-format Support**: Compress PDFs, JPEGs, PNGs, HEIC/HEIF, BMP, TIFF, and WebP files
- **User-friendly GUI**: Easy-to-use Tkinter interface with drag-and-drop-like file selection
- **Batch Processing**: Compress multiple files at once
- **Customizable Settings**: 
  - Adjustable image quality (10-100%)
  - PDF compression levels (Light, Medium, Heavy)
- **Progress Tracking**: Real-time progress bar and detailed logging
- **File Size Analysis**: Shows compression ratios and file size reduction

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sukantsondhi/Compressor.git
cd Compressor
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. For Linux users, ensure tkinter is installed:
```bash
sudo apt-get install python3-tk
```

## Usage

### Running the Application

```bash
python3 compressor.py
```

### Using the GUI

1. **Select Files**: Click "Select Files" to choose files for compression
2. **Choose Output Directory**: Select where compressed files will be saved
3. **Adjust Settings**: 
   - Set image quality using the slider (10-100%)
   - Choose PDF compression level (Light/Medium/Heavy)
4. **Compress**: Click "Compress Files" to start the compression process
5. **Monitor Progress**: Watch the progress bar and log messages for real-time updates

### Supported File Formats

- **Images**: JPEG, PNG, HEIC, HEIF, BMP, TIFF, WebP
- **Documents**: PDF

### Example

To test the application with sample files:

```bash
# Create test files
python3 create_test_files.py

# Test compression functionality
python3 test_compression.py

# Run the GUI application
python3 compressor.py
```

## How It Works

### Image Compression
- Uses PIL (Pillow) for image processing
- Supports quality adjustment for JPEG images
- Automatically handles format conversion (e.g., HEIC to JPEG)
- Preserves image orientation using EXIF data
- Handles transparency by converting to white background

### PDF Compression
- Uses PyPDF library for PDF processing
- Three compression levels:
  - **Light**: Basic content stream compression
  - **Medium**: Adds identical object compression
  - **Heavy**: Includes duplicate removal
- Maintains PDF structure and readability

## Requirements

- Python 3.6+
- tkinter (usually included with Python)
- Pillow >= 10.0.0
- PyPDF2 >= 3.0.0
- pypdf >= 4.0.0
- pillow-heif >= 0.16.0

## Project Structure

```
Compressor/
├── compressor.py          # Main application with GUI
├── requirements.txt       # Python dependencies
├── create_test_files.py   # Script to create test files
├── test_compression.py    # Unit tests for compression
├── test_files/           # Test input files
├── output/               # Compressed output files
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

1. **"No module named 'tkinter'"**:
   - On Linux: `sudo apt-get install python3-tk`
   - On macOS: tkinter should be included with Python
   - On Windows: tkinter is included with Python

2. **HEIC files not supported**:
   - Ensure `pillow-heif` is installed: `pip install pillow-heif`

3. **PDF compression not working**:
   - Check that the PDF file is not corrupted
   - Some PDFs may not compress significantly if already optimized

### Performance Tips

- For large files, compression may take several minutes
- Close other applications to free up memory during compression
- Use lower quality settings for smaller file sizes
- Heavy PDF compression works best on document-heavy PDFs