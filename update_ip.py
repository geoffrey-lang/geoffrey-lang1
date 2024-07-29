import requests
from github import Github
import datetime

def get_fastest_ips():
    url = "https://tonkiang.us/api/v1/ips"
    response = requests.get(url)
    data = response.json()
    
    regions = ["北京联通", "上海电信", "广东电信", "四川电信", "天津联通"]
    fastest_ips = {}
    
    for region in regions:
        region_ips = [ip for ip in data if ip['isp'] == region]
        sorted_ips = sorted(region_ips, key=lambda x: x['speed'])[:3]
        fastest_ips[region] = [ip['ip'] for ip in sorted_ips]
    
    return fastest_ips

def update_github_file(content):
    token = "YOUR_GITHUB_TOKEN"
    g = Github(token)
    repo = g.get_repo("geoffrey-lang/geoffrey-lang1")
    file_path = "IP"
    
    try:
        file = repo.get_contents(file_path)
        repo.update_file(file_path, f"Update IP {datetime.datetime.now()}", content, file.sha)
    except:
        repo.create_file(file_path, f"Create IP file {datetime.datetime.now()}", content)

if __name__ == "__main__":
    fastest_ips = get_fastest_ips()
    content = "\n".join([f"{region}: {', '.join(ips)}" for region, ips in fastest_ips.items()])
    update_github_file(content)
