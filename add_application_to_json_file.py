import tkinter as tk
from tkinter import messagebox
import json
import os


# 读取 JSON 文件
def load_json(file_path):
    """读取 JSON 文件"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}


# 保存 JSON 文件
def save_json(file_path, data):
    """保存 JSON 文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# 处理录入新的应用信息
def handle_add_application(app_name_entry, app_path_entry):
    app_name = app_name_entry.get()
    app_path = app_path_entry.get()

    if not app_name or not app_path:
        messagebox.showerror("错误", "应用名称和路径不能为空。")
        return

    # 读取现有的 JSON 文件
    data = load_json("applications.json")

    if app_name in data:
        messagebox.showerror("错误", f"应用 '{app_name}' 已存在。")
        return

    # 将新应用信息添加到 JSON 数据中
    data[app_name] = app_path
    save_json("applications.json", data)

    messagebox.showinfo("成功", f"成功录入应用 '{app_name}'。")


# 录入应用信息的 GUI 窗口
def attend_application():
    # 创建主窗口
    root = tk.Tk()
    root.title("应用录入系统")

    # 创建输入框和标签
    tk.Label(root, text="应用名称:").grid(row=0, column=0, padx=10, pady=5)
    app_name_entry = tk.Entry(root, width=40)
    app_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="应用路径:").grid(row=1, column=0, padx=10, pady=5)
    app_path_entry = tk.Entry(root, width=40)
    app_path_entry.grid(row=1, column=1, padx=10, pady=5)

    # 创建按钮
    add_button = tk.Button(root, text="添加应用", width=20, command=lambda: handle_add_application(app_name_entry, app_path_entry))
    add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    # 启动主事件循环
    root.mainloop()


if __name__ == "__main__":
    # 启动应用录入窗口
    attend_application()


