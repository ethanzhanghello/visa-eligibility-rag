# 🌍 Green Card RAG Helper - Simple UI

A clean, simple interface for testing all features of the Green Card RAG Helper system.

## 🚀 Quick Start

### 1. Start the API Server
```bash
python3 start_server.py
```

### 2. Start the UI
```bash
python3 start_ui.py
```

### 3. Access the UI
Open your browser and go to: **http://localhost:8501**

## 📱 UI Features

### 🔍 Query Interface
- **Ask Questions**: Submit immigration questions in English or Chinese
- **Language Selection**: Choose between auto, English (en), or Chinese (zh)
- **Real-time Processing**: Get instant responses with confidence scoring
- **Detailed Metrics**: View confidence scores, context relevance, and more

### 👨‍💼 Expert Review Dashboard
- **View Pending Questions**: See questions flagged for expert review
- **Question Details**: View confidence scores, frequency, and timestamps
- **Submit Reviews**: Expert review submission interface (ready for implementation)

### 📊 System Information
- **Configuration**: View LLM settings, confidence thresholds, and API status
- **System Status**: Check if all managers are running properly
- **Detailed Metrics**: View confidence weights and immigration terms

## 🧪 Testing Features

### Test English Questions
- "What documents do I need for EB-2?"
- "How long does the green card process take?"
- "What are the requirements for family-based immigration?"

### Test Chinese Questions
- "我需要哪些文件来申请绿卡？"
- "绿卡申请需要多长时间？"
- "家庭移民有什么要求？"

### Test Expert Review System
1. Ask a question that gets low confidence
2. Check the Expert Review tab
3. View the pending questions
4. See confidence metrics and frequency data

## 🔧 Troubleshooting

### UI Not Loading
- Make sure the API server is running: `python3 start_server.py`
- Check if port 8501 is available
- Try refreshing the browser

### API Connection Issues
- Verify API is running on port 8000
- Check the health endpoint: `curl http://localhost:8000/health`
- Ensure no firewall blocking localhost connections

### Streamlit Issues
- Install streamlit: `pip install streamlit`
- Check Python path: `python3 -m streamlit --version`

## 📊 Expected Results

### High Confidence Responses
- Confidence score > 0.7
- Green status indicators
- Detailed immigration information

### Low Confidence Responses
- Confidence score < 0.7
- Red status indicators
- Questions flagged for expert review
- Appears in Expert Review dashboard

## 🎯 Next Steps

1. **Test All Features**: Use the UI to test English and Chinese queries
2. **Expert Review**: Check the expert review dashboard
3. **System Info**: Verify all components are working
4. **UI Improvements**: Based on testing, we can enhance the interface

## 🔗 API Endpoints Used

- `GET /health` - Health check
- `POST /query` - Submit questions
- `GET /expert/pending-questions` - Get pending reviews
- `GET /system/info` - System information

---

**Ready to test!** Open http://localhost:8501 in your browser and start asking immigration questions. 