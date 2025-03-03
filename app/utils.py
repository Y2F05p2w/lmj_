import os
import secrets
from PIL import Image
from flask import current_app

def save_avatar(form_picture):
    """保存用户头像"""
    # 生成随机文件名
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    # 调整图片大小
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # 保存图片
    i.save(picture_path)
    
    return picture_fn 