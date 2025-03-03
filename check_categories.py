from app import create_app, db
from app.models.blog import Category

def check_categories():
    """检查数据库中的分类"""
    app = create_app()
    with app.app_context():
        categories = Category.query.all()
        print("现有分类：")
        for category in categories:
            print(f"- {category.name}: {category.description or '无描述'}")

if __name__ == "__main__":
    check_categories() 