import subprocess
import json
import os

def load_json(file_path):
    """读取 JSON 文件"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}

def open_application(app_name, json_file="applications.json"):
    """根据应用名称从 JSON 文件中获取路径并启动应用"""
    data = load_json(json_file)
    app_path = data.get(app_name)

    if app_path and os.path.exists(app_path):
        try:
            subprocess.run([app_path], check=True)
            return f"成功打开应用: {app_name}"
        except Exception as e:
            return f"启动应用失败: {str(e)}"
    else:
        return f"未找到应用或路径无效。"

