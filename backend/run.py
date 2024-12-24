import sys
import os
from app import app

def main():
    try:
        # 设置工作目录
        os.chdir(os.path.dirname(os.path.abspath(__file__)))


        # 创建必要的目录
        os.makedirs('data', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # 启动Flask应用
        app.run(host='127.0.0.1', port=14011)
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 