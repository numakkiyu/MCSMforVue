# logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name='mc_mapper'):
    """
    设置并返回一个配置好的logger实例
    """
    # 创建logs目录
    os.makedirs('logs', exist_ok=True)
    
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 防止重复添加handler
    if logger.handlers:
        return logger
    
    # 创建控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # 创建文件handler
    file_handler = RotatingFileHandler(
        'logs/mc_mapper.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # 添加handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# 创建一个默认logger实例
logger = setup_logger()

def log_info(message):
    """记录信息日志"""
    logger.info(message)

def log_error(message):
    """记录错误日志"""
    logger.error(message)

def log_warning(message):
    """记录警告日志"""
    logger.warning(message)

def log_debug(message):
    """记录调试日志"""
    logger.debug(message)

if __name__ == '__main__':
    # 测试日志功能
    log_info("这是一条信息日志")
    log_error("这是一条错误日志")
    log_warning("这是一条警告日志")
    log_debug("这是一条调试日志")
