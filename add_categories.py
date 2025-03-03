from app import create_app, db
from app.models.blog import Category

def add_categories():
    """检查并添加博客分类"""
    app = create_app()
    with app.app_context():
        # 要添加的分类列表
        categories = [
            {"name": "网络安全", "description": "关于网络安全、信息安全、安全防护等方面的文章"},
            {"name": "编程", "description": "编程语言、开发技巧、算法等相关内容"},
            {"name": "区块链", "description": "区块链技术、加密货币、智能合约等相关内容"},
            {"name": "网络技术", "description": "网络架构、协议、网络设备等相关内容"},
            {"name": "运维", "description": "系统运维、服务器管理、DevOps等相关内容"}
        ]
        
        # 检查并添加分类
        for category_data in categories:
            # 检查分类是否已存在
            existing = Category.query.filter_by(name=category_data["name"]).first()
            if existing:
                print(f"分类 '{category_data['name']}' 已存在")
            else:
                # 添加新分类
                new_category = Category(
                    name=category_data["name"],
                    description=category_data["description"]
                )
                db.session.add(new_category)
                print(f"添加新分类: '{category_data['name']}'")
        
        # 提交更改
        db.session.commit()
        print("分类添加完成")
        
        # 列出所有分类
        all_categories = Category.query.all()
        print("\n当前所有分类:")
        for category in all_categories:
            print(f"- {category.name}: {category.description}")

if __name__ == "__main__":
    add_categories() 