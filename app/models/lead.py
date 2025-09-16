"""
Pydantic models for lead qualification and scoring.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime


class LeadPriority(str, Enum):
    """Lead priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class LeadType(str, Enum):
    """Types of leads based on detected intent."""
    DEMO_REQUEST = "demo_request"
    ENTERPRISE_INQUIRY = "enterprise_inquiry"
    BULK_ORDER = "bulk_order"
    PRICING_INQUIRY = "pricing_inquiry"
    SUPPORT_ESCALATION = "support_escalation"
    FEATURE_REQUEST = "feature_request"
    GENERAL_INQUIRY = "general_inquiry"


class ConversationContextRequest(BaseModel):
    """Request model for conversation context information."""
    message_count: int = Field(..., description="Number of messages in conversation", ge=0)
    conversation_length: int = Field(..., description="Total character length of conversation", ge=0)
    engagement_score: float = Field(0.5, description="Engagement score (0.0 to 1.0)", ge=0.0, le=1.0)
    sentiment_history: List[float] = Field(default_factory=list, description="List of sentiment scores")
    previous_intents: List[str] = Field(default_factory=list, description="Previously detected intents")
    
    @validator('sentiment_history')
    def validate_sentiment_history(cls, v):
        """Validate sentiment scores are in valid range."""
        for score in v:
            if not -1.0 <= score <= 1.0:
                raise ValueError('Sentiment scores must be between -1.0 and 1.0')
        return v


class LeadAnalysisRequest(BaseModel):
    """Request model for lead analysis."""
    message: str = Field(..., description="Message to analyze for lead potential", min_length=1, max_length=2000)
    conversation_context: Optional[ConversationContextRequest] = Field(None, description="Optional conversation context")
    
    @validator('message')
    def validate_message(cls, v):
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()


class LeadScoreResponse(BaseModel):
    """Response model for lead scoring results."""
    total_score: float = Field(..., description="Total lead score (0.0 to 1.0)", ge=0.0, le=1.0)
    priority: LeadPriority = Field(..., description="Lead priority level")
    lead_type: LeadType = Field(..., description="Type of lead detected")
    confidence: float = Field(..., description="Confidence in scoring (0.0 to 1.0)", ge=0.0, le=1.0)
    should_qualify: bool = Field(..., description="Whether lead should trigger qualification workflow")
    factors: Dict[str, float] = Field(..., description="Individual scoring factors")
    extracted_data: Dict[str, Any] = Field(..., description="Extracted contact and company data")
    crm_mapping: Dict[str, Any] = Field(..., description="CRM field mappings for lead creation")
    analyzed_at: str = Field(..., description="Analysis timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "total_score": 0.75,
                "priority": "high",
                "lead_type": "demo_request",
                "confidence": 0.82,
                "should_qualify": True,
                "factors": {
                    "intent_confidence": 0.9,
                    "keyword_density": 0.6,
                    "conversation_engagement": 0.7,
                    "urgency_indicators": 0.4,
                    "company_size": 0.8,
                    "decision_maker": 0.0,
                    "contact_completeness": 0.6
                },
                "extracted_data": {
                    "email": "john.doe@enterprise.com",
                    "name": "John Doe",
                    "company": "Enterprise Corp"
                },
                "crm_mapping": {
                    "lead_source": "chatbot",
                    "lead_score": 0.75,
                    "lead_priority": "high",
                    "demo_requested": True,
                    "follow_up_action": "schedule_demo"
                },
                "analyzed_at": "2024-01-15T10:30:00Z"
            }
        }


