from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

# 导入核心模块
from port import PortManager
from logger import setup_logger
from mappings import load_mappings, save_mappings, update_mapping, validate_mapping

app = Flask(__name__)
CORS(app)

# 设置日志
logger = setup_logger()

# 初始化端口管理器
port_manager = PortManager()

@app.route('/api/mappings', methods=['GET', 'POST'])
def handle_mappings():
    if request.method == 'GET':
        try:
            mappings = load_mappings()
            # 获取每个映射的当前状态
            for mapping in mappings:
                status = port_manager.get_mapping_status(mapping['name'])
                mapping.update(status)
            return jsonify(mappings)
        except Exception as e:
            logger.error(f"获取映射列表失败: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        try:
            data = request.json
            # 验证数据
            valid, error = validate_mapping(data)
            if not valid:
                return jsonify({'error': error}), 400
            
            # 添加映射
            success = port_manager.add_mapping(data)
            if not success:
                return jsonify({'error': '添加映射失败'}), 500
            
            return jsonify({'message': '添加成功'})
        except Exception as e:
            logger.error(f"添加映射失败: {e}")
            return jsonify({'error': str(e)}), 500

@app.route('/api/mappings/<name>', methods=['PUT', 'DELETE'])
def handle_mapping(name):
    try:
        if request.method == 'DELETE':
            success = port_manager.remove_mapping(name)
            if not success:
                return jsonify({'error': '删除失败'}), 500
            return jsonify({'message': '删除成功'})
        else:
            data = request.json
            success = port_manager.update_mapping(name, data)
            if not success:
                return jsonify({'error': '更新失败'}), 500
            return jsonify({'message': '更新成功'})
    except Exception as e:
        logger.error(f"操作失败: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mappings/<name>/toggle', methods=['POST'])
def toggle_mapping(name):
    try:
        success = port_manager.toggle_mapping(name)
        if not success:
            return jsonify({'error': '切换状态失败'}), 500
        return jsonify({'message': '状态已更新'})
    except Exception as e:
        logger.error(f"切换映射状态失败: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<name>', methods=['GET'])
def get_mapping_status(name):
    try:
        status = port_manager.get_mapping_status(name)
        if not status:
            return jsonify({'error': '获取状态失败'}), 404
        return jsonify(status)
    except Exception as e:
        logger.error(f"获取映射状态失败: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 启动时加载所有活动的映射
    try:
        mappings = load_mappings()
        for mapping in mappings:
            if mapping.get('status') == 'running':
                port_manager.start_mapping(mapping['name'])
        logger.info("已加载所有活动映射")
    except Exception as e:
        logger.error(f"加载映射失败: {e}")
    
    app.run(host='127.0.0.1', port=14011) 