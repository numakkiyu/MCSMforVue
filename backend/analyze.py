# analyze.py
import dns.resolver
import socket
from mcstatus import JavaServer
from logger import log_info, log_error, log_warning

def resolve_address(server_address):
    """ 解析服务器域名或 IP """
    log_info(f"开始解析地址: {server_address}")
    last_exception = None

    if ':' in server_address:
        server_address, custom_port = server_address.split(':')
        custom_port = int(custom_port)
    else:
        custom_port = 25565  # 默认 Minecraft 端口

    if is_valid_ip(server_address):
        log_info(f"解析为合法IP: {server_address}:{custom_port}")
        return server_address, custom_port

    try:
        srv_records = dns.resolver.resolve(f'_minecraft._tcp.{server_address}', 'SRV')
        for srv in srv_records:
            log_info(f"SRV记录解析成功: {srv.target}:{srv.port}")
            return str(srv.target).rstrip('.'), srv.port
    except Exception as e:
        last_exception = e
        log_warning(f"SRV记录解析失败: {server_address}, 错误: {str(e)}")

    try:
        a_records = dns.resolver.resolve(server_address, 'A')
        log_info(f"A记录解析成功: {a_records[0].address}:{custom_port}")
        return a_records[0].address, custom_port
    except Exception as e:
        last_exception = e
        log_error(f"A记录解析失败: {server_address}, 错误: {str(e)}")

    if last_exception:
        log_error(f"解析失败: {server_address}, 错误: {str(last_exception)}")
        return None, None

def is_valid_ip(address):
    """ 验证是否为合法IP """
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False

def analyze_server(address):
    """
    分析Minecraft服务器状态
    """
    try:
        # 解析地址和端口
        host, port = resolve_address(address)
        if not host:
            return {
                'online': False,
                'error': '地址解析失败'
            }

        # 创建服务器对象
        server = JavaServer.lookup(f"{host}:{port}")
        
        # 获取状态
        status = server.status()
        
        # 获取延迟
        latency = server.ping()
        
        # 尝试获取查询信息
        try:
            query = server.query()
            has_query = True
            plugins = query.software.plugins
            players = query.players.names
        except:
            has_query = False
            plugins = []
            players = []

        return {
            'online': True,
            'version': status.version.name,
            'protocol': status.version.protocol,
            'description': str(status.description),
            'players': {
                'online': status.players.online,
                'max': status.players.max,
                'list': players if has_query else []
            },
            'latency': round(latency, 2),
            'has_query': has_query,
            'plugins': plugins if has_query else [],
            'favicon': status.favicon
        }
    except socket.timeout:
        return {
            'online': False,
            'error': '连接超时'
        }
    except Exception as e:
        return {
            'online': False,
            'error': str(e)
        }

if __name__ == '__main__':
    # 测试代码
    test_server = "mc.hypixel.net"
    result = analyze_server(test_server)
    print(f"服务器分析结果: {result}")
