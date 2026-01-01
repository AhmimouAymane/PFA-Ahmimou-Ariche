import os
from models.document import Document as DocumentModel
from database import db
from llm.translation_service import TranslationService
from llm.local_model_service import LocalModelService

class RAGService:
    def __init__(self):
        # Initialize Services (no embeddings needed for simple keyword search)
        print("Initializing RAG Service (Simplified Mode)...")
        self.translation_service = TranslationService()
        self.local_model = LocalModelService()
        print("RAG Service Ready!")
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        return self.translation_service.detect_language(text)

    def retrieve_and_generate(self, question: str, language: str = 'fr', conversation_history: list = None):
        """Retrieve relevant documents and generate answer using Local Models"""
        try:
            # Step 1: Detect Input Language
            detected_lang = self.translation_service.detect_language(question)
            user_lang = language if language else detected_lang
            
            print(f"Processing Query: {question} (Lang: {user_lang})")
            
            # Step 2: Translate to French (Admin Model Language)
            prompt_in_french = self.translation_service.translate(question, user_lang, 'fr')
            print(f"Translated to French: {prompt_in_french}")
            
            # Step 3: Simple keyword-based document retrieval
            # Extract keywords from the French question
            keywords = prompt_in_french.lower().split()
            
            # Query database for documents containing these keywords
            documents = DocumentModel.query.filter_by(active=True).all()
            
            # Simple scoring: count keyword matches
            scored_docs = []
            for doc in documents:
                content_lower = doc.content.lower()
                score = sum(1 for keyword in keywords if keyword in content_lower)
                if score > 0:
                    scored_docs.append((score, doc))
            
            # Sort by score and take top 3
            scored_docs.sort(reverse=True, key=lambda x: x[0])
            top_docs = [doc for score, doc in scored_docs[:3]]
            
            # Build context
            context_text = ""
            for doc in top_docs:
                doc_content = doc.content
                doc_lang = doc.language
                
                # Translate to French if needed
                if doc_lang != 'fr':
                    doc_content = self.translation_service.translate(doc_content, doc_lang, 'fr')
                
                context_text += f"\\n---\\n{doc_content[:500]}"  # Limit context size
            
            print(f"Retrieved Context Length: {len(context_text)}")
            
            # Step 4: Generate Response using Intelligent Local Model
            answer_french = self.local_model.generate_response(
                context=context_text,
                question=prompt_in_french,
                language='fr',
                conversation_history=conversation_history
            )
            print(f"Generated French Answer: {answer_french[:100]}...")
            
            # Step 5: Translate back to User Language
            final_answer = self.translation_service.translate(answer_french, 'fr', user_lang)
            print(f"Final Answer ({user_lang}): {final_answer[:100]}...")
            
            sources = [
                {
                    "title": doc.title,
                    "category": doc.category or "general",
                    "source": doc.source or "admin"
                }
                for doc in top_docs
            ]
            
            return {
                "answer": final_answer,
                "sources": sources,
                "language": user_lang,
                "original_language": detected_lang
            }
            
        except Exception as e:
            print(f"Error in retrieve_and_generate: {e}")
            import traceback
            traceback.print_exc()
            return {
                "answer": "Une erreur s'est produite lors du traitement. Veuillez réessayer.",
                "sources": [],
                "language": language
            }
