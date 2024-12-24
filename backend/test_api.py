import requests
import json
from colorama import init, Fore, Style

# 初始化colorama
init()

def print_response(name, response):
    """打印格式化的响应"""
    print(f"\n{Fore.CYAN}=== {name} ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}状态码:{Style.RESET_ALL} {response.status_code}")
    try:
        print(f"{Fore.GREEN}响应内容:{Style.RESET_ALL}")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except:
        print(f"{Fore.RED}响应内容不是JSON格式{Style.RESET_ALL}")
        print(response.text)

def test_api():
    base_url = 'http://127.0.0.1:14011'
    
    try:
        # 测试获取映射列表
        print(f"\n{Fore.YELLOW}测试获取映射列表{Style.RESET_ALL}")
        response = requests.get(f'{base_url}/api/mappings')
        print_response("GET /api/mappings", response)

        # 测试添加映射
        print(f"\n{Fore.YELLOW}测试添加映射{Style.RESET_ALL}")
        data = {
            'name': 'test_server',
            'address': 'localhost:25565'
        }
        response = requests.post(f'{base_url}/api/mappings', json=data)
        print_response("POST /api/mappings", response)

        # 测试获取特定映射状态
        print(f"\n{Fore.YELLOW}测试获取映射状态{Style.RESET_ALL}")
        response = requests.get(f'{base_url}/api/status/test_server')
        print_response("GET /api/status/test_server", response)

        # 测试切换映射状态
        print(f"\n{Fore.YELLOW}测试切换映射状态{Style.RESET_ALL}")
        response = requests.post(f'{base_url}/api/mappings/test_server/toggle')
        print_response("POST /api/mappings/test_server/toggle", response)

        # 测试分析服务器
        print(f"\n{Fore.YELLOW}测试服务器分析{Style.RESET_ALL}")
        response = requests.get(f'{base_url}/api/analyze/test_server')
        print_response("GET /api/analyze/test_server", response)

        # 测试获取日志
        print(f"\n{Fore.YELLOW}测试获取日志{Style.RESET_ALL}")
        response = requests.get(f'{base_url}/api/logs')
        print_response("GET /api/logs", response)

    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}错误: 无法连接到后端服务器 (http://127.0.0.1:14011){Style.RESET_ALL}")
        print("请确保后端服务器正在运行")
    except Exception as e:
        print(f"{Fore.RED}测试过程中出现错误:{Style.RESET_ALL}", str(e))

def cleanup():
    """清理测试数据"""
    try:
        base_url = 'http://127.0.0.1:14011'
        response = requests.delete(f'{base_url}/api/mappings/test_server')
        if response.status_code == 200:
            print(f"\n{Fore.GREEN}清理测试数据成功{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}清理测试数据失败: {response.json()}{Style.RESET_ALL}")
    except:
        print(f"\n{Fore.YELLOW}清理测试数据失败{Style.RESET_ALL}")

if __name__ == '__main__':
    try:
        print(f"{Fore.CYAN}开始API测试...{Style.RESET_ALL}")
        test_api()
    finally:
        print(f"\n{Fore.CYAN}测试完成,正在清理...{Style.RESET_ALL}")
        cleanup()
        input("\n按回车键退出...") 