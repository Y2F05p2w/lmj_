from app import create_app, db
from app.models.blog import Post, File

def update_database():
    """更新数据库表结构，添加缺少的列"""
    app = create_app()
    with app.app_context():
        # 检查post表是否存在like_count列
        try:
            # 尝试查询一条记录的like_count字段
            db.session.query(Post.like_count).first()
            print("like_count列已存在，无需添加")
        except Exception as e:
            if "Unknown column 'post.like_count'" in str(e):
                # 如果列不存在，则添加
                print("正在添加like_count列...")
                db.engine.execute("ALTER TABLE post ADD COLUMN like_count INTEGER DEFAULT 0")
                print("like_count列添加成功")
            else:
                print(f"查询like_count时出错: {e}")
        
        # 检查post_likes表是否存在
        try:
            # 尝试执行一个查询来检查表是否存在
            db.engine.execute("SELECT 1 FROM post_likes LIMIT 1")
            print("post_likes表已存在")
        except Exception as e:
            if "doesn't exist" in str(e) or "Unknown table" in str(e):
                # 如果表不存在，则创建
                print("正在创建post_likes表...")
                db.engine.execute("""
                CREATE TABLE post_likes (
                    post_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (post_id, user_id),
                    FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
                )
                """)
                print("post_likes表创建成功")
            else:
                print(f"检查post_likes表时出错: {e}")
        
        # 检查file表是否存在
        try:
            # 尝试执行一个查询来检查表是否存在
            db.engine.execute("SELECT 1 FROM file LIMIT 1")
            print("file表已存在")
        except Exception as e:
            if "doesn't exist" in str(e) or "Unknown table" in str(e):
                # 如果表不存在，则创建
                print("正在创建file表...")
                db.engine.execute("""
                CREATE TABLE file (
                    id INTEGER NOT NULL AUTO_INCREMENT,
                    filename VARCHAR(100) NOT NULL,
                    original_filename VARCHAR(100) NOT NULL,
                    file_path VARCHAR(200) NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_type VARCHAR(50) NOT NULL,
                    upload_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    description VARCHAR(200),
                    download_count INTEGER DEFAULT 0,
                    PRIMARY KEY (id),
                    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
                )
                """)
                print("file表创建成功")
            else:
                print(f"检查file表时出错: {e}")

if __name__ == "__main__":
    update_database() 