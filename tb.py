import requests
import time
from proxymanager import ProxyManager
import json

print("### TASKBOT RESTOCK MONITOR (v1.01) ###")
print("### BY @hasterestocks ###")
print('\n')

proxy_manager = ProxyManager('proxies.txt')
s = requests.session()

webhook = input("What is your webhook URL?\n")

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

while True:
    while True:
        try:
            proxydict = proxy_manager.next_proxy()
            proxies = proxydict.get_dict()

            try:
                response = requests.get("https://aiomacbot.myshopify.com/products.json", headers=headers, timeout=5, proxies=proxies)
                data = json.loads(response.text)
                stock = data['products'][0]['variants'][0]['available']
                variant = data['products'][0]['variants'][0]['id']
                atclink = 'https://aiomacbot.myshopify.com/cart/{}:1'.format(variant)
            except Exception as e:
                print(e)
                break

            if stock == True:
                print('Stock found!')
                print('Posting to discord...')
                data = {
                    "embeds": [{
                        "description": "Taskbot for macOS is back in stock!",
                        "url": atclink,
                        "description": 'Taskbot for macOS is back in stock!',
                        "author": {
                            "name": "TaskBot for macOS",
                            "url": atclink,
                            "icon_url": "https://cdn.shopify.com/s/files/1/1727/9043/products/icon_small.png?5554020967549010030"
                            },
                        "thumbnail": {
                            "url": 'https://aiomacbot.com/icon.png',
                            },
                            "color": "6397951",
                            "footer": {
                            "icon_url": "https://pbs.twimg.com/profile_images/956753895417499648/XeA2zLgk_400x400.jpg",
                            "text": ('Powered by hasterestocks | ' + str(time.ctime()))
                            }
                            }]
                            }
                res = s.post(webhook, json=data)
                print("Posted! Waiting...")
                time.sleep(1)

            elif stock == False:
                print("Taskbot - OOS! Checked with proxy: " + str(proxies))

        except Exception as e:
            print(str(e) + str(proxies))
            time.sleep(20)
            break
