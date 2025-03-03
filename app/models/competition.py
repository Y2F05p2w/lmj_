from datetime import datetime
from app import db

class Competition(db.Model):
    """比赛模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 关系
    results = db.relationship('CompetitionResult', backref='competition', lazy=True)
    creator = db.relationship('User', backref='created_competitions', foreign_keys=[created_by])
    
    def __repr__(self):
        return f"Competition('{self.name}')"

class CompetitionResult(db.Model):
    """比赛成绩模型"""
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 添加 user 关系
    user = db.relationship('User', back_populates='competition_results')
    
    def __repr__(self):
        return f"CompetitionResult(competition_id={self.competition_id}, user_id={self.user_id}, score={self.score})" 