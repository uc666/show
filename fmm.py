import json
import requests

url = "http://api.vipmisss.com:81/xcdsw/jsonhuahudie.txt"  
response = requests.get(url)

if response.status_code == 200:
    data = response.text
    if data.strip():
        try:
            # 获取 'zhubo' 键下的内容
            streams = json.loads(data).get('zhubo', [])
        except json.JSONDecodeError as e:
            print(f"JSON 解码失败: {e}")
            streams = []
    else:
        print("返回的数据为空。")
else:
    print(f"无法获取数据，状态码: {response.status_code}")

# 获取链接的文本内容
m3u_url = "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u"
m3u_response = requests.get(m3u_url)
m3u_content = m3u_response.text

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
        # 获取 group-title 的值
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

    # 将新频道添加到 ‘央视频道’ 中
    output_dict["央视频道"].extend(new_channels)

with open("zb3.txt", "r", encoding="utf-8") as file:
    existing_lines = file.readlines()

with open("zb3.txt", "w", encoding="utf-8") as file:
    found_header = False
    for line in existing_lines:
        if "内部测试_889966,#genre#" in line:
            found_header = True
            file.write(line)  # 保留标题行
            break
        file.write(line)  # 保留之前的所有行

    if found_header:
        # 写入替换后的内容
        for group_name, links in output_dict.items():
            file.write(f"{group_name},#genre#\n")
            for link in links:
                file.write(f"{link}\n")
        print("替换完成，已更新")
    else:
        file.write("内部测试_889966,#genre#\n")
        for group_name, links in output_dict.items():
            file.write(f"{group_name},#genre#\n")
            for link in links:
                file.write(f"{link}\n")
        print("未找到，已自动添加该行及内容。")
