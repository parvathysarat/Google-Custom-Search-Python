import urllib, json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

API_KEY = "AIzaSyDWl58M186uFxZswgMC7eWSvkFlWx7gkPw"
CSE_ID = "005384351359928257221:rfidza4h4cx"

query_list = "runner beans, split peas, soy beans, peas, snap peas, broccoflower, broccoli, brussels sprouts, cabbage, kohlrabi".split(",")
# for query in query_list:
query = "split peas"

URL = "https://www.googleapis.com/customsearch/v1?key="+API_KEY+"&cx="+CSE_ID+"&q="+query+"&start=0"

headers = {"user-agent": USER_AGENT}
resp = requests.get(URL, headers=headers)

soup = BeautifulSoup(resp.content, "html.parser")
print(soup.text)
# soup.text = soup.text.replace("a", "b")

try:
    # soup = json.loads((soup.text.replace('"', '')))
    soup = json.loads(soup.replace("\\", r"\\"))
    print(soup)
except:
    soup = json.loads(soup.text.encode('utf-8'))
links = []

for i in range(0,10):


    startInd = soup["queries"]["nextPage"][0]["startIndex"]
    
    for result in soup["items"]:
        links.append(result.get('link').encode('utf-8'))


    URL = "https://www.googleapis.com/customsearch/v1?key="+API_KEY+"&cx="+CSE_ID+"&q="+query+"&start="+str(startInd)
    
    soup = requests.get(URL).json()

write_text = []
text_link = []
for link in links:

    try:
        page=requests.get(link)

        soup = BeautifulSoup(page.content, 'html.parser')
        print("##############################NEW TEXT#############################")
        data=soup.find_all('p')
        for text in data:
            text_link.append(link)
            write_text.append(text.get_text())
            # print(text.get_text())
    except: 
        continue
csv_name = query+".csv"
df = pd.DataFrame({'link': text_link, 'content': write_text})
df.to_csv(csv_name,index=False)