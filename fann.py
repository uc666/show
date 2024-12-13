import re
import base64
import requests
import json
import os

headers = {'User-Agent': 'okhttp/3.15'}

B1  = os.getenv("B1")

if B1 is None:
    raise ValueError(" 'B1' 没有设置")
    
try:
    response = requests.get(B1, headers=headers)
    response.raise_for_status()  # 抛出异常，处理错误的响应状态

    # 使用正则表达式查找匹配项
    match = re.search(r'[A-Za-z0]{8}\*\*(.*)', response.text)

    if not match:
        print("在响应文本中未找到匹配项。")
    else:
        result = match.group(1)
        content = base64.b64decode(result).decode('utf-8')

        # 调试输出解析后的内容
        print("解析后的内容：")
        print(content)

        # 排除注释内容
        content_lines = content.split('\n')
        cleaned_content = [line for line in content_lines if not line.strip().startswith("//")]

        # 合并处理后的内容
        cleaned_content_text = '\n'.join(cleaned_content)

        # 解析内容
        data = json.loads(cleaned_content_text)

        # 找到并替换特定字段值
        for site in data.get("sites", []):
            if site.get("key") == "豆豆":
                site["name"] = "📺电视吧"
            if site.get("key") == "fan":
                site["name"] = "📺看电视吧"

        # 修改内容
        data["wallpaper"] ="http://www.kf666888.cn/api/tvbox/img"
        data["warningText"] ="烟笼寒水月笼沙，夜泊秦淮近酒家。"
        data["logo"] = "./jar/logo.gif"
        data["lives"] = [
            {
                "name": "LIVE",
                "ua": "okhttp/3.15",
                "type": 0,
                "playerType": 1,
                "epg": "http://epg.51zmt.top:8000/api/diyp/?ch={name}&date={date}",
                "logo": "https://live.fanmingming.com/tv/{name}.png",
                "url": "./zo.txt"
            },
            {
                "name": "TV",
                "ua": "okhttp/3.15",
                "type": 0,
                "playerType": 1,
                "epg": "http://epg.51zmt.top:8000/api/diyp/?ch={name}&date={date}",
                "logo": "https://live.fanmingming.com/tv/{name}.png",
                "url": "./zb.txt"
            },
            {
                "name": "TVB",
                "type": 0,
                "url": "./zba.txt",
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
      "api": "csp_XYQHiker",
      "searchable":1,
      "quickSearch":1,
      "changeable":1,
      "jar": "./jar/custom_spider.jar;md5;4557db37965e20fb46cb59c3f603383c",
      "ext": "./json/nm.json"
    }
            new_site2 = {
      "key": "ikun",
      "name": "🦢爱坤┃1080P",
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
            data["sites"].insert(0, new_site)
            data["sites"].insert(3, new_site2)
                        
        else:
            print('"sites" 键不在数据中')

        keys_to_remove = ["玩偶","YGP","抠搜","UC","贱贱","新6V","PanSso","YpanSo","xzso","米搜","夸搜","Aliso","YiSo"]
        data["sites"] = [site for site in data["sites"] if site.get("key") not in keys_to_remove]
        
        # 将修改后的内容转换为 JSON 字符串，并指定 ensure_ascii=False 以确保汉字和表情符号正常显示
        modified_content = json.dumps(data, indent=2, ensure_ascii=False)

        # 将修改后的 JSON 字符串写入 b1.txt 文件中
        with open('b1.txt', 'w', newline='', encoding='utf-8') as f:
            f.write(modified_content)

        print("修改后的内容已写入到 b1.txt 文件中。")
except requests.RequestException as e:
    print("请求失败:", e)
except Exception as ex:
    print("发生错误:", ex)
