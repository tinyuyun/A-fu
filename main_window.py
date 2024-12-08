#2.0
import tkinter as tk
from tkinter import scrolledtext, Label
import threading
from app_logic import check_and_print, show_photo  # 导入这两个函数
from model_setting_and_base_order import handle_conversation
from out_seting import exit_and_cleanup
import random
from auto_append_into_json import fuzzy_search
from out_seting import  attend_application
from applications_show import display_shortcuts
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

# 显示随机图像
show_photo(f"picture/{random_statum}.jpg", right_frame)

# 用户输入区域
user_input_entry = tk.Entry(root, width=40)
user_input_entry.grid(row=1, column=0, padx=10, pady=10)

# 提交按钮
# 提交按钮
def on_submit():
    user_input = user_input_entry.get().strip()
    if user_input:  # 检查输入是否为空
        threading.Thread(target=handle_conversation, args=(user_input, chat_window, right_frame, check_and_print)).start()
        user_input_entry.delete(0, tk.END)  # 清空输入框
    else:
        print("用户输入为空，请输入内容")


# 设置并退出按钮框架
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, padx=10, pady=10)

# 发送和退出按钮
submit_button = tk.Button(button_frame, text="发送", width=20, command=on_submit)
submit_button.grid(row=0, column=0, padx=5, pady=5)

exit_button = tk.Button(button_frame, text="退出", width=20, command=exit_and_cleanup)
exit_button.grid(row=0, column=1, padx=5, pady=5)

# 弹出设置和更多按钮
settings_button = tk.Button(right_frame, text="设置", width=15, command=lambda: toggle_scrollable_frame("设置"))
settings_button.grid(row=1, column=0, padx=10, pady=10)

more_button = tk.Button(right_frame, text="更多", width=15, command=lambda: toggle_scrollable_frame("更多"))
more_button.grid(row=2, column=0, padx=10, pady=10)

# 用于保存滚动框架的引用
scrollable_frame = None
current_frame_title = None  # 当前框架的标题

# 切换显示/隐藏滚动框架
# 用于保存滚动框架的引用
scrollable_frame = None
current_frame_title = None  # 当前框架的标题

# 切换显示/隐藏滚动框架
def toggle_scrollable_frame(title):
    global scrollable_frame, current_frame_title

    if scrollable_frame is not None:  # 已经有框架
        if current_frame_title != title:
            # 如果当前标题与传入的标题不同，销毁现有框架
            scrollable_frame.destroy()
            scrollable_frame = None
            current_frame_title = None  # 清空当前标题
            create_scrollable_button_frame(title)  # 创建新框架
        else:
            # 如果当前标题相同，销毁框架并将其重置
            scrollable_frame.destroy()
            scrollable_frame = None
            current_frame_title = None  # 清空当前标题
    else:
        # 如果没有滚动框架，直接创建一个
        create_scrollable_button_frame(title)

def create_scrollable_button_frame(title):
    global scrollable_frame, current_frame_title

    # 创建一个新的框架
    scrollable_frame = tk.Frame(root, width=150, height=300)
    scrollable_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

    canvas = tk.Canvas(scrollable_frame, width=150)
    scrollable_canvas = tk.Frame(canvas)
    scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.grid(row=0, column=0, sticky="nsew")
    canvas.create_window((0, 0), window=scrollable_canvas, anchor="nw")

    # 根据标题显示不同的内容
    if title == "设置":
        options = ["一键导入", "添加应用", "查看已有应用列表"]
    elif title == "更多":
        options = ["更多选项 1", "更多选项 2", "更多选项 3"]
    else:
        options = ["默认选项 1", "默认选项 2", "默认选项 3"]

    # 添加标题
    title_label = tk.Label(scrollable_canvas, text=title, font=("Helvetica", 14, "bold"))
    title_label.grid(row=0, column=0, padx=10, pady=10)

    # 添加按钮
    for i, option in enumerate(options):
        button = tk.Button(scrollable_canvas, text=option, command=lambda opt=option: execute_option(opt))
        button.grid(row=i + 1, column=0, padx=10, pady=5)

    # 更新滚动区域的大小
    scrollable_canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # 更新当前框架的标题
    current_frame_title = title
def execute_option(option):
    """执行选项对应的操作"""
    if option == "一键导入":
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, fuzzy_search())
        chat_window.config(state=tk.DISABLED)
        chat_window.yview(tk.END)
    elif option == "添加应用":
        attend_application()
    elif option == "查看已有应用列表":
        json_file = 'applications.json'  # 替换为你的 JSON 文件路径
        display_shortcuts(json_file)
    print(f"执行操作：{option}")

# 启动界面主循环
root.mainloop()
