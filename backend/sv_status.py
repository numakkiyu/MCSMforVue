# sv_status.py
from mcstatus import JavaServer
from logger import log_info, log_error

def get_server_status(address):
    """ 获取服务器状态信息 """
    try:
        # 使用 JavaServer.lookup 来解析服务器地址
        server = JavaServer.lookup(address)
        status = server.status()  # 获取服务器状态

        # 构造返回的服务器信息
        server_info = {
            'version': status.version.name,       # 服务器版本
            'latency': status.latency,            # 服务器延迟（毫秒）
            'motd': status.description,           # 服务器 MOTD（描述）
            'players': status.players.online,     # 在线玩家数量
            'icon': status.favicon                # Base64 编码的服务器图标
        }

        log_info(f"获取服务器状态成功: {address}")
        return server_info

    except Exception as e:
        log_error(f"无法获取服务器状态: {address}, 错误: {str(e)}")
        return None

def get_server_latency(address):
    """ 获取服务器延迟 """
    try:
        server = JavaServer.lookup(address)
        latency = server.ping()
        log_info(f"获取服务器延迟成功: {address}, 延迟: {latency} ms")
        return latency
    except Exception as e:
        log_error(f"无法获取服务器延迟: {address}, 错误: {str(e)}")
        return None

def get_server_query(address):
    """ 获取服务器查询信息（需要服务器启用 query 功能） """
    try:
        server = JavaServer.lookup(address)
        query = server.query()
        log_info(f"获取服务器查询成功: {address}")
        return {
            'players': query.players.names,      # 在线玩家名单
            'software': query.software.brand,   # 服务器软件信息
            'plugins': query.software.plugins   # 服务器插件信息
        }
    except Exception as e:
        log_error(f"无法获取服务器查询信息: {address}, 错误: {str(e)}")
        return None
