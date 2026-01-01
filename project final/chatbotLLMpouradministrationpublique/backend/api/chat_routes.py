from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.chat_service import ChatService

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """Send a message and get response"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        message = data.get('message')
        conversation_id = data.get('conversation_id')
        language = data.get('language')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        chat_service = ChatService()
        result = chat_service.process_message(
            user_id=user_id,
            message_content=message,
            conversation_id=conversation_id,
            language=language
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """Get all conversations for the current user"""
    try:
        user_id = int(get_jwt_identity())
        
        chat_service = ChatService()
        conversations = chat_service.get_user_conversations(user_id)
        
        return jsonify({'conversations': conversations}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversation/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    """Get conversation history"""
    try:
        user_id = int(get_jwt_identity())
        
        chat_service = ChatService()
        history = chat_service.get_conversation_history(conversation_id, user_id)
        
        if not history:
            return jsonify({'error': 'Conversation not found'}), 404
        
        return jsonify(history), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

