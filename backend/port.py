# port.py
import socket
import subprocess
import threading
import time
from logger import log_info, log_error, log_warning
from analyze import resolve_address, analyze_server
from mappings import load_mappings, save_mappings

class PortManager:
    def __init__(self):
        self.mappings = {}  # 存储活动的映射
        self.processes = {}  # 存储映射进程
        self.lock = threading.Lock()  # 线程锁

    def add_mapping(self, mapping_data):
        """添加新的映射"""
        try:
            with self.lock:
                # 验证端口可用性
                if not self._is_port_available(mapping_data.get('port', 0)):
                    log_error(f"端口 {mapping_data.get('port')} 不可用")
                    return False

                # 保存映射配置
                mappings = load_mappings()
                mappings.append(mapping_data)
                save_mappings(mappings)

                log_info(f"添加映射成功: {mapping_data['name']}")
                return True
        except Exception as e:
            log_error(f"添加映射失败: {str(e)}")
            return False

    def remove_mapping(self, name):
        """删除映射"""
        try:
            with self.lock:
                # 停止映射
                self.stop_mapping(name)

                # 从配置文件中删除
                mappings = load_mappings()
                mappings = [m for m in mappings if m['name'] != name]
                save_mappings(mappings)

                log_info(f"删除映射成功: {name}")
                return True
        except Exception as e:
            log_error(f"删除映射失败: {str(e)}")
            return False

    def update_mapping(self, name, new_data):
        """更新映射配置"""
        try:
            with self.lock:
                mappings = load_mappings()
                for mapping in mappings:
                    if mapping['name'] == name:
                        # 如果正在运行，需要先停止
                        was_running = mapping.get('status') == 'running'
                        if was_running:
                            self.stop_mapping(name)

                        # 更新配置
                        mapping.update(new_data)
                        save_mappings(mappings)

                        # 如果之前在运行，重新启动
                        if was_running:
                            self.start_mapping(name)

                        log_info(f"更新映射成功: {name}")
                        return True
                return False
        except Exception as e:
            log_error(f"更新映射失败: {str(e)}")
            return False

    def start_mapping(self, name):
        """启动端口映射"""
        try:
            with self.lock:
                mapping = self._get_mapping_config(name)
                if not mapping:
                    return False

                # 解析地址
                host, port = resolve_address(mapping['address'])
                if not host:
                    return False

                # 启动映射进程
                process = self._create_mapping_process(host, port, mapping['port'])
                if not process:
                    return False

                self.processes[name] = process
                mapping['status'] = 'running'
                save_mappings(load_mappings())  # 保存状态

                log_info(f"启动映射成功: {name}")
                return True
        except Exception as e:
            log_error(f"启动映射失败: {str(e)}")
            return False

    def stop_mapping(self, name):
        """停止端口映射"""
        try:
            with self.lock:
                if name in self.processes:
                    process = self.processes[name]
                    process.terminate()
                    del self.processes[name]

                    # 更新状态
                    mappings = load_mappings()
                    for mapping in mappings:
                        if mapping['name'] == name:
                            mapping['status'] = 'stopped'
                            break
                    save_mappings(mappings)

                    log_info(f"停止映射成功: {name}")
                return True
        except Exception as e:
            log_error(f"停止映射失败: {str(e)}")
            return False

    def toggle_mapping(self, name):
        """切换映射状态"""
        try:
            mapping = self._get_mapping_config(name)
            if not mapping:
                return False

            if mapping.get('status') == 'running':
                return self.stop_mapping(name)
            else:
                return self.start_mapping(name)
        except Exception as e:
            log_error(f"切换映射状态失败: {str(e)}")
            return False

    def get_mapping_status(self, name):
        """获取映射状态"""
        try:
            mapping = self._get_mapping_config(name)
            if not mapping:
                return None

            # 获取服务器状态
            server_status = analyze_server(mapping['address'])
            
            # 获取进程状态
            process_status = 'running' if name in self.processes else 'stopped'

            return {
                'name': name,
                'status': process_status,
                'server': server_status,
                'port': mapping.get('port')
            }
        except Exception as e:
            log_error(f"获取映射状态失败: {str(e)}")
            return None

    def _get_mapping_config(self, name):
        """获取映射配置"""
        mappings = load_mappings()
        for mapping in mappings:
            if mapping['name'] == name:
                return mapping
        return None

    def _is_port_available(self, port):
        """检查端口是否可用"""
        if port <= 0:
            return False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', port))
            sock.close()
            return True
        except:
            return False

    def _create_mapping_process(self, src_host, src_port, dst_port):
        """创建端口映射进程"""
        try:
            # 这里使用你之前的端口映射实现
            # 可能需要根据不同系统使用不同的命令
            # 例如: netsh, socat, iptables等
            # 返回进程对象
            pass
        except Exception as e:
            log_error(f"创建映射进程失败: {str(e)}")
            return None

if __name__ == '__main__':
    # 测试代码
    manager = PortManager()
    
    # 测试添加映射
    test_mapping = {
        'name': 'test',
        'address': 'localhost:25565',
        'port': 25566
    }
    
    manager.add_mapping(test_mapping)
    manager.start_mapping('test')
    print(manager.get_mapping_status('test'))
    time.sleep(5)
    manager.stop_mapping('test')
