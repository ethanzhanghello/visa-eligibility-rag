"""
LLM manager for handling interactions with language models.
"""
import os
import logging
from typing import Dict, Any, Optional
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMManager:
    """Manager class for handling LLM interactions."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize the LLM manager.
        
        Args:
            model_name (str): Name of the model to use.
        """
        try:
            logger.info(f"Initializing LLMManager with model: {model_name}")
            self.model_name = model_name
            
            # Initialize OpenAI client
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
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
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """Generate a response using the LLM.
        
        Args:
            context (str): Retrieved context documents.
            user_input (str): User's question.
            temperature (float): Sampling temperature.
            max_tokens (int): Maximum tokens in response.
            
        Returns:
            Dict[str, Any]: Response from the LLM.
        """
        try:
            # Prepare the prompt
            prompt = self._prepare_prompt(context, user_input)
            
            logger.info("Sending request to LLM")
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