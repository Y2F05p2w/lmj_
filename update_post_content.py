import pymysql
from app import create_app

def update_post_content_type():
    """更新post表中content字段的类型为LONGTEXT"""
    app = create_app()
    
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
            # 修改content字段类型为LONGTEXT
            cursor.execute("ALTER TABLE post MODIFY content LONGTEXT;")
            print("成功将post表的content字段类型修改为LONGTEXT")
        
        # 提交更改
        conn.commit()
        
    except Exception as e:
        print(f"更新数据库时出错: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    update_post_content_type() 