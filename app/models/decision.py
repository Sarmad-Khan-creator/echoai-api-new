"""
Pydantic models for intelligent decision-making system.
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ConversationContextType(str, Enum):
    """Types of conversation context."""
    GREETING = "greeting"
    QUESTION = "question"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"
    REQUEST = "request"
    CLARIFICATION = "clarification"
    FOLLOWUP = "followup"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"


class ProactiveActionType(str, Enum):
    """Types of proactive actions the system can take."""
    ASK_FOLLOWUP = "ask_followup"
    SUGGEST_TOPIC = "suggest_topic"
    CLARIFY_QUESTION = "clarify_question"
    OFFER_HELP = "offer_help"
    ESCALATE = "escalate"
    COLLECT_FEEDBACK = "collect_feedback"
    NONE = "none"


class ConversationContext(BaseModel):
    """Model for conversation context analysis."""
    message_count: int = Field(..., description="Number of messages in conversation", ge=0)
    conversation_length: int = Field(..., description="Total character length of conversation", ge=0)
    context_type: ConversationContextType = Field(..., description="Type of current message context")
    sentiment_score: float = Field(..., description="Current message sentiment score", ge=-1.0, le=1.0)
    sentiment_trend: List[float] = Field(default_factory=list, description="Recent sentiment scores")
    engagement_score: float = Field(..., description="User engagement level", ge=0.0, le=1.0)
    confusion_indicators: List[str] = Field(default_factory=list, description="Indicators of user confusion")
    satisfaction_indicators: List[str] = Field(default_factory=list, description="Indicators of user satisfaction")
    topic_changes: int = Field(default=0, description="Number of topic changes in conversation", ge=0)
    last_response_helpful: Optional[bool] = Field(None, description="Whether last response was helpful")
    user_intent_clarity: float = Field(..., description="Clarity of user intent", ge=0.0, le=1.0)
    knowledge_gaps: List[str] = Field(default_factory=list, description="Identified knowledge gaps")
    
    class Config:
        schema_extra = {
            "example": {
                "message_count": 3,
                "conversation_length": 450,
                "context_type": "question",
                "sentiment_score": 0.2,
                "sentiment_trend": [0.1, 0.0, 0.2],
                "engagement_score": 0.8,
                "confusion_indicators": ["what do you mean", "I don't understand"],
                "satisfaction_indicators": [],
                "topic_changes": 1,
                "last_response_helpful": True,
                "user_intent_clarity": 0.7,
                "knowledge_gaps": ["pricing details"]
            }
        }


class ProactiveAction(BaseModel):
    """Model for proactive actions the system can take."""
    action_type: ProactiveActionType = Field(..., description="Type of proactive action")
    priority: float = Field(..., description="Priority score for this action", ge=0.0, le=1.0)
    content: str = Field(..., description="Content of the proactive action")
    reasoning: str = Field(..., description="Reasoning behind this action")
    confidence: float = Field(..., description="Confidence in this action", ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the action")
    
    class Config:
        schema_extra = {
            "example": {
                "action_type": "ask_followup",
                "priority": 0.8,
                "content": "Would you like to know more about our pricing plans?",
                "reasoning": "User asked about features but didn't inquire about cost",
                "confidence": 0.75,
                "metadata": {"related_topics": ["pricing", "plans"]}
            }
        }


class ConversationIntelligence(BaseModel):
    """Model for conversation intelligence analysis."""
    conversation_id: str = Field(..., description="Conversation ID")
    user_id: str = Field(..., description="User ID")
    chatbot_id: Optional[str] = Field(None, description="Chatbot ID for widget conversations")
    context_understanding: float = Field(..., description="How well the system understands context", ge=0.0, le=1.0)
    proactive_score: float = Field(..., description="Score for proactive assistance opportunities", ge=0.0, le=1.0)
    helpfulness_score: float = Field(..., description="Predicted helpfulness of responses", ge=0.0, le=1.0)
    conversation_flow_score: float = Field(..., description="Quality of conversation flow", ge=0.0, le=1.0)
    user_satisfaction_prediction: float = Field(..., description="Predicted user satisfaction", ge=0.0, le=1.0)
    escalation_risk: float = Field(..., description="Risk of needing escalation", ge=0.0, le=1.0)
    lead_potential: float = Field(..., description="Potential for lead conversion", ge=0.0, le=1.0)
    topics_covered: List[str] = Field(default_factory=list, description="Topics discussed in conversation")
    user_goals_identified: List[str] = Field(default_factory=list, description="Identified user goals")
    knowledge_gaps_found: List[str] = Field(default_factory=list, description="Knowledge gaps discovered")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "user_id": "user_456",
                "chatbot_id": "bot_789",
                "context_understanding": 0.85,
                "proactive_score": 0.7,
                "helpfulness_score": 0.9,
                "conversation_flow_score": 0.8,
                "user_satisfaction_prediction": 0.85,
                "escalation_risk": 0.1,
                "lead_potential": 0.6,
                "topics_covered": ["pricing", "features", "support"],
                "user_goals_identified": ["evaluate_product", "compare_options"],
                "knowledge_gaps_found": ["integration_details"],
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class EnhancedChatResponse(BaseModel):
    """Enhanced chat response with intelligent decision-making features."""
    response: str = Field(..., description="AI-generated response")
    proactive_questions: List[str] = Field(default_factory=list, description="Suggested follow-up questions")
    suggested_topics: List[str] = Field(default_factory=list, description="Suggested related topics")
    conversation_actions: List[ProactiveAction] = Field(default_factory=list, description="Recommended conversation actions")
    intelligence_metadata: ConversationIntelligence = Field(..., description="Conversation intelligence analysis")
    context_used: bool = Field(..., description="Whether relevant context was found and used")
    sources_count: int = Field(..., description="Number of source documents used", ge=0)
    confidence_score: float = Field(..., description="Confidence score of the response", ge=0.0, le=1.0)
    
    # Standard chat response fields
    sentiment: str = Field(..., description="Detected sentiment of user message")
    sentiment_score: Optional[float] = Field(None, description="Sentiment score (-1.0 to 1.0)", ge=-1.0, le=1.0)
    sentiment_confidence: Optional[float] = Field(None, description="Sentiment confidence (0.0 to 1.0)", ge=0.0, le=1.0)
    triggers_detected: Optional[List[str]] = Field(None, description="Automation triggers detected")
    conversation_id: str = Field(..., description="Conversation ID for this exchange")
    session_id: Optional[str] = Field(None, description="Session ID for memory persistence")
    image_analysis: Optional[Dict[str, Any]] = Field(None, description="Image analysis results if image was uploaded")
    lead_analysis: Optional[Dict[str, Any]] = Field(None, description="Lead qualification analysis if qualified")
    
    class Config:
        schema_extra = {
            "example": {
                "response": "Based on your needs, our Pro plan would be perfect for you. It includes advanced analytics and priority support.",
                "proactive_questions": [
                    "Would you like to see a demo of the analytics features?",
                    "Do you have any questions about our implementation process?"
                ],
                "suggested_topics": ["demo_scheduling", "implementation_timeline", "pricing_details"],
                "conversation_actions": [
                    {
                        "action_type": "ask_followup",
                        "priority": 0.8,
                        "content": "Would you like to schedule a demo?",
                        "reasoning": "User showed interest in features",
                        "confidence": 0.75
                    }
                ],
                "intelligence_metadata": {
                    "conversation_id": "conv_123",
                    "user_id": "user_456",
                    "context_understanding": 0.85,
                    "proactive_score": 0.7,
                    "helpfulness_score": 0.9
                },
                "context_used": True,
                "sources_count": 3,
                "confidence_score": 0.85,
                "sentiment": "positive",
                "sentiment_score": 0.7,
                "conversation_id": "conv_123"
            }
        }


class DecisionRequest(BaseModel):
    """Request model for decision-making analysis."""
    message: str = Field(..., description="Current user message")
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list, description="Previous conversation messages")
    user_id: str = Field(..., description="User ID")
    chatbot_id: Optional[str] = Field(None, description="Chatbot ID for widget conversations")
    conversation_id: Optional[str] = Field(None, description="Conversation ID")
    rag_response: Optional[str] = Field(None, description="Generated RAG response for enhancement")
    context_documents: List[Dict[str, Any]] = Field(default_factory=list, description="Retrieved context documents")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What are your pricing plans?",
                "conversation_history": [
                    {"role": "user", "content": "Hi, I'm interested in your product"},
                    {"role": "assistant", "content": "Hello! I'd be happy to help you learn about our product."}
                ],
                "user_id": "user_456",
                "chatbot_id": "bot_789",
                "conversation_id": "conv_123",
                "rag_response": "We offer three pricing plans: Basic, Pro, and Enterprise.",
                "context_documents": [
                    {"content": "Pricing information...", "similarity_score": 0.9}
                ]
            }
        }


class DecisionResponse(BaseModel):
    """Response model for decision-making analysis."""
    enhanced_response: str = Field(..., description="Enhanced response with intelligent improvements")
    conversation_context: ConversationContext = Field(..., description="Analyzed conversation context")
    proactive_actions: List[ProactiveAction] = Field(default_factory=list, description="Recommended proactive actions")
    intelligence_analysis: ConversationIntelligence = Field(..., description="Conversation intelligence analysis")
    should_ask_followup: bool = Field(..., description="Whether to ask follow-up questions")
    followup_questions: List[str] = Field(default_factory=list, description="Generated follow-up questions")
    suggested_topics: List[str] = Field(default_factory=list, description="Suggested conversation topics")
    confidence_score: float = Field(..., description="Confidence in decision analysis", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "enhanced_response": "We offer three pricing plans tailored to different needs. Would you like me to explain which plan might work best for your specific requirements?",
                "conversation_context": {
                    "message_count": 2,
                    "context_type": "question",
                    "sentiment_score": 0.2,
                    "engagement_score": 0.8
                },
                "proactive_actions": [
                    {
                        "action_type": "ask_followup",
                        "priority": 0.8,
                        "content": "What's your team size?",
                        "reasoning": "Helps recommend appropriate plan"
                    }
                ],
                "should_ask_followup": True,
                "followup_questions": ["What's your team size?", "What features are most important to you?"],
                "suggested_topics": ["feature_comparison", "implementation_support"],
                "confidence_score": 0.85
            }
        }