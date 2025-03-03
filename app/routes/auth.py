from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models.user import User
from app.forms.auth_forms import RegistrationForm, LoginForm, SettingsForm, UpdateProfileForm
from app.utils import save_avatar
import os

auth = Blueprint('auth', __name__)

@auth.route('/auth')
def auth_home():
    """认证相关功能的首页，重定向到登录页面"""
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册路由"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！现在您可以登录了。', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', title='注册', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录路由"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('登录成功！', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('登录失败，请检查邮箱和密码。', 'danger')
    
    return render_template('login.html', title='登录', form=form)

@auth.route('/logout')
def logout():
    """用户登出路由"""
    logout_user()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.home'))

@auth.route('/profile')
@login_required
def profile():
    """用户个人资料页面"""
    form = UpdateProfileForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.notification_team.data = current_user.notification_team
    form.notification_competition.data = current_user.notification_competition
    return render_template('profile.html', title='个人资料', form=form)

@auth.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """用户设置页面"""
    form = SettingsForm()
    if form.validate_on_submit():
        # 更新基本信息
        current_user.username = form.username.data
        
        # 更新密码（如果提供了新密码）
        if form.current_password.data and form.new_password.data:
            if bcrypt.check_password_hash(current_user.password, form.current_password.data):
                current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            else:
                flash('当前密码错误。', 'danger')
                return redirect(url_for('auth.settings'))
        
        # 更新通知设置
        current_user.notification_team = form.team_notifications.data
        current_user.notification_competition = form.competition_notifications.data
        current_user.notification_system = form.system_notifications.data
        
        db.session.commit()
        flash('设置已更新！', 'success')
        return redirect(url_for('auth.settings'))
    
    # 预填充表单数据
    if request.method == 'GET':
        form.username.data = current_user.username
        form.team_notifications.data = current_user.notification_team
        form.competition_notifications.data = current_user.notification_competition
        form.system_notifications.data = current_user.notification_system
    
    return render_template('settings.html', title='设置', form=form)

@auth.route('/update_avatar', methods=['POST'])
@login_required
def update_avatar():
    form = UpdateProfileForm()
    if form.avatar.data:
        # 删除旧头像
        if current_user.avatar != 'default.jpg':
            old_avatar_path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.avatar)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)
        
        # 保存新头像
        picture_file = save_avatar(form.avatar.data)
        current_user.avatar = picture_file
        db.session.commit()
        flash('头像已更新！', 'success')
    return redirect(url_for('auth.profile'))

@auth.route('/update_settings', methods=['POST'])
@login_required
def update_settings():
    """更新用户设置"""
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.notification_team = form.notification_team.data
        current_user.notification_competition = form.notification_competition.data
        db.session.commit()
        flash('通知设置已更新！', 'success')
    return redirect(url_for('auth.profile')) 