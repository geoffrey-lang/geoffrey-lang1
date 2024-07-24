import requests
import re
from github import Github
import os

def get_fastest_ip():
    try:
        response = requests.get('https://tonkiang.us', timeout=10)
        ip_match = re.search(r'北京电信最快IP: (\d+\.\d+\.\d+\.\d+)', response.text)
        if ip_match:
            ip = ip_match.group(1)
            print(f"获取到的IP: {ip}")  # 调试信息
            return ip
    except Exception as e:
        print(f"获取IP时出错: {e}")
    return None

def update_zubo_file(ip):
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("未找到GITHUB_TOKEN环境变量")
        return

    g = Github(token)
    try:
        repo = g.get_repo("geoffrey-lang/geoffrey-lang1")
        file = repo.get_contents("zubo.txt")
        content = file.decoded_content.decode()
        
        print(f"当前文件内容: {content}")  # 调试信息
        
        # 更新IP，保留原端口号
        new_content = re.sub(r'(\d+\.\d+\.\d+\.\d+):\d+', f'{ip}:\\2', content)
        
        print(f"更新后的文件内容: {new_content}")  # 调试信息
        
        repo.update_file(file.path, f"更新IP到{ip}", new_content, file.sha)
        print(f"成功更新IP到: {ip}")
    except Exception as e:
        print(f"更新文件时出错: {e}")

if __name__ == "__main__":
    ip = get_fastest_ip()
    if ip:
        update_zubo_file(ip)
    else:
        print("未能获取有效IP")
