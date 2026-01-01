from datetime import datetime
from database import db

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='fr')  # fr, ar, am, en
    category = db.Column(db.String(100))  # e.g., 'identity', 'passport', 'certificates'
    source = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert document to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content[:200] + '...' if len(self.content) > 200 else self.content,
            'language': self.language,
            'category': self.category,
            'source': self.source,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Document {self.id}: {self.title}>'

