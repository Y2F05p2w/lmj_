from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    """主页路由"""
    return render_template('home.html', title='主页')

@main.route('/about')
def about():
    """关于页面路由"""
    return render_template('about.html', title='关于我们') 