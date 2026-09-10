"""
Pydantic Schemas for Document Extraction Pipeline (Assignment 5)
Supports 3 document types: Tax Invoices, Medical Insurance Claims, Government IDs
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
import re

class LineItem(BaseModel):
    description: str
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)
    total_amount: float = Field(ge=0)

class InvoiceSchema(BaseModel):
    doc_type: str = "INVOICE"
    invoice_number: str = Field(..., min_length=2)
    invoice_date: str = Field(..., description="YYYY-MM-DD")
    vendor_name: str = Field(..., min_length=2)
    tax_id: Optional[str] = None
    subtotal: float = Field(ge=0)
    tax_amount: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    line_items: List[LineItem] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0)

    @field_validator("invoice_date")
    def validate_date(cls, v):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("Invoice date must follow YYYY-MM-DD format")
        return v

    @field_validator("total_amount")
    def validate_arithmetic(cls, v, values):
        sub = values.data.get("subtotal", 0.0)
        tax = values.data.get("tax_amount", 0.0)
        if abs((sub + tax) - v) > 0.10:
            raise ValueError(f"Total amount {v} does not equal subtotal {sub} + tax {tax}")
        return v

class InsuranceClaimSchema(BaseModel):
    doc_type: str = "INSURANCE_CLAIM"
    claim_id: str = Field(..., min_length=4)
    patient_name: str = Field(..., min_length=2)
    policy_number: str = Field(..., min_length=5)
    incident_date: str = Field(..., description="YYYY-MM-DD")
    diagnosis_code: str = Field(..., description="ICD-10 code format")
    claimed_amount: float = Field(gt=0)
    provider_name: str = Field(..., min_length=2)
    confidence_score: float = Field(ge=0.0, le=1.0)

class IdentityDocumentSchema(BaseModel):
    doc_type: str = "GOVERNMENT_ID"
    document_id: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    date_of_birth: str = Field(..., description="YYYY-MM-DD")
    expiry_date: str = Field(..., description="YYYY-MM-DD")
    country_code: str = Field(..., min_length=2, max_length=3)
    confidence_score: float = Field(ge=0.0, le=1.0)
