"""
Pydantic models for training instruction endpoints.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime


class InstructionType(str, Enum):
    """Types of training instructions."""
    BEHAVIOR = "behavior"
    KNOWLEDGE = "knowledge"
    TONE = "tone"
    ESCALATION = "escalation"


class TrainingInstructionCreate(BaseModel):
    """Request model for creating training instructions."""
    chatbot_id: str = Field(..., description="Chatbot ID for instruction association", min_length=1)
    type: InstructionType = Field(..., description="Type of instruction")
    title: str = Field(..., description="Title of the instruction", min_length=1, max_length=255)
    content: str = Field(..., description="Content of the instruction", min_length=1)
    priority: int = Field(1, description="Priority level (1-10, higher is more important)", ge=1, le=10)
    is_active: bool = Field(True, description="Whether the instruction is active")
    
    @validator('title')
    def validate_title(cls, v):
        """Validate title format."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('content')
    def validate_content(cls, v):
        """Validate content format."""
        if not v or not v.strip():
            raise ValueError('Content cannot be empty')
        return v.strip()
    
    @validator('chatbot_id')
    def validate_chatbot_id(cls, v):
        """Validate chatbot ID format."""
        if not v or not v.strip():
            raise ValueError('Chatbot ID cannot be empty')
        return v.strip()


class TrainingInstructionUpdate(BaseModel):
    """Request model for updating training instructions."""
    type: Optional[InstructionType] = Field(None, description="Type of instruction")
    title: Optional[str] = Field(None, description="Title of the instruction", min_length=1, max_length=255)
    content: Optional[str] = Field(None, description="Content of the instruction", min_length=1)
    priority: Optional[int] = Field(None, description="Priority level (1-10)", ge=1, le=10)
    is_active: Optional[bool] = Field(None, description="Whether the instruction is active")
    
    @validator('title')
    def validate_title(cls, v):
        """Validate title format."""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v
    
    @validator('content')
    def validate_content(cls, v):
        """Validate content format."""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Content cannot be empty')
        return v.strip() if v else v


class TrainingInstructionResponse(BaseModel):
    """Response model for training instructions."""
    id: str = Field(..., description="Unique identifier for the instruction")
    chatbot_id: str = Field(..., description="Chatbot ID")
    type: InstructionType = Field(..., description="Type of instruction")
    title: str = Field(..., description="Title of the instruction")
    content: str = Field(..., description="Content of the instruction")
    priority: int = Field(..., description="Priority level")
    is_active: bool = Field(..., description="Whether the instruction is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    # Optional debug fields for embedding information
    embedding: Optional[List[float]] = Field(None, description="Embedding vector (for debugging)")
    embedding_length: Optional[int] = Field(None, description="Length of embedding vector (for debugging)")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "cm123abc456def",
                "chatbot_id": "cm789xyz123abc",
                "type": "behavior",
                "title": "Customer Service Tone",
                "content": "Always respond in a friendly, professional manner. Use empathetic language and offer solutions.",
                "priority": 5,
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "embedding": None,
                "embedding_length": None
            }
        }


