"""
LangChain AI Agent with Memory and Tool Integration

This module implements a production-ready AI agent that:
1. Uses OpenAI GPT-4o-mini for cost-efficient, fast responses
2. Maintains conversation memory across interactions
3. Integrates custom tools (Calculator, Weather, WebSearch, FitnessTracker)
4. Augments responses with RAG-retrieved fitness knowledge
5. Provides Langfuse observability for debugging and optimization
"""

from typing import List, Dict, Any, Optional
import json

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult

from app.core.config import settings
from app.tools import get_all_tools, get_tools_info
from app.rag import get_rag, augment_prompt_with_context


# ============================================================================
# Langfuse Integration (Optional - only if keys are configured)
# ============================================================================

def get_langfuse_handler():
    """
    Get Langfuse callback handler if credentials are configured.

    Returns:
        CallbackHandler or None
    """
    try:
        if (settings.LANGFUSE_PUBLIC_KEY and
            settings.LANGFUSE_SECRET_KEY and
            settings.LANGFUSE_PUBLIC_KEY != "pk-lf-your-public-key"):

            from langfuse.callback import CallbackHandler
            return CallbackHandler(
                public_key=settings.LANGFUSE_PUBLIC_KEY,
                secret_key=settings.LANGFUSE_SECRET_KEY,
                host=settings.LANGFUSE_HOST
            )
    except Exception as e:
        print(f"Langfuse not configured: {e}")

    return None


# ============================================================================
# Custom Callback for Debugging (Fallback if Langfuse not configured)
# ============================================================================

class DebugCallbackHandler(BaseCallbackHandler):
    """
    Custom callback handler for debugging agent execution.

    Logs LLM calls, tool usage, and agent decisions to console.
    """

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        """Called when LLM starts"""
        print(f"\n[LLM START] Generating response...")

    def on_llm_end(self, response: LLMResult, **kwargs):
        """Called when LLM ends"""
        print(f"[LLM END] Response generated")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs):
        """Called when tool execution starts"""
        tool_name = serialized.get("name", "unknown")
        print(f"\n[TOOL START] Using tool: {tool_name}")
        print(f"[TOOL INPUT] {input_str}")

    def on_tool_end(self, output: str, **kwargs):
        """Called when tool execution ends"""
        print(f"[TOOL OUTPUT] {output[:200]}...")  # First 200 chars

    def on_agent_action(self, action: AgentAction, **kwargs):
        """Called when agent decides to use a tool"""
        print(f"\n[AGENT ACTION] Tool: {action.tool}, Input: {action.tool_input}")

    def on_agent_finish(self, finish: AgentFinish, **kwargs):
        """Called when agent finishes"""
        print(f"\n[AGENT FINISH] Final output ready")


# ============================================================================
# Agent System Prompt
# ============================================================================

AGENT_SYSTEM_PROMPT = """You are FitBot, an intelligent fitness and wellness assistant with access to powerful tools and a comprehensive knowledge base.

Your capabilities:
- **Fitness Expertise**: You have deep knowledge of workouts, nutrition, recovery, and goal-setting
- **Data Analysis**: You can query and analyze user fitness data (workouts, goals, progress)
- **Calculations**: Perform complex calculations (BMI, calorie needs, macro splits, etc.)
- **Weather Info**: Check weather conditions for outdoor workout planning
- **Web Search**: Find up-to-date fitness, nutrition, and health information
- **Knowledge Base**: Access to evidence-based fitness and wellness information via RAG

Your personality:
- Professional yet friendly and encouraging
- Evidence-based and safety-conscious
- Personalized and context-aware
- Goal-oriented and motivational

Guidelines:
1. **Always prioritize user safety**: Recommend proper form, progressive overload, and adequate recovery
2. **Be specific and actionable**: Provide concrete recommendations with numbers (sets, reps, calories, etc.)
3. **Use tools when appropriate**:
   - Use fitness_tracker to query user data before making recommendations
   - Use calculator for precise calculations (BMI, TDEE, macro splits)
   - Use weather tool when users ask about outdoor workouts
   - Use web_search for latest research or equipment recommendations
4. **Cite sources**: When using knowledge base or web search, mention sources
5. **Ask clarifying questions**: If user goals or context are unclear
6. **Encourage consistency**: Remind users that sustainable progress requires patience and consistency
7. **Adapt to user level**: Tailor advice for beginners vs advanced athletes

Important safety notes:
- Always recommend consulting healthcare providers for medical concerns
- Do not diagnose medical conditions or injuries
- Emphasize proper form over weight/speed
- Encourage rest and recovery to prevent overtraining

Example interactions:
User: "I want to lose weight"
You: "I'd love to help you with weight loss! To give you the best plan, I need some info:
1. What's your current weight and height? (I can calculate your BMI and calorie needs)
2. Do you have any workout preferences or limitations?
3. What's your target weight loss timeline?

In general, healthy weight loss is 0.5-1kg per week through a 300-500 calorie deficit combined with exercise. Let me know your details and I'll create a personalized plan!"

User: "What are my workout stats this month?"
You: [Uses fitness_tracker tool to get user's workout data] "Here's your February summary:
- Total workouts: 12 sessions
- Total duration: 8.5 hours
- Calories burned: 4,200 cal
- Most frequent: Running (5 sessions)

Great consistency! You're averaging 3 workouts per week. To optimize results, consider adding 1-2 strength training sessions to complement your cardio."

Remember: You are here to help users achieve their fitness goals through evidence-based, personalized guidance. Be their supportive coach and data-driven analyst!
"""


