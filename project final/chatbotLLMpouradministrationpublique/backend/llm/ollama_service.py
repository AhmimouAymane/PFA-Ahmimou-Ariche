"""
Ollama Service - Local LLM Model Management
Manages interaction with Ollama for local model inference
"""
import requests
import json
from typing import Dict, List, Optional
import subprocess
import time

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize Ollama service"""
        self.base_url = base_url
        self.current_model = None
        self.available_models = []
        print(f"Initializing Ollama Service at {base_url}...")
        
    def check_ollama_running(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """List all downloaded Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                self.available_models = [model['name'] for model in data.get('models', [])]
                return self.available_models
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Download a model from Ollama library"""
        try:
            print(f"Pulling model: {model_name}...")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True
            )
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'status' in data:
                        print(f"  {data['status']}")
                    if data.get('status') == 'success':
                        print(f"✓ Model {model_name} downloaded successfully!")
                        return True
            return True
        except Exception as e:
            print(f"Error pulling model {model_name}: {e}")
            return False
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a model"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error deleting model {model_name}: {e}")
            return False
    
    def generate(
        self,
        model: str,
        prompt: str,
        system: str = None,
        context: List[Dict] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """Generate text using Ollama model"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            if system:
                payload["system"] = system
            
            if context:
                payload["context"] = context
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120  # 2 minutes timeout for generation
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error generating with {model}: {e}")
            return None
    
    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """Chat with Ollama model using conversation history"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['message']['content']
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error chatting with {model}: {e}")
            return None
    
    def set_model(self, model_name: str) -> bool:
        """Set the current active model"""
        models = self.list_models()
        if model_name in models:
            self.current_model = model_name
            print(f"Active model set to: {model_name}")
            return True
        else:
            print(f"Model {model_name} not found. Available: {models}")
            return False
