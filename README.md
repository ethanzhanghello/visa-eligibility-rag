# Green Card RAG Helper 🌍

A bilingual (English/Chinese) RAG-based assistant for answering immigration-related questions, powered by GPT-3.5-turbo and ChromaDB.

## 📚 Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Visuals](#visuals)
- [Support](#support)
- [Roadmap](#roadmap)
- [Project Status](#project-status)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## 🎯 Overview
Green Card RAG Helper is an intelligent assistant designed to provide accurate, context-aware responses to immigration-related questions in both English and Chinese. Using Retrieval-Augmented Generation (RAG), it combines the power of vector search with language models to deliver precise, factual answers based on reliable immigration information.

## 🛠️ Technologies Used
- **Language Model**: OpenAI GPT-3.5-turbo
- **Vector Database**: ChromaDB
- **Embeddings**: Multilingual E5 Base Model
- **Backend**: Python 3.9+
- **Testing**: pytest
- **Dependencies Management**: pip

## 📋 Requirements
- Python 3.9 or higher
- OpenAI API key
- 2GB+ free disk space for vector database
- RAM: 4GB minimum, 8GB recommended
- Internet connection for API calls

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

## 🚀 Usage
1. Populate the vector database:
```bash
python populate_db.py
```

2. Run the test pipeline:
```bash
python test_pipeline.py
```

3. Example queries:
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

## 📖 Documentation
Detailed documentation is available in the following sections:
- [src/embeddings/](src/embeddings/) - Embedding generation
- [src/vector_db/](src/vector_db/) - Vector database operations
- [src/retrieval/](src/retrieval/) - Query processing
- [src/llm/](src/llm/) - Language model integration

## 📸 Visuals
```
User Query (EN/CN) → Vector Search → Context Retrieval → LLM Response
     ↓                    ↓              ↓                  ↓
"EB-2 requirements" → Embeddings → Relevant Docs → Formatted Answer
```

## 🆘 Support
For support and questions:
- Open an issue on GitHub
- Email: support@example.com
- Documentation: [Wiki](https://github.com/yourusername/green-card-rag-helper/wiki)

## 🗺️ Roadmap
- [x] Basic RAG pipeline implementation
- [x] Bilingual support (EN/CN)
- [x] GPT-3.5-turbo integration
- [ ] Web interface
- [ ] Additional language support
- [ ] Custom fine-tuned model
- [ ] API endpoints

## 📊 Project Status
**Status**: Active Development

Current focus:
- Improving response accuracy
- Expanding the knowledge base
- Optimizing retrieval pipeline
- Adding more test cases

## 🤝 Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 👏 Acknowledgments
- OpenAI for GPT-3.5-turbo
- ChromaDB team for the vector database
- E5 team for multilingual embeddings
- All contributors and testers

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 