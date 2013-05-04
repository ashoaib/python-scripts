import requests
import sys


class SiteMonitor:
    """
    This is a simple wrapper class around the requests module. It can be used
    to monitor the HTTP status code returned by a website or URL. If the status
    code doesn't match an expected value, it can be used to send an email with
    the status.
    """

    def __init__(self, url=None):
        self.url = None

        if url is not None:
            self.set_url(url)

    def set_url(self, url):
        """Checks if a URL schema is set. If not, defaults to http://"""

        if len(url.split(':')) < 2:
            url = 'http://' + url

        self.url = url

    def make_request(self):
        """Calls the requests.get method if a url is set"""

        if self.url is not None:
            self.request = requests.get(self.url)
        else:
            raise AttributeError("URL is not set or is invalid")

    @property
    def status_code(self):
        return self.request.status_code

    def notify(self):
        pass


if __name__ == '__main__':
    url = sys.argv[1]

    sm = SiteMonitor()
    sm.set_url(url)
    sm.make_request()

    print sm.status_code
