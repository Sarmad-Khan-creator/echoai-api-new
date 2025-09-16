"""
Enhanced Pydantic models for sophisticated lead qualification and data collection.
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime


class CollectionStrategy(str, Enum):
    """Lead data collection strategies."""
    DIRECT = "direct"
    CONVERSATIONAL = "conversational"
    PROGRESSIVE = "progressive"


class QualificationStage(str, Enum):
    """Lead qualification stages."""
    INITIAL_INTEREST = "initial_interest"
    NEED_ASSESSMENT = "need_assessment"
    BUDGET_QUALIFICATION = "budget_qualification"
    AUTHORITY_VERIFICATION = "authority_verification"
    TIMELINE_DISCUSSION = "timeline_discussion"
    QUALIFIED = "qualified"
    DISQUALIFIED = "disqualified"


class LeadPriority(str, Enum):
    """Lead priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class LeadStatus(str, Enum):
    """Lead status tracking."""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class ContactInfo(BaseModel):
    """Contact information for leads."""
    email: Optional[str] = Field(None, description="Lead's email address")
    phone: Optional[str] = Field(None, description="Lead's phone number")
    name: Optional[str] = Field(None, description="Lead's full name")
    company: Optional[str] = Field(None, description="Lead's company name")
    job_title: Optional[str] = Field(None, description="Lead's job title")
    linkedin_url: Optional[str] = Field(None, description="Lead's LinkedIn profile")
    website: Optional[str] = Field(None, description="Company website")


class QualificationData(BaseModel):
    """BANT qualification data."""
    budget: Optional[str] = Field(None, description="Budget range or constraints")
    authority: Optional[str] = Field(None, description="Decision-making authority level")
    need: Optional[str] = Field(None, description="Specific needs or pain points")
    timeline: Optional[str] = Field(None, description="Implementation timeline")
    company_size: Optional[str] = Field(None, description="Number of employees")
    industry: Optional[str] = Field(None, description="Industry sector")
    current_solution: Optional[str] = Field(None, description="Current solution in use")
    pain_points: List[str] = Field(default_factory=list, description="Identified pain points")


class ConversationMetrics(BaseModel):
    """Metrics derived from conversation analysis."""
    engagement_score: float = Field(0.0, ge=0.0, le=1.0, description="Engagement level (0-1)")
    intent_strength: float = Field(0.0, ge=0.0, le=1.0, description="Buying intent strength (0-1)")
    urgency_level: float = Field(0.0, ge=0.0, le=1.0, description="Urgency level (0-1)")
    sentiment_score: float = Field(0.0, ge=-1.0, le=1.0, description="Sentiment (-1 to 1)")
    question_count: int = Field(0, ge=0, description="Number of questions asked")
    response_time_avg: float = Field(0.0, ge=0.0, description="Average response time in seconds")
    conversation_length: int = Field(0, ge=0, description="Total messages in conversation")


class LeadSignals(BaseModel):
    """Detected lead qualification signals."""
    buying_intent_keywords: List[str] = Field(default_factory=list)
    urgency_indicators: List[str] = Field(default_factory=list)
    budget_mentions: List[str] = Field(default_factory=list)
    authority_indicators: List[str] = Field(default_factory=list)
    competitor_mentions: List[str] = Field(default_factory=list)
    pain_point_expressions: List[str] = Field(default_factory=list)
    timeline_mentions: List[str] = Field(default_factory=list)


class QualificationQuestion(BaseModel):
    """Generated qualification questions."""
    question: str = Field(..., description="The qualification question to ask")
    category: str = Field(..., description="BANT category (budget, authority, need, timeline)")
    priority: int = Field(1, ge=1, le=5, description="Question priority (1-5)")
    context: str = Field(..., description="Context for when to ask this question")
    follow_up_questions: List[str] = Field(default_factory=list)


class LeadAnalysis(BaseModel):
    """Complete lead analysis results."""
    is_potential_lead: bool = Field(False, description="Whether this appears to be a lead")
    confidence_score: float = Field(0.0, ge=0.0, le=1.0, description="Confidence in lead assessment")
    qualification_stage: QualificationStage = Field(QualificationStage.INITIAL_INTEREST)
    lead_signals: LeadSignals = Field(default_factory=LeadSignals)
    suggested_questions: List[QualificationQuestion] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)


