from pathlib import Path
from src.parser import load_document


input_dir = Path("data/input")

for file_path in input_dir.rglob("*"):

    if file_path.suffix.lower() not in [".pdf", ".html", ".htm"]:
        continue

    print("=" * 80)
    print(f"FILE: {file_path}")
    print("=" * 80)

    try:
        text = load_document(str(file_path))

        print(text[:5000])

        print("\n\nTOTAL CHARACTERS:", len(text))

    except Exception as e:
        print(f"ERROR: {e}")

    print("\n")