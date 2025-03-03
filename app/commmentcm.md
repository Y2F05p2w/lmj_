# 社团管理系统目录结构说明

## 项目结构
```
app/
├── __init__.py              # Flask应用初始化、数据库配置、扩展初始化和蓝图注册
├── utils.py                 # 工具函数（如头像保存等）
├── routes/                  # 路由目录（控制器层）
│   ├── main.py             # 主页和基础路由
│   ├── auth.py             # 用户认证相关路由（登录、注册、个人资料）
│   ├── team.py             # 团队管理相关路由（创建、查看、加入团队等）
│   ├── competition.py      # 比赛管理相关路由（创建、查看、成绩录入等）
│   └── analytics.py        # 数据分析相关路由
├── models/                  # 数据模型目录（模型层）
│   ├── __init__.py         # 模型初始化和导入
│   ├── user.py             # 用户模型（用户信息、认证）
│   ├── team.py             # 团队模型（团队信息、成员关系）
│   └── competition.py      # 比赛模型（比赛信息、成绩记录）
├── forms/                   # 表单目录（表单验证）
│   ├── auth_forms.py       # 认证相关表单（登录、注册、个人资料更新）
│   ├── team_forms.py       # 团队相关表单（创建团队、添加成员）
│   └── competition_forms.py # 比赛相关表单（创建比赛、成绩录入）
├── templates/              # 模板目录（视图层）
│   ├── layout.html         # 基础布局模板（页面框架）
│   ├── home.html           # 首页模板（功能概览）
│   ├── about.html          # 关于页面
│   ├── login.html          # 登录页面
│   ├── register.html       # 注册页面
│   ├── profile.html        # 个人资料页面
│   ├── settings.html       # 用户设置页面
│   ├── auth/               # 认证相关模板
│   ├── team/               # 团队相关模板
│   ├── competition/        # 比赛相关模板
│   └── analytics/          # 数据分析相关模板
└── static/                 # 静态文件目录
    ├── css/                # CSS样式文件
    ├── js/                 # JavaScript文件
    ├── images/             # 网站通用图片资源
    └── profile_pics/       # 用户头像存储

```

## 技术架构

### 后端技术栈
- **Flask**: 轻量级Python Web框架
- **SQLAlchemy**: ORM数据库操作
- **Flask-Login**: 用户会话管理
- **Flask-WTF**: 表单处理与验证
- **Flask-Bcrypt**: 密码加密
- **Flask-Migrate**: 数据库迁移
- **MySQL**: 关系型数据库
- **PyMySQL**: MySQL数据库连接驱动

### 前端技术栈
- **Bootstrap 5**: 响应式UI框架
- **Chart.js**: 数据可视化图表
- **Font Awesome**: 图标库
- **jQuery**: JavaScript库

## 功能模块说明

### 1. 用户认证模块 (auth)
- 用户注册与登录
- 个人资料管理与头像上传
- 用户设置（通知偏好等）
- 用户权限控制

### 2. 团队管理模块 (team)
- 团队创建与基本信息管理
- 成员添加、移除与权限设置
- 团队领导与普通成员区分
- 团队数据统计与可视化
- 团队活动记录与历史查询

### 3. 比赛管理模块 (competition)
- 比赛创建与信息管理
- 比赛时间安排与状态跟踪
- 成绩录入与实时排名
- 比赛数据统计与可视化
- 历史比赛记录查询与分析

### 4. 数据分析模块 (analytics)
- 团队活动数据分析
- 比赛成绩统计分析
- 用户参与度分析
- 数据可视化展示

## 数据模型关系

### 用户模型 (User)
```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60))
    avatar = db.Column(db.String(120))
    notification_team = db.Column(db.Boolean)
    notification_competition = db.Column(db.Boolean)
    notification_system = db.Column(db.Boolean)
    teams = db.relationship('TeamMember', back_populates='user')
    competition_results = db.relationship('CompetitionResult', back_populates='user')
```

### 团队模型 (Team/TeamMember)
```python
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    members = db.relationship('TeamMember', back_populates='team')

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String(20))  # 'leader' or 'member'
    joined_at = db.Column(db.DateTime)
```

### 比赛模型 (Competition/CompetitionResult)
```python
class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime)
    results = db.relationship('CompetitionResult', backref='competition')

class CompetitionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Float)
    remarks = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime)
```

## 技术特点
1. 响应式设计，适配各种设备屏幕尺寸
2. Bootstrap 5 UI框架提供现代化界面
3. Font Awesome图标增强视觉体验
4. Chart.js数据可视化展示统计信息
5. CSRF保护确保表单安全
6. 文件上传处理支持头像
7. 数据库关系管理确保数据完整性
8. 用户权限控制保障系统安全
9. RESTful API设计规范化接口
10. 分页功能优化大数据量展示

## 部署说明
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 数据库配置：
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@主机地址/数据库名'
```

3. 初始化数据库：
```bash
flask db init
flask db migrate
flask db upgrade
```

4. 运行应用：
```bash
flask run
```

## 注意事项
1. 确保MySQL服务器已启动并正确配置
2. 检查数据库连接信息是否正确
3. 确保所有必要的Python包都已安装
4. 注意文件上传目录的权限设置
5. 定期备份数据库
