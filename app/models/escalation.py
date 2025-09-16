"""
Escalation management models for conversation escalation system.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class EscalationType(str, Enum):
    """Types of escalation scenarios."""
    TECHNICAL = "TECHNICAL"
    FRUSTRATION = "FRUSTRATION"
    COMPLEXITY = "COMPLEXITY"
    COMPLAINT = "COMPLAINT"
    REQUEST = "REQUEST"


class EscalationStatus(str, Enum):
    """Status of escalation requests."""
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"


class UrgencyLevel(str, Enum):
    """Urgency levels for escalation requests."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EscalationTrigger(BaseModel):
    """Represents detected escalation triggers."""
    trigger_type: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str
    context: Dict[str, Any] = Field(default_factory=dict)


class EscalationSignals(BaseModel):
    """Collection of escalation signals detected in conversation."""
    triggers: List[EscalationTrigger]
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0)
    frustration_indicators: List[str] = Field(default_factory=list)
    complexity_indicators: List[str] = Field(default_factory=list)
    technical_indicators: List[str] = Field(default_factory=list)


class EscalationResponse(BaseModel):
    """Response generated for escalation scenarios."""
    message: str
    escalation_type: EscalationType
    urgency_level: UrgencyLevel
    suggested_actions: List[str] = Field(default_factory=list)
    agent_context: Dict[str, Any] = Field(default_factory=dict)
    should_escalate: bool = True


class EscalationRequest(BaseModel):
    """Escalation request data model."""
    id: Optional[str] = None
    conversation_id: str
    chatbot_id: str
    escalation_type: EscalationType
    trigger_reason: Optional[str] = None
    escalation_data: Optional[Dict[str, Any]] = None
    status: EscalationStatus = EscalationStatus.PENDING
    assigned_agent_id: Optional[str] = None
    urgency_level: UrgencyLevel = UrgencyLevel.MEDIUM
    customer_sentiment: Optional[str] = None
    conversation_context: Optional[Dict[str, Any]] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class NotificationResult(BaseModel):
    """Result of agent notification."""
    success: bool
    notification_id: Optional[str] = None
    agent_id: Optional[str] = None
    message: str
    delivery_method: str  # email, slack, webhook, etc.
    timestamp: datetime


class EscalationAnalysis(BaseModel):
    """Analysis result for escalation detection."""
    should_escalate: bool
    escalation_type: Optional[EscalationType] = None
    urgency_level: UrgencyLevel = UrgencyLevel.MEDIUM
    confidence: float = Field(..., ge=0.0, le=1.0)
    triggers: List[EscalationTrigger] = Field(default_factory=list)
    recommended_response: Optional[str] = None
    agent_context: Dict[str, Any] = Field(default_factory=dict)


class ConversationContext(BaseModel):
    """Context information for escalation analysis."""
    conversation_id: str
    message_count: int
    user_messages: List[str]
    assistant_messages: List[str]
    sentiment_history: List[float] = Field(default_factory=list)
    topic_changes: int = 0
    unresolved_issues: List[str] = Field(default_factory=list)
    user_frustration_indicators: List[str] = Field(default_factory=list)
    technical_complexity_score: float = Field(0.0, ge=0.0, le=1.0)
    conversation_duration: Optional[int] = None  # minutes


class EscalationMetrics(BaseModel):
    """Metrics for escalation monitoring."""
    total_escalations: int
    escalations_by_type: Dict[EscalationType, int]
    escalations_by_urgency: Dict[UrgencyLevel, int]
    average_resolution_time: Optional[float] = None  # hours
    resolution_rate: float = Field(..., ge=0.0, le=1.0)
    customer_satisfaction: Optional[float] = Field(None, ge=0.0, le=1.0)
    agent_response_time: Optional[float] = None  # minutes


class AgentNotification(BaseModel):
    """Notification to human agents."""
    escalation_id: str
    agent_id: Optional[str] = None
    notification_type: str  # immediate, queued, broadcast
    priority: UrgencyLevel
    message: str
    conversation_summary: str
    customer_context: Dict[str, Any] = Field(default_factory=dict)
    estimated_complexity: str  # simple, moderate, complex
    required_skills: List[str] = Field(default_factory=list)