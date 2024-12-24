import PyInstaller.__main__
import os

def build():
    # 应用图标
    icon = os.path.abspath("assets/icon.ico")
    
    # PyInstaller参数
    params = [
        'run.py',                     # 主脚本
        '--name=MC端口映射工具',      # 应用名称
        '--icon=' + icon,            # 应用图标
        '--noconsole',               # 不显示控制台
        '--add-data=templates;templates', # 添加模板目录
        '--add-data=static;static',      # 添加静态文件
        '--onefile',                 # 打包成单个文件
        '--clean',                   # 清理临时文件
        '--win-private-assemblies',  # 打包Windows私有程序集
        '--win-no-prefer-redirects', # 不使用重定向
    ]
    
    # 执行打包
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    build() 