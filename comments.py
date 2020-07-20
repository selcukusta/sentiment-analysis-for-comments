
import requests
import time
import csv
import json
import argparse
import enum
import sys
from normalizer import normalizer
from crawler import crawler
from common import common

CRAWL_COUNTER = 0


def get_comments(product_id, size=10, same_product=False):
    time.sleep(3)

    global CRAWL_COUNTER
    if not(same_product):
        CRAWL_COUNTER += 1

    result = []
    url = f"https://api.trendyol.com/webbrowsinggw/api/review/{product_id}?pageSize={size}"

    print(f"({CRAWL_COUNTER}) {url} is crawling...")
    try:
        resp = requests.get(url, crawler.create_random_headers())
        if resp.status_code != 200 or resp.headers.get("Content-Type") != "application/json; charset=utf-8":
            common.colored_print(
                common.bcolors.FAIL, f"{url} response is invalid! Status code: {resp.status_code}")
            sys.exit(-1)

        output = resp.json()
        if output is None or output.get("result") is None:
            return result

        if "productReviews" not in output.get("result"):
            return result

        if "totalElements" in output.get("result").get("productReviews") and "size" in output.get("result").get("productReviews"):
            total_elements = int(output.get("result").get(
                "productReviews").get("totalElements"))
            if not(total_elements > 0):
                return result

            size = int(output.get("result").get("productReviews").get("size"))
            if total_elements > size:
                common.colored_print(
                    common.bcolors.WARNING, f"{product_id} has more than one page for comments!")
                return get_comments(product_id, total_elements, True)

        if "content" not in output.get("result").get("productReviews"):
            return result

        for comment in output.get("result").get("productReviews").get("content"):
            if 'comment' not in comment or 'rate' not in comment:
                continue

            value = normalizer.normalize(comment.get("comment"))
            if value == "":
                continue

            rate = int(comment.get('rate'))
            label = "__label__"
            if rate in [0, 1, 2]:
                label += "negative"
            elif rate in [3]:
                label += "notr"
            else:
                label += "positive"
            result.append(f"{label} {value}")

        return result
    except Exception as ex:
        common.colored_print(common.bcolors.FAIL, str(ex))
        sys.exit(-1)


if __name__ == "__main__":
    ft_type = enum.Enum("ft_type", ("train", "valid"))
    parser = argparse.ArgumentParser(
        description='Trendyol satıcısına ait ürünler yorumlarını FastText kütüphanesi kullanımı için etiketleyerek kaydeder.')
    parser.add_argument('merchant_id', type=int,
                        help='Trendyol satıcı numarasını giriniz')
    parser.add_argument('ft_type', type=str,
                        choices=tuple(t.name for t in ft_type),
                        default=ft_type.train.name,
                        help='FastText öğrenmesi esnasında kullanım tipini giriniz')
    parser.add_argument('start_line', type=int,
                        default=1,
                        help='Okumaya başlanacak satır sayısını giriniz')

    args = parser.parse_args()
    CRAWL_COUNTER = args.start_line - 1
    with open(f"products/{args.merchant_id}.csv", 'r') as f:
        reader = csv.reader(f)
        [next(reader, None) for item in range(CRAWL_COUNTER)]
        for row in reader:
            comments = get_comments(row[0])
            with open(f'fastText/comments.{args.ft_type}', 'a') as f:
                for item in comments:
                    f.write(f"{item}\n")

    common.colored_print(common.bcolors.OKBLUE, "=== COMPLETED ===")
