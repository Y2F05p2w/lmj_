import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # 配置数据库
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # MySQL数据库配置 - 请根据您的实际MySQL设置修改以下连接信息
    # 格式：mysql+pymysql://用户名:密码@主机地址/数据库名
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Lifei123!@121.199.60.27/wangz'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 10
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录以访问此页面'
    login_manager.login_message_category = 'info'
    
    # 注册蓝图
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.team import team
    from app.routes.competition import competition
    from app.routes.analytics import analytics
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(team)
    app.register_blueprint(competition)
    app.register_blueprint(analytics)
    
    return app 