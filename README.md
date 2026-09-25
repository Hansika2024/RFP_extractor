# Automated RFP Information Extraction with LLMs

## Overview

This project extracts structured information from **PDF and HTML RFP documents** and converts the information into standardized JSON.

The pipeline processes all documents belonging to each bid, uses **Gemini** for semantic information extraction, validates the output against a predefined **Pydantic schema**, and generates a consolidated JSON file.

## Architecture

```text
PDF / HTML Documents
        ↓
Document Parsing
(pdfplumber / BeautifulSoup)
        ↓
Text Extraction
        ↓
Combine Documents per Bid
        ↓
Gemini LLM Extraction
        ↓
Pydantic Schema Validation
        ↓
Structured JSON
        ↓
all_bids.json
```

## Features

* Supports **PDF and HTML** documents.
* Extracts information from multiple documents belonging to the same bid.
* Uses an LLM to map unstructured/semi-structured content to predefined fields.
* Handles **RFP addenda**, giving later addenda precedence when information conflicts.
* Validates extracted data using Pydantic.
* Generates both per-bid JSON files and a consolidated `all_bids.json`.
* Does not require a vector database or RAG for the current fixed-field extraction task.

## Extracted Fields

The system extracts:

* Bid Number
* Title
* Due Date
* Bid Submission Type
* Term of Bid
* Pre Bid Meeting
* Installation
* Bid Bond Requirement
* Delivery Date
* Payment Terms
* Any Additional Documentation Required
* MFG for Registration
* Contract or Cooperative to Use
* Model_no
* Part_no
* Product
* Contact_info
* Company_name
* Bid Summary
* Product Specification

## Project Structure

```text
rfp-extractor/
├── src/
│   ├── parser.py
│   ├── extractor.py
│   ├── schema.py
│   ├── validator.py
│   └── __init__.py
├── data/
│   └── output/
│       └── all_bids.json
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies

* Python
* Gemini API (`google-genai`)
* Pydantic
* pdfplumber
* BeautifulSoup
* lxml
* python-dotenv

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to version control.

## Input Structure

Place documents inside separate bid folders:

```text
data/
└── input/
    ├── Bid1/
    │   ├── document1.pdf
    │   ├── document2.pdf
    │   └── document3.html
    │
    └── Bid2/
        ├── document1.pdf
        ├── document2.pdf
        └── document3.html
```

All PDF and HTML files within a bid folder are treated as part of the same bid package.

## Run

From the project root:

```bash
python main.py
```

The program parses the documents, extracts the structured information, validates the result, and saves the outputs.

## Output

The generated files are:

```text
data/output/
├── bid1.json
├── bid2.json
└── all_bids.json
```

`all_bids.json` is the **consolidated JSON deliverable** containing the extracted information for all processed bids.

## Design Choice

The current solution uses direct document parsing followed by LLM-based structured extraction rather than RAG or a vector database.

This is appropriate because the assignment requires extraction of a fixed set of fields from a relatively small number of complete bid packages. All documents belonging to a bid can therefore be provided to the extraction model together.

For larger document collections, the architecture can be extended with chunking, retrieval/RAG, or other scalable processing techniques.

## Validation

Pydantic validation ensures that the extracted response conforms to the required schema and that fields have the expected data types.

The pipeline also checks important fields such as:

* Bid number
* Title
* Company name
* Due date
* Additional documentation format

## Limitations

* Image-only or scanned PDFs may require OCR.
* Very large document packages may require chunking or retrieval.
* LLM-extracted information should be reviewed for high-stakes procurement decisions.
