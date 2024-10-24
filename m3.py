import json
import requests

# 从指定网址获取数据
url = "http://api.vipmisss.com:81/xcdsw/jsonhuahudie.txt"
response = requests.get(url)

if response.status_code == 200:
    data = response.text
    if data.strip():
        try:
            streams = json.loads(data).get('zhubo', [])
        except json.JSONDecodeError as e:
            print(f"JSON 解码失败: {e}")
            streams = []

        # 读取现有文件内容
        with open('zb3.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 找到 "内部测试_889966,#genre#" 这一行
        with open('zb3.txt', 'w', encoding='utf-8') as f:
            found_header = False
            for line in lines:
                if "内部测试_889966,#genre#" in line:
                    found_header = True
                    f.write(line)  # 保留这一行标题
                    break
                f.write(line)  # 保留之前的所有行

            if found_header:
                # 只替换该行之后的内容
                for stream in streams:
                    title = stream['title']  # 使用 utf-8 处理字符
                    address = stream['address']
                    f.write(f"{title},{address}\n")
                print("替换完成，已更新 '内部测试_889966,#genre#' 之后的内容。")
            else:
                print("未找到 '内部测试_889966,#genre#' 行。")
    else:
        print("返回的数据为空。")
else:
    print(f"无法获取数据，状态码: {response.status_code}")
