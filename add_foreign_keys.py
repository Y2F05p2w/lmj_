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
            # 检查post表是否有指向category表的外键约束
            cursor.execute("""
                SELECT CONSTRAINT_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s 
                  AND TABLE_NAME = 'post' 
                  AND COLUMN_NAME = 'category_id'
                  AND REFERENCED_TABLE_NAME = 'category'
            """, (db_name,))
            constraint = cursor.fetchone()
            
            if not constraint:
                print("添加post表到category表的外键约束...")
                
                # 检查是否有索引，如果没有则添加
                cursor.execute("SHOW INDEX FROM post WHERE Column_name = 'category_id'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE post ADD INDEX idx_category_id (category_id)")
                    print("为category_id列添加了索引")
                
                # 添加外键约束
                cursor.execute("""
                    ALTER TABLE post 
                    ADD CONSTRAINT fk_post_category_id
                    FOREIGN KEY (category_id) REFERENCES category(id)
                """)
                print("成功添加外键约束")
            else:
                print(f"外键约束已存在: {constraint[0]}")
                
            # 检查所有外键约束
            cursor.execute("""
                SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'post' AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (db_name,))
            foreign_keys = cursor.fetchall()
            
            print("\nPost表的所有外键约束:")
            for fk in foreign_keys:
                print(f" - {fk[1]} ({fk[2]}) -> {fk[3]}.{fk[4]}")
                
        # 提交事务
        conn.commit()
        print("数据库更新成功")
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        conn.close() 