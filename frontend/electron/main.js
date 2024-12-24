const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const { spawn } = require('child_process')
const isDev = process.env.NODE_ENV === 'development'

let mainWindow
let pythonProcess

function createWindow() {
  // 创建主窗口
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    frame: false, // 无边框窗口
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    icon: path.join(__dirname, '../assets/icon.png')
  })

  // 加载页面
  if (isDev) {
    mainWindow.loadURL('http://localhost:8080')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  // 窗口控制
  ipcMain.on('window-min', () => mainWindow.minimize())
  ipcMain.on('window-max', () => {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize()
    } else {
      mainWindow.maximize()
    }
  })
  ipcMain.on('window-close', () => mainWindow.close())
}

function startPythonBackend() {
  // 启动Python后端
  const pythonExecutable = isDev ? 'python' : path.join(process.resourcesPath, 'backend/run.exe')
  const scriptPath = isDev ? path.join(__dirname, '../../backend/run.py') : path.join(process.resourcesPath, 'backend/run.py')

  pythonProcess = spawn(pythonExecutable, [scriptPath])

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python输出: ${data}`)
    mainWindow?.webContents.send('backend-log', data.toString())
  })

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python错误: ${data}`)
    mainWindow?.webContents.send('backend-error', data.toString())
  })
}

app.whenReady().then(() => {
  createWindow()
  startPythonBackend()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (pythonProcess) {
      pythonProcess.kill()
    }
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
}) 