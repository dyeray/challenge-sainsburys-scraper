import json
import argparse

from scraper import scrape_products

url = "http://hiring-tests.s3-website-eu-west-1.amazonaws.com" \
      "/2015_Developer_Scrape/5_products.html"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape market products')
    parser.add_argument('--url', default=url, help='url to parse')
    args = parser.parse_args()
    content = scrape_products(url=args.url)
    print(json.dumps(content, indent=4))