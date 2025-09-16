"""
Pydantic models for vision analysis endpoints and services.
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid


class AnalysisType(str, Enum):
    """Supported analysis types for vision API."""
    PRODUCT_CONDITION = "product_condition"
    INVOICE_EXTRACTION = "invoice_extraction"
    INVENTORY_COUNT = "inventory_count"
    CUSTOM = "custom"


class VisionAnalysisRequest(BaseModel):
    """Request model for vision analysis endpoint."""
    image_url: str = Field(..., description="URL of the image to analyze")
    analysis_type: AnalysisType = Field(..., description="Type of analysis to perform")
    custom_prompt: Optional[str] = Field(None, description="Custom prompt for analysis (required for custom type)")
    
    @validator('image_url')
    def validate_image_url(cls, v):
        """Validate image URL format."""
        if not v or not v.strip():
            raise ValueError('Image URL cannot be empty')
        # Basic URL validation
        if not (v.startswith('http://') or v.startswith('https://') or v.startswith('data:')):
            raise ValueError('Invalid image URL format')
        return v.strip()
    
    @validator('custom_prompt')
    def validate_custom_prompt(cls, v, values):
        """Validate custom prompt when analysis type is custom."""
        if values.get('analysis_type') == AnalysisType.CUSTOM:
            if not v or not v.strip():
                raise ValueError('Custom prompt is required for custom analysis type')
            return v.strip()
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "image_url": "https://example.com/product-image.jpg",
                "analysis_type": "product_condition",
                "custom_prompt": None
            }
        }


class ProductCondition(BaseModel):
    """Model for product condition analysis results."""
    condition: str = Field(..., description="Overall product condition (excellent, good, fair, poor)")
    condition_score: float = Field(..., description="Condition score from 0.0 to 1.0", ge=0.0, le=1.0)
    damage_detected: bool = Field(..., description="Whether damage was detected")
    damage_description: Optional[str] = Field(None, description="Description of any damage found")
    return_eligible: bool = Field(..., description="Whether the product is eligible for return")
    confidence: float = Field(..., description="Analysis confidence score", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "condition": "good",
                "condition_score": 0.8,
                "damage_detected": False,
                "damage_description": None,
                "return_eligible": True,
                "confidence": 0.92
            }
        }


class InvoiceData(BaseModel):
    """Model for invoice extraction results."""
    vendor_name: Optional[str] = Field(None, description="Vendor/supplier name")
    invoice_number: Optional[str] = Field(None, description="Invoice number")
    invoice_date: Optional[str] = Field(None, description="Invoice date")
    due_date: Optional[str] = Field(None, description="Payment due date")
    total_amount: Optional[float] = Field(None, description="Total invoice amount")
    currency: Optional[str] = Field(None, description="Currency code")
    line_items: List[Dict[str, Any]] = Field(default_factory=list, description="Invoice line items")
    confidence: float = Field(..., description="Extraction confidence score", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "vendor_name": "ACME Corp",
                "invoice_number": "INV-2024-001",
                "invoice_date": "2024-01-15",
                "due_date": "2024-02-15",
                "total_amount": 1250.00,
                "currency": "USD",
                "line_items": [
                    {"description": "Product A", "quantity": 2, "unit_price": 500.00, "total": 1000.00},
                    {"description": "Shipping", "quantity": 1, "unit_price": 250.00, "total": 250.00}
                ],
                "confidence": 0.95
            }
        }


class InventoryCount(BaseModel):
    """Model for inventory counting results."""
    total_items: int = Field(..., description="Total number of items counted", ge=0)
    item_categories: Dict[str, int] = Field(default_factory=dict, description="Items grouped by category")
    confidence: float = Field(..., description="Counting confidence score", ge=0.0, le=1.0)
    notes: Optional[str] = Field(None, description="Additional notes about the count")
    
    class Config:
        schema_extra = {
            "example": {
                "total_items": 45,
                "item_categories": {
                    "boxes": 30,
                    "pallets": 15
                },
                "confidence": 0.88,
                "notes": "Some items may be partially obscured"
            }
        }


class VisionAnalysisResponse(BaseModel):
    """Response model for vision analysis endpoint."""
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique analysis ID")
    analysis_type: AnalysisType = Field(..., description="Type of analysis performed")
    image_url: str = Field(..., description="URL of the analyzed image")
    result: Union[ProductCondition, InvoiceData, InventoryCount, Dict[str, Any]] = Field(..., description="Analysis results")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds", ge=0.0)
    created_at: str = Field(..., description="Analysis timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "analysis_id": "analysis_123e4567-e89b-12d3-a456-426614174000",
                "analysis_type": "product_condition",
                "image_url": "https://example.com/product-image.jpg",
                "result": {
                    "condition": "good",
                    "condition_score": 0.8,
                    "damage_detected": False,
                    "damage_description": None,
                    "return_eligible": True,
                    "confidence": 0.92
                },
                "processing_time_ms": 1250.5,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class ImageAnalysisRecord(BaseModel):
    """Model for storing image analysis results in database."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Analysis record ID")
    message_id: Optional[str] = Field(None, description="Associated message ID if from chat")
    image_url: str = Field(..., description="URL of the analyzed image")
    analysis_type: str = Field(..., description="Type of analysis performed")
    prompt: str = Field(..., description="Prompt used for analysis")
    analysis_result: Dict[str, Any] = Field(..., description="Structured analysis results")
    processing_time: int = Field(..., description="Processing time in milliseconds", ge=0)
    confidence_score: Optional[float] = Field(None, description="Overall confidence score", ge=0.0, le=1.0)
    created_at: str = Field(..., description="Analysis timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "img_analysis_123e4567-e89b-12d3-a456-426614174000",
                "message_id": "msg_123e4567-e89b-12d3-a456-426614174000",
                "image_url": "https://example.com/product-image.jpg",
                "analysis_type": "product_condition",
                "prompt": "Analyze this product image for condition and return eligibility...",
                "analysis_result": {
                    "condition": "good",
                    "condition_score": 0.8,
                    "damage_detected": False,
                    "return_eligible": True,
                    "confidence": 0.92
                },
                "processing_time": 1250,
                "confidence_score": 0.92,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class VisionError(BaseModel):
    """Model for vision analysis errors."""
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Error message")
    image_url: Optional[str] = Field(None, description="URL of the image that caused the error")
    
    class Config:
        schema_extra = {
            "example": {
                "error_type": "invalid_image",
                "error_message": "Unable to process image: unsupported format",
                "image_url": "https://example.com/invalid-image.txt"
            }
        }