# Receipt Information Extractor (OCR & Computer Vision)

This project provides an automated system for extracting key information from physical receipts using computer vision and Optical Character Recognition (OCR) techniques.

## Project Structure

```
├── README.md
├── notebook/
│   └── document_scanner_ocr.ipynb
├── src/
│   ├── transform.py
│   ├── ocr_parser.py
│   └── scan.py
├── sample_data/
│   ├── raw/
│   └── processed/
└── requirements.txt
```

## Setup

1.  Clone this repository.
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  Install Tesseract OCR engine (e.g., `sudo apt install tesseract-ocr` on Debian/Ubuntu).

## Usage

To run the document scanner and OCR on an image:

```bash
python src/scan.py --image sample_data/raw/receipt.jpg
```

## Features & Technologies

*   **Document Preprocessing:** Edge detection, contour finding, four-point perspective transformation.
*   **Adaptive Thresholding:** Enhances text clarity for OCR.
*   **OCR Integration:** Uses Tesseract via `pytesseract` with configurable Page Segmentation Modes (`--psm`).
*   **Information Parsing:** Extracts 'Vendor Name', 'Transaction Date', 'Total Amount', and 'Tax' using regular expressions.