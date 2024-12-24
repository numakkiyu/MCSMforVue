# Minecraft服务器映射工具 for Vue.js 3

Minecraft服务器映射工具是一款用于将远程 Minecraft 服务器映射到本地的工具，使其能够通过局域网方式连接；本库重新设计UI系统，基于Vue.js优化整体布局界面

## 功能介绍

主要工作原理就是通过获取服务器的域名地址进行获取 _minecraft._tcp 的 SRV 记录，如果失败，则会尝试解析 A 记录或 CNAME 记录，以确定服务器的 IP 地址和端口，并且本地启动一个socket代理服务器，双向数据转发建立双向的 TCP 连接，远程服务器的响应数据也会通过代理服务器转发回本地客户端，代理服务器会通过 UDP 广播MC的局域网发现协议包，模拟服务器在本地局域网中的存在，使得同一局域网内的其他设备可以发现并连接到该服务器，该工具在 DNS 解析时尽量采用标准的解析方法如 SRV、A、CNAME 记录。这种行为与普通客户端直接连接到服务器的方式没有区别，因此可能不会触发一些检测机制，所以这是legit的

## 安装方法

### 前提条件

- **Node.js**：请确保已安装 [Node.js](https://nodejs.org/) (版本 >= 14)。
- **Python 3**：请确保已安装 [Python 3](https://www.python.org/downloads/)。

### 安装前端依赖

进入前端目录并安装依赖：

```bash
cd frontend
cnpm install
```

### 安装后端依赖

进入后端目录并安装依赖：

```bash
cd ../backend
pip install -r requirements.txt
```

**注意**：确保 `backend/requirements.txt` 文件包含以下内容：

```plaintext
Flask
Flask-CORS
psutil
requests
mcstatus
dnspython
colorama
```

如果 `requirements.txt` 文件不存在，可以手动创建并添加上述内容。

### 安装Electron相关依赖

回到前端目录并安装Electron依赖：

```bash
cd ../frontend
cnpm install electron electron-builder -D
```

## 运行方法

### 使用启动器运行

启动器 `launcher.py` 可同时管理前端和后端进程，提供简便的运行方式。

1. 确保所有依赖已安装（参见安装方法）。
2. 回到项目根目录并运行启动器：

```bash
cd ..
python launcher.py
```

启动器会自动启动后端服务，并启动Electron应用。应用窗口应显示在桌面，且后端服务通过内部通信进行交互。

### 开发模式运行

在开发模式下，可以分别启动前端和后端，并通过Electron进行集成。

1. 启动后端服务：

```bash
cd backend
python run.py
```

2. 启动前端开发服务器：

```bash
cd ../frontend
cnpm run dev
```

3. 启动Electron应用：

打开一个新的终端窗口，进入前端目录并运行：

```bash
cnpm run electron:serve
```

### 生产模式运行

在生产模式下，应用将打包为独立的桌面应用程序。

1. 打包前端：

```bash
cd frontend
cnpm run build
```

2. 打包成Electron应用：

```bash
cnpm run electron:build
```

打包完成后，生成的安装程序将在 `frontend/dist_electron` 目录中。

3. 运行安装程序：

双击生成的安装程序，按照提示完成安装并启动应用。

## 使用方法

1. **启动应用**：
   - 使用启动器运行：`python launcher.py`
   - 或使用打包后的安装程序启动。

2. **添加服务器**：
   - 点击“添加服务器”按钮，填写服务器名称、地址和映射端口。
   - 保存后，服务器将显示在列表中。

3. **管理服务器**：
   - 使用“启动”或“停止”按钮控制服务器端口映射。
   - 编辑或删除服务器配置。

4. **查看服务器状态**：
   - 列表中显示每个服务器的在线状态、延迟、玩家信息等。

5. **日志查看**：
   - 后端日志保存在 `backend/logs/mc_mapper.log`，可用于调试和查看操作记录。

## 项目结构

```
mc-port-mapper/
├── backend/
│   ├── app.py
│   ├── analyze.py
│   ├── launcher.py
│   ├── logger.py
│   ├── mappings.py
│   ├── port.py
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   │   ├── main.css
│   │   │   └── icon.png
│   │   ├── components/
│   │   │   ├── ServerMonitor.vue
│   │   │   └── TitleBar.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── store/
│   │   │   └── index.js
│   │   ├── utils/
│   │   │   ├── animations.js
│   │   │   ├── dataTransfer.js
│   │   │   ├── date.js
│   │   │   ├── hotkeys.js
│   │   │   ├── motd.js
│   │   │   ├── request.js
│   │   │   └── theme.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   │   └── index.html
│   ├── electron/
│   │   └── main.js
│   ├── package.json
│   └── .env.development
└── README.md
```

## 贡献

欢迎提交Issues和Pull Requests。如果你有新的功能建议或发现bug，请随时提出。

1. Fork 本项目
2. 创建你的分支 (`git checkout -b feature/新功能`)
3. 提交你的修改 (`git commit -m '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建一个Pull Request

## 许可证

本项目采用 [GPL v3.0 许可证](LICENSE)。

## 联系方式

如有任何问题或建议，请联系：

- **博客**：[佰川的秘密基地](https://me.tianbeigm.cn/)
