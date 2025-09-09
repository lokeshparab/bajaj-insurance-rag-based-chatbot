# Bajaj Insurance RAG-Based Chatbot

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-active-green.svg)

A sophisticated Retrieval-Augmented Generation (RAG) chatbot specifically designed for Bajaj Insurance customer queries. This intelligent chatbot leverages advanced natural language processing to provide accurate, contextual responses about insurance policies, claims, and services.

## 🚀 Features

- **Intelligent Query Processing**: Advanced NLP capabilities for understanding complex insurance queries
- **RAG Architecture**: Combines retrieval and generation for accurate, context-aware responses
- **Bajaj Insurance Specific**: Trained on Bajaj Insurance policies, procedures, and FAQ data
- **Real-time Responses**: Fast and efficient query processing
- **Contextual Understanding**: Maintains conversation context for better user experience
- **Multi-format Support**: Handles text queries about various insurance products
- **Scalable Architecture**: Built to handle multiple concurrent users

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI/Streamlit
- **RAG Framework**: LangChain/LangGraph
- **Vector Database**: Pinecone/AstraDB
- **LLM**: Llama 3/GPT-OSS
- **Embeddings**: JinaAI
- **Frontend**: Streamlit/Gradio (if applicable)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lokeshparab/bajaj-insurance-rag-based-chatbot.git
   cd bajaj-insurance-rag-based-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_ENVIRONMENT=your_pinecone_environment
   DATABASE_URL=your_database_url
   ```

5. **Initialize the vector database**
   ```bash
   python scripts/initialize_db.py
   ```

## 🚀 Usage

### Running the Application

1. **Start the backend server**
   ```bash
   python app.py
   ```

2. **Access the chatbot**
   - Open your browser and navigate to `http://localhost:8000`
   - Or use the API endpoints directly

### API Endpoints

- `POST /chat` - Send a query to the chatbot
- `GET /health` - Check application health
- `POST /feedback` - Submit user feedback

### Example API Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "What is the claim process for my health insurance policy?",
        "session_id": "unique_session_id"
    }
)

print(response.json())
```

## 📊 Project Structure

```
bajaj-insurance-rag-based-chatbot/
│
├── app.py                     # Main application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # Project documentation
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Multi-container Docker setup
│
├── src/
│   ├── __init__.py
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── rag_pipeline.py        # Main RAG pipeline implementation
│   │   ├── document_loader.py     # Bajaj Insurance document loading
│   │   ├── embeddings.py          # Document embedding generation
│   │   ├── retriever.py           # Similarity search and retrieval
│   │   ├── generator.py           # Response generation with LLM
│   │   └── conversation_manager.py # Session and context management
│   │
│   ├── data/
│   │   ├── documents/             # Bajaj Insurance policy documents
│   │   │   ├── health_policies/   # Health insurance documents
│   │   │   ├── motor_policies/    # Motor insurance documents  
│   │   │   ├── travel_policies/   # Travel insurance documents
│   │   │   └── general_info/      # General Bajaj Insurance info
│   │   ├── processed/             # Preprocessed document chunks
│   │   ├── vectorstore/           # Vector database storage
│   │   └── sample_queries.txt     # Example queries for testing
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── document_processor.py  # PDF/DOCX processing utilities
│   │   ├── text_splitter.py      # Text chunking strategies
│   │   ├── config.py             # Application configuration
│   │   ├── logger.py             # Logging setup
│   │   └── validators.py         # Input validation
│   │
│   └── api/
│       ├── __init__.py
│       ├── routes.py             # FastAPI route definitions
│       ├── models.py             # Pydantic request/response models
│       └── middleware.py         # Custom middleware
│
├── scripts/
│   ├── initialize_vectordb.py    # Vector database setup
│   ├── process_documents.py      # Document ingestion pipeline
│   ├── evaluate_responses.py     # Response quality evaluation
│   └── update_knowledge_base.py  # Knowledge base updates
│
├── tests/
│   ├── __init__.py
│   ├── test_rag_pipeline.py      # RAG pipeline functionality tests
│   ├── test_api_endpoints.py     # API endpoint tests
│   ├── test_document_processing.py # Document processing tests
│   └── test_utilities.py         # Utility function tests
│
├── notebooks/
│   ├── data_exploration.ipynb    # Document analysis and exploration
│   ├── model_evaluation.ipynb    # Model performance evaluation
│   └── response_analysis.ipynb   # Response quality analysis
│
├── config/
│   ├── logging_config.yaml       # Logging configuration
│   ├── model_config.yaml         # Model parameters
│   └── database_config.yaml      # Database settings
│
└── docs/
    ├── api_documentation.md      # Detailed API documentation
    ├── deployment_guide.md       # Production deployment guide
    ├── bajaj_policies_guide.md   # Bajaj Insurance policies overview
    └── troubleshooting.md        # Common issues and solutions
```

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python -m pytest tests/test_api.py          # Test API endpoints
python -m pytest tests/test_rag.py          # Test RAG components  
python -m pytest tests/test_agent.py        # Test agent functionality

# Run with coverage
python -m pytest tests/ --cov=src/
```

### Evaluate RAG Performance

```bash
python -m src.rag_component.evaluation
```

## 🚀 Deployment

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t bajaj-insurance-chatbot .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 --env-file .env bajaj-insurance-chatbot
   ```

### Using Docker Compose

```bash
docker-compose up -d
```

### Cloud Deployment

The application can be deployed on various cloud platforms:

- **AWS**: Use ECS, Lambda, or EC2
- **Google Cloud**: Deploy on Cloud Run or Compute Engine
- **Azure**: Use Container Instances or App Service
- **Heroku**: Direct deployment with Procfile

## 📈 Performance Optimization

- **Caching**: Implement Redis for frequently asked questions
- **Async Processing**: Use async/await for better concurrency
- **Vector Database Optimization**: Tune similarity search parameters
- **Model Optimization**: Use quantized models for faster inference

## 🔒 Security

- API key management through environment variables
- Input validation and sanitization
- Rate limiting to prevent abuse
- HTTPS encryption in production
- User session management

## 📊 Monitoring and Analytics

- Log all user interactions for analysis
- Track response accuracy and user satisfaction
- Monitor system performance metrics
- Generate usage reports

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run code formatting:
   ```bash
   black src/
   isort src/
   ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Lokesh Parab**
- GitHub: [@lokeshparab](https://github.com/lokeshparab)
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

- Bajaj Insurance for domain expertise
- OpenAI for GPT models
- LangChain community for RAG frameworks
- All contributors and testers

## 📞 Support

For support and questions:
- Create an [Issue](https://github.com/lokeshparab/bajaj-insurance-rag-based-chatbot/issues)
- Email: your.email@example.com

## 🔄 Changelog

### Version 1.0.0
- Initial release with basic RAG functionality
- Support for insurance policy queries
- REST API implementation
- Docker containerization

---

⭐ If you found this project helpful, please give it a star on GitHub!