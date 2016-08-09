from bs4 import BeautifulSoup
import requests
import string
import re
import pandas as pd
import numpy as np
import os
import shutil
import json

with open('/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/aux_files/breed_dict.json') as bd:
    classes = json.load(bd)



akc_link = 'http://www.akc.org/dog-breeds/?letter='
print "Getting AKC List"
dog_list = []
img_list = []
for char in string.ascii_uppercase:
    page = requests.get(akc_link + char)
    soup = BeautifulSoup(page.text, 'html.parser')
    queried = soup.find_all(class_='scale-contents')
    for dog in queried:
        cleaned = re.sub('[^A-Za-z]+', '', dog.a.text)
        if cleaned in classes.values():
            dog_list.append((cleaned,dog.a.text, dog.a['href']))

    images = soup.find_all(class_='scale-img-image')
    for img in images:
        cleaned_image = re.sub('[^A-Za-z]+', '', img['alt'])
        if cleaned_image in classes.values():
            img_list.append((cleaned_image, img['src']))

for path, link in img_list:
    outpath = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/app/static/images/' + path + '.jpg'
    img_link = urllib2.urlopen('http:' + link)
    with open(outpath, 'wb') as f:
        f.write(img_link.read())

new_list = []
for tup in dog_list:
    link = tup[2]
    breed_link = 'http://www.akc.org' + link + 'detail/'
    breed_page = requests.get(breed_link)
    breed_soup = BeautifulSoup(breed_page.text, 'html.parser')
    query = breed_soup.find(class_='welcome-block')
    desc = (query.text,)
    print tup + desc
    new_list.append(tup + desc)

app_dict = {}
for i, tup in enumerate(new_list):
    app_dict[i] = (tup[1], tup[3])

with open('/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/app/predict/app_dict.json', 'wb') as ad:
    json.dump(app_dict, ad)
