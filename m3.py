import json
import requests
import datetime
import pytz
import os
import re

def get_beijing_time():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = datetime.datetime.now(beijing_tz)
    return beijing_time

JSON_URL = os.getenv("JSON_URL")
response = requests.get(JSON_URL)

exclude_keywords = ["oss", "mp4", "livi", "inke", "\u5077\u7aa5", "\u65e5\u672c", "\u5b9e\u529b", "\u5e26\u98de", "\u5408\u96c6"]

exclude_pattern = re.compile(r'|'.join(map(re.escape, exclude_keywords)), re.IGNORECASE)

def is_excluded(title, address):
    if exclude_pattern.search(title) or exclude_pattern.search(address):
        return True
    return False

if response.status_code == 200:
    data = response.text.strip()
    if data:
        try:
            streams = json.loads(data).get('zhubo', [])
        except json.JSONDecodeError as e:
            print(f"JSON 解码失败: {e}")
            streams = []

        with open('zb3.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open('zb3.txt', 'w', encoding='utf-8') as f:
            beijing_time = get_beijing_time()
            found_header = False
            updated = False

            if 3 <= beijing_time.hour < 5:
                for line in lines:
                    if "都市频道_j693k,#genre#" in line:
                        found_header = True
                        f.write(line)
                        for stream in streams:
                            title = stream.get('title', '未知频道')
                            address = stream.get('address', '无地址')
                            if not is_excluded(title, address):
                                f.write(f"{title},{address}\n")
                        print("替换完成，已更新。")
                        updated = True
                        break
                    else:
                        f.write(line)

                if not found_header:
                    f.write("\n都市频道_j693k,#genre#\n")
                    for stream in streams:
                        title = stream.get('title', '未知频道')
                        address = stream.get('address', '无地址')

                        if not is_excluded(title, address):
                            f.write(f"{title},{address}\n")
                    print("已添加并更新。")
                    updated = True
            else:
                for line in lines:
                    if "都市频道_j693k,#genre#" in line:
                        found_header = True
                        continue
                    if not found_header:
                        f.write(line)
                print("不在目标时间段")
                updated = True

            if not updated:
                print("文件没有更新。")
    else:
        print("返回的数据为空。")
else:
    print(f"无法获取数据，状态码: {response.status_code}")
