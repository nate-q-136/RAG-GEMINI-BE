# RAG Gemini Backend

A backend service for chat applications using Google Gemini Pro with Retrieval Augmented Generation (RAG) capabilities. This system enables users to engage in AI-driven conversations and upload documents, allowing AI to answer queries based on the document content.

![Demo GIF](demo.gif)

## 🌟 Features

- **Chat with Google Gemini Pro**
- **RAG support** for various file formats:
  - PDF
  - DOCX
  - CSV
- **Vector embeddings** storage using FAISS
- **Real-time chat** via WebSocket
- **Firebase Storage** integration for file management

## 🔧 Tech Stack

- **Django** (Web Framework)
- **Django Channels** (WebSocket Support)
- **LangChain** (Language Model Chaining)
- **Google Gemini Pro** (AI Model)
- **FAISS** (Vector Similarity Search)
- **HuggingFace Embeddings** (Text Embedding Models)
- **Firebase Storage** (Cloud Storage)

## 🚀 Installation Guide

### Prerequisites

- Python 3.8+
- Redis server (for WebSocket management)
- Google Gemini API key
- Firbase Credentials key

### Setup Steps

1. **Clone the Repository**
```bash
git clone https://github.com/nate-q-136/RAG-GEMINI-BE.git
cd rag-gemini-backend
```

2. **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Create an .env File**
```env
SECRET_KEY = django-secretkey
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini_model_available
FIRBASE_KEY = path_to_key_firebase_json
```

5. **Run Migrations**
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

6. **Start the Development Server**
```bash
python manage.py runserver
```

## 🔌 WebSocket Endpoints

- **Chat Endpoint**: `ws://localhost:8000/ws/chat/<room_id>/`

### Message Format
```json
// Normal chat message
{
  "message": {
    "content": "Your question here",
    "mode": "normal"
  }
}

// RAG-enabled message with document
{
  "message": {
    "content": "Your question about the document",
    "mode": "rag"
  },
  "attachments": [
    {
      "file_name": "document.pdf",
      "url": "firebase_storage_url"
    }
  ]
}
```

## 🌐 API Endpoints

### File Upload
- **URL**: `/api/upload/`
- **Method**: `POST`
- **Description**: Upload files to Firebase Storage
- **Request Body**: Form data containing the file

### Chat History (Update soon)

## 🔗 Useful Links

- [Frontend Repository](https://github.com/nate-q-136/RAG-GEMINI-FE.git)

## 🛠️ Development

### Project Structure
```
rag_gemini_backend/
├── firebase/               # Firebase configuration
├── rag_gemini_services/    # Core application services
├── utils/                  # Utility functions
│   ├── gemini_agent/       # Gemini AI implementation
│   └── urls.py             # URL management utilities
└── manage.py               # Django management script
```

### Key Components

1. **Gemini Agent** – Manages AI interactions and RAG functionality.
2. **WebSocket Consumer** – Handles real-time chat and WebSocket communications.
3. **Firebase Integration** – Manages file uploads and downloads.
4. **FAISS Vector Store** – Stores and retrieves document embeddings for RAG workflows.

## 🔒 Security Guidelines

- Never commit your `.env` file to version control.
- Keep sensitive data (API keys and Firebase credentials) private.
- Ensure authentication and authorization mechanisms are enforced for production environments.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Nate-Q** – [GitHub](https://github.com/nate-q-136)

## 🙏 Acknowledgments

- Google Gemini Pro Team
- LangChain Community
- Django Developers
- FAISS Contributors
- Open Source Community

