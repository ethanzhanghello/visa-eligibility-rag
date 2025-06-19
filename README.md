# Green Card RAG Helper

A bilingual (English/Chinese) RAG-based assistant for answering immigration-related questions.

## Features

- Bilingual support (English and Chinese)
- Semantic search using ChromaDB
- Multilingual embeddings using E5 base model
- GPT-4 powered responses
- Automatic language detection

## Setup

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

## Usage

1. Populate the vector database:
```bash
python populate_db.py
```

2. Run tests:
```bash
python test_pipeline.py
```

## Project Structure

```
green-card-rag-helper/
├── src/
│   ├── embeddings/      # Embedding generation
│   ├── vector_db/       # Vector database operations
│   ├── retrieval/       # Query processing and retrieval
│   └── llm/            # LLM interaction
├── chroma_db/          # Persistent vector database
├── populate_db.py      # Database population script
└── test_pipeline.py    # Integration tests
```

## Pipeline Flow

1. User submits a question in English or Chinese
2. Language is automatically detected
3. Question is converted to embeddings
4. Similar documents are retrieved from ChromaDB
5. Context is prepared and sent to GPT-4
6. Response is generated in the same language as the question

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 