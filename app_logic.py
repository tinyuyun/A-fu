import os
import re
from tkinter import Label
from PIL import Image, ImageTk
import random

# 随机图像名类
statum = [
    "乖乖坐着",
    "躲在角落",
    "打喷嚏",
    "被抓住",
    "被抚摸",
    "抱腿坐"
]
random_statum = random.choice(statum)

# 图像选择器，查看名称是否可用，文件是否存在，存在则展示文件，若不存在，则展示随机初始图像
def check_and_print(content, right_frame):
    if not isinstance(content, str):  # 检查 content 是否是字符串类型
        print(f"Warning: Expected a string, but got {type(content)}")
        content = str(content)  # 尝试将其转换为字符串

    matches = re.findall(r'\{(.*?)\}', content)
    # 后续的处理...
    found_files = []  # 用于存储存在的文件名

    for match in matches:
        # 构建 jpg 和 png 文件路径
        jpg_file = f"picture/{match}.jpg"
        png_file = f"picture/{match}.png"

        # 检查 jpg 文件和 png 文件是否存在
        if os.path.isfile(jpg_file):
            found_files.append(jpg_file)
        if os.path.isfile(png_file):
            found_files.append(png_file)

    if found_files:
        print("存在的文件:", found_files)  # 输出存在的文件名
        show_photo(found_files[0], right_frame)
        return "ok", re.sub(r'\{(.*?)\}', '', content)

    print("未找到任何文件")
    show_photo(f"picture/{random_statum}.jpg", right_frame)
    return "no", re.sub(r'\{(.*?)\}', '', content)

# 加载并显示图片
def show_photo(picture: str, right_frame):
    # 清空现有的图像以避免重复显示
    for widget in right_frame.winfo_children():
        if isinstance(widget, Label):  # 只销毁 Label 类型的控件（即图片）
            widget.destroy()
    try:
        # 使用Pillow加载图像
        image = Image.open(picture)  # 使用文件路径
        image = image.resize((200, 200), Image.LANCZOS)  # 使用 LANCZOS 进行缩放
        image = ImageTk.PhotoImage(image)  # 转换为Tkinter可用的格式

        # 创建标签并显示图像
        image_label = Label(right_frame, image=image)
        image_label.image = image  # 保持对图片对象的引用
        image_label.grid(row=0, column=0, padx=5, pady=5)  # 使用 grid 添加边距
    except Exception as e:
        print(f"Could not load image: {e}")
        show_photo(f"picture/{random_statum}.jpg", right_frame)
