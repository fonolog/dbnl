#scrapedbnl.py
'''Script to get all Dutch epub files collected by DBNL.org '''


import requests
from bs4 import BeautifulSoup

for x in range(1,59):
    url='https://www.dbnl.org/titels/titels_ebook.php?s=t&p='+str(x)
    print (url) # to keep track of where we are while waiting
    content = requests.get(url).content

    soup = BeautifulSoup(content, "html.parser")
    epubs = {i for i in [link.get('href') for link in soup.findAll('a')] if str(i)[-5:]=='.epub'}

    for epub in list(epubs):
        response = requests.get('https://www.dbnl.org'+epub)
        with open(epub.split('/')[-1], 'wb') as output_file:
            output_file.write(response.content)