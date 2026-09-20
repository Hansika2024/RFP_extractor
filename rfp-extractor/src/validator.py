from typing import Any, Dict, List

from src.schema import RFPExtractionSchema


def validate_rfp_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate extracted RFP data without modifying it.

    Returns:
        A list of validation warnings/errors.
        An empty list means no validation issues were found.
    """

    issues = []

    # Validate against the reference Pydantic schema.
    try:
        validated_data = RFPExtractionSchema.model_validate(data)
    except Exception as e:
        issues.append(f"Schema validation failed: {e}")
        return issues

    data = validated_data.model_dump()

    # Check important identification fields.
    if not data.get("bid_number"):
        issues.append("Missing bid_number.")

    if not data.get("title"):
        issues.append("Missing title.")

    if not data.get("company_name"):
        issues.append("Missing company_name.")

    # Check submission deadline.
    if not data.get("due_date"):
        issues.append("Missing due_date.")

    # Check list field.
    documentation = data.get(
        "additional_documentation_required"
    )

    if documentation is None:
        issues.append(
            "additional_documentation_required should be an empty list "
            "when no documentation is identified."
        )

    elif not isinstance(documentation, list):
        issues.append(
            "additional_documentation_required must be a list."
        )

    else:
        for item in documentation:
            if not isinstance(item, str):
                issues.append(
                    "Every item in additional_documentation_required "
                    "must be a string."
                )

    # Check fields that should contain text.
    string_fields = [
        "bid_number",
        "title",
        "due_date",
        "bid_submission_type",
        "term_of_bid",
        "pre_bid_meeting",
        "installation",
        "bid_bond_requirement",
        "delivery_date",
        "payment_terms",
        "mfg_for_registration",
        "contract_or_cooperative_to_use",
        "model_no",
        "part_no",
        "product",
        "contact_info",
        "company_name",
        "bid_summary",
        "product_specification",
    ]

    for field in string_fields:
        value = data.get(field)

        if value is not None and not isinstance(value, str):
            issues.append(
                f"{field} should be a string or null."
            )

    # Detect empty strings.
    for field in string_fields:
        value = data.get(field)

        if isinstance(value, str) and not value.strip():
            issues.append(
                f"{field} is an empty string; use null if information "
                f"is not available."
            )

    return issues


def validate_and_report(data: Dict[str, Any]) -> bool:
    """
    Validate extracted RFP data and print a human-readable report.

    Returns:
        True if validation passes without issues.
        False if issues are detected.
    """

    issues = validate_rfp_data(data)

    if not issues:
        print("[Validation] PASSED")
        return True

    print("[Validation] WARNINGS/ERRORS FOUND:")

    for issue in issues:
        print(f"  - {issue}")

    return False