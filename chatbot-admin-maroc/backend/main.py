from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue sur le Chatbot Administratif Marocain 🇲🇦"}
