import requests
import re
from github import Github
import os

# 配置
GITHUB_TOKEN = os.getenv('MY_GITHUB_TOKEN')
REPO_NAME = 'geoffrey-lang/geoffrey-lang1'  # 替换为你的GitHub用户名和存储库名
FILE_PATH = 'zubo.txt'
URL = "http://tonkiang.us/path_to_multicast_ip_list"  # 替换为实际的URL

def get_multicast_ips(url):
    response = requests.get(url)
    # 解析返回内容以提取IP地址
    ip_info_list = re.findall(r'(\d+\.\d+\.\d+\.\d+)\s+(.*?)\s+', response.text)
    return ip_info_list

def update_github_file(repo_name, file_path, content, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    file = repo.get_contents(file_path)
    repo.update_file(file.path, "Update IP addresses", content, file.sha)

if __name__ == "__main__":
    ip_info_list = get_multicast_ips(URL)
    # 假设所有IP都被保留或者经过筛选
    content = "\n".join([f"{ip} {info}" for ip, info in ip_info_list])
    update_github_file(REPO_NAME, FILE_PATH, content, MY_GITHUB_TOKEN)
