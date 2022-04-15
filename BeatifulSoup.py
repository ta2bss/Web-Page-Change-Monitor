from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import re
import ssl

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    if re.match(r"[\n]+",str(element)): return False
    return True
def text_from_html(url):
    body = urllib.request.urlopen(url,context=ssl._create_unverified_context()).read()
    soup = BeautifulSoup(body ,"lxml")
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    text = u",".join(t.strip() for t in visible_texts)
    text = text.lstrip().rstrip()
    text = text.split(',')
    clean_text = ''
    for sen in text:
        if sen:
            sen = sen.rstrip().lstrip()
            clean_text += sen+','
    return clean_text
url = 'https://testnet.run/'
print(text_from_html(url))