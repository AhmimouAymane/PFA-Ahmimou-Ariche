from datetime import datetime
from database import db
import json

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    message_metadata = db.Column('metadata', db.Text)  # JSON string for additional data (sources, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def set_metadata(self, data):
        """Set metadata as JSON string"""
        self.message_metadata = json.dumps(data) if data else None
    
    def get_metadata(self):
        """Get metadata as dictionary"""
        return json.loads(self.message_metadata) if self.message_metadata else {}
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Message {self.id} ({self.role})>'

