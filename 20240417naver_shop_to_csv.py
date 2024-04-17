#!usr/bin/env python
import urllib.request
import json
import pandas as pd
from operator import itemgetter

client_id =
client_secret =

product_name = input("Enter Product Name: ")
encText = urllib.parse.quote(product_name)

items = []
for start in range(1, 1000, 100):
    url = f"https://openapi.naver.com/v1/search/shop?query={encText}&display=100&start={start}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))

        for item in data['items']:
            try:
                item['lprice'] = int(item['lprice'])
                items.append(item)
            except ValueError:
                pass
    else:
        print("Error Code:", rescode)

sorted_items = sorted(items, key=itemgetter('lprice'))

df = pd.json_normalize(sorted_items)
df.to_csv('shop.csv', encoding='utf-8-sig')
filename = 'shop.csv'
print(filename + " saved!!!")