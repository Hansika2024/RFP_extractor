from pathlib import Path

from bs4 import BeautifulSoup
import pdfplumber


def parse_html(file_path: Path) -> str:
    """Extract clean, structured text from an HTML file."""

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:
        soup = BeautifulSoup(
            f.read(),
            "lxml"
        )

    # Remove irrelevant/non-content elements.
    # Header is intentionally preserved because it may contain
    # useful solicitation information.
    for tag_name in [
        "script",
        "style",
        "nav",
        "footer",
        "meta",
        "noscript"
    ]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Preserve structural separation between HTML elements.
    text = soup.get_text(
        separator="\n",
        strip=True
    )

    return text


def parse_pdf(file_path: Path) -> str:
    """Extract text and tables from a PDF page by page."""

    extracted_pages = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(
            pdf.pages,
            start=1
        ):

            page_content = [
                f"--- PAGE {page_number} ---"
            ]

            # Extract normal page text.
            text = page.extract_text()

            if text:
                page_content.append(text)

            # Extract tables when present.
            tables = page.extract_tables()

            for table_number, table in enumerate(
                tables,
                start=1
            ):

                if not table:
                    continue

                page_content.append(
                    f"\n--- TABLE {table_number} ---"
                )

                for row in table:
                    if row:
                        cleaned_row = [
                            str(cell).strip()
                            if cell
                            else ""
                            for cell in row
                        ]

                        page_content.append(
                            " | ".join(cleaned_row)
                        )

            extracted_pages.append(
                "\n".join(page_content)
            )

    return "\n\n".join(extracted_pages)


def load_document(file_path: str) -> str:
    """Load and parse an HTML or PDF document."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    suffix = path.suffix.lower()

    if suffix in [".html", ".htm"]:
        return parse_html(path)

    if suffix == ".pdf":
        return parse_pdf(path)

    raise ValueError(
        f"Unsupported file format: {suffix}. "
        "Only PDF and HTML are supported."
    )