import re

import requests
from bs4 import BeautifulSoup


money_regex = '£(([0-9]*[.])?[0-9]+)'

def scrape_products(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.select('ul.productLister.listView > li a')
    results = []
    total_price = 0
    for item in items:
        req_detail = requests.get(item['href'])
        soup_detail = BeautifulSoup(req_detail.text, 'html.parser')
        unit_price = float(re.search(money_regex, soup_detail.find(class_='pricePerUnit').find(
            text=True)).group(1))
        total_price += unit_price
        results.append({
            'title': soup_detail.find(class_='productSummary').h1.text,
            'size': "{0:.2f}kb".format(round(len(req_detail.text)/1024, 2)),
            'unit_price': unit_price,
            'description': soup_detail.find(class_='productText').get_text(strip=True)
        })
    return {'results': results, 'total': round(total_price, 2)}
