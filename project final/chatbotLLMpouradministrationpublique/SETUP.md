# Setup Instructions

## Prerequisites

1. **Python 3.10+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download](https://nodejs.org/)
3. **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/mysql/)
4. **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

## Step 1: Database Setup

1. Install MySQL and start the service
2. Create a new database:
```sql
CREATE DATABASE chatbot_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Step 2: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file (copy from `.env.example`):
```bash
# On Windows PowerShell
Copy-Item .env.example .env

# On macOS/Linux
cp .env.example .env
```

6. Edit `.env` and add your configuration:
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/chatbot_admin
SECRET_KEY=your_secret_key_change_this
JWT_SECRET_KEY=your_jwt_secret_key_change_this
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

7. Initialize the database and seed documents:
```bash
python app.py
# Wait for "Database tables created" message

# In another terminal, seed documents:
python scripts/seed_documents.py
```

8. Start the backend server:
```bash
python app.py
```

The backend should now be running on http://localhost:5000

## Step 3: Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```bash
# On Windows PowerShell
Copy-Item .env.example .env

# On macOS/Linux
cp .env.example .env
```

4. Edit `.env`:
```
VITE_API_URL=http://localhost:5000
```

5. Start the development server:
```bash
npm run dev
```

The frontend should now be running on http://localhost:3000

## Step 4: Using the Application

1. Open your browser and go to http://localhost:3000
2. Click "S'inscrire" (Register) to create an account
3. Fill in your details and preferred language
4. After registration, you'll be logged in automatically
5. Start chatting with the administrative assistant!

## Troubleshooting

### Database Connection Issues
- Make sure MySQL is running
- Check your DATABASE_URL in `.env`
- Verify the database `chatbot_admin` exists
- Ensure pymysql is installed: `pip install pymysql`

### OpenAI API Issues
- Verify your API key is correct in `.env`
- Make sure you have credits in your OpenAI account
- Check API rate limits

### Frontend Can't Connect to Backend
- Ensure backend is running on port 5000
- Check CORS settings in `backend/config.py`
- Verify `VITE_API_URL` in frontend `.env`

### Vector Store Issues
- The vector store will be created automatically on first run
- If issues persist, delete the `chroma_db` folder and restart

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` and `FLASK_DEBUG=False`
2. Use a production WSGI server like Gunicorn
3. Configure Nginx as reverse proxy
4. Use environment variables for all secrets
5. Enable HTTPS
6. Set up proper database backups

## Support

For issues or questions, please check:
- The README.md file
- The code comments
- The project documentation

