# mapping.py
import socket
import threading
import time
from analyze import resolve_address
from logger import log_info, log_error, log_debug, log_warning

active_mappings = {}
local_ports = {}  # 用于存储每个映射的本地 IP 和端口

def start_mapping(name, address, preferred_port=25565):
    """ 启动映射 """
    if name in active_mappings:
        log_info(f"映射 {name} 已经在运行。")
        return True

    try:
        remote_host, remote_port = resolve_address(address)
        if not remote_host:
            log_error(f"无法解析地址: {address}")
            return False
    except Exception as e:
        log_error(f"解析 {address} 失败: {str(e)}")
        return False

    local_port = find_available_port(preferred_port)
    if local_port is None:
        log_error(f"没有可用的端口来启动映射 {name}.")
        return False

    try:
        stop_event = threading.Event()
        thread = threading.Thread(target=start_proxy, args=(name, remote_host, remote_port, local_port, stop_event))
        thread.start()
        active_mappings[name] = (thread, stop_event)
        local_ports[name] = f"127.0.0.1:{local_port}"  # 记录分配的本地 IP 和端口

        # 启动局域网广播
        lan_thread = threading.Thread(target=broadcast_lan, args=(name, local_port, stop_event))
        lan_thread.start()
        log_info(f"映射 {name} 成功启动，监听端口: {local_port}")
        return True
    except Exception as e:
        log_error(f"无法连接到 {address} ({remote_host}:{remote_port}): {str(e)}")
        return False

def stop_mapping(name):
    """ 停止指定映射 """
    if name in active_mappings:
        log_info(f"停止映射 {name}")
        thread, stop_event = active_mappings[name]
        stop_event.set()
        thread.join()
        del active_mappings[name]
        del local_ports[name]  # 删除本地 IP 和端口记录
        log_info(f"映射 {name} 已停止")
    else:
        log_warning(f"尝试停止不存在的映射: {name}")

def modify_mapping(name, new_address=None, new_port=None):
    """ 修改映射的地址或端口 """
    if name in active_mappings:
        log_info(f"修改映射 {name}，新地址: {new_address}, 新端口: {new_port}")
        stop_mapping(name)
        return start_mapping(name, new_address, new_port or 25565)
    else:
        log_warning(f"映射 {name} 不存在，无法修改。")
        return False

def get_log_data():
    """ 获取所有映射的日志数据 """
    logs = []
    for name, (thread, stop_event) in active_mappings.items():
        logs.append(f"映射: {name}, 状态: {'运行中' if thread.is_alive() else '已停止'}")
    log_info("获取映射日志数据")
    return logs

def get_assigned_ports():
    """ 获取已分配的本地 IP 和端口 """
    return local_ports

def find_available_port(start_port=25565):
    """ 查找可用的端口 """
    port = start_port
    while port <= 65535:
        if not is_port_in_use(port):
            log_debug(f"找到可用端口: {port}")
            return port
        port += 1
    log_error("没有找到可用的端口")
    return None

def is_port_in_use(port):
    """ 检查端口是否被占用 """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_proxy(name, remote_host, remote_port, local_port, stop_event):
    """ 启动代理线程 """
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', local_port))
        server.listen(5)
        log_info(f"[{name}] 监听 0.0.0.0:{local_port}")

        while not stop_event.is_set():
            try:
                server.settimeout(1.0)
                client_socket, addr = server.accept()
                log_info(f"[{name}] 接受来自 {addr[0]}:{addr[1]} 的连接")

                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_socket.connect((remote_host, remote_port))

                client_handler = threading.Thread(target=handle_client, args=(client_socket, remote_socket, stop_event))
                server_handler = threading.Thread(target=handle_server, args=(remote_socket, client_socket, stop_event))

                client_handler.start()
                server_handler.start()

            except socket.timeout:
                continue

        server.close()
        log_info(f"[{name}] 已停止监听 {local_port}")

    except Exception as e:
        log_error(f"代理启动失败: {str(e)}")

def handle_client(client_socket, remote_socket, stop_event):
    """ 处理客户端数据转发 """
    try:
        while not stop_event.is_set():
            data = client_socket.recv(4096)
            if len(data) == 0:
                break
            remote_socket.sendall(data)
    except Exception as e:
        log_error(f"客户端数据转发错误: {str(e)}")
    finally:
        client_socket.close()
        remote_socket.close()

def handle_server(remote_socket, client_socket, stop_event):
    """ 处理服务器数据转发 """
    try:
        while not stop_event.is_set():
            data = remote_socket.recv(4096)
            if len(data) == 0:
                break
            client_socket.sendall(data)
    except Exception as e:
        log_error(f"服务器数据转发错误: {str(e)}")
    finally:
        client_socket.close()
        remote_socket.close()

def broadcast_lan(server_name, local_port, stop_event):
    """ 通过局域网广播Minecraft服务器 """
    try:
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        while not stop_event.is_set():
            message = f"[MOTD]{server_name}[/MOTD][AD]{local_port}[/AD]".encode('utf-8')
            broadcast_socket.sendto(message, ('<broadcast>', 4445))
            time.sleep(1)

        broadcast_socket.close()
    except Exception as e:
        log_error(f"局域网广播失败: {str(e)}")
