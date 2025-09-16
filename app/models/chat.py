"""
Pydantic models for chat endpoints and RAG service.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
import uuid


class ChatRequest(BaseModel):
    """Request model for chat endpoint with proper validation."""
    message: str = Field(..., description="User's chat message", min_length=1, max_length=2000)
    user_id: Optional[str] = Field(None, description="User ID (will be overridden by API key validation)")
    chatbot_id: Optional[str] = Field(None, description="Chatbot ID for multi-chatbot support")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    user_email: Optional[str] = Field(None, description="External user email for session management")
    session_id: Optional[str] = Field(None, description="Session ID for memory persistence")
    image_url: Optional[str] = Field(None, description="URL of uploaded image for analysis")
    
    @validator('message')
    def validate_message(cls, v):
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
    
    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        """Validate conversation ID format if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('Conversation ID cannot be empty if provided')
            return v.strip()
        return v
    
    @validator('user_email')
    def validate_user_email(cls, v):
        """Validate user email format if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('User email cannot be empty if provided')
            # Basic email validation
            if '@' not in v:
                raise ValueError('Invalid email format')
            return v.strip().lower()
        return v


class ChatRequestWithApiKey(BaseModel):
    """Request model for chat endpoint with API key authentication."""
    message: str = Field(..., description="User's chat message", min_length=1, max_length=2000)
    api_key: str = Field(..., description="User's API key for authentication", min_length=1)
    chatbot_id: Optional[str] = Field(None, description="Chatbot ID for widget requests")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    user_email: Optional[str] = Field(None, description="External user email for session management")
    session_id: Optional[str] = Field(None, description="Session ID for memory persistence")
    image_url: Optional[str] = Field(None, description="URL of uploaded image for analysis")
    
    @validator('message')
    def validate_message(cls, v):
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
    
    @validator('api_key')
    def validate_api_key(cls, v):
        """Validate API key format."""
        if not v or not v.strip():
            raise ValueError('API key cannot be empty')
        return v.strip()
    
    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        """Validate conversation ID format if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('Conversation ID cannot be empty if provided')
            return v.strip()
        return v
    
    @validator('user_email')
    def validate_user_email(cls, v):
        """Validate user email format if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('User email cannot be empty if provided')
            # Basic email validation
            if '@' not in v:
                raise ValueError('Invalid email format')
            return v.strip().lower()
        return v


class ChatResponse(BaseModel):
    """Response model for chat endpoint with AI response and metadata."""
    response: str = Field(..., description="AI-generated response")
    sentiment: str = Field(..., description="Detected sentiment of user message")
    sentiment_score: Optional[float] = Field(None, description="Sentiment score (-1.0 to 1.0)", ge=-1.0, le=1.0)
    sentiment_confidence: Optional[float] = Field(None, description="Sentiment confidence (0.0 to 1.0)", ge=0.0, le=1.0)
    triggers_detected: Optional[List[str]] = Field(None, description="Automation triggers detected")
    conversation_id: str = Field(..., description="Conversation ID for this exchange")
    session_id: Optional[str] = Field(None, description="Session ID for memory persistence")
    image_analysis: Optional[Dict[str, Any]] = Field(None, description="Image analysis results if image was uploaded")
    lead_analysis: Optional[Dict[str, Any]] = Field(None, description="Lead qualification analysis if qualified")
    context_used: bool = Field(..., description="Whether relevant context was found and used")
    sources_count: int = Field(..., description="Number of source documents used", ge=0)
    confidence_score: Optional[float] = Field(None, description="Confidence score of the response", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "response": "Based on your company's documentation, I can help you with that. Your product offers...",
                "sentiment": "neutral",
                "sentiment_score": 0.1,
                "sentiment_confidence": 0.7,
                "triggers_detected": [],
                "conversation_id": "conv_123e4567-e89b-12d3-a456-426614174000",
                "session_id": "sess_123e4567-e89b-12d3-a456-426614174000",
                "lead_analysis": {
                    "lead_qualified": True,
                    "lead_score": 0.75,
                    "priority": "high",
                    "lead_type": "demo_request"
                },
                "context_used": True,
                "sources_count": 3,
                "confidence_score": 0.85
            }
        }


class RetrievedDocument(BaseModel):
    """Model for documents retrieved during RAG process."""
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(..., description="Document metadata")
    similarity_score: float = Field(..., description="Similarity score", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "content": "Our company provides AI-powered customer support solutions...",
                "metadata": {
                    "source": "https://example.com/about",
                    "source_type": "url",
                    "document_id": "doc_123"
                },
                "similarity_score": 0.92
            }
        }


class RAGContext(BaseModel):
    """Model for RAG context information."""
    query_embedding_generated: bool = Field(..., description="Whether query embedding was successfully generated")
    documents_retrieved: int = Field(..., description="Number of documents retrieved", ge=0)
    context_length: int = Field(..., description="Total length of context used", ge=0)
    retrieval_time_ms: float = Field(..., description="Time taken for document retrieval in milliseconds", ge=0.0)
    generation_time_ms: float = Field(..., description="Time taken for response generation in milliseconds", ge=0.0)
    
    class Config:
        schema_extra = {
            "example": {
                "query_embedding_generated": True,
                "documents_retrieved": 3,
                "context_length": 2450,
                "retrieval_time_ms": 125.5,
                "generation_time_ms": 890.2
            }
        }


class ConversationMessage(BaseModel):
    """Model for conversation message storage."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Message ID")
    conversation_id: str = Field(..., description="Conversation ID")
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    sentiment: Optional[str] = Field(None, description="Sentiment analysis result")
    sentiment_score: Optional[float] = Field(None, description="Sentiment score (-1.0 to 1.0)", ge=-1.0, le=1.0)
    triggers_detected: Optional[List[str]] = Field(None, description="Automation triggers detected")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional message metadata")
    
    @validator('role')
    def validate_role(cls, v):
        """Validate message role."""
        if v not in ['user', 'assistant']:
            raise ValueError('Role must be either "user" or "assistant"')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "id": "msg_123e4567-e89b-12d3-a456-426614174000",
                "conversation_id": "conv_123e4567-e89b-12d3-a456-426614174000",
                "role": "user",
                "content": "What services does your company offer?",
                "sentiment": "neutral",
                "sentiment_score": 0.1,
                "triggers_detected": [],
                "metadata": {
                    "timestamp": "2024-01-15T10:30:00Z",
                    "sources_used": 3
                }
            }
        }


class StreamChatResponse(BaseModel):
    """Response model for streaming chat endpoint."""
    type: str = Field(..., description="Response type: 'token', 'metadata', or 'done'")
    content: Optional[str] = Field(None, description="Token content for streaming")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for metadata responses")
    sentiment: Optional[str] = Field(None, description="Sentiment for metadata responses")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata for the response")
    
    @validator('type')
    def validate_type(cls, v):
        """Validate response type."""
        if v not in ['token', 'metadata', 'done']:
            raise ValueError('Type must be "token", "metadata", or "done"')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "type": "token",
                "content": "Based on your documentation, ",
                "metadata": None
            }
        }


class StreamChatRequest(BaseModel):
    """Request model for streaming chat endpoint."""
    message: str = Field(..., description="User's chat message", min_length=1, max_length=2000)
    user_id: Optional[str] = Field(None, description="User ID (will be overridden by API key validation)")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    stream_metadata: bool = Field(True, description="Whether to include metadata in stream")
    
    @validator('message')
    def validate_message(cls, v):
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
    
    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        """Validate conversation ID format if provided."""
        if v is not None:
            if not v.strip():
                raise ValueError('Conversation ID cannot be empty if provided')
            return v.strip()
        return v