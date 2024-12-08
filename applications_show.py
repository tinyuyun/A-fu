import json
import tkinter as tk
from tkinter import scrolledtext

def load_shortcuts(json_file):
    """读取 JSON 文件并返回快捷方式名称的列表"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 返回快捷方式名称列表
            return list(data.keys())
    except FileNotFoundError:
        print(f"文件 {json_file} 未找到。")
        return []  # 如果文件不存在，返回空列表
    except json.JSONDecodeError:
        print(f"文件 {json_file} 的格式有误。")
        return []  # 如果JSON解析出错，返回空列表

def display_shortcuts(json_file):
    """读取 JSON 文件并在滚动文本框中显示快捷方式名称"""
    # 创建主窗口
    root = tk.Tk()
    root.title("应用列表")

    # 创建一个滚动文本框
    text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20,font=("Arial", 12))
    text_box.pack(padx=10, pady=10)

    # 读取快捷方式名称
    shortcuts = load_shortcuts(json_file)

    # 插入快捷方式名称到文本框
    for shortcut in shortcuts:
        text_box.insert(tk.END, shortcut + '\n')

    # 启动 Tkinter 主循环
    root.mainloop()

if __name__ == "__main__":
    json_file = 'applications.json'  # 替换为你的 JSON 文件路径
    display_shortcuts(json_file)