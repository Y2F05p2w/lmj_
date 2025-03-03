from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.team import Team, TeamMember
from app.forms.team_forms import TeamForm, AddMemberForm
from datetime import datetime
from app.models.user import User

team = Blueprint('team', __name__, url_prefix='/team')

@team.route('/')
@login_required
def team_list():
    """显示所有团队"""
    teams = Team.query.all()
    return render_template('team/list.html', title='团队列表', teams=teams)

@team.route('/create', methods=['GET', 'POST'])
@login_required
def create_team():
    """创建新团队"""
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data, description=form.description.data, created_by=current_user.id)
        db.session.add(team)
        db.session.commit()
        # 创建者自动成为团队成员，并设置为领导
        member = TeamMember(user_id=current_user.id, team_id=team.id, role='leader')
        db.session.add(member)
        db.session.commit()
        flash('团队创建成功！', 'success')
        return redirect(url_for('team.team_list'))
    return render_template('team/create.html', title='创建团队', form=form)

@team.route('/<int:team_id>')
@login_required
def team_detail(team_id):
    """团队详情页面"""
    team = Team.query.get_or_404(team_id)
    
    # 直接查询数据库确定用户是否是团队成员
    is_member = TeamMember.query.filter_by(team_id=team_id, user_id=current_user.id).first() is not None
    
    print(f"访问团队详情页面：{team.name}，当前用户：{current_user.username}")
    print(f"当前用户是否是团队成员（直接查询）：{is_member}")
    
    return render_template('team/detail.html', 
                          title=team.name, 
                          team=team, 
                          is_member=is_member, 
                          now=datetime.utcnow())

@team.route('/<int:team_id>/add_member', methods=['GET', 'POST'])
@login_required
def add_member(team_id):
    """添加团队成员"""
    team = Team.query.get_or_404(team_id)
    # 检查当前用户是否是团队领导
    member = TeamMember.query.filter_by(team_id=team_id, user_id=current_user.id, role='leader').first()
    if not member:
        flash('只有团队领导才能添加成员！', 'danger')
        return redirect(url_for('team.team_detail', team_id=team_id))
    
    form = AddMemberForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        # 检查用户是否已经是团队成员
        existing_member = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
        if existing_member:
            flash('该用户已经是团队成员！', 'warning')
        else:
            new_member = TeamMember(user_id=user_id, team_id=team_id, role='member')
            db.session.add(new_member)
            db.session.commit()
            flash('团队成员添加成功！', 'success')
        return redirect(url_for('team.team_detail', team_id=team_id))
    
    return render_template('team/add_member.html', title='添加成员', form=form, team=team)

@team.route('/dashboard')
@login_required
def team_dashboard():
    """团队分组统计图表"""
    # 获取所有团队及其成员数量
    teams = Team.query.all()
    team_data = []
    team_names = []
    member_counts = []
    leader_counts = []
    activity_scores = []
    
    # 用户数据
    user_team_data = []

    for t in teams:
        member_count = TeamMember.query.filter_by(team_id=t.id).count()
        leader_count = TeamMember.query.filter_by(team_id=t.id, role='leader').count()
        
        # 计算一个简单的活跃度分数（示例）
        activity_score = member_count * 10  # 简单示例，可以根据实际需求调整计算方式
        
        team_data.append({
            'id': t.id,
            'name': t.name, 
            'member_count': member_count,
            'leader_count': leader_count,
            'created_at': t.created_at
        })
        
        team_names.append(t.name)
        member_counts.append(member_count)
        leader_counts.append(leader_count)
        activity_scores.append(activity_score)
    
    # 获取所有用户及其加入的团队信息
    team_members = db.session.query(
        User.username,
        Team.name.label('team_name'),
        TeamMember.joined_at,
        Team.id.label('team_id')
    ).join(
        TeamMember, User.id == TeamMember.user_id
    ).join(
        Team, TeamMember.team_id == Team.id
    ).order_by(User.username, TeamMember.joined_at.desc()).all()
    
    for member in team_members:
        user_team_data.append({
            'username': member.username,
            'team_name': member.team_name,
            'date_joined': member.joined_at,
            'team_id': member.team_id
        })
    
    return render_template('team/dashboard.html', 
                           title='团队统计', 
                           team_data=team_data,
                           team_names=team_names,
                           member_counts=member_counts,
                           leader_counts=leader_counts,
                           activity_scores=activity_scores,
                           user_team_data=user_team_data)

@team.route('/<int:team_id>/join', methods=['POST'])
@login_required
def join_team(team_id):
    """加入团队"""
    team = Team.query.get_or_404(team_id)
    
    # 检查用户是否已经是团队成员
    existing_member = TeamMember.query.filter_by(team_id=team_id, user_id=current_user.id).first()
    if existing_member:
        flash('您已经是该团队成员！', 'info')
    else:
        new_member = TeamMember(user_id=current_user.id, team_id=team_id, role='member')
        db.session.add(new_member)
        db.session.commit()
        flash('成功加入团队！', 'success')
    
    return redirect(url_for('team.team_detail', team_id=team_id))

@team.route('/<int:team_id>/leave', methods=['POST'])
@login_required
def leave_team(team_id):
    """退出团队"""
    team = Team.query.get_or_404(team_id)
    
    # 检查用户是否是团队成员
    member = TeamMember.query.filter_by(team_id=team_id, user_id=current_user.id).first()
    
    if not member:
        flash('您不是该团队成员！', 'warning')
        return redirect(url_for('team.team_detail', team_id=team_id))
    
    # 检查是否是团队领导且是唯一的领导
    if member.role == 'leader':
        leader_count = TeamMember.query.filter_by(team_id=team_id, role='leader').count()
        if leader_count <= 1:
            flash('您是该团队唯一的领导，请先指定其他领导或解散团队！', 'danger')
            return redirect(url_for('team.team_detail', team_id=team_id))
    
    # 删除成员记录
    db.session.delete(member)
    db.session.commit()
    
    flash('您已成功退出团队！', 'success')
    return redirect(url_for('team.team_list')) 