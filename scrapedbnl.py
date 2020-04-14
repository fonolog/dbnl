#scrapedbnl.py
toelichting = '''Dit script haalt epub-bestanden van de pagina's met e-boeken van de DBNL.
Gebruik deze bestanden alleen voor eigen gebruik, met name onderzoek.
De gebruiksvoorwaarden van de DBNL van kracht: https://www.dbnl.org/overdbnl/copyright.php'''

print(toelichting)

import requests
from bs4 import BeautifulSoup

file_formats = ['epub'] # extensions (last four characters)

for x in range(1,59):
    url='https://www.dbnl.org/titels/titels_ebook.php?s=t&p='+str(x)
    print (url) # to keep track of where we are while waiting
    content = requests.get(url).content

    soup = BeautifulSoup(content, "html.parser")
    epubs = {i for i in [link.get('href') for link in soup.findAll('a')] if str(i)[-4:] in file_formats}

    for epub in list(epubs):
        response = requests.get('https://www.dbnl.org'+epub)
        with open(epub.split('/')[-1], 'wb') as output_file:
            output_file.write(response.content)