# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Prerequisites Check
- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed  
- ✅ MySQL installed and running
- ✅ OpenAI API key ready

### 2. Database Setup (One-time)

```sql
CREATE DATABASE chatbot_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate

pip install -r requirements.txt

# Create .env file
echo OPENAI_API_KEY=your_key_here > .env
echo DATABASE_URL=mysql+pymysql://root:password@localhost:3306/chatbot_admin >> .env
echo SECRET_KEY=your_secret_key >> .env
echo JWT_SECRET_KEY=your_jwt_secret >> .env

# Run the app (creates tables)
python app.py

# In another terminal, seed documents
python scripts/seed_documents.py
```

### 4. Frontend Setup

```bash
cd frontend
npm install

# Create .env file
echo VITE_API_URL=http://localhost:5000 > .env

# Start dev server
npm run dev
```

### 5. Open Browser

Go to: **http://localhost:3000**

## 🎯 What You Can Do

1. **Register** - Create a new account
2. **Login** - Sign in with your credentials
3. **Chat** - Ask questions about Moroccan administration in:
   - 🇫🇷 French
   - 🇸🇦 Arabic  
   - ⵎⴰⵣⵉⵖ Amazigh
   - 🇬🇧 English

4. **View History** - Access all your past conversations
5. **Switch Languages** - Change language on the fly

## 📝 Example Questions

- "Comment obtenir une carte d'identité ?"
- "Quels documents pour un passeport ?"
- "كيف أحصل على جواز سفر؟"
- "How to get a residence certificate?"

## 🐛 Troubleshooting

**Backend won't start?**
- Check MySQL is running
- Verify DATABASE_URL in .env
- Check OpenAI API key is valid
- Ensure pymysql is installed: `pip install pymysql`

**Frontend can't connect?**
- Ensure backend is running on port 5000
- Check VITE_API_URL in frontend/.env
- Check browser console for errors

**No responses from chatbot?**
- Verify OpenAI API key has credits
- Check backend logs for errors
- Ensure documents were seeded (run seed_documents.py)

## 📚 Next Steps

- Read [SETUP.md](SETUP.md) for detailed setup
- Check [README.md](README.md) for features and architecture
- Customize documents in `backend/scripts/seed_documents.py`

## 💡 Tips

- The vector store is created automatically on first run
- Conversations are saved automatically
- You can add more documents to the knowledge base
- Language detection is automatic but you can override it

Happy chatting! 🎉

