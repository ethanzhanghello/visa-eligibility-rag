# Green Card RAG Helper 🌍

A bilingual (English/Chinese) RAG-based assistant for answering immigration-related questions, powered by GPT-3.5-turbo and ChromaDB. Features automatic low-confidence question detection and expert review workflow for continuous improvement.

## 📚 Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Low-Confidence Question Detection](#low-confidence-question-detection)
- [Expert Review Workflow](#expert-review-workflow)
- [API Endpoints](#api-endpoints)
- [Documentation](#documentation)
- [Visuals](#visuals)
- [Support](#support)
- [Roadmap](#roadmap)
- [Project Status](#project-status)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview
Green Card RAG Helper is an intelligent assistant designed to provide accurate, context-aware responses to immigration-related questions in both English and Chinese. Using Retrieval-Augmented Generation (RAG), it combines the power of vector search with language models to deliver precise, factual answers based on reliable immigration information.

**Key Features:**
- **Bilingual Support**: English and Chinese question handling
- **Confidence Scoring**: Automatic detection of low-confidence responses
- **Expert Review System**: Professional validation of uncertain answers
- **Anti-Bias Protection**: Source tracking and validation pipeline
- **Continuous Learning**: Integration of expert-reviewed content into FAQ database

## 🛠️ Technologies Used
- **Language Model**: OpenAI GPT-3.5-turbo
- **Vector Database**: ChromaDB
- **Embeddings**: Multilingual E5 Base Model
- **API**: FastAPI
- **Backend**: Python 3.9+
- **Caching**: Redis (with in-memory fallback)
- **Testing**: pytest
- **Dependencies Management**: pip

## 📋 Requirements
- Python 3.9 or higher
- OpenAI API key
- 2GB+ free disk space for vector database
- RAM: 4GB minimum, 8GB recommended
- Internet connection for API calls
- FastAPI and Uvicorn
- Redis (optional, falls back to in-memory cache)

## 💻 Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/green-card-rag-helper.git
cd green-card-rag-helper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

4. (Optional) Install and start Redis for persistent caching:
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis
```

## 🚀 Usage
1. Populate the vector database:
```bash
python populate_db.py
```

2. Run the API server:
```bash
uvicorn src.api.main:app --reload
```

3. API Endpoints:
- `POST /query` - Submit immigration questions
- `GET /health` - Check API health
- `POST /cache/clear` - Clear all cached responses
- `GET /cache/stats` - View cache statistics

4. Example queries:
```python
from src.retrieval.retrieval_manager import RetrievalManager
from src.llm.llm_manager import LLMManager

retrieval_manager = RetrievalManager()
llm_manager = LLMManager()

# English query
results = retrieval_manager.process_query("What documents do I need for EB-2?")
response = llm_manager.generate_response(context, query)

# Chinese query
results = retrieval_manager.process_query("我需要哪些文件来申请 EB-2？")
response = llm_manager.generate_response(context, query)
```

## 🔍 Low-Confidence Question Detection

The system automatically detects when it's not confident in its responses and flags them for expert review.

### How It Works:
1. **Confidence Scoring**: Each response is evaluated based on:
   - Context relevance to the question
   - Source quality and official documentation
   - Response length and completeness
   - Presence of immigration-specific terminology

2. **Automatic Flagging**: Questions with confidence scores below 0.7 are automatically flagged for expert review

3. **Frequency Tracking**: Repeated low-confidence questions are prioritized for review

### Confidence Factors:
- **Context Relevance**: How well the retrieved context matches the question
- **Source Quality**: Presence of official government sources
- **Response Completeness**: Length and structure of the answer
- **Immigration Terms**: Proper use of immigration-specific vocabulary

## 👨‍💼 Expert Review Workflow

### For Users:
1. **Ask Questions**: Submit immigration questions normally
2. **Get Responses**: Receive immediate answers with confidence scores
3. **Transparency**: See if your question was flagged for expert review

### For Experts:
1. **Review Dashboard**: Access pending questions via `/expert/pending-questions`
2. **Submit Reviews**: Provide professional answers with sources via `/expert/review`
3. **Validation**: System validates reviews for bias and quality
4. **Integration**: Approved answers are added to the FAQ database

### Anti-Bias Features:
- **Source Validation**: Requires official government sources
- **Expert Credentials**: Tracks reviewer qualifications
- **Audit Trail**: Complete history of all changes
- **Quality Checks**: Validates answer length, relevance, and completeness

## 🔌 API Endpoints

### Core Endpoints
- `POST /query` - Submit questions and get responses with confidence scores
- `GET /health` - Check system health
- `GET /cache/stats` - View caching statistics

### Expert Review Endpoints
- `GET /expert/pending-questions` - Get questions pending expert review
- `GET /expert/question/{question_id}` - Get detailed question information
- `POST /expert/review` - Submit expert review for a question
- `GET /expert/stats` - Get expert review statistics

### FAQ Integration Endpoints
- `GET /faq/pending-integrations` - Get approved questions ready for FAQ integration
- `POST /faq/integrate/{question_id}` - Integrate expert-reviewed question into FAQ
- `GET /faq/validate/{question_id}` - Validate expert review for bias/issues
- `GET /faq/integration-stats` - Get FAQ integration statistics

### Example API Usage:
```bash
# Submit a question
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What documents do I need for EB-2?", "language": "en"}'

# Get pending expert reviews
curl "http://localhost:8000/expert/pending-questions"

# Submit expert review
curl -X POST "http://localhost:8000/expert/review" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "q_1_abc123",
    "expert_answer": "For EB-2, you need Form I-140, medical examination, and police certificates.",
    "expert_sources": ["uscis.gov/forms/i-140", "state.gov/visa"],
    "expert_credentials": "Immigration Attorney, 10+ years experience",
    "confidence_level": "high",
    "notes": "Common question that needs clear guidance"
  }'
```

## 📖 Documentation
Detailed documentation is available in the following sections:
- [src/embeddings/](src/embeddings/) - Embedding generation
- [src/vector_db/](src/vector_db/) - Vector database operations
- [src/retrieval/](src/retrieval/) - Query processing
- [src/llm/](src/llm/) - Language model integration
- [src/api/](src/api/) - API and confidence system

## 📸 Visuals
```
User Query (EN/CN) → Vector Search → Context Retrieval → LLM Response → Confidence Scoring
     ↓                    ↓              ↓                  ↓                ↓
"EB-2 requirements" → Embeddings → Relevant Docs → Formatted Answer → Score: 0.85 ✅
                                                                      Score: 0.45 ❌ → Expert Review
```

## 🆘 Support
For support and questions:
- Open an issue on GitHub
- Email: ezhang0606@gmail.com
- Documentation: [Wiki](https://github.com/yourusername/green-card-rag-helper/wiki)

## 🗺️ Roadmap
- [x] Basic RAG pipeline implementation
- [x] Bilingual support (EN/CN)
- [x] GPT-3.5-turbo integration
- [x] Confidence scoring system
- [x] Expert review workflow
- [x] Anti-bias validation
- [x] FAQ integration system
- [ ] Web interface
- [ ] Additional language support
- [ ] Custom fine-tuned model
- [ ] Mobile app

## 📊 Project Status
**Status**: Active Development

Current focus:
- Improving response accuracy through expert review
- Expanding the knowledge base with validated content
- Optimizing confidence scoring algorithms
- Adding more comprehensive test coverage

## 🤝 Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 