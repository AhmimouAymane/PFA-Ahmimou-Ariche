# Chatbot LLM pour l'Administration Publique Marocaine

A specialized conversational assistant based on Large Language Models (LLM) to respond to citizen queries related to administrative procedures, forms, and steps in the Moroccan public administration system.

## Features

- 🤖 **Intelligent Chatbot** with RAG (Retrieval-Augmented Generation)
- 🌍 **Multilingual Support** (French, Arabic, Amazigh, English)
- 🔐 **User Authentication** (Sign in/Sign up)
- 💬 **Conversation History** - Save and retrieve past conversations
- 📚 **Morocco-specific Knowledge Base** - Information about Moroccan administrative procedures
- ⚡ **Real-time Responses** with optimized performance
- 🎨 **Modern UI** with React

## Tech Stack

### Backend
- Python 3.10+
- Flask (REST API)
- LangChain (LLM orchestration)
- OpenAI API (GPT-4)
- MySQL (Database)
- ChromaDB (Vector Store)
- JWT (Authentication)

### Frontend
- React 18+
- React Router
- Axios
- Styled Components
- Context API

## Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- MySQL 8.0 or higher
- OpenAI API Key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OpenAI API key and database credentials

# Initialize database
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# Run server
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install

# Create .env file
cp .env.example .env
# Edit .env and add API URL

# Run development server
npm start
```

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/chatbot_admin
SECRET_KEY=your_secret_key_for_jwt
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000
```

## Usage

1. Start MySQL database
2. Start backend server (port 5000)
3. Start frontend server (port 3000)
4. Open browser at http://localhost:3000
5. Sign up or sign in
6. Start chatting with the administrative assistant

## Project Structure

```
chatbot LLM pour administration publique/
├── backend/
│   ├── api/           # API routes
│   ├── services/      # Business logic
│   ├── models/        # Database models
│   ├── database/      # DB utilities
│   ├── llm/          # LLM integration
│   └── utils/        # Helper functions
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── hooks/       # Custom hooks
│   └── public/
└── database/
    └── migrations/    # Database migrations
```

## License

MIT License

