"""
Intelligent Local Model Service - Moroccan Administrative Assistance
Uses Ollama for natural, ChatGPT-like conversations
"""
from llm.ollama_service import OllamaService
from typing import List, Dict, Optional

class LocalModelService:
    def __init__(self):
        print("Initializing Intelligent Moroccan Admin Assistant...")
        self.ollama = OllamaService()
        
        # Preferred model priority (will use first available)
        self.model_priority = [
            "aya-expanse:8b",
            "command-r:7b",
            "qwen2.5:7b",
            "mistral:7b"
        ]
        
        # System prompt with Moroccan administrative knowledge
        self.system_prompt = """Tu es un assistant expert en administration publique marocaine. Tu aides les citoyens à comprendre les démarches administratives au Maroc.

DOMAINES D'EXPERTISE:
1. Documents d'identité: Carte d'identité (CNIE), passeport, casier judiciaire
2. État civil: Actes de naissance, mariage, divorce, succession
3. Transport: Permis de conduire, carte grise, vignette
4. Logement: Logement social, certificat de résidence
5. Protection sociale: RAMED, CNSS, AMO, aides directes (Tayssir, Daam)
6. Éducation: Bourses universitaires, inscriptions
7. Emploi: Marchés publics, attestations professionnelles
8. Voyage: Visas, formalités consulaires

INFORMATIONS CLÉS PAR SUJET:

CARTE D'IDENTITÉ (CNIE):
- Documents: acte de naissance, certificat de résidence, 2 photos
- Lieu: Commune/arrondissement de domicile
- Délai: ~2 semaines
- Coût: Gratuit (première carte)
- Validité: 10 ans

PASSEPORT:
- Documents: CNIE valide, 4 photos, formulaire
- Rendez-vous: www.passeport.ma
- Délai: 7-10 jours ouvrables
- Coût: 300 DH (ordinaire), 500 DH (express)
- Validité: 5 ans

PERMIS DE CONDUIRE:
- Auto-école agréée obligatoire
- Formation théorique: 40h minimum
- Formation pratique: 20h minimum
- Coût total: 3000-5000 DH
- Durée: 3-6 mois

MARIAGE:
- Documents: CNIE, certificat naissance, certificat célibat, certificat médical
- Lieu: Section Adoul + Tribunal de la famille
- Coût: 200-500 DH
- Présence: Témoins + tuteur(wali) pour femme

RAMED/AMO:
- Conditions: Revenu faible, pas d'assurance
- Documents: CNIE, certificat résidence, justificatifs revenus
- Gratuit, validité 1 an
- Soins gratuits hôpitaux publics

LOGEMENT SOCIAL:
- Programmes: Fogarim, Fogaloge, Lkouacem
- Conditions: Revenu < 6000 DH/mois, non-propriétaire
- Prix: 140,000-250,000 DH

STYLE DE RÉPONSE:
- Sois naturel et conversationnel (comme ChatGPT)
- Donne des informations précises et pratiques
- Structure tes réponses clairement
- Adapte-toi au contexte de la conversation
- Pose des questions de clarification si besoin
- Sois empathique et patient"""

        # Arabic system prompt
        self.system_prompt_ar = """أنت مساعد خبير في الإدارة العامة المغربية. تساعد المواطنين على فهم الإجراءات الإدارية في المغرب.

مجالات الخبرة:
1. وثائق الهوية: بطاقة التعريف الوطنية، جواز السفر، السجل العدلي
2. الحالة المدنية: عقود الازدياد، الزواج، الطلاق، الإرث
3. النقل: رخصة السياقة، البطاقة الرمادية
4. السكن: السكن الاجتماعي، شهادة السكنى
5. الحماية الاجتماعية: راميد، الضمان الاجتماعي، الدعم المباشر
6. التعليم: المنح الدراسية
7. العمل: الصفقات العمومية

معلومات رئيسية:

بطاقة التعريف الوطنية:
- الوثائق: عقد ازدياد، شهادة سكنى، صورتان
- المكان: الجماعة/المقاطعة
- المدة: أسبوعان تقريباً
- مجاني (البطاقة الأولى)

جواز السفر:
- الوثائق: بطاقة تعريف سارية، 4 صور
- الموعد: www.passeport.ma
- المدة: 7-10 أيام
- الثمن: 300 درهم (عادي)، 500 درهم (سريع)

أسلوب الرد:
- كن طبيعياً ومحاوراً
- أعط معلومات دقيقة وعملية
- نظّم إجاباتك بوضوح
- كن متعاطفاً وصبوراً"""

        self.selected_model = self._select_best_model()
        if not self.selected_model:
            print("WARNING: No Ollama models found. Please install models.")
        else:
            print(f"✓ Using model: {self.selected_model}")
    
    def _select_best_model(self) -> Optional[str]:
        """Select the best available model from priority list"""
        if not self.ollama.check_ollama_running():
            print("WARNING: Ollama service not running!")
            return None
        
        available = self.ollama.list_models()
        for model in self.model_priority:
            # Check exact match orpartial match
            for avail in available:
                if model in avail or avail.startswith(model.split(':')[0]):
                    return avail
        
        # If none from priority, use first available
        if available:
            print(f"Using first available model: {available[0]}")
            return available[0]
        
        return None
    
    def generate_response(self, context: str, question: str, language: str = 'fr', conversation_history: List[Dict] = None) -> str:
        """
        Generate intelligent response using Ollama LLM.
        
        Args:
            context: Retrieved relevant documents (from RAG)
            question: User's question
            language: Response language
            conversation_history: Previous messages for context
        
        Returns:
            Intelligent, conversational response
        """
        if not self.selected_model:
            return self._fallback_response(question, language)
        
        # Select system prompt based on language
        if language == 'ar':
            system = self.system_prompt_ar
        else:
            system = self.system_prompt
        
        # Build enhanced prompt with context
        if context and len(context.strip()) > 50:
            enhanced_prompt = f"""Contexte pertinent de la base de connaissances:
{context}

Question de l'utilisateur: {question}

Réponds de manière naturelle et conversationnelle en utilisant les informations ci-dessus et tes connaissances sur l'administration marocaine."""
        else:
            enhanced_prompt = question
        
        # Build conversation messages for chat API
        messages = [{"role": "system", "content": system}]
        
        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history[-6:]:  # Last 6 messages for context
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        # Add current question
        messages.append({"role": "user", "content": enhanced_prompt})
        
        try:
            # Use chat API for conversational context
            response = self.ollama.chat(
                model=self.selected_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            
            if response:
                return response
            else:
                return self._fallback_response(question, language)
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._fallback_response(question, language)
    
    def _fallback_response(self, question: str, language: str = 'fr') -> str:
        """Fallback response when LLM is unavailable"""
        if language == 'ar':
            return """عذراً، النظام غير متاح حالياً. يرجى المحاولة لاحقاً أو الاتصال بالإدارة المحلية للحصول على المساعدة."""
        else:
            return """Je m'excuse, le système est temporairement indisponible. Veuillez réessayer plus tard ou contacter votre administration locale pour assistance."""
