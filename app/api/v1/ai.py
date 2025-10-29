"""
AI Agent API Endpoints

This module provides REST API endpoints for AI agent interactions:
- POST /chat: Chat with the AI fitness assistant
- GET /health: Health check for AI services
- GET /tools: List available AI tools
- GET /agent: Get agent information and capabilities
- POST /clear-memory: Clear conversation memory
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import json
import asyncio

from app.agent import get_agent, get_agent_info
from app.tools import get_tools_info


# ============================================================================
# Request/Response Schemas
# ============================================================================

class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=5000, description="User's message to the AI assistant")
    use_memory: bool = Field(default=True, description="Whether to use conversation memory")
    use_rag: bool = Field(default=True, description="Whether to augment response with fitness knowledge")
    stream: bool = Field(default=False, description="Whether to stream the response (SSE)")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What's a good workout plan for weight loss?",
                "use_memory": True,
                "use_rag": True,
                "stream": False
            }
        }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    response: str = Field(..., description="AI assistant's response")
    tools_used: list = Field(default=[], description="List of tools used during response generation")
    success: bool = Field(..., description="Whether the request was successful")
    error: Optional[str] = Field(None, description="Error message if request failed")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "For effective weight loss, I recommend a combination of cardio and strength training...",
                "tools_used": [
                    {
                        "tool": "fitness_tracker",
                        "input": "get_stats",
                        "output": "Retrieved user workout statistics"
                    }
                ],
                "success": True,
                "error": None
            }
        }


class HealthResponse(BaseModel):
    """Response schema for health check"""
    status: str = Field(..., description="Service health status")
    services: dict = Field(..., description="Status of individual services")


# ============================================================================
# Router Configuration
# ============================================================================

router = APIRouter()


# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest = Body(...)
) -> ChatResponse:
    """
    Chat with the AI fitness assistant.

    This endpoint processes user messages and returns AI-generated responses.
    The agent can use tools, retrieve fitness knowledge, and maintain conversation context.

    Args:
        request: ChatRequest with message and configuration options

    Returns:
        ChatResponse with AI response and metadata

    Example:
        ```
        POST /api/v1/chat
        {
            "message": "What are my workout stats this month?",
            "use_memory": true,
            "use_rag": true
        }
        ```
    """
    try:
        # Get or create agent instance
        agent = get_agent(use_memory=request.use_memory)

        # Process message
        result = agent.invoke(
            user_input=request.message,
            use_rag=request.use_rag
        )

        # Return response
        return ChatResponse(
            response=result["response"],
            tools_used=result.get("tools_used", []),
            success=result["success"],
            error=result.get("error")
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Check health status of AI services.

    Returns:
        HealthResponse with status of all AI services

    Example:
        ```
        GET /api/v1/health
        ```
    """
    try:
        # Check agent initialization
        agent_status = "healthy"
        try:
            agent = get_agent(use_memory=False)
            agent_status = "healthy" if agent else "unhealthy"
        except Exception as e:
            agent_status = f"unhealthy: {str(e)}"

        # Check RAG system
        rag_status = "healthy"
        try:
            from app.rag import get_rag
            rag = get_rag()
            rag_status = "healthy" if rag.vectorstore else "unhealthy"
        except Exception as e:
            rag_status = f"unhealthy: {str(e)}"

        # Check tools
        tools_status = "healthy"
        try:
            from app.tools import get_all_tools
            tools = get_all_tools()
            tools_status = f"healthy ({len(tools)} tools available)"
        except Exception as e:
            tools_status = f"unhealthy: {str(e)}"

        # Overall status
        overall_status = "healthy" if all(
            "healthy" in status for status in [agent_status, rag_status, tools_status]
        ) else "degraded"

        return HealthResponse(
            status=overall_status,
            services={
                "agent": agent_status,
                "rag": rag_status,
                "tools": tools_status
            }
        )

    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            services={"error": str(e)}
        )


@router.get("/tools")
async def list_tools():
    """
    Get list of available AI tools.

    Returns:
        List of tool metadata (name, description)

    Example:
        ```
        GET /api/v1/tools
        ```
    """
    try:
        tools_info = get_tools_info()
        return {
            "tools": tools_info,
            "count": len(tools_info)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve tools: {str(e)}"
        )


@router.get("/agent")
async def agent_info():
    """
    Get AI agent information and capabilities.

    Returns:
        Agent metadata including model, capabilities, and available tools

    Example:
        ```
        GET /api/v1/agent
        ```
    """
    try:
        info = get_agent_info()
        return info
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve agent info: {str(e)}"
        )


@router.post("/clear-memory")
async def clear_memory():
    """
    Clear conversation memory for the current session.

    Returns:
        Success message

    Example:
        ```
        POST /api/v1/clear-memory
        ```
    """
    try:
        agent = get_agent(use_memory=True)
        agent.clear_memory()
        return {
            "success": True,
            "message": "Conversation memory cleared successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear memory: {str(e)}"
        )


@router.get("/memory")
async def get_memory():
    """
    Get current conversation history from memory.

    Returns:
        List of messages in conversation history

    Example:
        ```
        GET /api/v1/memory
        ```
    """
    try:
        agent = get_agent(use_memory=True)
        messages = agent.get_memory_messages()
        return {
            "messages": messages,
            "count": len(messages)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve memory: {str(e)}"
        )
