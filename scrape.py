import argparse
from xml.etree import ElementTree
import re
import requests
from urllib.parse import urlencode
import webbrowser


def get_magazine_articles(year, month, day):
    urls = []

    for week in range(1,5):
        url=f'https://www.newyorker.com/sitemap.xml?year={year}&month={month}&week={week}'
        print(url)
        reply = requests.get(url)

        #print(reply.content)
        root = ElementTree.fromstring(reply.content)
        print(root)

        for url in root:
            if not url.tag.endswith('url'):
                raise RuntimeError(f"Expected to find 'url' but found '{url.tag}'")
            loc = url[0]
            if loc.text.startswith(f'https://www.newyorker.com/magazine/{year}/{month}/{day}/'):
                urls.append(loc.text)

    return urls

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('year')
    argparser.add_argument('month')
    argparser.add_argument('day')

    args = argparser.parse_args()

    urls = get_magazine_articles(args.year, args.month, args.day)

    for url in urls:
        print(url)
        param = urlencode({'url' : url})
        webbrowser.open(f'https://getpocket.com/edit?{param}')

