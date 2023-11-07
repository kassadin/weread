import argparse
import time
import random

import requests
import sys, traceback, logging
import config
import json

config = config.read_config()

logger = logging.getLogger("weread")


def exception_handler(exctype, value, tb):
    logger.error(exctype)
    logger.error(value)
    logger.error(traceback.extract_tb(tb))


sys.excepthook = exception_handler

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "referer": "https://weread.qq.com/"
}


def get_page(maxIndex):
    url = f"https://weread.qq.com/web/bookListInCategory/{config['category']}?maxIndex={maxIndex}"
    res = requests.get(url, headers=headers, )
    return res.json()


def check_mode():
    resp = get_page(20)

    if resp["totalCount"] == config["totalCount"]:
        logger.info("No changes: TotalCount is the same as the existing configuration.")
    else:
        logger.info(f"Changes detected: TotalCount has changed from {config['totalCount']} to {json['totalCount']}.")


def full_update_mode():
    books = []
    for i in range(0, config["totalCount"], 20):
        resp = get_page(i)
        books.extend(resp["books"])
        if resp['hasMore'] == 0:
            break
        delay = random.uniform(0, 5)
        time.sleep(delay)
    with open('books.json', 'w', encoding='utf-8') as outfile:
        json.dump(books, outfile, ensure_ascii=False)


def incremental_update_mode():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web Scraper with Different Modes')

    parser.add_argument('-c', action='store_true', help='Check mode (check if the website is accessible)')
    parser.add_argument('-a', action='store_true', help='Full update mode (retrieves all data)')
    parser.add_argument('-u', action='store_true', help='Incremental update mode (retrieves new data)')

    args = parser.parse_args()

    if sum([args.c, args.a, args.u]) != 1:
        print("Please select one and only one mode: -c, -a, or -u")
        sys.exit(1)

    if args.c:
        check_mode()
    elif args.a:
        full_update_mode()
    elif args.u:
        incremental_update_mode()
