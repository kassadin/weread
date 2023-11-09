import argparse
import json
import logging
import random
import sys
import time

import requests

import config

config = config.read_config()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "referer": "https://weread.qq.com/"
}


def get_page(maxIndex):
    url = f"https://weread.qq.com/web/bookListInCategory/{config['category']}?maxIndex={maxIndex}"
    res = requests.get(url, headers=headers, )
    logger.info(f"{maxIndex:}: http status: {res.status_code}")
    return res.json()


def check_mode():
    resp = get_page(20)

    if resp["totalCount"] == config["totalCount"]:
        logger.info("No changes: TotalCount is the same as the existing configuration.")
    else:
        logger.info(f"Changes detected: TotalCount has changed from {config['totalCount']} to {resp['totalCount']}.")


def full_update_mode():
    books = []
    for i in range(0, 500, 20):
        resp = get_page(i)
        logger.info(f"{i:} {resp['totalCount']}, {resp['hasMore']}")
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
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', action='store_true', help='check')
    parser.add_argument('-a', action='store_true', help='full')
    parser.add_argument('-u', action='store_true', help='incremental')

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
