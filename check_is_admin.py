#check_is_admin.py
import os
import sys
import subprocess
import platform
import ctypes

def is_admin():
    """检查当前用户是否具有管理员权限"""
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        return os.geteuid() == 0

def run_as_admin():
    """以管理员身份重新启动当前程序"""
    if platform.system() == "Windows":
        # 以管理员权限运行当前脚本
        script = sys.argv[0]
        params = ' '.join(sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(None,"runas", sys.executable, "", None, 1)
    else:
        print("当前操作系统不支持此功能")
        sys.exit(1)

def admin_function():
    """需要管理员权限的操作"""
    print("管理员功能已启动！")