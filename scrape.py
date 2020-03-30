import urllib, json
import requests
from bs4 import BeautifulSoup
from pprint import pprint

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

API_KEY = "add your key here"
CSE_ID = "add your cse id here"

query_list = "runner beans, split peas, soy beans, peas, snap peas, broccoflower, broccoli, brussels sprouts, cabbage, kohlrabi".split(",")
# for query in query_list:
query = "split peas"

URL = "https://www.googleapis.com/customsearch/v1?key="+API_KEY+"&cx="+CSE_ID+"&q="+query+"&start=0"

headers = {"user-agent": USER_AGENT}
resp = requests.get(URL, headers=headers)

soup = BeautifulSoup(resp.content, "html.parser")

try:
    soup = json.loads(soup.replace("\\", r"\\"))
except:
    soup = json.loads(soup.text.encode('utf-8'))
links = []
for i in range(0,10):
    startInd = soup["queries"]["nextPage"][0]["startIndex"]
    for result in soup["items"]:
        print(result.get('link'))
        links.append(result.get('link').encode('utf-8'))
        // get whatever other content you want
    URL = "https://www.googleapis.com/customsearch/v1?key="+API_KEY+"&cx="+CSE_ID+"&q="+query+"&start="+str(startInd)
    soup = requests.get(URL).json()
