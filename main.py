"""PDF Merger & Splitter using pypdf."""

from pathlib import Path
from pypdf import PdfReader, PdfWriter


def merge_pdfs():
    paths_text = input("Enter PDF file paths separated by commas: ").strip()
    paths = [Path(p.strip().strip('"')) for p in paths_text.split(",") if p.strip()]

    if len(paths) < 2:
        print("Please provide at least two PDF files.")
        return

    writer = PdfWriter()
    for path in paths:
        if not path.is_file() or path.suffix.lower() != ".pdf":
            print(f"Invalid PDF file: {path}")
            return
        try:
            reader = PdfReader(str(path))
            if reader.is_encrypted:
                print(f"Encrypted PDFs are not supported: {path.name}")
                return
            for page in reader.pages:
                writer.add_page(page)
        except Exception as error:
            print(f"Could not read {path.name}: {error}")
            return

    output_text = input("Enter output PDF name (default: merged.pdf): ").strip()
    output = Path(output_text or "merged.pdf")
    if output.suffix.lower() != ".pdf":
        output = output.with_suffix(".pdf")

    try:
        with output.open("wb") as file:
            writer.write(file)
        print(f"Successfully merged {len(paths)} files into: {output.resolve()}")
    except OSError as error:
        print(f"Could not save merged PDF: {error}")


def split_pdf():
    source = Path(input("Enter source PDF path: ").strip().strip('"'))
    if not source.is_file() or source.suffix.lower() != ".pdf":
        print("Please provide a valid PDF file.")
        return

    try:
        reader = PdfReader(str(source))
        if reader.is_encrypted:
            print("Encrypted PDFs are not supported.")
            return
        total_pages = len(reader.pages)
        print(f"PDF contains {total_pages} page(s).")
        page_text = input(f"Enter page number to extract (1-{total_pages}): ").strip()
        page_number = int(page_text)
        if not 1 <= page_number <= total_pages:
            print("Page number is out of range.")
            return

        writer = PdfWriter()
        writer.add_page(reader.pages[page_number - 1])
        output_text = input("Enter output PDF name (default: extracted_page.pdf): ").strip()
        output = Path(output_text or "extracted_page.pdf")
        if output.suffix.lower() != ".pdf":
            output = output.with_suffix(".pdf")

        with output.open("wb") as file:
            writer.write(file)
        print(f"Successfully extracted page {page_number} to: {output.resolve()}")
    except ValueError:
        print("Please enter a valid whole page number.")
    except Exception as error:
        print(f"Could not split PDF: {error}")


def main():
    while True:
        print("\n========== PDF MERGER & SPLITTER ==========")
        print("1. Merge PDF files")
        print("2. Extract one page from a PDF")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            merge_pdfs()
        elif choice == "2":
            split_pdf()
        elif choice == "3":
            print("Thank you for using PDF Merger & Splitter!")
            break
        else:
            print("Invalid choice. Please select 1, 2 or 3.")


if __name__ == "__main__":
    main()
