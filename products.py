from bs4 import BeautifulSoup
import requests
import re
import math as m
import argparse
import sys
import time
from crawler import crawler
from common import common

PRODUCT_PER_PAGE = 24


def get_product_count(merchant_id):
    url = "https://www.trendyol.com/tum--urunler?satici={}".format(merchant_id)
    resp = requests.get(url, crawler.create_random_headers())
    if resp.status_code != 200:
        common.colored_print(
            common.bcolors.FAIL, f"Application is terminating! Status code: {resp.status_code}")
        sys.exit(-1)

    soup = BeautifulSoup(resp.content, 'html.parser')
    title = soup.select("div.dscrptn")[0].getText()
    regex = r"(\d+)"
    match = re.findall(regex, title, re.IGNORECASE)
    if len(match) > 0:
        return match[0]
    return -1


def get_ids(merchant_id, page):
    time.sleep(3)
    result = []
    url = "https://www.trendyol.com/tum--urunler?satici={}&pi={}".format(merchant_id,
                                                                         str(page))
    resp = requests.get(url, crawler.create_random_headers(),
                        allow_redirects=False)
    if resp.status_code != 200:
        if resp.headers.get("Location") is not None:
            common.colored_print(
                common.bcolors.WARNING, f"This page ({page}) is skipping because of redirect header! Status code: {resp.status_code}, Location: {resp.headers.get('Location')}")
            return result
        else:
            common.colored_print(
                common.bcolors.FAIL, f"Application is terminating! Status code: {resp.status_code}")
            sys.exit(-1)

    print(f"Products on page {page} are crawling...")
    soup = BeautifulSoup(resp.content, 'html.parser')
    for item in soup.find_all('div', class_='p-card-wrppr'):
        result.append({"id": item['data-id'], "url": item.find('a')['href']})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Trendyol satıcısının ürünlerini listeler')
    parser.add_argument('merchant_id', type=int,
                        help='Trendyol satıcı numarasını giriniz')

    args = parser.parse_args()
    count = get_product_count(args.merchant_id)

    if count == -1:
        common.colored_print(common.bcolors.OKGREEN, "No any products!")
        sys.exit()

    total_page = m.ceil(float(count) / PRODUCT_PER_PAGE)
    current_page = 1
    while current_page <= total_page:
        products_current_page = get_ids(args.merchant_id, current_page)
        for product in products_current_page:
            with open(f"products/{args.merchant_id}.csv", 'a') as f:
                f.write(f"{product.get('id')},{product.get('url')}\n")
        current_page += 1

    common.colored_print(common.bcolors.OKBLUE, "=== COMPLETED ===")
