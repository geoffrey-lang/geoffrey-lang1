import requests
from collections import defaultdict

def get_top_3_ips():
    response = requests.get('https://tonkiang.us/api')
    data = response.json()

    regions = ['北京联通', '上海电信', '广东电信', '四川电信', '天津联通']
    top_3_ips = defaultdict(list)

    for region in regions:
        sorted_ips = sorted(data[region], key=lambda x: x['speed'], reverse=True)
        top_3_ips[region] = [ip['ip'] for ip in sorted_ips[:3]]

    return top_3_ips

def update_ip_file():
    top_3_ips = get_top_3_ips()
    new_content = '\n'.join([f"{region}: {', '.join(ips)}" for region, ips in top_3_ips.items()])

    with open('IP', 'w') as f:
        f.write(new_content)

if __name__ == "__main__":
    update_ip_file()
