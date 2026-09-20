from typing import Optional, List
from pydantic import BaseModel, Field


class RFPExtractionSchema(BaseModel):
    bid_number: Optional[str] = Field(
        None,
        description="Bid or RFP identification number"
    )
    title: Optional[str] = Field(
        None,
        description="Title of the bid or project"
    )
    due_date: Optional[str] = Field(
        None,
        description="Submission deadline date and time"
    )
    bid_submission_type: Optional[str] = Field(
        None,
        description="Method of submission, e.g., online portal, sealed envelope"
    )
    term_of_bid: Optional[str] = Field(
        None,
        description="Contract duration or term length"
    )
    pre_bid_meeting: Optional[str] = Field(
        None,
        description="Details regarding pre-bid conferences or meetings"
    )
    installation: Optional[str] = Field(
        None,
        description="Installation requirements or specifications"
    )
    bid_bond_requirement: Optional[str] = Field(
        None,
        description="Bond percentage or requirements"
    )
    delivery_date: Optional[str] = Field(
        None,
        description="Expected delivery date or timeframe"
    )
    payment_terms: Optional[str] = Field(
        None,
        description="Payment schedule or terms (e.g., Net 30)"
    )
    additional_documentation_required: Optional[List[str]] = Field(
        default_factory=list,
        description="List of required certificates, forms, or licenses"
    )
    mfg_for_registration: Optional[str] = Field(
        None,
        description="Required manufacturer for registration"
    )
    contract_or_cooperative_to_use: Optional[str] = Field(
        None,
        description="Cooperative contract vehicle to use"
    )
    model_no: Optional[str] = Field(
        None,
        description="Specified product model numbers"
    )
    part_no: Optional[str] = Field(
        None,
        description="Specified product part or SKU numbers"
    )
    product: Optional[str] = Field(
        None,
        description="Primary product or commodity name"
    )
    contact_info: Optional[str] = Field(
        None,
        description="Contact details of procurement officer"
    )
    company_name: Optional[str] = Field(
        None,
        description="Name of the issuing organization/agency"
    )
    bid_summary: Optional[str] = Field(
        None,
        description="High-level summary of the bid requirement"
    )
    product_specification: Optional[str] = Field(
        None,
        description="Key technical specifications or performance requirements"
    )