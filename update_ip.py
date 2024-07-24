import requests
import re
from github import Github
import os

def get_fastest_ip():
    try:
        response = requests.get('https://tonkiang.us', timeout=10)
        ip_match = re.search(r'北京电信最快IP: (\d+\.\d+\.\d+\.\d+)', response.text)
        if ip_match:
            return ip_match.group(1)
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
        
        new_content = re.sub(r'(ipip=).*', f'\\1{ip}', content)
        new_content = re.sub(r'(\d+\.\d+\.\d+\.\d+)', ip, new_content, count=1)
        
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
