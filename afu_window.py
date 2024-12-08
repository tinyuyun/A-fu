#1.0
import tkinter as tk
from tkinter import scrolledtext, Label
from PIL import Image, ImageTk
import threading
import os
import re
from model_setting_and_base_order import handle_conversation
from out_seting import exit_and_cleanup
import random

#管理员权限确认，打包时清除注释
# import check_is_admin
# import sys
#
# if check_is_admin.is_admin():
#     check_is_admin.admin_function()  # 如果是管理员，执行管理员操作
# else:
#     print("正在请求管理员权限...")
#     check_is_admin.run_as_admin()  # 如果不是管理员，尝试以管理员权限重新启动程序
#     sys.exit()

#图像选择器，查看名称是否可用，文件是否存在，存在则展示文件，若不存在，则展示随机初始图像
def check_and_print(content,on):
    # 使用正则表达式查找 { } 包裹的内容
    matches = re.findall(r'\{(.*?)\}', content)

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

            # 如果找到存在的文件，打印它们
    if found_files:
        print("存在的文件:", found_files)  # 输出存在的文件名
        show_photo(found_files[0])
        return "ok",re.sub(r'\{(.*?)\}', '', content)

    print("未找到任何文件")
    show_photo(f"picture/{random_statum}.jpg")
    return "no",re.sub(r'\{(.*?)\}', '', content)

#随机图像名类
statum = [
    "乖乖坐着",
    "躲在角落",
    "打喷嚏",
    "被抓住",
    "被抚摸",
    "抱腿坐"
]
random_statum = random.choice(statum)

# 加载并显示图片
def show_photo(picture: str):
    # 清空现有的图像以避免重复显示
    for widget in right_frame.winfo_children():
        widget.destroy()

    try:
        # 使用Pillow加载图像
        image = Image.open(picture)  # 使用文件路径
        image = image.resize((200, 200), Image.LANCZOS)  # 使用 LANCZOS 进行缩放
        image = ImageTk.PhotoImage(image)  # 转换为Tkinter可用的格式

        # 创建标签并显示图像
        image_label = Label(right_frame, image=image)
        image_label.image = image  # 保持对图片对象的引用
        image_label.pack(padx=5, pady=5)  # 添加边距
    except Exception as e:
        print(f"Could not load image: {e}")
        show_photo( f"picture/{random_statum }.jpg")

# 创建主窗口
root = tk.Tk()
root.title("猫娘对话界面")
root.resizable(False, False)

# 创建滚动文本框用于显示聊天内容
chat_window = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD, state=tk.DISABLED)
chat_window.grid(row=0, column=0, padx=10, pady=10)

# 创建右侧框架用于显示时评或图片
right_frame = tk.Frame(root, width=200, height=300)
right_frame.grid(row=0, column=1, padx=10, pady=10)



show_photo(f"picture/{random_statum }.jpg")
# 用户输入区域
user_input_entry = tk.Entry(root, width=40)
user_input_entry.grid(row=1, column=0, padx=10, pady=10)


# 提交按钮
def on_submit():
    user_input = user_input_entry.get().strip()
    if user_input:  # 检查输入是否为空
        threading.Thread(target=handle_conversation, args=(user_input, chat_window,"", check_and_print)).start()
        user_input_entry.delete(0, tk.END)  # 清空输入框
    else:
        print("用户输入为空，请输入内容")
    # 创建按钮框架


button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, padx=10, pady=10)

# 发送和退出按钮
submit_button = tk.Button(button_frame, text="发送", width=20, command=on_submit)
submit_button.pack(side=tk.LEFT, padx=5)
exit_button = tk.Button(button_frame, text="退出", width=20, command=exit_and_cleanup)
exit_button.pack(side=tk.LEFT, padx=5)

# 启动界面主循环
root.mainloop()

# 编写过程出现的问题
# 注意：导入Pillow时使用 from PIL import Image, ImageTk
# Pillow 10.0.0 及以上版本中，ANTIALIAS 已被移除，直接使用 Image.LANCZOS 代替。