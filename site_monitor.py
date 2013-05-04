import requests
import sys


class SiteMonitor:
    def __init__(self, url):
        self.url = url
        self.request = requests.get(url)
        self.status_code = self.request.status_code


if __name__ == '__main__':
    url = sys.argv[1]
    sm = SiteMonitor(url)
