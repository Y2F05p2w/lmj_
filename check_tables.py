from app import create_app, db
import pymysql

app = create_app()

# 使用Flask应用上下文
with app.app_context():
    # 获取数据库连接信息
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    # 解析连接信息
    parts = db_uri.replace('mysql+pymysql://', '').split('/')
    db_name = parts[1]
    conn_info = parts[0].split('@')
    user_pass = conn_info[0].split(':')
    username = user_pass[0]
    password = user_pass[1]
    host = conn_info[1]
    
    # 连接数据库
    conn = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )
    
    try:
        with conn.cursor() as cursor:
            # 检查表是否存在
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            
            print("数据库中的表:")
            for table in tables:
                print(f" - {table}")
            
            # 检查特定表是否存在
            required_tables = ['post', 'comment', 'category', 'tag', 'post_tags']
            print("\n检查必要表是否存在:")
            
            for table in required_tables:
                if table in tables:
                    print(f" - {table} 表存在")
                else:
                    print(f" - {table} 表不存在")
                    
                    # 如果是post_tags表不存在，尝试创建它
                    if table == 'post_tags':
                        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS post_tags (
                            post_id INTEGER NOT NULL,
                            tag_id INTEGER NOT NULL,
                            PRIMARY KEY (post_id, tag_id),
                            CONSTRAINT fk_post_tags_post_id FOREIGN KEY (post_id) REFERENCES post (id),
                            CONSTRAINT fk_post_tags_tag_id FOREIGN KEY (tag_id) REFERENCES tag (id)
                        )
                        ''')
                        print(f"   - 创建了 {table} 表")
                    
                    # 如果是tag表不存在，尝试创建它
                    elif table == 'tag':
                        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS tag (
                            id INTEGER NOT NULL AUTO_INCREMENT, 
                            name VARCHAR(30) NOT NULL,
                            description VARCHAR(200),
                            created_at DATETIME,
                            PRIMARY KEY (id),
                            UNIQUE (name)
                        )
                        ''')
                        print(f"   - 创建了 {table} 表")
                    
                    # 如果是category表不存在，尝试创建它
                    elif table == 'category':
                        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS category (
                            id INTEGER NOT NULL AUTO_INCREMENT,
                            name VARCHAR(50) NOT NULL,
                            description VARCHAR(200),
                            created_at DATETIME,
                            PRIMARY KEY (id),
                            UNIQUE (name)
                        )
                        ''')
                        print(f"   - 创建了 {table} 表")
            
            # 检查post表的外键约束
            cursor.execute("""
                SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'post' AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (db_name,))
            foreign_keys = cursor.fetchall()
            
            print("\nPost表的外键约束:")
            for fk in foreign_keys:
                print(f" - {fk[1]} -> {fk[3]}.{fk[4]}")
                
        # 提交事务
        conn.commit()
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        conn.close() 