"""
Simplified Pydantic models for chatbot instruction endpoints.
"""
from typing import Optional
from pydantic import BaseModel, Field, validator


class ChatbotInstructionUpdate(BaseModel):
    """Request model for updating chatbot instruction."""
    instructions: str = Field(..., description="System instruction for the chatbot", min_length=1)
    
    @validator('instructions')
    def validate_instruction(cls, v):
        """Validate instruction format."""
        if not v or not v.strip():
            raise ValueError('Instruction cannot be empty')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "instructions": "You are a customer service assistant for TechCorp. Always be polite, professional, and helpful. When users ask about pricing, direct them to our sales team. For technical issues, provide step-by-step solutions."
            }
        }


class ChatbotInstructionResponse(BaseModel):
    """Response model for chatbot instruction."""
    chatbot_id: str = Field(..., description="Chatbot ID")
    instructions: str = Field(..., description="System instruction for the chatbot")
    
    class Config:
        schema_extra = {
            "example": {
                "chatbot_id": "cm789xyz123abc",
                "instructions": "You are a customer service assistant for TechCorp. Always be polite, professional, and helpful."
            }
        }


class ChatbotWithInstructionResponse(BaseModel):
    """Response model for chatbot with full details including instruction."""
    id: str = Field(..., description="Chatbot ID")
    name: str = Field(..., description="Chatbot name")
    welcomeMessage: str = Field(..., description="Welcome message")
    primaryColor: str = Field(..., description="Primary color")
    isActive: bool = Field(..., description="Whether chatbot is active")
    instructions: str = Field(..., description="System instruction for the chatbot")
    userId: str = Field(..., description="Owner user ID")
    createdAt: str = Field(..., description="Creation timestamp")
    updatedAt: str = Field(..., description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "cm789xyz123abc",
                "name": "Customer Support Bot",
                "welcomeMessage": "Hello! How can I help you today?",
                "primaryColor": "#3B82F6",
                "isActive": True,
                "instructions": "You are a customer service assistant for TechCorp. Always be polite, professional, and helpful.",
                "userId": "user123",
                "createdAt": "2024-01-15T10:30:00Z",
                "updatedAt": "2024-01-15T10:30:00Z"
            }
        }