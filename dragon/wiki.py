import requests
import lxml.html
import json
def get_wiki():
    baseurl = "http://en.wikipedia.org/wiki/Golden_Generation"
    r = requests.get("http://en.wikipedia.org/wiki/Golden_Generation")
    root = lxml.html.fromstring(r.content)
    root.make_links_absolute(baseurl)
    for li in root.xpath("//li/a[contains(@href, '/wiki/')]"):
        try:
            p = li.xpath("./preceding::h3")[-1].text_content()
        except:
            p = "NOPE"
        yield (p,
               li.attrib['href'])

print json.dumps(list(get_wiki()), indent = 2)
