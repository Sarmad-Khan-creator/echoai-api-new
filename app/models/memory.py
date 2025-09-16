"""
Pydantic models for enhanced memory-aware conversational context.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class MemoryType(str, Enum):
    """Types of memory storage."""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    USER_PROFILE = "user_profile"
    CONTEXTUAL_FACTS = "contextual_facts"
    TOPIC_HISTORY = "topic_history"


class ConversationSummaryModel(BaseModel):
    """Model for conversation summary."""
    conversation_id: str = Field(..., description="Conversation ID")
    summary_text: str = Field(..., description="Summary of conversation segment")
    key_topics: List[str] = Field(default_factory=list, description="Key topics discussed")
    user_goals: List[str] = Field(default_factory=list, description="Identified user goals")
    sentiment_trend: str = Field(..., description="Overall sentiment trend")
    message_count: int = Field(..., description="Number of messages in segment", ge=0)
    start_time: datetime = Field(..., description="Start time of conversation segment")
    end_time: datetime = Field(..., description="End time of conversation segment")
    importance_score: float = Field(..., description="Importance score of the segment", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "summary_text": "User inquired about pricing plans and discussed integration requirements",
                "key_topics": ["pricing", "integration", "features"],
                "user_goals": ["evaluate_solution", "understand_pricing"],
                "sentiment_trend": "positive",
                "message_count": 8,
                "start_time": "2024-01-15T10:00:00Z",
                "end_time": "2024-01-15T10:15:00Z",
                "importance_score": 0.8
            }
        }


class UserProfileModel(BaseModel):
    """Model for user profile built from conversation history."""
    user_id: str = Field(..., description="User ID")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences")
    communication_style: str = Field(..., description="User's communication style")
    technical_level: str = Field(..., description="User's technical expertise level")
    common_questions: List[str] = Field(default_factory=list, description="Frequently asked questions")
    satisfaction_history: List[float] = Field(default_factory=list, description="Historical satisfaction scores")
    interaction_patterns: Dict[str, Any] = Field(default_factory=dict, description="User interaction patterns")
    last_updated: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user_456",
                "preferences": {
                    "communication_style": "detailed",
                    "preferred_topics": ["technical", "integration"]
                },
                "communication_style": "polite",
                "technical_level": "advanced",
                "common_questions": [
                    "How does the API work?",
                    "What are the pricing options?"
                ],
                "satisfaction_history": [0.8, 0.9, 0.7, 0.85],
                "interaction_patterns": {
                    "preferred_hours": {"14": 5, "15": 3, "16": 2},
                    "session_length": "medium"
                },
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }


class ContextualFactModel(BaseModel):
    """Model for contextual facts extracted from conversations."""
    fact_id: str = Field(..., description="Unique fact identifier")
    conversation_id: str = Field(..., description="Conversation ID where fact was extracted")
    fact_text: str = Field(..., description="The extracted fact text")
    fact_type: str = Field(..., description="Type of fact (preference, requirement, constraint, goal)")
    confidence_score: float = Field(..., description="Confidence in fact extraction", ge=0.0, le=1.0)
    extracted_at: datetime = Field(..., description="When the fact was extracted")
    relevance_score: float = Field(..., description="Relevance score for retrieval", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "fact_id": "conv_123_abc123",
                "conversation_id": "conv_123",
                "fact_text": "User prefers detailed technical documentation",
                "fact_type": "preference",
                "confidence_score": 0.85,
                "extracted_at": "2024-01-15T10:30:00Z",
                "relevance_score": 0.9
            }
        }


class TopicTransitionModel(BaseModel):
    """Model for topic transition tracking."""
    from_topic: Optional[str] = Field(None, description="Previous topic")
    to_topic: str = Field(..., description="Current topic")
    transition_time: datetime = Field(..., description="When the transition occurred")
    transition_type: str = Field(..., description="Type of transition (natural, abrupt, clarification)")
    context_maintained: bool = Field(..., description="Whether context was maintained across transition")
    
    class Config:
        schema_extra = {
            "example": {
                "from_topic": "pricing",
                "to_topic": "features",
                "transition_time": "2024-01-15T10:30:00Z",
                "transition_type": "natural",
                "context_maintained": True
            }
        }


class ConversationMemoryModel(BaseModel):
    """Comprehensive conversation memory model."""
    conversation_id: str = Field(..., description="Conversation ID")
    short_term_memory: List[Dict[str, Any]] = Field(default_factory=list, description="Recent messages")
    long_term_memory: List[ConversationSummaryModel] = Field(default_factory=list, description="Conversation summaries")
    user_profile: Optional[UserProfileModel] = Field(None, description="User profile data")
    contextual_facts: List[ContextualFactModel] = Field(default_factory=list, description="Extracted contextual facts")
    topic_history: List[TopicTransitionModel] = Field(default_factory=list, description="Topic transition history")
    last_updated: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "short_term_memory": [
                    {
                        "role": "user",
                        "content": "What are your pricing plans?",
                        "timestamp": "2024-01-15T10:30:00Z",
                        "metadata": {}
                    }
                ],
                "long_term_memory": [],
                "user_profile": {
                    "user_id": "user_456",
                    "communication_style": "polite",
                    "technical_level": "intermediate"
                },
                "contextual_facts": [],
                "topic_history": [],
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }


class MemoryRetrievalRequest(BaseModel):
    """Request model for memory retrieval."""
    conversation_id: str = Field(..., description="Conversation ID")
    user_id: str = Field(..., description="User ID")
    current_message: str = Field(..., description="Current user message")
    max_items: int = Field(5, description="Maximum number of items to retrieve", ge=1, le=20)
    memory_types: List[MemoryType] = Field(
        default_factory=lambda: [MemoryType.SHORT_TERM, MemoryType.CONTEXTUAL_FACTS],
        description="Types of memory to retrieve"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "user_id": "user_456",
                "current_message": "Can you tell me more about the integration process?",
                "max_items": 5,
                "memory_types": ["short_term", "contextual_facts"]
            }
        }


class MemoryRetrievalResponse(BaseModel):
    """Response model for memory retrieval."""
    recent_context: List[Dict[str, Any]] = Field(default_factory=list, description="Recent conversation context")
    relevant_facts: List[ContextualFactModel] = Field(default_factory=list, description="Relevant contextual facts")
    relevant_summaries: List[ConversationSummaryModel] = Field(default_factory=list, description="Relevant conversation summaries")
    user_profile: Optional[UserProfileModel] = Field(None, description="User profile data")
    current_topic: str = Field(..., description="Detected current topic")
    topic_history: List[TopicTransitionModel] = Field(default_factory=list, description="Recent topic transitions")
    context_quality_score: float = Field(..., description="Quality score of retrieved context", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "recent_context": [
                    {
                        "role": "user",
                        "content": "What are your pricing plans?",
                        "timestamp": "2024-01-15T10:30:00Z"
                    }
                ],
                "relevant_facts": [],
                "relevant_summaries": [],
                "user_profile": {
                    "user_id": "user_456",
                    "communication_style": "polite",
                    "technical_level": "intermediate"
                },
                "current_topic": "integration",
                "topic_history": [],
                "context_quality_score": 0.85
            }
        }


class MemoryUpdateRequest(BaseModel):
    """Request model for memory updates."""
    conversation_id: str = Field(..., description="Conversation ID")
    user_id: str = Field(..., description="User ID")
    user_message: Dict[str, Any] = Field(..., description="User message data")
    ai_response: Dict[str, Any] = Field(..., description="AI response data")
    
    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "user_id": "user_456",
                "user_message": {
                    "content": "What are your pricing plans?",
                    "metadata": {"sentiment": "neutral"}
                },
                "ai_response": {
                    "content": "We offer three pricing tiers...",
                    "metadata": {"confidence": 0.9}
                }
            }
        }


class MemoryUpdateResponse(BaseModel):
    """Response model for memory updates."""
    success: bool = Field(..., description="Whether the update was successful")
    memory_summary: Dict[str, Any] = Field(..., description="Summary of updated memory state")
    new_facts_extracted: int = Field(..., description="Number of new facts extracted", ge=0)
    topic_transitions: int = Field(..., description="Number of topic transitions detected", ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "memory_summary": {
                    "short_term_messages": 4,
                    "total_facts": 2,
                    "current_topic": "pricing"
                },
                "new_facts_extracted": 1,
                "topic_transitions": 1
            }
        }


class ConversationContextRequest(BaseModel):
    """Request model for getting formatted conversation context."""
    conversation_id: str = Field(..., description="Conversation ID")
    user_id: str = Field(..., description="User ID")
    current_message: str = Field(..., description="Current user message")
    include_user_profile: bool = Field(True, description="Whether to include user profile in context")
    include_facts: bool = Field(True, description="Whether to include contextual facts")
    include_summaries: bool = Field(True, description="Whether to include conversation summaries")
    max_context_length: int = Field(2000, description="Maximum context length in characters", ge=100, le=5000)
    
    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "user_id": "user_456",
                "current_message": "Can you explain the integration process?",
                "include_user_profile": True,
                "include_facts": True,
                "include_summaries": True,
                "max_context_length": 2000
            }
        }


class ConversationContextResponse(BaseModel):
    """Response model for formatted conversation context."""
    formatted_context: str = Field(..., description="Formatted context for LLM consumption")
    context_components: Dict[str, Any] = Field(..., description="Breakdown of context components")
    context_length: int = Field(..., description="Total context length in characters", ge=0)
    truncated: bool = Field(..., description="Whether context was truncated due to length limits")
    
    class Config:
        schema_extra = {
            "example": {
                "formatted_context": "User Profile: Communication style: polite, Technical level: intermediate\n\nRecent Conversation:\nUser: What are your pricing plans?\nAssistant: We offer three pricing tiers...",
                "context_components": {
                    "user_profile": True,
                    "recent_messages": 2,
                    "facts": 1,
                    "summaries": 0
                },
                "context_length": 245,
                "truncated": False
            }
        }


class MemoryServiceStatus(BaseModel):
    """Model for memory service status information."""
    service_ready: bool = Field(..., description="Whether the service is ready")
    redis_connected: bool = Field(..., description="Whether Redis is connected")
    supabase_connected: bool = Field(..., description="Whether Supabase is connected")
    memory_window_size: int = Field(..., description="Current memory window size")
    summary_threshold: int = Field(..., description="Conversation summary threshold")
    profile_retention_days: int = Field(..., description="User profile retention period in days")
    
    class Config:
        schema_extra = {
            "example": {
                "service_ready": True,
                "redis_connected": True,
                "supabase_connected": True,
                "memory_window_size": 20,
                "summary_threshold": 50,
                "profile_retention_days": 30
            }
        }