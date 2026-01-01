from datetime import datetime
from models.conversation import Conversation
from models.message import Message
from database import db
from llm.rag_service import RAGService

# Initialize RAG Service globally to avoid reloading models on every request
# This will happen when the module is imported (at app startup if imported)
rag_service_singleton = RAGService()

class ChatService:
    def __init__(self):
        self.rag_service = rag_service_singleton
    
    def process_message(self, user_id: int, message_content: str, conversation_id: int = None, language: str = None):
        """Process user message and generate response"""
        # Detect language if not provided
        if not language:
            language = self.rag_service.detect_language(message_content)
        
        # Get or create conversation
        if conversation_id:
            conversation = Conversation.query.get(conversation_id)
            if not conversation or conversation.user_id != user_id:
                conversation = None
        else:
            conversation = None
        
        if not conversation:
            conversation = Conversation(
                user_id=user_id,
                language=language,
                title=message_content[:50] if message_content else "Nouvelle conversation"
            )
            db.session.add(conversation)
            db.session.commit()
        
        # Get conversation history for context
        history_messages = Message.query.filter_by(
            conversation_id=conversation.id
        ).order_by(Message.created_at).all()
        
        # Convert to simple format for LLM
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages[-6:]  # Last 6 messages
        ]
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            content=message_content,
            role='user'
        )
        db.session.add(user_message)
        db.session.commit()
        
        # Generate response using RAG with conversation history
        rag_result = self.rag_service.retrieve_and_generate(
            message_content,
            language,
            conversation_history=conversation_history
        )
        
        # Save assistant response
        assistant_message = Message(
            conversation_id=conversation.id,
            content=rag_result["answer"],
            role='assistant'
        )
        assistant_message.set_metadata({
            "sources": rag_result["sources"],
            "language": rag_result["language"]
        })
        db.session.add(assistant_message)
        
        # Update conversation
        conversation.updated_at = datetime.utcnow()
        if not conversation.title or conversation.title.startswith("Nouvelle"):
            conversation.title = message_content[:50]
        db.session.commit()
        
        return {
            "conversation_id": conversation.id,
            "response": rag_result["answer"],
            "sources": rag_result["sources"],
            "language": rag_result["language"]
        }
    
    def get_conversation_history(self, conversation_id: int, user_id: int):
        """Get conversation history"""
        conversation = Conversation.query.filter_by(
            id=conversation_id,
            user_id=user_id
        ).first()
        
        if not conversation:
            return None
        
        messages = Message.query.filter_by(
            conversation_id=conversation_id
        ).order_by(Message.created_at).all()
        
        return {
            "conversation": conversation.to_dict(),
            "messages": [msg.to_dict() for msg in messages]
        }
    
    def get_user_conversations(self, user_id: int):
        """Get all conversations for a user"""
        conversations = Conversation.query.filter_by(
            user_id=user_id
        ).order_by(Conversation.updated_at.desc()).all()
        
        return [conv.to_dict() for conv in conversations]

