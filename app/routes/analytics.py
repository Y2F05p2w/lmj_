from flask import Blueprint, render_template
from flask_login import login_required
from app.models.user import User
from app.models.team import Team, TeamMember
from app.models.competition import Competition, CompetitionResult
from app import db
from sqlalchemy import func
import json

analytics = Blueprint('analytics', __name__)

@analytics.route('/analytics/dashboard')
@login_required
def analytics_dashboard():
    """数据分析仪表板"""
    # 获取基础统计数据
    total_users = User.query.count()
    total_teams = Team.query.count()
    total_competitions = Competition.query.count()
    
    # 获取最活跃的团队（基于成员数量）
    active_teams = db.session.query(
        Team,
        func.count(TeamMember.id).label('member_count')
    ).join(TeamMember).group_by(Team).order_by(func.count(TeamMember.id).desc()).limit(5).all()
    
    # 获取比赛参与情况统计
    competition_stats = db.session.query(
        Competition.name,
        func.count(CompetitionResult.id).label('participant_count')
    ).join(CompetitionResult).group_by(Competition).order_by(func.count(CompetitionResult.id).desc()).limit(5).all()
    
    # 准备图表数据
    competition_labels = [stat[0] for stat in competition_stats]
    competition_data = [stat[1] for stat in competition_stats]
    
    team_labels = [team[0].name for team in active_teams]
    team_data = [team[1] for team in active_teams]
    
    return render_template('analytics/dashboard.html',
                         title='数据分析',
                         total_users=total_users,
                         total_teams=total_teams,
                         total_competitions=total_competitions,
                         competition_labels=json.dumps(competition_labels),
                         competition_data=json.dumps(competition_data),
                         team_labels=json.dumps(team_labels),
                         team_data=json.dumps(team_data)) 