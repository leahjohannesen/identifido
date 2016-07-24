from bs4 import BeautifulSoup
import requests
import string
import re
import pandas as pd
import numpy as np
import os
import shutil

save_loc = '/Users/lzkatz/Desktop/Galvanize/Capstone/Identifido/aux_files/'

def dog_list():
    akc_link = 'http://www.akc.org/dog-breeds/?letter='
    print "Getting AKC List"
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
    return dog_frame

def scrape_for_image_num(dog_frame):
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
    return filter_dog_frame

img_list_link = 'http://www.image-net.org/api/text/imagenet.synset.geturls?'

def make_init_dog_list(filter_dog_frame):
    print "Getting ind image links"
    for filter_idx in filter_dog_frame.index:
        full_link = filter_dog_frame.loc[filter_idx, 'Net']
        breed_link = re.search("\?(.*)", full_link).groups()[0]
        img_page = requests.get(img_list_link + breed_link)
        img_soup = BeautifulSoup(img_page.text, 'html.parser')
        img_link_full = img_soup.text
        img_link_full = re.sub('[\n]', '', img_link_full)
        img_link_list = img_link_full.split('\r')
        # filter_dog_frame.loc[filter_idx, 'Images'] = len(img_link_list)
    filter_dog_frame.to_csv(save_loc + 'doglist.csv')
    return

def img_list():
    print "Scraping for images"
    #path stuff
    img_list_path = save_loc + 'img_list/'
    try:
        shutil.rmtree(img_list_path)
    except:
        pass
    os.mkdir(img_list_path)

    #read in the csv
    filter_dog_frame = pd.read_csv(save_loc + 'doglist.csv')
    final_dog = filter_dog_frame[filter_dog_frame['Images'] > 1000]

    for filter_idx in final_dog.index:
        try:
            breed = final_dog.loc[filter_idx, 'Breed']
            full_link = final_dog.loc[filter_idx, 'Net']
            breed_link = re.search("\?(.*)", full_link).groups()[0]
            img_page = requests.get(img_list_link + breed_link)
            img_soup = BeautifulSoup(img_page.text, 'html.parser')
            img_link_full = img_soup.text
            img_link_full = re.sub('[\n]', '', img_link_full)
            img_link_list = img_link_full.split('\r')
            breed_series = pd.Series(img_link_list, name='Link')
            print breed
            csv_path = img_list_path + breed + '.csv'
            breed_series.to_csv(csv_path)
        except:
            next
