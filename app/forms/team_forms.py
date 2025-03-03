from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.models.user import User

class TeamForm(FlaskForm):
    """团队创建表单"""
    name = StringField('团队名称', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('团队描述', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('创建团队')

class AddMemberForm(FlaskForm):
    """添加团队成员表单"""
    user_id = SelectField('选择成员', coerce=int, validators=[DataRequired()])
    submit = SubmitField('添加成员')

    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(user.id, user.username) for user in User.query.order_by(User.username).all()] 