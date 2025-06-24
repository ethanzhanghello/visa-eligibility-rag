import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd

# Configuration
API_BASE_URL = "http://localhost:8000"

def init_session_state():
    """Initialize session state variables."""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Query Interface"
    if 'expert_mode' not in st.session_state:
        st.session_state.expert_mode = False

def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

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

def get_expert_stats():
    """Get expert review statistics."""
    try:
        response = requests.get(f"{API_BASE_URL}/expert/stats", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def submit_expert_review(question_id, expert_answer, expert_sources, expert_credentials, confidence_level, notes):
    """Submit an expert review."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/expert/review",
            json={
                "question_id": question_id,
                "expert_answer": expert_answer,
                "expert_sources": expert_sources.split(",") if expert_sources else [],
                "expert_credentials": expert_credentials,
                "confidence_level": confidence_level,
                "notes": notes
            },
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error submitting expert review: {str(e)}")
        return None

def get_pending_integrations():
    """Get pending FAQ integrations."""
    try:
        response = requests.get(f"{API_BASE_URL}/faq/pending-integrations", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def integrate_to_faq(question_id):
    """Integrate a question into the FAQ database."""
    try:
        response = requests.post(f"{API_BASE_URL}/faq/integrate/{question_id}", timeout=30)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error integrating to FAQ: {str(e)}")
        return None

def get_cache_stats():
    """Get cache statistics."""
    try:
        response = requests.get(f"{API_BASE_URL}/cache/stats", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def main():
    st.set_page_config(
        page_title="Green Card RAG Helper",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_session_state()
    
    # Header
    st.title("🌍 Green Card RAG Helper")
    st.markdown("Bilingual Immigration Assistant with Expert Review System")
    
    # API Health Check
    api_healthy = check_api_health()
    if not api_healthy:
        st.error("⚠️ API server is not running. Please start the server with: `uvicorn src.api.main:app --reload`")
        st.stop()
    else:
        st.success("✅ API server is running")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        tabs = ["Query Interface", "Expert Review Dashboard", "FAQ Integration", "System Stats"]
        current_tab = st.selectbox("Select View", tabs, index=0)
        
        st.header("Expert Mode")
        expert_mode = st.checkbox("Enable Expert Mode", value=st.session_state.expert_mode)
        st.session_state.expert_mode = expert_mode
        
        if expert_mode:
            st.info("🔧 Expert mode enabled - you can submit expert reviews")
    
    # Main Content
    if current_tab == "Query Interface":
        render_query_interface()
    elif current_tab == "Expert Review Dashboard":
        render_expert_dashboard()
    elif current_tab == "FAQ Integration":
        render_faq_integration()
    elif current_tab == "System Stats":
        render_system_stats()

def render_query_interface():
    """Render the main query interface."""
    st.header("🔍 Query Interface")
    
    # Query Form
    with st.form("query_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            question = st.text_area(
                "Ask your immigration question:",
                placeholder="e.g., What documents do I need for EB-2 visa?",
                height=100
            )
        
        with col2:
            language = st.selectbox("Language", ["auto", "en", "zh"], index=0)
            submit_button = st.form_submit_button("Submit Question", type="primary")
    
    if submit_button and question.strip():
        with st.spinner("Processing your question..."):
            result = submit_query(question.strip(), language)
            
            if result:
                # Display Results
                st.success("✅ Response Generated")
                
                # Answer
                st.subheader("Answer")
                st.write(result["answer"])
                
                # Confidence Information
                confidence = result.get("confidence", {})
                if confidence:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Confidence Score", f"{confidence.get('score', 0):.2f}")
                    
                    with col2:
                        level = confidence.get('level', 'unknown')
                        level_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}
                        st.metric("Confidence Level", f"{level_emoji.get(level, '❓')} {level}")
                    
                    with col3:
                        st.metric("Context Relevance", f"{confidence.get('context_relevance', 0):.2f}")
                    
                    with col4:
                        st.metric("Source Quality", f"{confidence.get('source_quality', 0):.2f}")
                    
                    # Confidence Details
                    with st.expander("📊 Detailed Confidence Analysis"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Confidence Factors:**")
                            st.write(f"• Context Relevance: {confidence.get('context_relevance', 0):.2f}")
                            st.write(f"• Source Quality: {confidence.get('source_quality', 0):.2f}")
                            st.write(f"• Response Length: {confidence.get('response_length', 0)} characters")
                            st.write(f"• Immigration Terms: {'✅' if confidence.get('contains_immigration_terms') else '❌'}")
                        
                        with col2:
                            st.write("**Response Info:**")
                            st.write(f"• Model: {result.get('model', 'Unknown')}")
                            st.write(f"• Cached: {'✅' if result.get('cached') else '❌'}")
                            st.write(f"• Flagged for Review: {'✅' if confidence.get('flagged_for_review') else '❌'}")
                            if confidence.get('question_id'):
                                st.write(f"• Question ID: {confidence['question_id']}")
                    
                    # Expert Review Notice
                    if confidence.get('flagged_for_review'):
                        st.warning("⚠️ This question has been flagged for expert review due to low confidence. Check the Expert Review Dashboard for updates.")
                
                # Usage Information
                if 'usage' in result:
                    with st.expander("📈 Usage Information"):
                        usage = result['usage']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Tokens", usage.get('total_tokens', 0))
                        with col2:
                            st.metric("Prompt Tokens", usage.get('prompt_tokens', 0))
                        with col3:
                            st.metric("Completion Tokens", usage.get('completion_tokens', 0))

def render_expert_dashboard():
    """Render the expert review dashboard."""
    st.header("👨‍💼 Expert Review Dashboard")
    
    if not st.session_state.expert_mode:
        st.warning("Please enable Expert Mode in the sidebar to access this dashboard.")
        return
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    # Get pending questions
    pending_data = get_pending_questions()
    
    if pending_data and pending_data.get('pending_questions'):
        questions = pending_data['pending_questions']
        st.success(f"Found {len(questions)} questions pending expert review")
        
        # Display questions in a table
        df = pd.DataFrame(questions)
        df['first_asked'] = pd.to_datetime(df['first_asked']).dt.strftime('%Y-%m-%d %H:%M')
        df['last_asked'] = pd.to_datetime(df['last_asked']).dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(
            df[['id', 'question', 'language', 'confidence_score', 'frequency_count', 'first_asked']],
            use_container_width=True
        )
        
        # Expert Review Form
        st.subheader("📝 Submit Expert Review")
        
        if questions:
            selected_question = st.selectbox(
                "Select a question to review:",
                options=questions,
                format_func=lambda x: f"{x['question'][:50]}... ({x['frequency_count']} times asked)"
            )
            
            if selected_question:
                with st.form("expert_review_form"):
                    st.write(f"**Question:** {selected_question['question']}")
                    st.write(f"**Language:** {selected_question['language']}")
                    st.write(f"**Confidence Score:** {selected_question['confidence_score']:.2f}")
                    st.write(f"**Times Asked:** {selected_question['frequency_count']}")
                    
                    expert_answer = st.text_area(
                        "Expert Answer:",
                        placeholder="Provide a comprehensive, accurate answer with proper immigration terminology...",
                        height=150
                    )
                    
                    expert_sources = st.text_input(
                        "Sources (comma-separated):",
                        placeholder="uscis.gov/forms/i-140, state.gov/visa, etc."
                    )
                    
                    expert_credentials = st.text_input(
                        "Your Credentials:",
                        placeholder="e.g., Immigration Attorney, 10+ years experience"
                    )
                    
                    confidence_level = st.selectbox(
                        "Confidence Level:",
                        ["high", "medium", "low"]
                    )
                    
                    notes = st.text_area(
                        "Additional Notes:",
                        placeholder="Any additional context or notes..."
                    )
                    
                    submit_review = st.form_submit_button("Submit Expert Review", type="primary")
                    
                    if submit_review:
                        if expert_answer and expert_sources and expert_credentials:
                            with st.spinner("Submitting expert review..."):
                                result = submit_expert_review(
                                    selected_question['id'],
                                    expert_answer,
                                    expert_sources,
                                    expert_credentials,
                                    confidence_level,
                                    notes
                                )
                                
                                if result:
                                    st.success("✅ Expert review submitted successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to submit expert review")
                        else:
                            st.error("Please fill in all required fields")
    else:
        st.info("No questions pending expert review")

def render_faq_integration():
    """Render the FAQ integration interface."""
    st.header("📚 FAQ Integration")
    
    if not st.session_state.expert_mode:
        st.warning("Please enable Expert Mode in the sidebar to access this dashboard.")
        return
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    # Get pending integrations
    pending_data = get_pending_integrations()
    
    if pending_data and pending_data.get('pending_integrations'):
        integrations = pending_data['pending_integrations']
        st.success(f"Found {len(integrations)} questions ready for FAQ integration")
        
        # Display integrations
        for integration in integrations:
            with st.expander(f"Question: {integration['question'][:50]}..."):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Question:** {integration['question']}")
                    st.write(f"**Language:** {integration['language']}")
                    st.write(f"**Times Asked:** {integration['frequency_count']}")
                    st.write(f"**Expert Answer:** {integration['expert_answer']}")
                    st.write(f"**Sources:** {', '.join(integration['expert_sources'])}")
                    st.write(f"**Credentials:** {integration['expert_credentials']}")
                
                with col2:
                    if st.button(f"Integrate to FAQ", key=f"integrate_{integration['id']}"):
                        with st.spinner("Integrating to FAQ..."):
                            result = integrate_to_faq(integration['id'])
                            
                            if result and result.get('success'):
                                st.success("✅ Successfully integrated to FAQ!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to integrate to FAQ")
                                if result:
                                    st.write("Validation issues:")
                                    for error in result.get('validation', {}).get('errors', []):
                                        st.write(f"• {error}")
    else:
        st.info("No questions ready for FAQ integration")

def render_system_stats():
    """Render system statistics."""
    st.header("📊 System Statistics")
    
    # Cache Stats
    st.subheader("Cache Statistics")
    cache_stats = get_cache_stats()
    
    if cache_stats:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if cache_stats.get('type') == 'redis':
                st.metric("Cache Type", "Redis")
                st.metric("Connected Clients", cache_stats.get('connected_clients', 0))
            else:
                st.metric("Cache Type", "Memory")
                st.metric("Cached Items", cache_stats.get('cached_items', 0))
        
        with col2:
            if cache_stats.get('type') == 'redis':
                st.metric("Memory Usage", cache_stats.get('used_memory_human', '0B'))
                st.metric("Cache Hits", cache_stats.get('keyspace_hits', 0))
        
        with col3:
            if cache_stats.get('type') == 'redis':
                st.metric("Cache Misses", cache_stats.get('keyspace_misses', 0))
                hit_rate = 0
                if cache_stats.get('keyspace_hits', 0) + cache_stats.get('keyspace_misses', 0) > 0:
                    hit_rate = cache_stats.get('keyspace_hits', 0) / (cache_stats.get('keyspace_hits', 0) + cache_stats.get('keyspace_misses', 0))
                st.metric("Hit Rate", f"{hit_rate:.2%}")
    else:
        st.error("Unable to retrieve cache statistics")
    
    # Expert Stats
    st.subheader("Expert Review Statistics")
    expert_stats = get_expert_stats()
    
    if expert_stats:
        stats = expert_stats.get('question_statistics', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Questions", stats.get('total_questions', 0))
        
        with col2:
            st.metric("Pending Review", stats.get('pending_questions', 0))
        
        with col3:
            st.metric("Reviewed", stats.get('reviewed_questions', 0))
        
        with col4:
            confidence_threshold = expert_stats.get('confidence_threshold', 0.7)
            st.metric("Confidence Threshold", f"{confidence_threshold:.1f}")
        
        # Top frequent questions
        if stats.get('top_frequent_questions'):
            st.write("**Top Frequent Questions:**")
            for q in stats['top_frequent_questions']:
                st.write(f"• {q['question']} (asked {q['frequency']} times, status: {q['status']})")
    else:
        st.error("Unable to retrieve expert statistics")

if __name__ == "__main__":
    main() 