import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from src.parser import load_document
from src.extractor import extract_rfp_data
from src.validator import validate_and_report


SUPPORTED_EXTENSIONS = {".pdf", ".html", ".htm"}


def process_rfp(
    input_folder: Path,
    output_file: Path,
    client
):
    print(f"\n{'=' * 80}")
    print(f"Processing: {input_folder.name}")
    print(f"{'=' * 80}")

    files = sorted(
        file
        for file in input_folder.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not files:
        print(
            f"No PDF/HTML files found in {input_folder}"
        )
        return None

    print(f"Found {len(files)} documents.")

    all_documents = []

    for i, file in enumerate(files, start=1):

        print(
            f"[{i}/{len(files)}] Parsing: {file.name}"
        )

        text = load_document(str(file))

        all_documents.append(
            f"""
================ DOCUMENT: {file.name} ================

{text}

================ END DOCUMENT: {file.name} ================
"""
        )

    combined_text = "\n\n".join(all_documents)

    print(
        "[Extraction] Extracting structured data via Gemini..."
    )

    extracted_data = extract_rfp_data(
        combined_text,
        client
    )

    print(
        "[Validation] Validating extracted data..."
    )

    validation_passed = validate_and_report(
        extracted_data
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"[Saving] Saving output to: {output_file}"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            extracted_data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Completed: {input_folder.name}"
    )

    return {
        "data": extracted_data,
        "validation_passed": validation_passed
    }


def main():
    load_dotenv()

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. "
            "Make sure your .env file contains your Gemini API key."
        )

    client = genai.Client(
        api_key=api_key
    )

    input_root = Path(
        "data/input"
    )

    output_root = Path(
        "data/output"
    )

    if not input_root.exists():
        raise FileNotFoundError(
            f"Input directory not found: {input_root}"
        )

    output_root.mkdir(
        parents=True,
        exist_ok=True
    )

    # Find all bid folders such as Bid1, Bid2, Bid3...
    bid_folders = sorted(
        folder
        for folder in input_root.iterdir()
        if folder.is_dir()
    )

    if not bid_folders:
        raise FileNotFoundError(
            f"No bid folders found inside {input_root}"
        )

    print(
        f"Found {len(bid_folders)} bid(s)."
    )

    successful = 0

    all_bids = {}

    for bid_folder in bid_folders:

        output_file = (
            output_root
            / f"{bid_folder.name.lower()}.json"
        )

        try:

            result = process_rfp(
                bid_folder,
                output_file,
                client
            )

            if result is not None:

                successful += 1

                all_bids[
                    bid_folder.name
                ] = result["data"]

        except Exception as e:

            print(
                f"ERROR processing "
                f"{bid_folder.name}: {e}"
            )

    # ------------------------------------------------------------------
    # Create the single consolidated JSON deliverable.
    # ------------------------------------------------------------------

    combined_output_file = (
        output_root / "all_bids.json"
    )

    print(
        f"\n[Saving] Saving consolidated output to: "
        f"{combined_output_file}"
    )

    with open(
        combined_output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_bids,
            f,
            indent=2,
            ensure_ascii=False
        )

    # ------------------------------------------------------------------
    # Final processing summary.
    # ------------------------------------------------------------------

    print(
        f"\n{'=' * 80}"
    )

    print(
        "PROCESSING SUMMARY"
    )

    print(
        f"{'=' * 80}"
    )

    print(
        f"Total bids: {len(bid_folders)}"
    )

    print(
        f"Successful: {successful}"
    )

    print(
        f"Failed: {len(bid_folders) - successful}"
    )

    print(
        f"Output directory: {output_root}"
    )

    print(
        f"Final JSON deliverable: "
        f"{combined_output_file}"
    )


if __name__ == "__main__":
    main()