# ============================================================================
# Agent Factory
# ============================================================================

class FitnessAgent:
    """
    AI Agent for fitness and wellness assistance.

    Combines LLM, tools, memory, and RAG for intelligent responses.
    """

    def __init__(self, use_memory: bool = True):
        """
        Initialize the fitness agent.

        Args:
            use_memory: Whether to maintain conversation memory
        """
        self.use_memory = use_memory

        # Initialize LLM (GPT-4o-mini for cost efficiency)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,  # Balance creativity and consistency
            openai_api_key=settings.OPENAI_API_KEY,
            streaming=True  # Enable streaming for real-time responses
        )

        # Get tools
        self.tools = get_all_tools()

        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        ) if use_memory else None

        # Create agent prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", AGENT_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        # Create agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,  # Enable detailed logging
            max_iterations=5,  # Prevent infinite loops
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )

        # Get Langfuse handler if available
        self.langfuse_handler = get_langfuse_handler()

        # Use debug handler as fallback
        self.debug_handler = DebugCallbackHandler()

    def invoke(self, user_input: str, use_rag: bool = True) -> Dict[str, Any]:
        """
        Process user input and generate response.

        Args:
            user_input: User's message/question
            use_rag: Whether to augment with RAG context

        Returns:
            Dict with response and metadata
        """
        try:
            # Augment input with RAG context if enabled
            if use_rag:
                augmented_input = augment_prompt_with_context(user_input, k=2)
            else:
                augmented_input = user_input

            # Prepare callbacks
            callbacks = [self.debug_handler]
            if self.langfuse_handler:
                callbacks.append(self.langfuse_handler)

            # Invoke agent
            result = self.agent_executor.invoke(
                {"input": augmented_input},
                config={"callbacks": callbacks}
            )

            # Extract tool usage info
            tools_used = []
            if "intermediate_steps" in result:
                for action, output in result["intermediate_steps"]:
                    tools_used.append({
                        "tool": action.tool,
                        "input": str(action.tool_input)[:100],  # Truncate for brevity
                        "output": str(output)[:200]
                    })

            return {
                "response": result["output"],
                "tools_used": tools_used,
                "success": True
            }

        except Exception as e:
            print(f"Error in agent execution: {e}")
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question or contact support.",
                "tools_used": [],
                "success": False,
                "error": str(e)
            }

    async def ainvoke(self, user_input: str, use_rag: bool = True) -> Dict[str, Any]:
        """
        Async version of invoke for streaming responses.

        Args:
            user_input: User's message/question
            use_rag: Whether to augment with RAG context

        Returns:
            Dict with response and metadata
        """
        # For now, just call synchronous version
        # TODO: Implement true async streaming
        return self.invoke(user_input, use_rag)

    def clear_memory(self):
        """Clear conversation memory"""
        if self.memory:
            self.memory.clear()

    def get_memory_messages(self) -> List[Dict[str, str]]:
        """
        Get conversation history from memory.

        Returns:
            List of message dicts with role and content
        """
        if not self.memory:
            return []

        messages = []
        if hasattr(self.memory, "chat_memory") and hasattr(self.memory.chat_memory, "messages"):
            for msg in self.memory.chat_memory.messages:
                messages.append({
                    "role": "assistant" if hasattr(msg, "type") and msg.type == "ai" else "user",
                    "content": msg.content
                })

        return messages


# ============================================================================
# Global Agent Instance (Singleton)
# ============================================================================

_agent_instance: Optional[FitnessAgent] = None


def get_agent(use_memory: bool = True) -> FitnessAgent:
    """
    Get or create the global agent instance.

    Args:
        use_memory: Whether to use conversation memory

    Returns:
        FitnessAgent instance
    """
    global _agent_instance
    if _agent_instance is None or _agent_instance.use_memory != use_memory:
        _agent_instance = FitnessAgent(use_memory=use_memory)
    return _agent_instance


def get_agent_info() -> Dict[str, Any]:
    """
    Get agent metadata for API documentation.

    Returns:
        Dict with agent info
    """
    return {
        "name": "FitBot",
        "description": "Intelligent fitness and wellness AI assistant",
        "model": "gpt-4o-mini",
        "capabilities": [
            "Fitness data analysis (workouts, goals, progress)",
            "Mathematical calculations (BMI, TDEE, macros)",
            "Weather information for outdoor workout planning",
            "Web search for latest fitness and nutrition info",
            "Evidence-based fitness knowledge via RAG",
            "Personalized workout and nutrition recommendations"
        ],
        "available_tools": get_tools_info(),
        "memory": "Maintains conversation context across interactions",
        "observability": "Langfuse integration for LLM tracing and debugging"
    }
