import re

import requests
from bs4 import BeautifulSoup


money_regex = '£(([0-9]*[.])?[0-9]+)'

def scrape_products(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.select('ul.productLister > li a')
    results = [scrape_product(item['href']) for item in items]
    total_price = sum((r['unit_price'] for r in results))
    return {'results': results, 'total': round(total_price, 2)}

def scrape_product(url):
    req_detail = requests.get(url)
    soup_detail = BeautifulSoup(req_detail.text, 'html.parser')
    unit_price = float(re.search(money_regex, soup_detail.find(class_='pricePerUnit').find(
        text=True)).group(1))
    return {
        'title': soup_detail.find(class_='productSummary').h1.text,
        'size': "{0:.2f}kb".format(round(len(req_detail.text)/1024, 2)),
        'unit_price': unit_price,
        'description': soup_detail.find(class_='productText').get_text(strip=True)
    }
