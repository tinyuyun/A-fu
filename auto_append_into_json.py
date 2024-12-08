import os
import json
import win32com.client

def get_shortcut_target(shortcut_path):
    """获取快捷方式指向的目标路径"""
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    return shortcut.Targetpath

def get_shortcuts(folder_path):
    """递归获取指定文件夹及其所有子文件夹内的所有快捷方式的名称及其目标"""
    shortcuts = {}
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.lnk'):
                shortcut_path = os.path.join(root, filename)  # 获取完整的快捷方式路径
                try:
                    target_path = get_shortcut_target(shortcut_path)
                    # 去掉文件后缀名
                    shortcut_name = filename[:-4]
                    # 仅在目标路径不存在时添加
                    shortcuts[shortcut_name] = target_path
                except Exception as e:
                    print(f"无法读取{shortcut_path}: {e}")

    return shortcuts

def load_existing_shortcuts(output_file):
    """从 JSON 文件加载现有的快捷方式信息"""
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_shortcuts_to_json(shortcuts, output_file):
    """将快捷方式信息保存为 JSON 文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(shortcuts, f, ensure_ascii=False, indent=4)

def fuzzy_query(shortcuts, query):
    """模糊查询快捷方式，返回匹配的结果"""
    matched_shortcuts = {}
    query_lower = query.lower()  # 转为小写以实现不区分大小写的匹配
    for shortcut_name, target_path in shortcuts.items():
        if query_lower in shortcut_name.lower() or query_lower in target_path.lower():  # 不区分大小写
            matched_shortcuts[shortcut_name] = target_path
    return matched_shortcuts

def fuzzy_search():
    folder_path = r"C:\ProgramData\Microsoft\Windows\Start Menu"  # 替换为你的快捷方式文件夹路径
    output_file = 'applications.json'

    # 加载现有快捷方式
    existing_shortcuts = load_existing_shortcuts(output_file)

    # 获取新的快捷方式
    new_shortcuts = get_shortcuts(folder_path)

    # 合并新快捷方式与现有快捷方式
    existing_shortcuts.update(new_shortcuts)

    # 保存合并后的信息到 JSON 文件
    save_shortcuts_to_json(existing_shortcuts, output_file)

    return f"已导出 {len(new_shortcuts)} 个快捷方式到 {output_file}"

def fuzzy_search_and_save(query):
    output_file = 'applications.json'
    existing_shortcuts = load_existing_shortcuts(output_file)
    # 模糊查询

    matched_shortcuts = fuzzy_query(existing_shortcuts, query)

    if matched_shortcuts:
        print("匹配的程序:")
        for name, path in matched_shortcuts.items():
            print(f"{name}: {path}")
    else:
        print("未找到匹配的程序。")
    return matched_shortcuts

