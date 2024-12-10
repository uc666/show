import os
import requests
import re
from datetime import datetime
import subprocess
import sys
import pytz

try:
    import pytz
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytz"])
    import pytz

headers = {'User-Agent': 'okhttp/3.15'}

url1 = os.getenv("URL_1")
url2 = os.getenv("URL_2")
url3 = os.getenv("URL_3")

beijing_tz = pytz.timezone('Asia/Shanghai')
current_beijing_time = datetime.now(beijing_tz)

current_date_str = current_beijing_time.strftime("%Y-%m-%d")

processed_contents = [None] * 3

urls = [url1, url2, url3]

url3_playlist = ""
if url3:
    try:
        response = requests.get(url3, headers=headers)
        response.raise_for_status()
        url3_playlist = response.text
        response.encoding = 'utf-8'
        print(f"从 {url3} 获取到的内容长度: {len(url3_playlist)}")

        pattern = re.compile(
            r'(🐼电视公告[\s\S]*?(?=(VIP|🔥|🐼|$)))|'
            r'(<script[\s\S]*?</script>)',
            flags=re.IGNORECASE
        )

        updated_playlist = re.sub(pattern, '', url3_playlist)

        updated_playlist = re.sub(r'\n{2,}', '\n\n', updated_playlist).strip()

        updated_playlist = re.sub(r"更新\d{4}-\d{2}-\d{2},", f"更新{current_date_str},", updated_playlist)

        if not updated_playlist.endswith('\n'):
            updated_playlist += '\n'

        url3_playlist = updated_playlist
        print(f"URL3 内容已成功处理")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {url3} - {e}")
        url3_playlist = ""

for index, url in enumerate(urls[:2]):
    try:
        if url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            playlist = response.text

            response.encoding = 'utf-8'
            playlist = response.text

            print(f"从 {url} 获取到的内容长度: {len(playlist)}")

            if url == url1:
                playlist = re.sub(r'🐼电视公告[\s\S]*?(?=(VIP|🔥|🐼|$))', '', playlist)
                
                playlist = re.sub(r'<script[\s\S]*?</script>', '', playlist)

            if url3_playlist:
                url3_playlist = re.sub(r'^AKTV,#genre#\n?', '', url3_playlist)
                pattern = r'(🔥AKTV恢复,#genre#)[\s\S]*?(?=(VIP|🔥|🐼|$))'
                playlist = re.sub(pattern, r'\1\n' + url3_playlist + '\n', playlist)

            if url == url2:
                playlist = re.sub(r"更新\d{4}-\d{2}-\d{2},", f"更新{current_date_str},", playlist)

            playlist = re.sub(r'\n{2,}', '\n\n', playlist).strip()

            if not playlist.endswith('\n'):
                playlist += '\n'

            processed_contents[index] = playlist

            print(f"内容已成功从 {url} 获取并处理")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {url} - {e}")
        processed_contents[index] = ""

write_order = [1, 0]

with open("zo.txt", "w", encoding='utf-8') as file:
    for idx in write_order:
        if idx < len(processed_contents) and processed_contents[idx]:
            file.write(processed_contents[idx])
            file.write("\n")

print("已处理")
