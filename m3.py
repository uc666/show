import json
import requests

# 从指定网址获取数据
url = "http://api.vipmisss.com:81/xcdsw/jsonhuahudie.txt"
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    data = response.text
    if data.strip():  # 确保数据不为空
        try:
            streams = json.loads(data).get('zhubo', [])  # 使用 .get() 避免 KeyError
        except json.JSONDecodeError as e:
            print(f"JSON 解码失败: {e}")
            streams = []

        if streams:
            # 打开 zb3.txt 文件并写入数据
            with open('zb3.txt', 'w', encoding='utf-8') as f:
                f.write("内部测试_889966,#genre#\n")
                for stream in streams:
                    title = stream['title'].encode('utf-8').decode('unicode_escape')
                    address = stream['address']
                    f.write(f"{title},{address}\n")
            print("转换完成，已更新 'zb3.txt'")
        else:
            print("没有找到 'zhubo' 数据，可能返回格式不正确。")
    else:
        print("返回的数据为空。")
else:
    print(f"无法获取数据，状态码: {response.status_code}")
