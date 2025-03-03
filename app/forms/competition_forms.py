from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FloatField
from wtforms.fields import DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models.user import User

class CompetitionForm(FlaskForm):
    """比赛创建表单"""
    name = StringField('比赛名称', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('比赛描述', validators=[DataRequired(), Length(min=10, max=500)])
    start_date = DateTimeField('开始日期', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    end_date = DateTimeField('结束日期', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('创建比赛')

class ResultForm(FlaskForm):
    """比赛成绩录入表单"""
    user_id = SelectField('参赛成员', coerce=int, validators=[DataRequired()])
    score = FloatField('得分', validators=[DataRequired(), NumberRange(min=0)])
    remarks = TextAreaField('备注', validators=[Length(max=200)])
    submit = SubmitField('提交成绩')

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(user.id, user.username) for user in User.query.order_by(User.username).all()] 