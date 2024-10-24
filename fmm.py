import json
import requests

json_url = "http://api.vipmisss.com:81/xcdsw/jsonhuahudie.txt"  
response = requests.get(json_url)
streams = []

if response.status_code == 200:
    data = response.text
    if data.strip():
        try:
            streams = json.loads(data).get('zhubo', [])
        except json.JSONDecodeError as e:
            print(f"JSON 解码失败: {e}")
else:
    print(f"无法获取 JSON 数据，状态码: {response.status_code}")

# 处理 M3U 链接
m3u_url = "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u"
response = requests.get(m3u_url)
m3u_content = response.text

# 移除 M3U 的第一行
m3u_content = m3u_content.split('\n', 1)[1]

# 初始化变量
group_name = ""
channel_name = ""
channel_link = ""
output_dict = {}

# 处理 M3U 数据
for line in m3u_content.split('\n'):
    if line.startswith("#EXTINF"):
        group_name = line.split('group-title="')[1].split('"')[0]
        channel_name = line.split(',')[-1]
    elif line.startswith("http"):
        channel_link = line
        combined_link = f"{channel_name},{channel_link}"
        if group_name not in output_dict:
            output_dict[group_name] = []
        output_dict[group_name].append(combined_link)

# 在 '央视频道' 下添加新频道
if "央视频道" in output_dict:
    new_channels = [
        "纬来体育,https://hls.yjjcfw.com/live/vl.m3u8?hwSecret=8b6d7dbcec85c678564613c8e13763e54b28361ef3560dd3c872267ef4237c64&hwTime=67286CF8",
        "纬来体育,https://v4-5d0c7b68cc16e296da25095c872bee1f.livehwc3.cn/hls.yjjcfw.com/live/vl.m3u8?hwTime=67286CF8&user_session_id=2a84eb39379ec398b4010984d656193f&hwSecret=8b6d7dbcec85c678564613c8e13763e54b28361ef3560dd3c872267ef4237c64&edge_slice=true&sub_m3u8=true",
        "纬来体育,http://hls.szsummer.cn/live/446035/playlist.m3u8?k=32f9ec7c13e4b390289143a8e1b2a898&t=1840341130",
        "纬来体育,http://cloud.yumixiu768.com/tmp/123.m3u8",
        "东森超视,rtmp://f13h.mine.nu/sat/tv331",
        "非凡新闻,rtmp://f13h.mine.nu/sat/tv581",
        "华视,rtmp://f13h.mine.nu/sat/tv111",
        "民视,rtmp://f13h.mine.nu/sat/tv051",
        "台视,rtmp://f13h.mine.nu/sat/tv071",
        "中视,rtmp://f13h.mine.nu/sat/tv091",
        "纬来育乐,rtmp://f13h.mine.nu/sat/tv701",
        "纬来体育,rtmp://f13h.mine.nu/sat/tv721",
        "纬来日本,rtmp://f13h.mine.nu/sat/tv771"
    ]
    output_dict["央视频道"].extend(new_channels)

# 将 JSON 和 M3U 数据写入 zb3.txt 文件
with open('zb3.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

found_header = False
with open('zb3.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line)
        if "熊猫看看_j693k,#genre#" in line:
            found_header = True
            break

    if found_header:
        for stream in streams:
            title = stream['title']
            address = stream['address']
            f.write(f"{title},{address}\n")
        print("已更新。")
    else:
        f.write("熊猫看看_j693k,#genre#\n")
        for stream in streams:
            title = stream['title']
            address = stream['address']
            f.write(f"{title},{address}\n")
        print("未找到，已添加新行。")

    # 处理 M3U 数据的写入
    for group_name, links in output_dict.items():
        f.write(f"{group_name},#genre#\n")
        for link in links:
            f.write(f"{link}\n")