class InstructionListResponse(BaseModel):
    """Response model for listing training instructions."""
    instructions: List[TrainingInstructionResponse] = Field(..., description="List of training instructions")
    total_count: int = Field(..., description="Total number of instructions", ge=0)
    active_count: int = Field(..., description="Number of active instructions", ge=0)
    type_breakdown: Dict[str, int] = Field(..., description="Breakdown by instruction type")
    
    class Config:
        schema_extra = {
            "example": {
                "instructions": [
                    {
                        "id": "cm123abc456def",
                        "chatbot_id": "cm789xyz123abc",
                        "type": "behavior",
                        "title": "Customer Service Tone",
                        "content": "Always respond in a friendly, professional manner.",
                        "priority": 5,
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                ],
                "total_count": 1,
                "active_count": 1,
                "type_breakdown": {
                    "behavior": 1,
                    "knowledge": 0,
                    "tone": 0,
                    "escalation": 0
                }
            }
        }


class InstructionBulkImportRequest(BaseModel):
    """Request model for bulk importing instructions."""
    chatbot_id: str = Field(..., description="Chatbot ID for instruction association")
    instructions: List[TrainingInstructionCreate] = Field(..., description="List of instructions to import")
    replace_existing: bool = Field(False, description="Whether to replace existing instructions")
    
    @validator('instructions')
    def validate_instructions(cls, v):
        """Validate instructions list."""
        if not v or len(v) == 0:
            raise ValueError('At least one instruction must be provided')
        if len(v) > 100:  # Reasonable limit for bulk import
            raise ValueError('Cannot import more than 100 instructions at once')
        return v


class InstructionBulkImportResponse(BaseModel):
    """Response model for bulk import operations."""
    success: bool = Field(..., description="Whether the bulk import was successful")
    message: str = Field(..., description="Human-readable message about the operation")
    imported_count: int = Field(..., description="Number of instructions imported", ge=0)
    skipped_count: int = Field(..., description="Number of instructions skipped", ge=0)
    error_count: int = Field(..., description="Number of instructions that failed", ge=0)
    errors: List[str] = Field([], description="List of error messages for failed imports")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully imported 5 instructions",
                "imported_count": 5,
                "skipped_count": 0,
                "error_count": 0,
                "errors": []
            }
        }


class InstructionTestRequest(BaseModel):
    """Request model for testing instruction effectiveness."""
    instruction_id: str = Field(..., description="ID of the instruction to test")
    test_query: str = Field(..., description="Test query to evaluate against the instruction", min_length=1)
    
    @validator('test_query')
    def validate_test_query(cls, v):
        """Validate test query format."""
        if not v or not v.strip():
            raise ValueError('Test query cannot be empty')
        return v.strip()


class InstructionTestResponse(BaseModel):
    """Response model for instruction testing."""
    instruction_id: str = Field(..., description="ID of the tested instruction")
    test_query: str = Field(..., description="The test query used")
    relevance_score: float = Field(..., description="Relevance score (0.0 to 1.0)", ge=0.0, le=1.0)
    similarity_score: float = Field(..., description="Similarity score (0.0 to 1.0)", ge=0.0, le=1.0)
    would_be_retrieved: bool = Field(..., description="Whether this instruction would be retrieved for the query")
    explanation: str = Field(..., description="Explanation of the test results")
    
    class Config:
        schema_extra = {
            "example": {
                "instruction_id": "cm123abc456def",
                "test_query": "How should I handle angry customers?",
                "relevance_score": 0.85,
                "similarity_score": 0.78,
                "would_be_retrieved": True,
                "explanation": "This instruction is highly relevant for customer service scenarios involving frustrated customers."
            }
        }


class EnhancedTrainRequest(BaseModel):
    """Enhanced training request that includes both documents and instructions."""
    chatbot_id: str = Field(..., description="Chatbot ID for training association")
    documents: Optional[List[str]] = Field(None, description="List of document URLs to process")
    instructions: Optional[List[TrainingInstructionCreate]] = Field(None, description="List of custom instructions")
    replace_existing: bool = Field(False, description="Whether to replace existing training data")
    instruction_types: Optional[List[InstructionType]] = Field(None, description="Types of instructions to include")
    
    @validator('chatbot_id')
    def validate_chatbot_id(cls, v):
        """Validate chatbot ID format."""
        if not v or not v.strip():
            raise ValueError('Chatbot ID cannot be empty')
        return v.strip()
    
    def __init__(self, **data):
        super().__init__(**data)
        # Validate that at least one training source is provided
        if not self.documents and not self.instructions:
            raise ValueError('At least one document URL or instruction must be provided')


class EnhancedTrainResponse(BaseModel):
    """Response model for enhanced training operations."""
    success: bool = Field(..., description="Whether the training was successful")
    message: str = Field(..., description="Human-readable message about the operation")
    documents_processed: int = Field(..., description="Number of documents processed", ge=0)
    instructions_processed: int = Field(..., description="Number of instructions processed", ge=0)
    embeddings_generated: int = Field(..., description="Total embeddings generated", ge=0)
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds", ge=0.0)
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully processed 3 documents and 5 instructions",
                "documents_processed": 3,
                "instructions_processed": 5,
                "embeddings_generated": 8,
                "processing_time_ms": 2500.0
            }
        }