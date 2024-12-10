import os
import cloudscraper

B3 = os.getenv('B3')

scraper = cloudscraper.create_scraper()

headers = {
    "Accept-Language": "zh-CN,zh;q=0.8",
    "User-Agent": "okhttp/3.15",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}

try:
    response = scraper.get(B3, headers=headers, allow_redirects=False)

    if response.status_code == 302:
        print(f"Found redirect: {response.headers['Location']}")
    else:
        print("No redirect found. Status code:", response.status_code)
        print("Response headers:", response.headers)

except Exception as e:
    print(f"Error during request: {e}")
