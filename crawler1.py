import sys
import csv
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
r=requests.get('http://60.30.69.47')
soup=BeautifulSoup(r.text,'html.parser')
tmp=soup.find('div',{'style':'margin-top: 70px;'}).tr.findAll('imgs')
imgs=[img.attrs['scr'] for img in tmp]
for i in range(0, len(imgs)):
    a = requests.get(imgs[i])
    filename = '{}.jpg'.format(i)
    with open(Path(imgs1).joinpath(filename), 'wb') as f:
        for chunk in a:
            f.write(chunk)








