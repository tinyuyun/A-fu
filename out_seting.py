import glob
import os
import open_application_from_json_file
import add_application_to_json_file
from auto_append_into_json import fuzzy_search_and_save
def get_exe_open(exe_play: str):
    """打开应用"""

    result = open_application_from_json_file.open_application(exe_play)  # 打开程序
    if result != "未找到应用或路径无效。":
        return {"exe_play": result},None
    matched_shortcuts = fuzzy_search_and_save(exe_play)  # 模糊搜索程序并保存结果
    if not matched_shortcuts:
        return {"exe_play":"未找到匹配的程序。"},None  # 如果没有找到匹配的程序
    if len(matched_shortcuts) == 1:
        # 如果只有一个匹配的程序，直接打开并返回结果
        exe_name = list(matched_shortcuts.keys())[0]  # 获取唯一匹配的程序名称
        result = open_application_from_json_file.open_application(exe_name)  # 打开程序
        return {"exe_name": result} , None# 返回打开的结果

    # 如果找到了多个匹配的程序，返回它们的编号和程序名
    matched_str = ""
    for index, (name, path) in enumerate(matched_shortcuts.items(), 1):
        matched_str += f"{index}. {name}\n"  # 格式化输出程序的序号和名称
        matched_str=str(matched_str)
    return {"exe_play":"找到多个程序,请选择一个打开"},f"\n找到多个程序,\n{matched_str}" # 返回找到的多个程序的列表

def attend_application():
    """添加应用的过程"""
    p = add_application_to_json_file.attend_application()
    return {"attend_application_process": "successfully opened"}

def exit_and_cleanup():
    """退出并清理 MP3 文件"""
    cleanup_mp3_files()
    print("退出程序...")
    exit()

def cleanup_mp3_files():
    """清理当前目录下的所有 MP3 文件"""
    mp3_files = glob.glob("*.mp3")
    for mp3_file in mp3_files:
        try:
            os.remove(mp3_file)
            print(f"成功删除文件: {mp3_file}")
        except Exception as e:
            print(f"无法删除文件 {mp3_file}: {e}")


