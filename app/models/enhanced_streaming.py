"""
Enhanced streaming models for intelligent chatbot responses.
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum

from app.models.decision import ProactiveAction, ConversationIntelligence


class StreamResponseType(str, Enum):
    """Types of streaming response chunks."""
    TOKEN = "token"
    METADATA = "metadata"
    PROACTIVE_QUESTION = "proactive_question"
    SUGGESTED_TOPIC = "suggested_topic"
    CONVERSATION_ACTION = "conversation_action"
    INTELLIGENCE_METADATA = "intelligence_metadata"
    FALLBACK_STRATEGY = "fallback_strategy"
    ERROR = "error"
    DONE = "done"


class FallbackStrategy(BaseModel):
    """Model for fallback response strategies when knowledge gaps exist."""
    strategy_type: str = Field(..., description="Type of fallback strategy")
    content: str = Field(..., description="Fallback content to display")
    reasoning: str = Field(..., description="Why this fallback was chosen")
    alternative_suggestions: List[str] = Field(default_factory=list, description="Alternative suggestions")
    escalation_offered: bool = Field(default=False, description="Whether escalation was offered")
    
    class Config:
        schema_extra = {
            "example": {
                "strategy_type": "related_information",
                "content": "While I don't have specific information about that topic, I can help you with related areas like...",
                "reasoning": "No direct match found, providing related context",
                "alternative_suggestions": ["Check our documentation", "Contact support"],
                "escalation_offered": True
            }
        }


class EnhancedStreamResponse(BaseModel):
    """Enhanced streaming response model with intelligent features."""
    type: StreamResponseType = Field(..., description="Type of streaming chunk")
    content: Optional[str] = Field(None, description="Content for token streaming")
    proactive_question: Optional[str] = Field(None, description="Proactive follow-up question")
    suggested_topic: Optional[str] = Field(None, description="Suggested conversation topic")
    conversation_action: Optional[ProactiveAction] = Field(None, description="Conversation action recommendation")
    intelligence_metadata: Optional[ConversationIntelligence] = Field(None, description="Intelligence analysis")
    fallback_strategy: Optional[FallbackStrategy] = Field(None, description="Fallback strategy for knowledge gaps")
    error_message: Optional[str] = Field(None, description="Error message if type is error")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    # Remove the validator for now to avoid field ordering issues
    # The validation will be handled at the service level instead
    
    class Config:
        schema_extra = {
            "example": {
                "type": "token",
                "content": "Based on your requirements, ",
                "metadata": {
                    "token_index": 5,
                    "confidence": 0.85
                }
            }
        }


class EnhancedStreamRequest(BaseModel):
    """Enhanced streaming request model."""
    message: str = Field(..., description="User's chat message", min_length=1, max_length=2000)
    user_id: Optional[str] = Field(None, description="User ID (will be overridden by API key validation)")
    chatbot_id: Optional[str] = Field(None, description="Chatbot ID for multi-chatbot support")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    user_email: Optional[str] = Field(None, description="External user email for session management")
    session_id: Optional[str] = Field(None, description="Session ID for memory persistence")
    image_url: Optional[str] = Field(None, description="URL of uploaded image for analysis")
    
    # Enhanced streaming options
    enable_proactive_questions: bool = Field(default=True, description="Enable proactive question streaming")
    enable_topic_suggestions: bool = Field(default=True, description="Enable topic suggestion streaming")
    enable_conversation_actions: bool = Field(default=True, description="Enable conversation action streaming")
    enable_intelligence_metadata: bool = Field(default=True, description="Enable intelligence metadata streaming")
    enable_fallback_strategies: bool = Field(default=True, description="Enable fallback strategy streaming")
    avoid_i_dont_know: bool = Field(default=True, description="Avoid 'I don't know' responses")
    
    @validator('message')
    def validate_message(cls, v):
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What are your pricing plans?",
                "conversation_id": "conv_123",
                "enable_proactive_questions": True,
                "enable_topic_suggestions": True,
                "enable_conversation_actions": True,
                "avoid_i_dont_know": True
            }
        }


class EnhancedStreamRequestWithApiKey(BaseModel):
    """Enhanced streaming request model with API key authentication."""
    message: str = Field(..., description="User's chat message", min_length=1, max_length=2000)
    api_key: str = Field(..., description="User's API key for authentication", min_length=1)
    chatbot_id: Optional[str] = Field(None, description="Chatbot ID for widget requests")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    user_email: Optional[str] = Field(None, description="External user email for session management")
    session_id: Optional[str] = Field(None, description="Session ID for memory persistence")
    image_url: Optional[str] = Field(None, description="URL of uploaded image for analysis")
    
    # Enhanced streaming options
    enable_proactive_questions: bool = Field(default=True, description="Enable proactive question streaming")
    enable_topic_suggestions: bool = Field(default=True, description="Enable topic suggestion streaming")
    enable_conversation_actions: bool = Field(default=True, description="Enable conversation action streaming")
    enable_intelligence_metadata: bool = Field(default=True, description="Enable intelligence metadata streaming")
    enable_fallback_strategies: bool = Field(default=True, description="Enable fallback strategy streaming")
    avoid_i_dont_know: bool = Field(default=True, description="Avoid 'I don't know' responses")
    
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
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What are your pricing plans?",
                "api_key": "sk-1234567890abcdef",
                "conversation_id": "conv_123",
                "enable_proactive_questions": True,
                "enable_topic_suggestions": True,
                "avoid_i_dont_know": True
            }
        }


class StreamingConfig(BaseModel):
    """Configuration for streaming behavior."""
    chunk_size: int = Field(default=1, description="Number of tokens per chunk", ge=1, le=10)
    delay_ms: int = Field(default=50, description="Delay between chunks in milliseconds", ge=0, le=1000)
    include_metadata: bool = Field(default=True, description="Include metadata in stream")
    enable_typing_indicator: bool = Field(default=True, description="Enable typing indicator")
    max_response_tokens: int = Field(default=2000, description="Maximum tokens in response", ge=100, le=4000)
    
    class Config:
        schema_extra = {
            "example": {
                "chunk_size": 1,
                "delay_ms": 50,
                "include_metadata": True,
                "enable_typing_indicator": True,
                "max_response_tokens": 2000
            }
        }