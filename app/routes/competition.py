from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.competition import Competition, CompetitionResult
from app.forms.competition_forms import CompetitionForm, ResultForm
from datetime import datetime

competition = Blueprint('competition', __name__, url_prefix='/competition')

@competition.route('/')
@login_required
def competition_list():
    """显示所有比赛列表"""
    now = datetime.utcnow()
    competitions = Competition.query.all()
    
    # 计算不同状态的比赛数量
    active_competitions = sum(1 for comp in competitions if comp.start_date <= now and comp.end_date >= now)
    finished_competitions = sum(1 for comp in competitions if comp.end_date < now)
    upcoming_competitions = sum(1 for comp in competitions if comp.start_date > now)
    
    # 获取最新的成绩记录
    latest_results = CompetitionResult.query.order_by(CompetitionResult.date_submitted.desc()).limit(5).all()
    
    return render_template('competition/list.html', 
                          title='比赛列表', 
                          competitions=competitions,
                          active_competitions=active_competitions,
                          finished_competitions=finished_competitions,
                          upcoming_competitions=upcoming_competitions,
                          latest_results=latest_results,
                          now=now)

@competition.route('/create', methods=['GET', 'POST'])
@login_required
def create_competition():
    """创建新比赛"""
    form = CompetitionForm()
    if form.validate_on_submit():
        competition = Competition(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            created_by=current_user.id
        )
        db.session.add(competition)
        db.session.commit()
        flash('比赛创建成功！', 'success')
        return redirect(url_for('competition.competition_list'))
    return render_template('competition/create.html', title='创建比赛', form=form)

@competition.route('/<int:competition_id>')
@login_required
def competition_detail(competition_id):
    """比赛详情页面"""
    competition = Competition.query.get_or_404(competition_id)
    results = CompetitionResult.query.filter_by(competition_id=competition_id).order_by(CompetitionResult.score.desc()).all()
    
    # 直接查询当前用户的成绩
    user_result = CompetitionResult.query.filter_by(
        competition_id=competition_id, 
        user_id=current_user.id
    ).first()
    
    return render_template('competition/detail.html', 
                          title=competition.name, 
                          competition=competition, 
                          results=results,
                          user_result=user_result,
                          now=datetime.utcnow())

@competition.route('/<int:competition_id>/add_result', methods=['GET', 'POST'])
@login_required
def add_result(competition_id):
    """添加比赛成绩"""
    competition = Competition.query.get_or_404(competition_id)
    form = ResultForm()
    
    # 检查用户是否已经提交过成绩
    existing_result = CompetitionResult.query.filter_by(
        competition_id=competition_id, 
        user_id=current_user.id
    ).first()
    
    if existing_result:
        flash('您已经提交过成绩，不能重复提交！', 'warning')
        return redirect(url_for('competition.competition_detail', competition_id=competition_id))
    
    if form.validate_on_submit():
        result = CompetitionResult(
            competition_id=competition_id,
            user_id=current_user.id,  # 使用当前登录用户的ID
            score=form.score.data,
            remarks=form.remarks.data
        )
        db.session.add(result)
        db.session.commit()
        flash('成绩添加成功！', 'success')
        return redirect(url_for('competition.competition_detail', competition_id=competition_id))
    
    # 设置表单的默认值
    if form.user_id.choices:
        form.user_id.data = current_user.id
    
    return render_template('competition/add_result.html', 
                          title='添加成绩', 
                          form=form, 
                          competition=competition,
                          now=datetime.utcnow())

@competition.route('/dashboard')
@login_required
def competition_dashboard():
    """比赛成绩排名图表"""
    # 获取所有比赛
    all_competitions = Competition.query.all()
    now = datetime.utcnow()
    
    # 计算基本统计数据
    total_competitions = len(all_competitions)
    active_competitions = sum(1 for comp in all_competitions if comp.start_date <= now and comp.end_date >= now)
    
    # 获取所有成绩
    all_results = CompetitionResult.query.all()
    total_participants = len(all_results)
    
    # 计算平均分
    average_score = 0
    if total_participants > 0:
        average_score = sum(result.score for result in all_results) / total_participants
    
    # 获取最近的比赛（按开始日期降序）
    recent_competitions = Competition.query.order_by(Competition.start_date.desc()).limit(5).all()
    recent_comp_data = []
    
    # 成绩分布
    score_distribution = [0, 0, 0, 0, 0]  # 0-20, 21-40, 41-60, 61-80, 81-100
    
    # 参与度趋势（最近6个月）
    from datetime import timedelta
    trend_dates = []
    trend_counts = []
    
    # 生成最近6个月的日期
    for i in range(5, -1, -1):
        month_date = (now - timedelta(days=30 * i))
        trend_dates.append(month_date.strftime('%Y-%m'))
        # 计算该月的参与人数
        month_start = datetime(month_date.year, month_date.month, 1)
        if month_date.month == 12:
            month_end = datetime(month_date.year + 1, 1, 1)
        else:
            month_end = datetime(month_date.year, month_date.month + 1, 1)
        
        month_count = CompetitionResult.query.join(Competition).filter(
            CompetitionResult.date_submitted >= month_start,
            CompetitionResult.date_submitted < month_end
        ).count()
        trend_counts.append(month_count)
    
    # 处理每个比赛的详细数据
    for comp in recent_competitions:
        comp_results = CompetitionResult.query.filter_by(competition_id=comp.id).all()
        participant_count = len(comp_results)
        
        comp_data = {
            'name': comp.name,
            'id': comp.id,
            'participant_count': participant_count,
            'average_score': 0,
            'highest_score': 0,
            'lowest_score': 0
        }
        
        if participant_count > 0:
            scores = [r.score for r in comp_results]
            comp_data['average_score'] = sum(scores) / participant_count
            comp_data['highest_score'] = max(scores) if scores else 0
            comp_data['lowest_score'] = min(scores) if scores else 0
            
            # 更新成绩分布
            for score in scores:
                if score <= 20:
                    score_distribution[0] += 1
                elif score <= 40:
                    score_distribution[1] += 1
                elif score <= 60:
                    score_distribution[2] += 1
                elif score <= 80:
                    score_distribution[3] += 1
                else:
                    score_distribution[4] += 1
        
        recent_comp_data.append(comp_data)
    
    # 构建完整的数据结构
    competition_data = {
        'total_competitions': total_competitions,
        'active_competitions': active_competitions,
        'total_participants': total_participants,
        'average_score': average_score,
        'trend_dates': trend_dates,
        'trend_counts': trend_counts,
        'score_distribution': score_distribution,
        'recent_competitions': recent_comp_data
    }
    
    return render_template('competition/dashboard.html', 
                          title='比赛成绩统计', 
                          competition_data=competition_data,
                          now=now) 