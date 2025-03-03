from datetime import datetime
from app import db

class Team(db.Model):
    """团队模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 关系
    members = db.relationship('TeamMember', back_populates='team', lazy=True)
    creator = db.relationship('User', backref='created_teams', foreign_keys=[created_by])
    
    def __repr__(self):
        return f"Team('{self.name}')"

class TeamMember(db.Model):
    """团队成员模型"""
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')  # 'leader' or 'member'
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 关系
    team = db.relationship('Team', back_populates='members')
    user = db.relationship('User', back_populates='teams')
    
    def __repr__(self):
        return f"TeamMember(team_id={self.team_id}, user_id={self.user_id}, role='{self.role}')" 