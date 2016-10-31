import unittest
import os
import json

from httmock import urlmatch, HTTMock

from scraper import scrape_products, scrape_product

base_path = os.path.dirname(__file__)


@urlmatch(netloc=r'(.*)$')
def mock_func(url, request):
    file_path = 'data/products.html' if url.netloc == 'testurl' else 'data/product.html'
    with open(os.path.join(base_path, file_path), 'r') as htmldoc:
        return htmldoc.read()


class ScraperTests(unittest.TestCase):

    product_info = {
        "size": "38.27kb",
        "description": "Apricots",
        "title": "Sainsbury's Apricot Ripe & Ready x5",
        "unit_price": 3.5
    }

    def test_products(self):
        with HTTMock(mock_func):
            output = scrape_products('http://testurl')
        self.assertEqual(len(output['results']), 7)
        self.assertEqual(output['total'], 24.5)

    def test_product(self):
        with HTTMock(mock_func):
            output = scrape_product('http://test')
        self.assertEqual(output, self.product_info)
