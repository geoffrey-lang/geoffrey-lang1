import requests
from bs4 import BeautifulSoup
from github import Github
import os

MY_GITHUB_TOKEN = os.getenv('MY_GITHUB_TOKEN')
REPO_NAME = 'geoffrey-lang/geoffrey-lang1'
FILE_PATH = 'IP'

def get_multicast_ips():
    url = 'https://tonkiang.us'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    regions = {
        '北京联通': 'beijing-unicom',
        '上海电信': 'shanghai-telecom',
        '广东电信': 'guangdong-telecom',
        '四川电信': 'sichuan-telecom',
        '天津联通': 'tianjin-unicom'
    }
    multicast_ips = {}

    for region, class_name in regions.items():
        ip_elements = soup.find_all('div', class_=class_name)
        if ip_elements:
            top_ips = [ip.text.strip() for ip in ip_elements[:3]]
            multicast_ips[region] = top_ips
    
    return multicast_ips

def update_github(multicast_ips):
    g = Github(MY_GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    try:
        contents = repo.get_contents(FILE_PATH)
        new_content = "\n".join([f"{region}: {', '.join(ips)}" for region, ips in multicast_ips.items()])
        repo.update_file(contents.path, "Update multicast IP addresses", new_content, contents.sha)
    except Exception as e:
        print(f"An error occurred: {e}")

multicast_ips = get_multicast_ips()
update_github(multicast_ips)
