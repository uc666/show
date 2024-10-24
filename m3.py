import json
import requests

# 从指定网址获取数据
url = "http://api.vipmisss.com:81/xcdsw/jsonhuahudie.txt"
response = requests.get(url)

# 确保请求成功
if response.status_code == 200:
    data = response.text
    streams = json.loads(data)['zhubo']

    # 打开 zb3.txt 文件以追加内容（a 模式）
    with open('zb3.txt', 'a', encoding='utf-8') as f:
        for stream in streams:
            title = stream['title'].encode('utf-8').decode('unicode_escape')  # 解码 Unicode
            address = stream['address']
            f.write(f"{title},{address}\n")  # 按格式写入每一行

    print("转换完成，已追加到 'zb3.txt'")
else:
    print("无法获取数据，状态码:", response.status_code)
