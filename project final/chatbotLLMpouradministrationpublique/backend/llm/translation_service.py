from transformers import MarianMTModel, MarianTokenizer
import langdetect
import torch

class TranslationService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {}
        self.tokenizers = {}
        # Pre-load Arabic<->English models as requested (user mentioned ar-en, but also ar-fr is common in Morocco. 
        # The user specifically requested Helsinki-NLP/opus-mt-ar-en and en-ar. 
        # But also mentioned translating to "French or Admin Model Language". 
        # If Admin model is French, we need AR->FR. MarianMT AR->FR exists but might be less common than AR->EN->FR.
        # Direct AR->FR models exist (Helsinki-NLP/opus-mt-ar-fr). I will use direct if available or pivotal.
        # User prompt said: "Translate user input from Arabic... into French".
        # Let's try to load ar-fr if possible, or ar-en then en-fr.
        # User SPECIFICALLY said: "Model Name: Helsinki-NLP/opus-mt-ar-en" and "Helsinki-NLP/opus-mt-en-ar".
        # AND "Translate user input ... into French". 
        # If I strictly follow the user's "Translation Model" section, I have AR->EN. 
        # But if the Admin model is French, I need EN->FR as well? 
        # Or maybe the user implies the Admin model accepts English? 
        # "Public Administration Model... Language: Primarily French".
        # So I need to get to French.
        # Path: Ar -> En -> Fr? Or Ar -> Fr directly?
        # I will implement a flexible load capability.
        
        self.model_maps = {
            'ar-en': 'Helsinki-NLP/opus-mt-ar-en',
            'en-ar': 'Helsinki-NLP/opus-mt-en-ar',
            'fr-en': 'Helsinki-NLP/opus-mt-fr-en',
            'en-fr': 'Helsinki-NLP/opus-mt-en-fr'
        }
        
    def _load_model(self, source, target):
        key = f"{source}-{target}"
        if key not in self.models:
            model_name = self.model_maps.get(key)
            if not model_name:
                # Try to find a direct model or fallback
                model_name = f"Helsinki-NLP/opus-mt-{source}-{target}"
            
            try:
                print(f"Loading translation model: {model_name}...")
                self.tokenizers[key] = MarianTokenizer.from_pretrained(model_name)
                self.models[key] = MarianMTModel.from_pretrained(model_name).to(self.device)
            except Exception as e:
                print(f"Error loading model {model_name}: {e}")
                return False
        return True

    def detect_language(self, text):
        try:
            return langdetect.detect(text)
        except:
            return 'fr' # Default

    def translate(self, text, source_lang, target_lang):
        if source_lang == target_lang:
            return text
            
        # Check if direct translation is possible/loaded
        if self._load_model(source_lang, target_lang):
            return self._perform_translation(text, f"{source_lang}-{target_lang}")
            
        # Pivot through English if needed (e.g. Ar -> Fr via En)
        if source_lang != 'en' and target_lang != 'en':
            step1 = self.translate(text, source_lang, 'en')
            return self.translate(step1, 'en', target_lang)
            
        return text # Fail safe

    def _perform_translation(self, text, key):
        tokenizer = self.tokenizers[key]
        model = self.models[key]
        
        # Tokenize
        encoded = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        
        # Translate
        generated_tokens = model.generate(**encoded)
        
        # Decode
        return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
