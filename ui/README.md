# Green Card RAG Helper UI 🌍

A comprehensive web interface for the Green Card RAG Helper system, built with Streamlit.

## Features

### 🔍 Query Interface
- Submit immigration questions in English or Chinese
- Real-time confidence scoring and analysis
- Detailed confidence breakdown (context relevance, source quality, etc.)
- Usage statistics and token tracking
- Automatic low-confidence question flagging

### 👨‍💼 Expert Review Dashboard
- View questions pending expert review
- Submit professional answers with sources
- Track question frequency and confidence scores
- Expert credential tracking
- Anti-bias validation

### 📚 FAQ Integration
- Review approved expert answers
- Integrate validated content into FAQ database
- Source tracking and validation
- Quality assurance checks

### 📊 System Statistics
- Cache performance metrics
- Expert review statistics
- Question frequency analysis
- System health monitoring

## Setup

### Prerequisites
1. Make sure the API server is running:
```bash
uvicorn src.api.main:app --reload
```

2. Install UI dependencies:
```bash
pip install -r requirements.txt
```

### Running the UI
```bash
streamlit run ui/app.py
```

The UI will be available at `http://localhost:8501`

## Usage

### For Regular Users
1. Navigate to the "Query Interface" tab
2. Enter your immigration question
3. Select language (auto-detect, English, or Chinese)
4. Submit and view the answer with confidence analysis
5. Check if your question was flagged for expert review

### For Experts
1. Enable "Expert Mode" in the sidebar
2. Navigate to "Expert Review Dashboard"
3. View pending questions that need review
4. Submit professional answers with proper sources
5. Use "FAQ Integration" to add validated content to the knowledge base

### System Monitoring
- Use "System Stats" to monitor cache performance
- Track expert review progress
- View question frequency patterns

## Configuration

The UI connects to the API at `http://localhost:8000` by default. To change this:

1. Edit `ui/app.py`
2. Modify the `API_BASE_URL` variable
3. Restart the Streamlit application

## Troubleshooting

### API Connection Issues
- Ensure the API server is running on port 8000
- Check that all dependencies are installed
- Verify the API endpoints are accessible

### UI Performance
- The UI automatically refreshes data when needed
- Use the refresh buttons to manually update data
- Large datasets may take a moment to load

## Security Notes

- Expert mode should only be enabled for authorized personnel
- All expert reviews are logged with credentials
- Source validation ensures only official government sources are accepted
- Audit trails track all system changes 