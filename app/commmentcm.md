# 社团管理系统目录结构说明

## 项目结构
```
app/
├── __init__.py              # Flask应用初始化、数据库配置、扩展初始化和蓝图注册
├── routes/                  # 路由目录（控制器层）
│   ├── main.py             # 主页和基础路由
│   ├── auth.py             # 用户认证相关路由（登录、注册、个人资料）
│   ├── team.py             # 团队管理相关路由（创建、查看、加入团队等）
│   ├── competition.py      # 比赛管理相关路由（创建、查看、成绩录入等）   
├── models/                  # 数据模型目录（模型层）
│   ├── user.py             # 用户模型（用户信息、认证）
│   ├── team.py             # 团队模型（团队信息、成员关系）
│   ├── competition.py      # 比赛模型（比赛信息、成绩记录） 
├── forms/                   # 表单目录（表单验证）
│   ├── auth_forms.py       # 认证相关表单（登录、注册）
│   ├── team_forms.py       # 团队相关表单（创建团队、添加成员）
│   ├── competition_forms.py # 比赛相关表单（创建比赛、成绩录入）
│   └── blog_forms.py       # 博客相关表单（发布文章、评论）
├── templates/              # 模板目录（视图层）
│   ├── layout.html         # 基础布局模板（页面框架）
│   ├── home.html           # 首页模板（功能概览）
│   ├── login.html          # 登录页面
│   ├── register.html       # 注册页面
│   ├── profile.html        # 个人资料页面
│   ├── auth/               # 认证相关模板
│   │   ├── email_verification.html # 邮箱验证页面
│   │   ├── reset_request.html     # 密码重置请求页面
│   │   ├── reset_token.html       # 密码重置页面
│   │   ├── reset_success.html     # 密码重置成功页面
│   │   └── settings.html          # 用户设置页面
│   ├── team/               # 团队相关模板
│   │   ├── list.html       # 团队列表页面
│   │   ├── detail.html     # 团队详情页面
│   │   ├── create.html     # 创建团队页面
│   │   ├── add_member.html # 添加成员页面
│   │   └── dashboard.html  # 团队统计仪表盘
│   ├── competition/        # 比赛相关模板
│   │   ├── list.html       # 比赛列表页面
│   │   ├── detail.html     # 比赛详情页面
│   │   ├── create.html     # 创建比赛页面
│   │   ├── add_result.html # 添加成绩页面
│   │   └── dashboard.html  # 比赛统计仪表盘
│   
└── static/                 # 静态文件目录
    ├── css/                # CSS样式文件
    ├── js/                 # JavaScript文件
    ├── images/             # 网站通用图片资源
    ├── profile_pics/       # 用户头像存储
    └── blog_pics/          # 博客图片存储
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

### 前端技术栈
- **Bootstrap 5**: 响应式UI框架
- **Chart.js**: 数据可视化图表
- **Font Awesome**: 图标库
- **jQuery**: JavaScript库
- **EasyMDE/Quill**: Markdown/富文本编辑器

## 功能模块说明

### 1. 用户认证模块
- 用户注册与邮箱验证
- 用户登录与会话管理
- 用户登出
- 个人资料管理与头像上传
- 密码重置功能
- 用户权限控制

### 2. 团队管理模块
- 团队创建与基本信息管理
- 成员添加、移除与权限设置
- 团队领导与普通成员区分
- 团队数据统计与可视化
- 团队活动记录与历史查询

### 3. 比赛管理模块
- 比赛创建与信息管理
- 比赛时间安排与状态跟踪
- 成绩录入与实时排名
- 比赛数据统计与可视化
- 历史比赛记录查询与分析

### 4. 博客系统模块
- 文章发布与Markdown支持
- 文章分类与标签管理
- 评论系统与互动功能
- 用户文章管理与权限控制
- 文章搜索与筛选功能
- 图片上传与管理

## 模板功能说明

### 基础模板
- `layout.html`: 提供基础页面结构，包含导航栏、页脚、通知系统和通用样式
- `home.html`: 展示网站主页，包含功能概览、最新动态和快速入口

### 用户认证模板
- `login.html`: 用户登录表单和验证
- `register.html`: 用户注册表单和验证
- `profile.html`: 个人资料展示和编辑
- `auth/email_verification.html`: 邮箱验证页面
- `auth/reset_request.html`: 密码重置请求页面
- `auth/reset_token.html`: 密码重置页面
- `auth/reset_success.html`: 密码重置成功页面
- `auth/settings.html`: 用户设置页面（通知、隐私等）

### 团队模板
- `team/list.html`: 展示所有团队列表，支持分页和搜索
- `team/detail.html`: 显示团队详细信息和成员列表
- `team/create.html`: 团队创建表单
- `team/add_member.html`: 添加团队成员表单
- `team/dashboard.html`: 团队数据统计和图表展示

### 比赛模板
- `competition/list.html`: 展示比赛列表，包含状态过滤
- `competition/detail.html`: 显示比赛详情和成绩排名
- `competition/create.html`: 比赛创建表单
- `competition/add_result.html`: 成绩录入表单
- `competition/dashboard.html`: 比赛数据统计和图表分析

### 博客模板
- `blog/list.html`: 文章列表展示，支持分页和分类筛选
- `blog/detail.html`: 文章详情页，包含评论系统
- `blog/create.html`: 文章创建页面，支持Markdown编辑器
- `blog/edit.html`: 文章编辑页面，支持富文本编辑
- `blog/user_posts.html`: 用户文章列表页
- `blog/category.html`: 分类文章列表页

## 数据模型关系

### 用户模型 (User)
- 一对多关系：用户可以创建多个团队、比赛和博客文章
- 多对多关系：用户可以加入多个团队（通过TeamMember中间表）
- 一对多关系：用户可以参加多个比赛并记录成绩

### 团队模型 (Team/TeamMember)
- 多对多关系：团队可以有多个成员，用户可以加入多个团队
- 一对多关系：团队可以由一个用户创建
- 区分团队领导和普通成员的权限控制

### 比赛模型 (Competition/CompetitionResult)
- 一对多关系：比赛可以记录多个参赛成绩
- 多对多关系：多个用户可以参加多个比赛（通过CompetitionResult中间表）
- 时间范围控制：比赛有开始和结束时间

### 博客模型 (Post/Comment)
- 一对多关系：文章可以有多个评论
- 一对多关系：用户可以发布多篇文章
- 一对多关系：用户可以发表多个评论

## 技术特点
1. 响应式设计，适配各种设备屏幕尺寸
2. Bootstrap 5 UI框架提供现代化界面
3. Font Awesome图标增强视觉体验
4. Chart.js数据可视化展示统计信息
5. Markdown和富文本编辑器支持多种内容格式
6. CSRF保护确保表单安全
7. 文件上传处理支持头像和博客图片
8. 数据库关系管理确保数据完整性
9. 用户权限控制保障系统安全
10. RESTful API设计规范化接口
11. 邮箱验证和密码重置增强账户安全
12. 分页功能优化大数据量展示

## 博客系统功能模块

### 数据模型

博客系统基于以下数据模型：

1. **Post（文章）**
   - 基本字段：id、标题、内容、发布日期、更新日期、作者ID、分类ID、图片文件、是否草稿、查看次数
   - 关系：与评论（一对多）、标签（多对多）、分类（多对一）、用户（多对一）

2. **Comment（评论）**
   - 基本字段：id、内容、发布日期、用户ID、文章ID
   - 关系：与用户和文章（多对一）

3. **Category（分类）**
   - 基本字段：id、名称、描述、创建时间
   - 关系：与文章（一对多）

4. **Tag（标签）**
   - 基本字段：id、名称、描述、创建时间
   - 关系：与文章（多对多）

### 功能特性

1. **文章管理**
   - 创建、编辑和删除文章
   - 支持Markdown格式内容
   - 图片上传和管理
   - 草稿功能（保存为草稿、预览、发布）
   - 文章分类和标签
   - 阅读计数

2. **评论系统**
   - 文章评论功能
   - 评论管理（删除评论）

3. **分类管理**
   - 创建、编辑和删除分类
   - 分类统计（使用Chart.js可视化）
   - 按分类浏览文章

4. **标签管理**
   - 创建、编辑和删除标签
   - 标签云展示
   - 按标签浏览文章
   - 标签统计（使用Chart.js可视化）

5. **搜索功能**
   - 多条件搜索（关键词、分类、标签、时间范围）
   - 排序选项（最新、最受欢迎、评论最多）
   - 搜索结果统计和可视化

6. **用户相关**
   - 用户文章列表
   - 用户发布统计
   - 用户权限控制（只能编辑自己的文章）

### 界面设计

1. **文章列表页（list.html）**
   - 分页显示所有文章
   - 侧边栏显示热门分类

2. **文章详情页（detail.html）**
   - 显示完整文章内容（支持Markdown渲染）
   - 评论区功能
   - a作者信息和相关文章推荐

3. **分类页面（category.html）**
   - 显示特定分类下的文章
   - 分类列表和统计

4. **标签页面（tag.html）**
   - 显示特定标签下的文章
   - 标签云和相关文章

5. **草稿箱页面（drafts.html）**
   - 用户草稿管理
   - 草稿预览和发布功能

6. **搜索页面（search.html）**
   - 高级搜索表单
   - 搜索结果展示和统计

7. **管理页面**
   - 分类管理（category_manage.html）
   - 标签管理（tags.html）

### 技术特点

1. **前端技术**
   - Bootstrap 5响应式设计
   - Chart.js数据可视化
   - Markdown编辑器集成
   - AJAX无刷新操作

2. **后端功能**
   - 图片上传和处理（使用Pillow）
   - 简易Markdown到HTML转换
   - 复杂数据库查询（使用SQLAlchemy）
   - 权限控制和安全检查

3. **用户体验优化**
   - 标签云动态大小
   - 模态框操作
   - 表单验证
   - 动画效果
