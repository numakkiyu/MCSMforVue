import os
import sys
import subprocess
import threading
import time
import signal
import psutil
from pathlib import Path

class Launcher:
    def __init__(self):
        self.frontend_process = None
        self.electron_process = None
        self.is_dev = True  # 开发模式标志
        
        # 获取项目根目录
        self.root_dir = Path(__file__).parent
        self.frontend_dir = self.root_dir / 'frontend'
        self.backend_dir = self.root_dir / 'backend'

    def start_frontend(self):
        """启动前端"""
        os.chdir(self.frontend_dir)
        if self.is_dev:
            # 开发模式
            npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
            self.frontend_process = subprocess.Popen(
                [npm_cmd, 'run', 'electron:serve'],
                cwd=self.frontend_dir
            )
        else:
            # 生产模式
            electron_exe = self.frontend_dir / 'dist_electron' / 'win-unpacked' / 'MC端口映射工具.exe'
            if electron_exe.exists():
                self.frontend_process = subprocess.Popen([str(electron_exe)])
            else:
                print("错误: 找不到打包后的应用程序")
                sys.exit(1)

    def start_backend(self):
        """启动后端"""
        os.chdir(self.backend_dir)
        python_exe = 'python'
        self.electron_process = subprocess.Popen(
            [python_exe, 'run.py'],
            cwd=self.backend_dir
        )

    def cleanup(self):
        """清理进程"""
        def kill_process_tree(pid):
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.kill()
                parent.kill()
            except psutil.NoSuchProcess:
                pass

        if self.frontend_process:
            kill_process_tree(self.frontend_process.pid)
        if self.electron_process:
            kill_process_tree(self.electron_process.pid)

    def check_dependencies(self):
        """检查必要的依赖是否已安装"""
        required_packages = {
            'flask': 'Flask',
            'flask-cors': 'Flask-CORS',
            'psutil': 'psutil',
            'requests': 'requests',
            'mcstatus': 'mcstatus'
        }
        
        missing_packages = []
        
        for import_name, package_name in required_packages.items():
            try:
                __import__(import_name)
            except ImportError:
                missing_packages.append(package_name)
        
        if missing_packages:
            print("缺少必要的依赖包，正在安装...")
            for package in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("依赖安装完成！")

    def run(self):
        """运行应用"""
        try:
            print("正在启动MC端口映射工具...")
            self.check_dependencies()
            
            # 启动后端
            print("启动后端服务...")
            self.start_backend()
            time.sleep(2)  # 等待后端启动
            
            # 启动前端
            print("启动前端界面...")
            self.start_frontend()
            
            print("应用程序已启动!")
            
            # 等待进程结束
            while True:
                if self.frontend_process.poll() is not None or \
                   self.electron_process.poll() is not None:
                    break
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n正在关闭应用程序...")
        finally:
            self.cleanup()
            print("应用程序已关闭")

def create_dev_bat():
    """创建开发模式启动脚本"""
    content = """@echo off
echo 正在启动MC端口映射工具(开发模式)...
python launcher.py
pause
"""
    with open('dev.bat', 'w') as f:
        f.write(content)

def create_run_bat():
    """创建生产模式启动脚本"""
    content = """@echo off
echo 正在启动MC端口映射工具...
python launcher.py
pause
"""
    with open('run.bat', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    create_dev_bat()
    create_run_bat()

    launcher = Launcher()
    launcher.run() 