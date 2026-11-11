import argparse
import shutil
from pathlib import Path


CSS_PATH = Path(__file__).resolve().with_name("styles.css")

# MathJax script to enable LaTeX rendering in HTML
mathjax_script = """
<script type="text/javascript" async
    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
"""


def md_to_pdf(md_file, pdf_file, config):
    import markdown2
    import pdfkit

    html_content = markdown2.markdown(md_file.read_text(encoding="utf-8"), extras=["fenced-code-blocks"])
    full_html = f"<!DOCTYPE html><html><head>{mathjax_script}</head><body>{html_content}</body></html>"
    pdfkit.from_string(full_html, str(pdf_file), configuration=config, css=str(CSS_PATH))


def markdown_files(folder_path):
    return [path for path in folder_path.iterdir() if path.suffix == ".md" and path.is_file()]


def convert_and_merge_md_files(folder_path, output_pdf, wkhtmltopdf):
    import pdfkit
    from PyPDF2 import PdfMerger

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)
    pdf_files = []
    for md_path in markdown_files(folder_path):
        pdf_path = md_path.with_suffix(".pdf")
        md_to_pdf(md_path, pdf_path, config)
        pdf_files.append(pdf_path)

    merger = PdfMerger()
    try:
        for pdf_file in pdf_files:
            merger.append(str(pdf_file))
        merger.write(str(output_pdf))
    finally:
        merger.close()

    print(f"Merged PDF created at: {output_pdf}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert a folder of Markdown files into a merged PDF.")
    parser.add_argument("input_dir", type=Path, help="directory containing Markdown files")
    parser.add_argument("output_pdf", type=Path, help="path to the merged PDF")
    parser.add_argument("--wkhtmltopdf", type=Path, metavar="PATH", help="executable path (default: look on PATH)")
    args = parser.parse_args(argv)
    input_dir = args.input_dir.expanduser()
    output_pdf = args.output_pdf.expanduser()

    if not input_dir.is_dir():
        parser.error(f"input directory does not exist: {input_dir}")
    if not output_pdf.parent.is_dir():
        parser.error(f"output directory does not exist: {output_pdf.parent}")
    if output_pdf.is_dir():
        parser.error(f"output path is a directory: {output_pdf}")

    output_target = output_pdf.resolve()
    for md_path in markdown_files(input_dir):
        if output_target in (md_path.resolve(), md_path.with_suffix(".pdf").resolve()):
            parser.error(f"output path would overwrite an input or intermediate file: {output_pdf}")

    if args.wkhtmltopdf is None:
        executable = shutil.which("wkhtmltopdf")
        if executable is None:
            parser.error("wkhtmltopdf was not found on PATH. Install it or use --wkhtmltopdf PATH.")
    else:
        executable_path = args.wkhtmltopdf.expanduser().resolve()
        executable = shutil.which(str(executable_path))
        if executable is None:
            parser.error(f"wkhtmltopdf is not executable: {executable_path}")

    convert_and_merge_md_files(input_dir, output_pdf, str(Path(executable).resolve()))


if __name__ == "__main__":
    main()
