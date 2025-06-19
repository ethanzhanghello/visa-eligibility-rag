"""
Test the LLM manager functionality.
"""
import os
import pytest
from unittest.mock import MagicMock, patch
from src.llm.llm_manager import LLMManager

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    class MockResponse:
        def __init__(self):
            self.choices = [
                MagicMock(message=MagicMock(content="Test response"))
            ]
            self.model = "gpt-4"
            self.usage = MagicMock(
                prompt_tokens=10,
                completion_tokens=20,
                total_tokens=30
            )
    return MockResponse()

@pytest.fixture
def llm_manager():
    """Create LLM manager with mocked API key."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        return LLMManager()

def test_prepare_prompt(llm_manager):
    """Test prompt preparation."""
    context = "Test context"
    user_input = "Test question"
    prompt = llm_manager._prepare_prompt(context, user_input)
    
    assert "Test context" in prompt
    assert "Test question" in prompt
    assert "bilingual immigration assistant" in prompt

@patch("openai.OpenAI")
def test_generate_response(mock_openai, llm_manager, mock_openai_response):
    """Test response generation."""
    # Setup mock
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai.return_value = mock_client
    
    # Test
    response = llm_manager.generate_response(
        context="Test context",
        user_input="Test question"
    )
    
    assert response["content"] == "Test response"
    assert response["model"] == "gpt-4"
    assert response["usage"]["total_tokens"] == 30
    
    # Verify API call
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["model"] == "gpt-4"
    assert len(call_args["messages"]) == 1
    assert call_args["messages"][0]["role"] == "user"

def test_init_no_api_key():
    """Test initialization without API key."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable not set"):
            LLMManager() 