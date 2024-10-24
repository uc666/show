import json
import requests

# 从指定网址获取数据
url = "https://l.gmbbk.com/upload/37933793.txt"
response = requests.get(url)

# 确保请求成功
if response.status_code == 200:
    data = response.text
    streams = json.loads(data)['zhubo']

    # 打开 zb3.txt 文件，先清空文件并写入新的头部
    with open('zb3.txt', 'w', encoding='utf-8') as f:
        f.write("内部测试_889966,#genre#\n")  # 写入新的头部
        for stream in streams:
            # 正确解码 Unicode 字符
            title = stream['title'].encode('utf-8').decode('unicode_escape')
            address = stream['address']
            f.write(f"{title},{address}\n")  # 按格式写入每一行

    print("转换完成，已更新 'zb3'")
else:
    print("无法获取数据，状态码:", response.status_code)
