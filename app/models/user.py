from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar = db.Column(db.String(120), nullable=False, default='default.jpg')
    
    # 通知设置
    notification_team = db.Column(db.Boolean, default=True)
    notification_competition = db.Column(db.Boolean, default=True)
    notification_system = db.Column(db.Boolean, default=True)
    
    # 关系
    teams = db.relationship('TeamMember', back_populates='user', lazy=True)
    competition_results = db.relationship('CompetitionResult', back_populates='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"