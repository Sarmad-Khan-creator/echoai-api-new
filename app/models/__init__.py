"""
Models package for EchoAI FastAPI service.
Exports all Pydantic models for use across the application.
"""

# Import all models to make them available when importing from app.models
from .chat import *
from .decision import *
from .enhanced_lead import *
from .enhanced_streaming import *
from .escalation import *
from .ingest import *
from .instruction import *
from .lead import *
from .memory import *
from .simple_instruction import *
from .vision import *

__all__ = [
    # Chat models
    "ChatRequest",
    "ChatResponse", 
    "StreamingChatResponse",
    "ChatMessage",
    "ChatHistory",
    
    # Decision models
    "DecisionRequest",
    "DecisionResponse",
    "DecisionContext",
    
    # Enhanced lead models
    "EnhancedLeadRequest",
    "EnhancedLeadResponse",
    "LeadAnalysis",
    "LeadScore",
    
    # Enhanced streaming models
    "StreamingRequest",
    "StreamingResponse",
    "StreamingChunk",
    
    # Escalation models
    "EscalationRequest",
    "EscalationResponse",
    "EscalationContext",
    
    # Ingest models
    "IngestRequest",
    "IngestResponse",
    "ProcessingStats",
    "VectorStorageStats",
    
    # Instruction models
    "InstructionRequest",
    "InstructionResponse",
    "InstructionUpdate",
    
    # Lead models
    "LeadRequest",
    "LeadResponse",
    "LeadData",
    
    # Memory models
    "MemoryRequest",
    "MemoryResponse",
    "MemoryItem",
    
    # Simple instruction models
    "ChatbotInstructionUpdate",
    "ChatbotInstructionResponse",
    "ChatbotWithInstructionResponse",
    # Vision models
    "VisionRequest",
    "VisionResponse",
    "ImageAnalysis",
]
