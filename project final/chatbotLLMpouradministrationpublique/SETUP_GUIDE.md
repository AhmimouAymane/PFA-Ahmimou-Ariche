# 🚀 Chatbot Setup Guide - Local LLM Models

## What's Been Done

✅ **Frontend Language Display Fixed**
- Added Noto Sans Arabic fonts for proper Arabic/Amazigh rendering
- Added RTL (right-to-left) support for Arabic text
- Language selector now properly displays all 4 languages

✅ **Backend Intelligence Upgraded**
- Replaced template-based responses with intelligent Ollama LLM
- Added conversation history for context-aware responses
- Supports multiple languages (French, Arabic, Amazigh, English)
- Natural ChatGPT-like conversations

✅ **Models Selected**
- **Aya Expanse 8B** - Best for multilingual (23 languages)
- **Command R 7B** - Optimized for MENA region (Arabic/French)
- **Qwen 2.5 7B** - Excellent general multilingual model

## 📋 Installation Steps

### Step 1: Install Ollama

1. **Download & Install**:
   - OllamaSetup.exe should be in your Downloads folder (already downloaded)
   - If not, download from: https://ollama.com/download/windows
   - Double-click OllamaSetup.exe and follow installation wizard
   - Ollama will start automatically after installation

2. **Verify Installation**:
   ```powershell
   ollama --version
   ```

### Step 2: Install Python Dependencies

```powershell
cd "c:\Users\Administrator\Desktop\rapport pfa\chatbotLLMpouradministrationpublique\backend"
pip install -r requirements.txt
```

### Step 3: Download AI Models

**Option A: Automated Setup (Recommended)**
```powershell
python scripts/setup_ollama.py
```
This script will guide you through downloading models interactively.

**Option B: Manual Download**
```powershell
# Download recommended models (choose one or all)
ollama pull aya-expanse:8b        # 23 languages, best multilingual
ollama pull command-r:7b           # MENA specialized
ollama pull qwen2.5:7b            # Fast multilingual

# Verify downloads
ollama list
```

### Step 4: Test Models (Optional but Recommended)

```powershell
python scripts/test_ollama_models.py
```
This will test all downloaded models and recommend the best one.

## 🎯 Running the Chatbot

### Start Backend

```powershell
cd "c:\Users\Administrator\Desktop\rapport pfa\chatbotLLMpouradministrationpublique\backend"
python app.py
```

The backend should start on `http://localhost:5000`

### Start Frontend

Open a NEW terminal:
```powershell
cd "c:\Users\Administrator\Desktop\rapport pfa\chatbotLLMpouradministrationpublique\frontend"
npm run dev
```

The frontend will open at `http://localhost:5173` (or displayed port)

## ✅ Testing Checklist

### 1. Test Language Display
- [ ] Open browser at frontend URL
- [ ] Check language selector dropdown
- [ ] Verify all 4 languages are visible: Français, العربية, ⵜⴰⵎⴰⵣⵉⵖⵜ, English
- [ ] Switch between languages - dropdown should render correctly

### 2. Test Basic Chatbot
- [ ] Register a new account or login
- [ ] Send French query: "Comment obtenir une carte d'identité?"
- [ ] Verify response is intelligent (not template-like)
- [ ] Response should mention: documents, lieu, délai, coût

### 3. Test Conversation Context
- [ ] Send follow-up: "Combien ça coûte?"
- [ ] Response should be context-aware about CNIE cost (gratuit première carte)
- [ ] Send: "Et la validité?"
- [ ] Should answer about 10 years validity

### 4. Test Arabic
- [ ] Switch language to Arabic
- [ ] Send: "كيف احصل على جواز السفر؟"
- [ ] Response should be in Arabic
- [ ] Verify Arabic text displays correctly (right-to-left)

### 5. Test Different Topics
- [ ] "Je veux me marier" - Marriage procedure
- [ ] "RAMED ou CNSS?" - Should explain difference
- [ ] "Comment avoir un permis de conduire?" - Driving license

## 🎨 Expected Behavior

**OLD (Template-based)**:
```
User: Comment obtenir une carte d'identité?
Bot: Pour obtenir une carte d'identité nationale (CNIE) au Maroc:
1. Documents requis: acte de naissance récent, certificat de résidence...
[Rigid template response]
```

**NEW (Intelligent)**:
```
User: Comment obtenir une carte d'identité?
Bot: Pour obtenir votre carte d'identité nationale (CNIE), voici les étapes:

Tout d'abord, vous devrez vous rendre à la commune ou l'arrondissement de votre 
domicile avec ces documents:
- Un acte de naissance récent
- Un certificat de résidence
- 2 photos d'identité récentes

Le processus prend environ 2 semaines et la première carte est gratuite. 
Elle sera valable pendant 10 ans.

Avez-vous besoin de plus de détails sur l'une de ces étapes?
```

## 🔧 Troubleshooting

### "Ollama service not running"
- Start Ollama from Windows Start menu
- Or run: `ollama serve` in a terminal

### "No models found"
- Download models using Step 3 above
- Verify with: `ollama list`

### "Model response takes too long"
- First query is always slower (model loading)
- Subsequent queries should be faster
- Consider using smaller model (qwen2.5:7b) if slow

### "Language still not displaying"
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Check browser console for font loading errors

## 📊 Model Performance

From testing with similar setups:

| Model | Speed | Quality | Languages | Recommend |
|-------|-------|---------|-----------|-----------|
| Aya Expanse 8B | Medium | Excellent | 23 | ⭐⭐⭐⭐⭐ |
| Command R 7B | Fast | Very Good | 10+ | ⭐⭐⭐⭐ |
| Qwen 2.5 7B | Fast | Good | 29 | ⭐⭐⭐⭐ |

**Recommendation**: Use `aya-expanse:8b` if you have 16GB+ RAM, otherwise use `command-r:7b`

## 🎉 Success Criteria

Your chatbot is working correctly if:
- ✅ All languages display in dropdown
- ✅ Responses are natural and conversational
- ✅ Follow-up questions get context-aware answers  
- ✅ Arabic/French responses are accurate
- ✅ No template-sounding responses

## 📞 Need Help?

If you encounter issues:
1. Check Ollama is running: `ollama list`
2. Check backend logs in terminal
3. Check browser console (F12) for errors
4. Verify database is running (MySQL)