class EnhancedLeadData(BaseModel):
    """Complete enhanced lead data model."""
    id: Optional[str] = Field(None, description="Lead ID")
    conversation_id: str = Field(..., description="Associated conversation ID")
    chatbot_id: str = Field(..., description="Chatbot that generated this lead")
    
    # Core lead information
    contact_info: ContactInfo = Field(default_factory=ContactInfo)
    qualification_data: QualificationData = Field(default_factory=QualificationData)
    conversation_metrics: ConversationMetrics = Field(default_factory=ConversationMetrics)
    
    # Lead management
    collection_strategy: CollectionStrategy = Field(CollectionStrategy.CONVERSATIONAL)
    lead_score: float = Field(0.0, ge=0.0, le=100.0, description="Lead score (0-100)")
    priority: LeadPriority = Field(LeadPriority.LOW)
    status: LeadStatus = Field(LeadStatus.NEW)
    qualification_stage: QualificationStage = Field(QualificationStage.INITIAL_INTEREST)
    
    # Analysis results
    lead_analysis: Optional[LeadAnalysis] = Field(None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_interaction: Optional[datetime] = Field(None)
    
    # Additional context
    source: str = Field("chatbot", description="Lead source")
    tags: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    
    @validator('lead_score')
    def validate_lead_score(cls, v):
        """Ensure lead score is within valid range."""
        return max(0.0, min(100.0, v))
    
    @validator('updated_at', always=True)
    def set_updated_at(cls, v):
        """Always update the timestamp when model is modified."""
        return datetime.utcnow()


class LeadCollectionRequest(BaseModel):
    """Request for collecting lead data during conversation."""
    conversation_id: str = Field(..., description="Conversation ID")
    message: str = Field(..., description="User message to analyze")
    collection_strategy: CollectionStrategy = Field(CollectionStrategy.CONVERSATIONAL)
    force_collection: bool = Field(False, description="Force data collection even if not natural")


class LeadCollectionResponse(BaseModel):
    """Response from lead data collection."""
    collected_data: Dict[str, Any] = Field(default_factory=dict)
    collection_questions: List[QualificationQuestion] = Field(default_factory=list)
    should_ask_questions: bool = Field(False)
    collection_complete: bool = Field(False)
    next_collection_strategy: Optional[CollectionStrategy] = Field(None)


class LeadQualificationRequest(BaseModel):
    """Request for lead qualification analysis."""
    conversation_id: str = Field(..., description="Conversation ID")
    conversation_history: List[Dict[str, Any]] = Field(..., description="Full conversation history")
    existing_lead_data: Optional[EnhancedLeadData] = Field(None)


class LeadQualificationResponse(BaseModel):
    """Response from lead qualification analysis."""
    lead_data: EnhancedLeadData = Field(..., description="Updated lead data")
    qualification_questions: List[QualificationQuestion] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    should_escalate: bool = Field(False, description="Whether to escalate to human")
    escalation_reason: Optional[str] = Field(None)


class LeadScoringFactors(BaseModel):
    """Factors used in lead scoring calculation."""
    engagement_factor: float = Field(0.0, description="Weight for engagement metrics")
    intent_factor: float = Field(0.0, description="Weight for buying intent")
    qualification_factor: float = Field(0.0, description="Weight for BANT qualification")
    urgency_factor: float = Field(0.0, description="Weight for urgency indicators")
    fit_factor: float = Field(0.0, description="Weight for ideal customer profile fit")


class LeadScoringConfig(BaseModel):
    """Configuration for lead scoring algorithm."""
    factors: LeadScoringFactors = Field(default_factory=LeadScoringFactors)
    thresholds: Dict[str, float] = Field(default_factory=dict)
    weights: Dict[str, float] = Field(default_factory=dict)


class BulkLeadAnalysisRequest(BaseModel):
    """Request for analyzing multiple conversations for leads."""
    conversation_ids: List[str] = Field(..., description="List of conversation IDs to analyze")
    chatbot_id: str = Field(..., description="Chatbot ID")
    analysis_depth: str = Field("standard", description="Analysis depth: quick, standard, deep")


class BulkLeadAnalysisResponse(BaseModel):
    """Response from bulk lead analysis."""
    analyzed_conversations: int = Field(0)
    leads_identified: int = Field(0)
    leads_data: List[EnhancedLeadData] = Field(default_factory=list)
    analysis_summary: Dict[str, Any] = Field(default_factory=dict)
    processing_time: float = Field(0.0)