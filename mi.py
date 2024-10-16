import os
import hashlib
import requests
import json
import re

url = 'http://www.mpanso.com/%E5%B0%8F%E7%B1%B3/DEMO.json'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

try:
    # 发送 GET 请求
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_text = response.text

    print("Response text:", response_text)
    
    match = re.search(r'[A-Za-z0-9]{8}\*\*(.*)', response_text)
    
    if not match:
        print("在响应文本中未找到匹配项。")
    else:
        result = match.group(1)
        print("正则匹配到的内容:", result)

    data = json.loads(response_text)

    # 找到并替换特定字段值
    for site in data.get("sites", []):
        if site.get("key") == "豆瓣":
            site["name"] = "📺电视吧"
        if site.get("key") == "push_agent":
            site["name"] = "请勿相信视频中广告"

    # 修改内容
    data["wallpaper"] = "http://www.kf666888.cn/api/tvbox/img"
    data["logo"] = "./jar/logo.gif"
    data["warningText"] = "否极泰来,好运连连。"

    # 处理 spider 字段
    spider_url = data.get("spider")
    if spider_url:
        jar_url = spider_url.split(';')[0]
        md5_remote = spider_url.split(';')[2]  # 获取 MD5 值

        # 本地 JAR 文件路径
        jar_filename = os.path.basename(jar_url)
        local_jar_path = os.path.join('./jar', jar_filename)

        # 创建 jar 目录（如果不存在）
        os.makedirs('./jar', exist_ok=True)

        # 计算本地 JAR 文件的 MD5 值
        def calculate_md5(file_path):
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()

        # 检查本地文件是否存在，并计算 MD5
        if os.path.exists(local_jar_path):
            md5_local = calculate_md5(local_jar_path)
        else:
            md5_local = None

        # 比较 MD5 值
        if md5_local != md5_remote:
            print("MD5 值不匹配，开始下载新的 JAR 文件...")
            response = requests.get(jar_url)
            response.raise_for_status()

            # 保存新 JAR 文件
            with open(local_jar_path, 'wb') as jar_file:
                jar_file.write(response.content)
            print(f"成功下载并更新 JAR 文件到: {local_jar_path}")
        else:
            print("MD5 值一致，跳过下载。")

        data["lives"] = [
        {
            "name": "LIVE",
            "ua": "okhttp/3.15",
            "type": 0,
            "playerType": 1,
            "epg": "http://epg.51zmt.top:8000/api/diyp/?ch={name}&date={date}",
            "logo": "https://live.fanmingming.com/tv/{name}.png",
            "url": "./zb1.txt"
        },
        {
            "name": "TV",
            "ua": "okhttp/3.15",
            "type": 0,
            "playerType": 1,
            "url": "./zb.txt"
        },
        {
            "name": "TVB",
            "type": 0,
            "url": "./zba.txt",
            "playerType": 1
        },
        {
            "name": "NOW",
            "type": 0,
            "url": "./zb3.txt",
            "playerType": 1
        },
        {
      "name": "BTV",
      "type": 0,
      "url": "https://l.gmbbk.com/upload/37933793.txt",
      "playerType": 1
        }
    ]

        # 添加新数据到 "sites" 的第二段
        if "sites" in data:
        # 如果 "sites" 是一个包含列表的列表，则将其转换为单一的列表
        if isinstance(data["sites"], list) and isinstance(data["sites"][0], list):
            data["sites"] = [item for sublist in data["sites"] for item in sublist]

        new_site = {
            "key": "农民影视",
            "name": "📺看电视吧",
            "type": 3,
            "api": "csp_WexNmys",
            "searchable": 1,
            "quickSearch": 1,
            "changeable": 1,
            "jar": "./jar/nmys.jar;md5;819aa9a38e837b51f65abd51817f7b77"
        }
        new_site2 = {
            "key": "追剧影视",
            "name": "🏅追剧┃1080P",
            "type": 3,
            "api": "csp_AppZJ",
            "searchable": 1,
            "quickSearch": 1,
            "changeable": 1,
            "jar": "./jar/0914.jar;md5;03c83adc48ceacbda2ab7fae8b1c6597",
            "ext": "http://z.kzjtv.com/"
        }
        new_site3 = {
            "key": "qwqfun",
            "name": "🍦qwqfun┃1080P",
            "type": 1,
            "api": "https://www.qwqfun.one/api.php/tvbox",
            "searchable": 1,
            "quickSearch": 1,
            "changeable": 1,
            "ext": "qwqfun"
        }
        new_site4 = {
            "key": "ikun",
            "name": "🐔爱坤┃1080P",
            "type": 1,
            "api": "https://ikzy7.com/api.php/provide/vod?",
            "searchable": 1,
            "changeable": 1,
            "categories": [
    "大陆综艺",
    "国产剧",
    "香港剧",
    "爽文短剧",
    "喜剧片",
    "国产动漫"
   ]
        }
        new_site5 = {
            "key": "天天弹幕",
            "name": "👻天天┃1080P",
            "type": 3,
            "api": "csp_TianTian",
            "searchable": 1,
            "quickSearch": 1,
            "changeable": 1,
            "jar": "./jar/wddanmu.jar;md5;c52fb9e051491089b007fea2b3109ee8",
            "ext": {"danmu": True}
        }
        new_site6 = {
            "key": "Wexwwe",
            "name": "WWE┃1080P",
            "type": 3,
            "api": "csp_Wexwwe",
            "searchable": 1,
            "changeable": 0,
            "jar": "./jar/wex.txt;md5;b446cb40c1aa36eaf5174e5fb3d2f5d9"
        }
        
        # 将 new_site 和 new_site2 插入到特定位置
        data["sites"].insert(0, new_site)
        data["sites"].insert(3, new_site2)
        data["sites"].insert(4, new_site3)
        data["sites"].insert(5, new_site4)
        data["sites"].insert(6, new_site5)
        data["sites"].insert(7, new_site6)

    else:
        print('"sites" 键不在数据中')

    # 删除指定的键
    keys_to_remove = ["csp_wanou", "csp_zhizhen", "米搜", "配置", "虎牙直播js", "荐片"]
    data["sites"] = [site for site in data["sites"] if site.get("key") not in keys_to_remove]

    # 将修改后的内容转换为 JSON 字符串，并写入 b2.txt 文件
    modified_content = json.dumps(data, indent=2, ensure_ascii=False)
    with open('b2.txt', 'w', newline='', encoding='utf-8') as f:
        f.write(modified_content)

    print("修改后的内容已写入到 b2.txt 文件中。")

except requests.RequestException as e:
    print(f"请求失败: {e}")

except json.JSONDecodeError as e:
    print(f"JSON 解析失败: {e}")

except Exception as e:
    print(f"发生错误: {e}")
