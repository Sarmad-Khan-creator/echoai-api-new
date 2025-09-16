"""
Pydantic models for document ingestion endpoints.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class IngestRequest(BaseModel):
    """Request model for document ingestion with proper validation."""
    user_id: str = Field(..., description="User ID for document association", min_length=1)
    urls: Optional[List[str]] = Field(None, description="List of URLs to process")
    
    @validator('urls')
    def validate_urls(cls, v):
        """Validate URL format."""
        if v is not None:
            if not isinstance(v, list):
                raise ValueError('URLs must be a list')
            if len(v) == 0:
                raise ValueError('URLs list cannot be empty if provided')
            for url in v:
                if not isinstance(url, str) or not url.strip():
                    raise ValueError('Each URL must be a non-empty string')
                # Basic URL validation
                if not (url.startswith('http://') or url.startswith('https://')):
                    raise ValueError(f'Invalid URL format: {url}')
        return v
    
    @validator('user_id')
    def validate_user_id(cls, v):
        """Validate user ID format."""
        if not v or not v.strip():
            raise ValueError('User ID cannot be empty')
        return v.strip()


class IngestResponse(BaseModel):
    """Response model for document ingestion with detailed information."""
    success: bool = Field(..., description="Whether the ingestion was successful")
    message: str = Field(..., description="Human-readable message about the operation")
    documents_processed: int = Field(..., description="Number of source documents processed", ge=0)
    processing_stats: Optional[Dict[str, Any]] = Field(None, description="Detailed processing statistics")
    vector_storage_stats: Optional[Dict[str, Any]] = Field(None, description="Vector storage statistics")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully processed 3 documents into 15 chunks",
                "documents_processed": 3,
                "processing_stats": {
                    "total_documents": 3,
                    "total_chunks": 15,
                    "source_types": {"url": 1, "pdf": 1, "docx": 1},
                    "avg_chunk_size": 850
                },
                "vector_storage_stats": {
                    "total_documents": 15,
                    "unique_sources": 3,
                    "avg_content_length": 850.5
                }
            }
        }


class ProcessingStats(BaseModel):
    """Model for processing statistics."""
    total_documents: int = Field(..., description="Total number of source documents processed", ge=0)
    total_chunks: int = Field(..., description="Total number of text chunks created", ge=0)
    source_types: Dict[str, int] = Field(..., description="Breakdown of documents by source type")
    avg_chunk_size: int = Field(..., description="Average size of text chunks in characters", ge=0)
    chunk_size_config: int = Field(..., description="Configured chunk size", ge=0)
    chunk_overlap_config: int = Field(..., description="Configured chunk overlap", ge=0)


class VectorStorageStats(BaseModel):
    """Model for vector storage statistics."""
    total_documents: int = Field(..., description="Total documents in vector storage for user", ge=0)
    unique_sources: int = Field(..., description="Number of unique sources", ge=0)
    avg_content_length: float = Field(..., description="Average content length", ge=0.0)
    first_document: Optional[str] = Field(None, description="Timestamp of first document")
    last_document: Optional[str] = Field(None, description="Timestamp of last document")
    source_types: Dict[str, int] = Field(..., description="Breakdown by source type")