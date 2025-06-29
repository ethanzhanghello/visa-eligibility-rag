#!/usr/bin/env python3
"""
Simple UI for Green Card RAG Helper
A clean, functional interface for testing all features.
"""
import streamlit as st
import requests
import json
from datetime import datetime
import os

# Configuration
API_BASE_URL = "http://localhost:8000"

def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, None

def submit_query(question, language):
    """Submit a query to the API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question, "language": language},
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error submitting query: {str(e)}")
        return None

def get_pending_questions():
    """Get questions pending expert review."""
    try:
        response = requests.get(f"{API_BASE_URL}/expert/pending-questions", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_system_info():
    """Get system information."""
    try:
        response = requests.get(f"{API_BASE_URL}/system/info", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def main():
    st.set_page_config(
        page_title="Green Card RAG Helper",
        page_icon="🌍",
        layout="wide"
    )
    
    # Header
    st.title("🌍 Green Card RAG Helper")
    st.markdown("**Simple Interface for Testing Immigration Q&A System**")
    
    # API Health Check
    api_healthy, health_data = check_api_health()
    
    if not api_healthy:
        st.error("⚠️ **API server is not running!**")
        st.markdown("""
        Please start the server first:
        ```bash
        python3 start_server.py
        ```
        """)
        st.stop()
    else:
        st.success("✅ **API server is running**")
        if health_data:
            st.info(f"Status: {health_data.get('status', 'unknown')} | Version: {health_data.get('version', 'unknown')}")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Query Interface", "👨‍💼 Expert Review", "📊 System Info"])
    
    with tab1:
        render_query_interface()
    
    with tab2:
        render_expert_review()
    
    with tab3:
        render_system_info()

def render_query_interface():
    """Render the main query interface."""
    st.header("Ask Immigration Questions")
    
    # Query Form
    with st.form("query_form"):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            question = st.text_area(
                "Your Question:",
                placeholder="e.g., What documents do I need for EB-2 visa?",
                height=120
            )
        
        with col2:
            language = st.selectbox("Language", ["auto", "en", "zh"], index=0)
            submit_button = st.form_submit_button("Submit", type="primary")
    
    if submit_button and question.strip():
        with st.spinner("Processing your question..."):
            result = submit_query(question.strip(), language)
            
            if result:
                # Success message
                st.success("✅ Response generated successfully!")
                
                # Answer
                st.subheader("Answer")
                st.write(result["answer"])
                
                # Confidence metrics
                confidence = result.get("confidence", {})
                if confidence:
                    st.subheader("Confidence Analysis")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        score = confidence.get('score', 0)
                        st.metric("Confidence Score", f"{score:.2f}")
                    
                    with col2:
                        level = confidence.get('level', 'unknown')
                        level_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}
                        st.metric("Level", f"{level_emoji.get(level, '❓')} {level}")
                    
                    with col3:
                        flagged = confidence.get('flagged_for_review', False)
                        status = "🔴 Flagged" if flagged else "🟢 Good"
                        st.metric("Review Status", status)
                    
                    with col4:
                        tokens = result.get('usage', {}).get('total_tokens', 0)
                        st.metric("Tokens Used", tokens)
                    
                    # Additional confidence details
                    with st.expander("Detailed Confidence Metrics"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Context Relevance:** {confidence.get('context_relevance', 0):.2f}")
                            st.write(f"**Source Quality:** {confidence.get('source_quality', 0):.2f}")
                        with col2:
                            st.write(f"**Response Length:** {confidence.get('response_length', 0)} chars")
                            st.write(f"**Immigration Terms:** {'✅' if confidence.get('contains_immigration_terms', False) else '❌'}")
                
                # Model info
                st.info(f"Generated by: {result.get('model', 'unknown')}")
                
            else:
                st.error("❌ Failed to get response from API")

def render_expert_review():
    """Render the expert review interface."""
    st.header("Expert Review Dashboard")
    
    # Get pending questions
    pending_data = get_pending_questions()
    
    if pending_data and pending_data.get('pending_questions'):
        questions = pending_data['pending_questions']
        st.success(f"Found {len(questions)} questions pending review")
        
        for i, question in enumerate(questions):
            with st.expander(f"Question {i+1}: {question['question'][:50]}..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Question:** {question['question']}")
                    st.write(f"**Language:** {question['language']}")
                    st.write(f"**Confidence Score:** {question['confidence_score']:.2f}")
                    st.write(f"**Frequency:** {question['frequency_count']} times asked")
                
                with col2:
                    st.write(f"**Status:** {question['status']}")
                    st.write(f"**First Asked:** {question['first_asked']}")
                    st.write(f"**Last Asked:** {question['last_asked']}")
                    
                    if question.get('expert_answer'):
                        st.write("**Expert Answer:**")
                        st.write(question['expert_answer'])
    else:
        st.info("No questions pending expert review")
    
    # Expert review submission form
    st.subheader("Submit Expert Review")
    with st.form("expert_review_form"):
        question_id = st.text_input("Question ID (from above)")
        expert_answer = st.text_area("Expert Answer", height=150)
        expert_sources = st.text_input("Sources (comma-separated URLs)")
        expert_credentials = st.text_input("Your Credentials")
        confidence_level = st.selectbox("Confidence Level", ["high", "medium", "low"])
        notes = st.text_area("Additional Notes")
        
        submit_review = st.form_submit_button("Submit Review", type="primary")
        
        if submit_review and question_id and expert_answer:
            st.info("Expert review submission feature would be implemented here")

def render_system_info():
    """Render system information."""
    st.header("System Information")
    
    # Get system info
    system_info = get_system_info()
    
    if system_info:
        st.success("✅ System information retrieved")
        
        # Basic info
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Configuration")
            config = system_info.get('config', {})
            
            llm_config = config.get('llm', {})
            st.write(f"**Model:** {llm_config.get('model_name', 'unknown')}")
            st.write(f"**API Key:** {'✅ Set' if llm_config.get('api_key_set') else '❌ Not Set'}")
            st.write(f"**Temperature:** {llm_config.get('temperature', 'unknown')}")
            st.write(f"**Max Tokens:** {llm_config.get('max_tokens', 'unknown')}")
            
            confidence_config = config.get('confidence', {})
            st.write(f"**Confidence Threshold:** {confidence_config.get('threshold', 'unknown')}")
        
        with col2:
            st.subheader("System Status")
            managers = system_info.get('managers', {})
            st.write(f"**Retrieval Manager:** {'✅' if managers.get('retrieval') else '❌'}")
            st.write(f"**Confidence Manager:** {'✅' if managers.get('confidence') else '❌'}")
            st.write(f"**Question Tracker:** {'✅' if managers.get('question_tracker') else '❌'}")
            st.write(f"**FAQ Integration:** {'✅' if managers.get('faq_integration') else '❌'}")
            st.write(f"**LLM Manager:** {'✅' if managers.get('llm') else '❌'}")
        
        # Confidence configuration details
        with st.expander("Confidence Configuration Details"):
            confidence_config = system_info.get('confidence_config', {})
            weights = confidence_config.get('weights', {})
            st.write(f"**Context Weight:** {weights.get('context', 'unknown')}")
            st.write(f"**Source Weight:** {weights.get('source', 'unknown')}")
            st.write(f"**Length Weight:** {weights.get('length', 'unknown')}")
            st.write(f"**Terms Weight:** {weights.get('terms', 'unknown')}")
            
            terms_count = confidence_config.get('immigration_terms_count', {})
            st.write(f"**English Terms:** {terms_count.get('english', 'unknown')}")
            st.write(f"**Chinese Terms:** {terms_count.get('chinese', 'unknown')}")
    
    else:
        st.error("❌ Failed to retrieve system information")

if __name__ == "__main__":
    main() 