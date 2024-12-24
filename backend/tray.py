import pystray
from PIL import Image
import threading
import webbrowser

class SystemTray:
    def __init__(self):
        self.icon = None
        self.setup_tray()

    def setup_tray(self):
        # 加载图标
        image = Image.open("assets/icon.png")
        
        # 创建菜单
        menu = (
            pystray.MenuItem("打开界面", self.open_ui),
            pystray.MenuItem("重启服务", self.restart_service),
            pystray.MenuItem("退出", self.quit_app)
        )
        
        # 创建托盘图标
        self.icon = pystray.Icon(
            "MC端口映射工具",
            image,
            "MC端口映射工具",
            menu
        )

    def run(self):
        self.icon.run()

    def open_ui(self):
        webbrowser.open('http://localhost:14011')

    def restart_service(self):
        # 实现重启逻辑
        pass

    def quit_app(self):
        self.icon.stop()
        # 实现退出逻辑 