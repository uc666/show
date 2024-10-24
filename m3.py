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

        # 找到 "内部测试" 的行，保留之前的内容
        with open('zb3.txt', 'w', encoding='utf-8') as f:
            found_header = False
            for line in lines:
                if "内部测试" in line:
                    found_header = True
                    f.write(line)  # 保留 "内部测试" 行
                    break
                f.write(line)  # 保留之前的所有行

            if found_header:
                f.write("#genre#\n")  # 替换 header 后面的行
                for stream in streams:
                    title = bytes(stream['title'], 'latin1').decode('unicode_escape')
                    address = stream['address']
                    f.write(f"{title},{address}\n")
                print("转换完成，已替换 '内部测试' 之后的内容。")
            else:
                print("未找到 '内部测试' 行。")
    else:
        print("返回的数据为空。")
else:
    print(f"无法获取数据，状态码: {response.status_code}")
