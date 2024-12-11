import requests
import json
import os
import re

# 环境变量配置
FMM = os.getenv("FMM")
response = requests.get(FMM)
m3u_content = response.text

# 移除第一行
m3u_content = m3u_content.split('\n', 1)[1]

# 初始化变量
group_name = ""
channel_name = ""
channel_link = ""
output_dict = {}

# 处理每两行为一组的情况
for line in m3u_content.split('\n'):
    if line.startswith("#EXTINF"):
        # 获取group-title的值
        group_name = line.split('group-title="')[1].split('"')[0]

        # 获取频道名
        channel_name = line.split(',')[-1]
    elif line.startswith("http"):
        # 获取频道链接
        channel_link = line
        # 合并频道名和频道链接
        combined_link = f"{channel_name},{channel_link}"

        # 将组名作为键，合并链接作为值存储在字典中
        if group_name not in output_dict:
            output_dict[group_name] = []
        output_dict[group_name].append(combined_link)

# 在央视频道组下添加新的频道
if "央视频道" in output_dict:
    new_channels = [
        "精品体育,http://ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221225674/index.m3u8"
    ]

    # 将新频道添加到 ‘央视频道’ 中
    output_dict["央视频道"].extend(new_channels)

exclude_keywords = ["oss", "mp4", "livi", "inke", "\u5077\u7aa5", "\u65e5\u672c", "\u5b9e\u529b", "\u5e26\u98de", "\u5408\u96c6"]

exclude_pattern = re.compile(r'|'.join(map(re.escape, exclude_keywords)), re.IGNORECASE)

JK = os.getenv("JK", "false").lower() == "true"

if JK:
    JSON_URL = os.getenv("JSON_URL")
    response = requests.get(JSON_URL)

    if response.status_code == 200:
        data = response.text
        if data.strip():
            try:
                streams = json.loads(data).get('zhubo', [])
            except json.JSONDecodeError as e:
                print(f"JSON 解码失败: {e}")
                streams = []

            output_dict["都市频道_j693k"] = []

            for stream in streams:
                title = stream['title']
                address = stream['address']
                if exclude_pattern.search(address) or exclude_pattern.search(title):
                    continue
                output_dict["都市频道_j693k"].append(f"{title},{address}")
        else:
            print("返回的数据为空。")
    else:
        print(f"无法获取数据，状态码: {response.status_code}")

with open("zb3.txt", "w", encoding="utf-8") as output_file:
    for idx, (group_name, links) in enumerate(output_dict.items()):
        if idx > 0:
            output_file.write("\n")
        output_file.write(f"{group_name},#genre#\n")
        for link in links:
            output_file.write(f"{link}\n")

print("任务完成")
