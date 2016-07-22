from bs4 import BeautifulSoup
import requests
import string
import re
import pandas as pd
import numpy as np


# Queries the AKC for official list
print "Getting AKC List"
akc_link = 'http://www.akc.org/dog-breeds/?letter='

dog_list = []
for char in string.ascii_uppercase:
    page = requests.get(akc_link + char)
    soup = BeautifulSoup(page.text, 'html.parser')
    queried = soup.find_all(class_='scale-contents')
    for dog in queried:
        cleaned = re.sub('[^A-Za-z ]+', '', dog.a.text)
        dog_list.append(cleaned)

dog_frame = pd.DataFrame(dog_list, columns=['Breed'])
dog_frame['Links'] = np.nan
dog_frame['Net'] = np.nan


# Queries image-net for result links
img_link = 'http://www.image-net.org/'

print "Getting breed links"
for idx in dog_frame.index:
    breed = dog_frame.iloc[idx,0]
    dog_page = requests.get(img_link + 'search?q=' + breed)
    dog_soup = BeautifulSoup(dog_page.text, 'html.parser')
    link_list = dog_soup.findAll('td', {'width': '70%'})
    dog_frame.iloc[idx, 1] = len(link_list)

    if len(link_list) > 0:
        first_href = link_list[0].find('a')['href']
        dog_frame.iloc[idx, 2] = first_href


filter_dog_frame = dog_frame[dog_frame['Links'] > 0]
filter_dog_frame['Images'] = np.nan

img_list_link = 'http://www.image-net.org/api/text/imagenet.synset.geturls?'

print "Getting ind image links"
for filter_idx in filter_dog_frame.index:
    full_link = filter_dog_frame.loc[filter_idx, 'Net']
    breed_link = re.search("\?(.*)", full_link).groups()[0]
    img_page = requests.get(img_list_link + breed_link)
    img_soup = BeautifulSoup(img_page.text, 'html.parser')
    img_link_full = img_soup.text
    img_link_full = re.sub('[\n]', '', img_link_full)
    img_link_list = img_link_full.split('\r')
    filter_dog_frame.loc[filter_idx, 'Images'] = len(img_link_list)

filter_dog_frame.to_csv('/Users/lzkatz/Desktop/Galvanize/Capstone/data/doglist.csv')
