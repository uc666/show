import requests
import re
from datetime import datetime
import subprocess
import sys
import os

# 检查并安装 pytz
try:
    import pytz
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytz"])
    import pytz

headers = {'User-Agent': 'okhttp/3.15'}

# 定义两个 URL
urls = [
    "http://8.138.7.223/8.php?all=1",
    "https://ghp.ci/https://raw.githubusercontent.com/uc666/show/main/zb2.txt"
]

# 获取当前的北京时间
beijing_tz = pytz.timezone('Asia/Shanghai')
current_beijing_time = datetime.now(beijing_tz)

# 格式化为“YYYY-MM-DD”
current_date_str = current_beijing_time.strftime("%Y-%m-%d")

# 存储处理后的内容
processed_contents = [None] * len(urls)  # 初始化列表以存储每个 URL 的内容

for index, url in enumerate(urls):
    try:
        if url:  # 检查 URL 是否为空
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            playlist = response.text

            # 检查获取到的内容长度
            print(f"从 {url} 获取到的内容长度: {len(playlist)}")

            # 定义正则表达式模式
            pattern = re.compile(
                r'(🐼电视公告[\s\S]*?(?=(🐼|$)))|'  # 匹配“🐼电视公告”及其后续内容，直到下一个“🐼”或文件结尾
                r'(<script[\s\S]*?</script>)',     # 匹配 <script> 标签及其内容
                flags=re.IGNORECASE
            )

            # 使用 re.sub 进行替换
            updated_playlist = re.sub(pattern, '', playlist)

            # 进一步清理可能的多余空行
            updated_playlist = re.sub(r'\n{2,}', '\n\n', updated_playlist).strip()

            # 确认删除段落后的内容长度
            print(f"处理后的内容长度: {len(updated_playlist)}")

            # 更新日期为当前北京时间
            updated_playlist = re.sub(r"更新\d{4}-\d{2}-\d{2},", f"更新{current_date_str},", updated_playlist)

            # 检查最后一行是否为空行
            if not updated_playlist.endswith('\n'):
                updated_playlist += '\n'

            # 将处理后的内容存储在对应的索引位置
            processed_contents[index] = updated_playlist

            print(f"内容已成功从 {url} 获取并处理")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {url} - {e}")
        processed_contents[index] = ""  # 遇到请求失败时，存储空字符串以避免写入 None

# 确定写入顺序：将第二个 URL 的内容放在开头，第一个 URL 的内容放在后面
write_order = [1, 0]  # 索引 1 对应第二个 URL，索引 0 对应第一个 URL

# 打开文件以写入模式
with open("zb1.txt", "w", encoding='utf-8') as file:
    for idx in write_order:
        if idx < len(processed_contents) and processed_contents[idx]:
            file.write(processed_contents[idx])
            file.write("\n")  # 可选：添加换行符以分隔不同 URL 的内容

print("所有内容已处理完毕并写入 zb1.txt 文件中")
