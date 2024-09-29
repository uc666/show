import re
import base64
import requests
import json

headers = {'User-Agent': 'okhttp/3.15'}

url = 'http://www.饭太硬.com/tv/'
try:
    response = requests.get(url, headers=headers)
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
        data["parses"] =[
    {"name":"解析聚合","type":3,"url":"Demo"},{"name":"Web聚合","type":3,"url":"Web"},{"name":"Json轮询","type":2,"url":"Sequence"},{"name":"Json并发","type":2,"url":"Parallel"},{"name":"解析1","type":1,"url":"http://pan.qiaoji8.com/tvbox/neibu.php?url=","ext":{"flag":["qq","腾讯","qiyi","爱奇艺","奇艺","youku","优酷","tucheng","sohu","搜狐","letv","乐视","mgtv","芒果","tnmb","seven","yzm","aliyun","RJuMao","bilibili","1905","xinvip","XAL","qiqi","XALS","YuMi-vip"]}},{"name":"解析2","url":"https://jx.xmflv.com/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"解析3","url":"https://jx.xmflv.cc/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"90","url":"https://www.8090g.cn/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"7K","url":"https://jx.7kjx.com/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"盘古","url":"https://www.pangujiexi.com/jiexi/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"逍遥","url":"https://jx.m3u8.pw/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"80","url":"https://www.8090.la/8090/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"CK","url":"https://www.ckplayer.vip/jiexi/?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"play","url":"https://www.playm3u8.cn/jiexi.php?url=","type":0,"ext":{"flag":["qiyi","imgo","爱奇艺","奇艺","qq","qq 预告及花絮","腾讯","youku","优酷","pptv","PPTV","letv","乐视","leshi","mgtv","芒果","sohu","xigua","fun","风行"]},"header":{"User-Agent":"Mozilla/5.0"}},{"name":"嗅探1","type":0,"url":"https://jx.m3u8.tv/jiexi/?url=","ext":{"flag":["qq","腾讯","qiyi","iqiyi","爱奇艺","奇艺","youku","yk","优酷","mgtv","imgo","芒果"]}},{"name":"嗅探2","type":0,"url":"https://www.yemu.xyz/?url="}
  ]
        data["logo"] = "./jar/logo.gif"
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
      "jar": "./jar/custom_spider.jar;md5;705ba6e23c4384c37a11dd904727520b",
      "ext": "./json/农民影视.json"
    }
            new_site2 = {
      "key": "freeok",
      "name": "🦁freeOK┃独家",
      "type": 3,
      "changeable": 1,
      "click": 'document.querySelector("#playleft iframe").contentWindow.document.querySelector("#start").click();',
      "api": "csp_FreeOK",
      "jar": "./jar/08015.jar;md5;d797a2aea119c4c5e217172e274d72f6"
    }
            new_site3 = {
      "key": "csp_SP360",
      "name": "🐠360┃1080P",
      "type": 3,
      "changeable": 0,
      "api": "csp_SP360",
      "jar": "./jar/08015.jar;md5;d797a2aea119c4c5e217172e274d72f6"
    }
            new_site4 = {
      "key": "追剧影视",
      "name": "🏅追剧┃不卡",
      "type": 3,
      "api": "csp_AppZJ",
      "searchable":1,
      "quickSearch":1,
      "changeable":1,
      "jar": "./jar/0914.jar;md5;7de46c7534b68d446aa91e6ecfb267cd",
      "ext": "http://z.kzjtv.com/"
    }
            new_site5 = {
      "key": "csp_瓜子",
      "name": "🌰瓜子┃1080P",
      "type": 3,
      "api": "csp_Gz360",
      "searchable":1,
      "playerType":2,
      "timeout":30,
      "changeable":0,
      "jar": "./jar/08015.jar;md5;d797a2aea119c4c5e217172e274d72f6"
    }
            new_site6 = {
      "key": "hipy_js_腾云驾雾[官]",
      "name": "🌞腾腾┃解析",
      "type": 3,
      "api": "http://我不是.摸鱼儿.top/json/js/drpy.min.js",
      "searchable":1,
      "quickSearch":1,
      "filterable":1,
      "order_num":0,
      "changeable":0,
      "jar": "./jar/08015.jar;md5;d797a2aea119c4c5e217172e274d72f6",
      "ext": "http://www.mpanso.com/%E5%B0%8F%E7%B1%B3/tx.js"
    }
            data["sites"].insert(0, new_site)
            data["sites"].insert(3, new_site2)
            data["sites"].insert(4, new_site3)
            data["sites"].insert(5, new_site4)
            data["sites"].insert(6, new_site5)
            data["sites"].insert(7, new_site6)
                        
        else:
            print('"sites" 键不在数据中')

        keys_to_remove = ["玩偶", "YGP", "米搜", "抠搜","Sso","夸搜","YiSo","PanSearch","新6V","贱贱"]
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
