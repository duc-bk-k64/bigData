import requests
import pandas as pd
import random
import time
import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

# Param list
# Thoi-trang-nam: 915
# Thoi-trang-nu: 931
# Giay-dep-nam: 1686
# Giay-dep-nu: 1703
# tui-vi-nu/c976
# tui-thoi-trang-nam/c27616
# phu-kien-thoi-trang/c27498
# dong-ho-va-trang-suc/c8371

# params = {
#     'limit': '40',
#     'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
#     'aggregations': '2',
#     'trackity_id': '648bc5aa-93d1-ca54-80c7-88ad8776510e',
#     'category': '915',
#     'page': '1',
#     'src': 'c915',
#     'urlKey': 'thoi-trang-nam',
# }
# params = {
#     'limit': '40',
#     'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
#     'aggregations': '2',
#     'trackity_id': '648bc5aa-93d1-ca54-80c7-88ad8776510e',
#     'category': '1703',
#     'page': '1',
#     'src': 'c1703',
#     'urlKey': 'giay-dep-nu',
# }

paramList = [
    {
        'urlKey': 'thoi-trang-nam',
        'category': '915',
        'src': 'c915'
    },
    {
        'urlKey': 'thoi-trang-nu',
        'category': '931',
        'src': 'c931'
    },
    {
        'urlKey': 'giay-dep-nam',
        'category': '1686',
        'src': 'c1686'
    },
    {
        'urlKey': 'giay-dep-nu',
        'category': '1703',
        'src': 'c1703'
    },
    {
        'urlKey': 'tui-vi-nu',
        'category': '976',
        'src': 'c976'
    },
    {
        'urlKey': 'tui-thoi-trang-nam',
        'category': '27616',
        'src': 'c27616'
    },
    {
        'urlKey': 'phu-kien-thoi-trang',
        'category': '27498',
        'src': 'c27498'
    },
    {
        'urlKey': 'dong-ho-va-trang-suc',
        'category': '8371',
        'src': 'c8371'
    },

]

params = {
    'limit': '40',
    'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
    'aggregations': '2',
    'trackity_id': '648bc5aa-93d1-ca54-80c7-88ad8776510e',
    'category': '8371',
    'page': '1',
    'src': 'c8371',
    'urlKey': 'dong-ho-va-trang-suc',
}

product_list = []

# datetime object containing current date and time
now = datetime.datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


def parse_json_data_to_product(json_product):
    product = {
        'id': json_product.get('id'),
        'productname': json_product.get('name'),
        'priceafterdiscount': json_product.get('price'),
        'pricebeforediscount': json_product.get('original_price'),
        'discount': json_product.get('discount'),
        'discountrate': json_product.get('discount_rate'),
        'rating_average': json_product.get('rating_average'),
        'review_count': json_product.get('review_count'),
        'date': dt_string
    }
    product['url'] = 'https://tiki.vn/product-p' + str(product['id']) + '.html?spid=99156611'

    if json_product.get('quantity_sold') is not None:
        product['quantity_sold'] = json_product.get('quantity_sold').get('value')
    else:
        product['quantity_sold'] = 0
    if json_product.get('categories') is not None:
        product['category'] = json_product.get('categories').get('name')
    else:
        product['category'] = 'Thời trang'
    if json_product.get('specifications') is not None:
        product['location'] = json_product.get('specifications')[0].get('value')
    else:
        product['location'] = 'Việt Nam'
    print(product)
    return product


for element in paramList:
    params['urlKey'] = element['urlKey']
    params['category'] = element['category']
    params['src'] = element['src']
    for i in range(1, 50):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/v2/products', headers=headers, params=params)
        if response.status_code == 200:
            print('request success!!!')
            for record in response.json().get('data'):
                product_list.append(parse_json_data_to_product(record))
        else:
            continue
        time.sleep(random.randrange(3, 10))
    print(product_list)

df_product_list = pd.DataFrame(product_list)
fileName = 'crawled_product_' + 'v3.csv'
df_product_list.to_csv(fileName, index=False)
