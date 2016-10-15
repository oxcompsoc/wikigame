import urllib.parse
import urllib.request
import json
import re
import wikicache

agent = "OxCompSocWikiGame/1.0 (https://ox.compsoc.net; secretary@ox.compsoc.net)"
base = "https://en.wikipedia.org/w/api.php"

deadends = wikicache.get_deadends()

def wikipedia_request(params):
    params["format"] = "json"
    params["action"] = "query"
    url = base + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
            url,
            data=None,
            headers={ "User-Agent": agent })
    contents = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(contents)

def get_redirect(page):
    params = { "titles"    : page
             , "redirects" : True
             }
    parsed = wikipedia_request(params)["query"]
    if "redirects" in parsed and len(parsed["redirects"]) > 0:
        return parsed["redirects"][0]["to"]
    return None

def get_markup(page):
    params = { "prop"   : "revisions"
             , "rvprop" : "content"
             , "titles" : page
             }
    parsed = wikipedia_request(params)
    if len(parsed["query"]["pages"]) == 0 or "-1" in parsed["query"]["pages"]:
        redirect = get_redirect(page)
        if redirect and redirect != page:
            return get_markup(redirect)
        else:
            return ""
    firstPage = next(iter(parsed["query"]["pages"].values()))
    if "revisions" in firstPage and len(firstPage["revisions"]) > 0:
        contents = firstPage["revisions"][0]["*"]
        if re.match(r'^#REDIRECT', contents, re.IGNORECASE):
            redirect = get_redirect(page)
            if redirect and redirect != page:
                return get_markup(redirect)
        else:
            return contents
    return ""

def links_in_order(page, onlyarticles=True, cache=True):
    links = None
    if cache:
        links = wikicache.get(page)
    if not links:
        content = get_markup(page)
        links = []
        linkSet = set()
        for match in re.finditer(r'\[\[(.*?)\]\]', content):
            linkText = match.group(1)
            barIndex = linkText.find("|")
            if barIndex != -1:
                linkText = linkText[0:barIndex]
            if not linkText in linkSet:
                linkSet.add(linkText)
                links.append(linkText)
        links = [l.partition('#')[0] for l in links if l.lower() != page.lower()]
        links = [l for l in links if not l in deadends]
        links = [l for l in links if len(l) > 0]
        if cache:
            wikicache.put(page, links)
    if not links or len(links) == 0:
        links = []
        deadends.add(page)
        wikicache.put_deadends(deadends)
    if onlyarticles:
        links = [link for link in links if not re.match(r'[A-z]*:', link)]
    return links

def random_article():
    params = { "list"       : "random"
             , "rnlimit"    : 1
             , "rnnamespace": 0
             }
    parsed = wikipedia_request(params)
    return parsed["query"]["random"][0]["title"]
