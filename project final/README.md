# Intelligent Moroccan Admin Assistant

## Requirements
*   **Python 3.8+**
*   **Node.js 16+**
*   **Ollama** (for local AI models)

## Quick Start

### 1. Setup AI Models
Ensure Ollama is installed and running, then pull a compatible model:
```bash
ollama pull command-r:7b
```

### 2. Run Backend
Open a terminal and run:
```bash
cd "chatbotLLMpouradministrationpublique/backend"
# Create/Activate virtual environment (optional but recommended)
# python -m venv venv
# .\venv\Scripts\activate

pip install -r requirements.txt
python app.py
```
*Backend runs on: http://localhost:5000*

### 3. Run Frontend
Open a **new** terminal and run:
```bash
cd "chatbotLLMpouradministrationpublique/frontend"
npm install
npm run dev
```
*Frontend runs on: http://localhost:3000* (or similar)
