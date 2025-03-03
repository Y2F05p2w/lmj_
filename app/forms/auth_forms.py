from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models.user import User

class RegistrationForm(FlaskForm):
    """用户注册表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        """验证用户名是否已存在"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请选择其他用户名。')

    def validate_email(self, email):
        """验证邮箱是否已存在"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被注册，请使用其他邮箱。')

class LoginForm(FlaskForm):
    """用户登录表单"""
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

class SettingsForm(FlaskForm):
    """用户设置表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    current_password = PasswordField('当前密码')
    new_password = PasswordField('新密码')
    confirm_password = PasswordField('确认新密码', validators=[EqualTo('new_password')])
    team_notifications = BooleanField('团队通知')
    competition_notifications = BooleanField('比赛通知')
    system_notifications = BooleanField('系统通知')
    submit = SubmitField('保存更改')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('该用户名已被使用。请选择其他用户名。')

class UpdateProfileForm(FlaskForm):
    """用户资料更新表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    avatar = FileField('更新头像', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    notification_team = BooleanField('团队通知')
    notification_competition = BooleanField('比赛通知')
    submit = SubmitField('更新')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('该用户名已被使用')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('该邮箱已被注册') 