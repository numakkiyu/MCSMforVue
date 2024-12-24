import os
import json
from logger import log_info, log_error

# 映射配置文件路径
MAPPINGS_FILE = 'data/mappings.json'

def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs('data', exist_ok=True)

def load_mappings():
    """
    加载映射配置
    返回: 映射列表
    """
    ensure_data_dir()
    try:
        if os.path.exists(MAPPINGS_FILE):
            with open(MAPPINGS_FILE, 'r', encoding='utf-8') as f:
                mappings = json.load(f)
                log_info(f"成功加载 {len(mappings)} 个映射配置")
                return mappings
        else:
            log_info("映射配置文件不存在，返回空列表")
            return []
    except Exception as e:
        log_error(f"加载映射配置失败: {str(e)}")
        return []

def save_mappings(mappings):
    """
    保存映射配置
    参数:
        mappings: 映射列表
    """
    ensure_data_dir()
    try:
        with open(MAPPINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, ensure_ascii=False, indent=2)
        log_info(f"成功保存 {len(mappings)} 个映射配置")
        return True
    except Exception as e:
        log_error(f"保存映射配置失败: {str(e)}")
        return False

def update_mapping(mapping, new_data):
    """
    更新映射配置
    参数:
        mapping: 现有映射配置
        new_data: 新的配置数据
    """
    try:
        # 更新基本信息
        mapping.update({
            'name': new_data.get('name', mapping['name']),
            'address': new_data.get('address', mapping['address']),
            'description': new_data.get('description', mapping.get('description', '')),
            'status': new_data.get('status', mapping.get('status', 'stopped'))
        })

        # 更新端口配置
        if 'port' in new_data:
            mapping['port'] = new_data['port']

        # 更新高级选项
        if 'options' in new_data:
            mapping['options'] = new_data['options']

        log_info(f"成功更新映射配置: {mapping['name']}")
        return True
    except Exception as e:
        log_error(f"更新映射配置失败: {str(e)}")
        return False

def find_mapping(mappings, name):
    """
    查找指定名称的映射
    参数:
        mappings: 映射列表
        name: 映射名称
    返回: (映射索引, 映射配置) 或 (-1, None)
    """
    for i, mapping in enumerate(mappings):
        if mapping['name'] == name:
            return i, mapping
    return -1, None

def validate_mapping(mapping):
    """
    验证映射配置是否有效
    参数:
        mapping: 映射配置
    返回: (是否有效, 错误信息)
    """
    required_fields = ['name', 'address']
    
    # 检查必填字段
    for field in required_fields:
        if field not in mapping:
            return False, f"缺少必填字段: {field}"
    
    # 检查名称格式
    if not mapping['name'].strip():
        return False, "名称不能为空"
    
    # 检查地址格式
    address = mapping['address']
    if ':' in address:
        host, port = address.split(':')
        try:
            port = int(port)
            if not (1 <= port <= 65535):
                return False, "端口号必须在1-65535之间"
        except ValueError:
            return False, "端口号必须是数字"
    
    return True, ""

if __name__ == '__main__':
    # 测试代码
    test_mapping = {
        'name': 'test_server',
        'address': 'localhost:25565',
        'description': '测试服务器',
        'status': 'stopped'
    }
    
    # 测试保存
    mappings = [test_mapping]
    save_mappings(mappings)
    
    # 测试加载
    loaded_mappings = load_mappings()
    print("加载的映射:", loaded_mappings)
    
    # 测试更新
    update_data = {
        'description': '更新后的描述',
        'port': 25566
    }
    if loaded_mappings:
        update_mapping(loaded_mappings[0], update_data)
        save_mappings(loaded_mappings) 