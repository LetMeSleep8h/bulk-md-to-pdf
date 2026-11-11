# Markdown to Merged PDF Converter

This Python script converts all Markdown (`.md`) files in a specified folder into PDF files and then merges them into a single PDF. This is especially useful for organizing notes, combining documentation, or preparing project reports.

## Features

- **Converts Markdown files to PDF**: Each `.md` file in the folder is converted to a PDF.
- **Merges PDFs**: Combines all individual PDFs into a single merged PDF file.
- Individual PDFs stay alongside their Markdown sources.

## Requirements

- Python 3.x
- Libraries:
  - `markdown2` - for converting Markdown to HTML.
  - `pdfkit` - for converting HTML to PDF.
  - `PyPDF2` - for merging PDF files.
- [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) - an external tool that `pdfkit` uses for HTML-to-PDF conversion.

## Installation

1. **Install the required Python libraries**:

    ```bash
    pip install markdown2 pdfkit PyPDF2
    ```

2. **Install wkhtmltopdf**:
   - Download `wkhtmltopdf` from the official website: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
   - Follow the installation instructions for your OS.

## Usage

Run the script with the input folder and the path to the merged PDF. Quote paths that contain spaces.

```bash
python main.py "path/to/Markdown notes" "path/to/merged output.pdf"
```

If `wkhtmltopdf` is outside your `PATH`, provide its executable path.

```bash
python main.py "path/to/Markdown notes" "path/to/merged output.pdf" --wkhtmltopdf "/path/to/wkhtmltopdf"
```

The output folder must exist. Individual PDFs stay in the input folder, so choose a merged filename that differs from them.

## Troubleshooting

- If the executable is unavailable, install `wkhtmltopdf`, add it to `PATH`, or supply its executable path with `--wkhtmltopdf`.
- **Permission Errors**:
  Check that you have the necessary permissions for the folder where PDFs are saved.

## Example

If your folder contains:
- `notes1.md`
- `notes2.md`
- `summary.md`

Passing this folder and `merged_output.pdf` as the two arguments creates a merged PDF containing the three documents.