class LeadQualificationTrigger(BaseModel):
    """Model for lead qualification trigger events."""
    trigger_id: str = Field(..., description="Unique trigger identifier")
    lead_score: LeadScoreResponse = Field(..., description="Lead scoring results")
    conversation_id: str = Field(..., description="Associated conversation ID")
    user_email: Optional[str] = Field(None, description="User email if available")
    message_id: str = Field(..., description="Message that triggered qualification")
    trigger_type: str = Field("lead_qualification", description="Type of trigger")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional trigger metadata")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Trigger creation time")
    
    class Config:
        schema_extra = {
            "example": {
                "trigger_id": "trig_123e4567-e89b-12d3-a456-426614174000",
                "lead_score": {
                    "total_score": 0.75,
                    "priority": "high",
                    "lead_type": "demo_request"
                },
                "conversation_id": "conv_123e4567-e89b-12d3-a456-426614174000",
                "user_email": "prospect@company.com",
                "message_id": "msg_123e4567-e89b-12d3-a456-426614174000",
                "trigger_type": "lead_qualification",
                "metadata": {
                    "source": "chat_widget",
                    "chatbot_id": "bot_123"
                },
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class CRMLeadData(BaseModel):
    """Model for CRM lead creation data."""
    lead_source: str = Field("chatbot", description="Source of the lead")
    lead_score: float = Field(..., description="Lead score", ge=0.0, le=1.0)
    lead_priority: LeadPriority = Field(..., description="Lead priority level")
    lead_type: LeadType = Field(..., description="Type of lead")
    confidence: float = Field(..., description="Scoring confidence", ge=0.0, le=1.0)
    
    # Contact information
    email: Optional[str] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    name: Optional[str] = Field(None, description="Contact name")
    company: Optional[str] = Field(None, description="Company name")
    
    # Lead details
    original_message: str = Field(..., description="Original message that triggered lead", max_length=500)
    follow_up_action: Optional[str] = Field(None, description="Recommended follow-up action")
    qualification_date: str = Field(..., description="Date of qualification")
    
    # Flags for specific lead types
    demo_requested: bool = Field(False, description="Whether demo was requested")
    enterprise_inquiry: bool = Field(False, description="Whether this is an enterprise inquiry")
    bulk_order_inquiry: bool = Field(False, description="Whether this is a bulk order inquiry")
    
    # Scoring breakdown
    scoring_factors: Dict[str, float] = Field(..., description="Individual scoring factors")
    
    # Additional metadata
    conversation_id: str = Field(..., description="Associated conversation ID")
    chatbot_id: Optional[str] = Field(None, description="Chatbot that captured the lead")
    
    @validator('email')
    def validate_email(cls, v):
        """Validate email format if provided."""
        if v is not None and v.strip():
            if '@' not in v:
                raise ValueError('Invalid email format')
            return v.strip().lower()
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone format if provided."""
        if v is not None and v.strip():
            # Basic phone validation - remove non-digits and check length
            digits = ''.join(filter(str.isdigit, v))
            if len(digits) < 10:
                raise ValueError('Phone number must have at least 10 digits')
            return v.strip()
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "lead_source": "chatbot",
                "lead_score": 0.75,
                "lead_priority": "high",
                "lead_type": "demo_request",
                "confidence": 0.82,
                "email": "john.doe@enterprise.com",
                "name": "John Doe",
                "company": "Enterprise Corp",
                "original_message": "Hi, I'm interested in seeing a demo of your enterprise solution for our 500-person company.",
                "follow_up_action": "schedule_demo",
                "qualification_date": "2024-01-15T10:30:00Z",
                "demo_requested": True,
                "enterprise_inquiry": True,
                "bulk_order_inquiry": False,
                "scoring_factors": {
                    "intent_confidence": 0.9,
                    "keyword_density": 0.6,
                    "company_size": 0.8
                },
                "conversation_id": "conv_123e4567-e89b-12d3-a456-426614174000",
                "chatbot_id": "bot_123"
            }
        }


class LeadQualificationStats(BaseModel):
    """Model for lead qualification statistics."""
    total_leads_analyzed: int = Field(..., description="Total number of leads analyzed", ge=0)
    qualified_leads: int = Field(..., description="Number of qualified leads", ge=0)
    qualification_rate: float = Field(..., description="Qualification rate percentage", ge=0.0, le=100.0)
    average_score: float = Field(..., description="Average lead score", ge=0.0, le=1.0)
    priority_breakdown: Dict[str, int] = Field(..., description="Breakdown by priority level")
    type_breakdown: Dict[str, int] = Field(..., description="Breakdown by lead type")
    period_start: str = Field(..., description="Statistics period start date")
    period_end: str = Field(..., description="Statistics period end date")
    
    class Config:
        schema_extra = {
            "example": {
                "total_leads_analyzed": 150,
                "qualified_leads": 45,
                "qualification_rate": 30.0,
                "average_score": 0.42,
                "priority_breakdown": {
                    "urgent": 5,
                    "high": 15,
                    "medium": 20,
                    "low": 5
                },
                "type_breakdown": {
                    "demo_request": 20,
                    "enterprise_inquiry": 10,
                    "pricing_inquiry": 15
                },
                "period_start": "2024-01-01T00:00:00Z",
                "period_end": "2024-01-31T23:59:59Z"
            }
        }