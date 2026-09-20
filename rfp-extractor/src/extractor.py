from google import genai

from src.schema import RFPExtractionSchema


def extract_rfp_data(
    document_text: str,
    client: genai.Client
) -> dict:
    """Extract structured RFP information from a complete bid package."""

    system_prompt = """
You are an expert procurement analysis assistant.

Extract accurate, factual information from the COMPLETE RFP BID PACKAGE
according to the provided schema.

Rules:

1. Use information from ALL provided documents.

2. Do not invent information.

3. If a field is not mentioned or cannot be determined, return null.

4. For additional_documentation_required, return an empty list if none
   is identified.

5. Preserve dates, times, numbers, percentages, model numbers, part numbers,
   and contractual terms accurately.

6. When multiple documents contain different values for the same field,
   prefer the latest addendum or amendment.

7. Addenda modify or clarify the original RFP and therefore take precedence
   over earlier information when there is a conflict.

8. If the original RFP and an addendum contain different submission
   deadlines, use the deadline from the latest applicable addendum.

9. Do not confuse a quote-request date, award date, evaluation date,
   advertisement date, or question deadline with the proposal submission
   due date.

10. For term_of_bid, extract the actual contract duration and renewal period,
    not purchasing or ordering timelines.

11. For pre_bid_meeting, include the meeting date/time and method when available.

12. For contact_info, extract the relevant procurement/buyer contact information.

13. For bid_number, prefer an explicitly labeled "Solicitation Number".
    If no Solicitation Number is provided, use the RFP, RFQ, or PORFP number
    that identifies the procurement. Do not combine multiple identifiers
    such as eMMA project numbers, sourcing numbers, or master contract numbers.

14. For delivery_date, return only an actual specified delivery date or
    delivery timeframe. Do not use a quote-request date, award date, or
    purchasing start date as the delivery date. If the document only says
    delivery will be agreed upon later, return null.

15. For term_of_bid, extract the duration of the resulting contract,
    agreement, or procurement term. Do not use a product warranty period,
    extended warranty, maintenance period, or service warranty as the bid term.
    If the contract duration is not specified, return null.

16. For mfg_for_registration, only extract a manufacturer when the documents
    explicitly state that manufacturer registration, registration with the
    manufacturer, or a manufacturer is required for registration. Do not copy
    the general product manufacturer into this field merely because the
    manufacturer name is provided.

17. Extract each field according to its specific meaning. Do not place
    information in a field merely because it is related to that field.
"""

    prompt = f"""
{system_prompt}

Extract the required information from the following COMPLETE BID PACKAGE.

================ DOCUMENT TEXT ================

{document_text}

================ END DOCUMENT TEXT ================
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": RFPExtractionSchema.model_json_schema(),
        },
    )

    extracted_data = RFPExtractionSchema.model_validate_json(
        interaction.output_text
    )

    return extracted_data.model_dump()