"""
Base agent class for PTNutritionAI AI coaches
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import asyncio
import logging
from openai import AsyncAzureOpenAI
from ..core.config import settings

logger = logging.getLogger(__name__)


class BaseAIAgent(ABC):
    """Base class for all AI agents in PTNutritionAI"""
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the AI agent with Azure OpenAI client"""
        self.model_name = model_name or "gpt-4"
        self.client = None
        self.conversation_history: List[Dict[str, str]] = []
        self.user_context: Dict[str, Any] = {}
        
        # Initialize Azure OpenAI client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Azure OpenAI client"""
        if not settings.azure_openai_endpoint or not settings.azure_openai_api_key:
            logger.warning("Azure OpenAI credentials not configured")
            return
            
        self.client = AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Define the agent's personality, expertise, and behavior"""
        pass
    
    @abstractmethod
    def get_agent_name(self) -> str:
        """Return the agent's name for identification"""
        pass
    
    def set_user_context(self, context: Dict[str, Any]):
        """Set user profile information for personalized responses"""
        self.user_context.update(context)
        logger.info(f"{self.get_agent_name()} updated user context")
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # Keep conversation history manageable (last 20 messages)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info(f"{self.get_agent_name()} conversation history cleared")
    
    def get_context_summary(self) -> str:
        """Generate a summary of user context for the agent"""
        if not self.user_context:
            return "No user context available."
        
        context_parts = []
        
        # Basic info
        if 'age' in self.user_context:
            context_parts.append(f"Age: {self.user_context['age']}")
        if 'weight' in self.user_context:
            context_parts.append(f"Weight: {self.user_context['weight']} kg")
        if 'height' in self.user_context:
            context_parts.append(f"Height: {self.user_context['height']} cm")
        
        # Goals and preferences
        if 'goals' in self.user_context:
            context_parts.append(f"Goals: {self.user_context['goals']}")
        if 'workout_frequency' in self.user_context:
            context_parts.append(f"Workout frequency: {self.user_context['workout_frequency']}")
        
        return " | ".join(context_parts) if context_parts else "Limited user context available."
    
    async def get_response(self, user_input: str, include_context: bool = True) -> str:
        """Get response from the AI agent"""
        if not self.client:
            return "Sorry, I'm not properly configured. Please check Azure OpenAI settings."
        
        try:
            # Add user message to history
            self.add_message("user", user_input)
            
            # Prepare system message with context
            system_prompt = self.get_system_prompt()
            if include_context and self.user_context:
                system_prompt += f"\n\nUser Context: {self.get_context_summary()}"
            
            # Prepare messages for API call
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history
            for msg in self.conversation_history[-10:]:  # Last 10 messages
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Call Azure OpenAI
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            agent_response = response.choices[0].message.content
            
            # Add agent response to history
            self.add_message("assistant", agent_response)
            
            logger.info(f"{self.get_agent_name()} provided response to user")
            return agent_response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            logger.error(f"{self.get_agent_name()} error: {str(e)}")
            return error_msg
    
    async def get_structured_response(self, prompt: str, response_format: Dict[str, Any]) -> Dict[str, Any]:
        """Get a structured response from the agent"""
        try:
            structured_prompt = f"""
            {self.get_system_prompt()}
            
            User Context: {self.get_context_summary()}
            
            Request: {prompt}
            
            Please respond in the following JSON format:
            {response_format}
            """
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "system", "content": structured_prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            # Try to parse JSON response
            import json
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return {"error": "Failed to parse structured response", "raw_response": response.choices[0].message.content}
                
        except Exception as e:
            logger.error(f"{self.get_agent_name()} structured response error: {str(e)}")
            return {"error": str(e)}
