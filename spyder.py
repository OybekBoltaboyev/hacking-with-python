import re
import requests
import urlparse

target_url = "http://apple.com"


def extract_link(url):
    response = requests.get(target_url)
    return re.findall(b'(?:href=")(.*?)"', response.content)


href_link = extract_link(target_url)

for link in href_link:
    link = urlparse.urljoin(target_url,link)

    if target_url in link:
        print(link)