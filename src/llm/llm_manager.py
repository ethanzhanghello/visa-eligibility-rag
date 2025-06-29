"""
LLM manager for handling interactions with language models.
"""
import os
import logging
from typing import Dict, Any, Optional
from openai import OpenAI

from src.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMManager:
    """Manager class for handling LLM interactions."""
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the LLM manager.
        
        Args:
            model_name (str): Name of the model to use. If None, uses config default.
        """
        try:
            self.model_name = model_name or config.llm.model_name
            logger.info(f"Initializing LLMManager with model: {self.model_name}")
            
            # Initialize OpenAI client with configuration
            api_key = config.llm.api_key
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            
            # Create client with minimal configuration to avoid compatibility issues
            self.client = OpenAI(api_key=api_key)
            
        except Exception as e:
            logger.exception(f"Failed to initialize LLMManager: {str(e)}")
            raise
    
    def _prepare_prompt(self, context: str, user_input: str) -> str:
        """Prepare the prompt for the LLM.
        
        Args:
            context (str): Retrieved context documents.
            user_input (str): User's question.
            
        Returns:
            str: Formatted prompt.
        """
        return f"""You are a bilingual immigration assistant.
Answer the user's question based only on the following documents:

{context}

Question: {user_input}

Respond in the same language as the question. If you cannot find a relevant answer in the provided documents, 
say so clearly in the same language as the question. Do not make up information."""
    
    def generate_response(
        self,
        context: str,
        user_input: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate a response using the LLM.
        
        Args:
            context (str): Retrieved context documents.
            user_input (str): User's question.
            temperature (Optional[float]): Sampling temperature. If None, uses config default.
            max_tokens (Optional[int]): Maximum tokens in response. If None, uses config default.
            
        Returns:
            Dict[str, Any]: Response from the LLM.
        """
        try:
            # Use config defaults if not provided
            temperature = temperature if temperature is not None else config.llm.temperature
            max_tokens = max_tokens if max_tokens is not None else config.llm.max_tokens
            
            # Prepare the prompt
            prompt = self._prepare_prompt(context, user_input)
            
            logger.info(f"Sending request to LLM (model: {self.model_name}, temp: {temperature}, max_tokens: {max_tokens})")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract and return the response
            result = {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
            logger.info(f"Generated response with {result['usage']['total_tokens']} total tokens")
            return result
            
        except Exception as e:
            logger.exception(f"Failed to generate response: {str(e)}")
            raise
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the current LLM configuration."""
        return {
            "model_name": self.model_name,
            "temperature": config.llm.temperature,
            "max_tokens": config.llm.max_tokens,
            "api_key_set": bool(config.llm.api_key)
        }
    
    def test_connection(self) -> bool:
        """Test the connection to the OpenAI API.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            # Try a simple test request
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            logger.info("LLM connection test successful")
            return True
        except Exception as e:
            logger.error(f"LLM connection test failed: {str(e)}")
            return False 