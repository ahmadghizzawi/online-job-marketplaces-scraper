import argparse
from selenium import webdriver
import json
import urllib.request
import time
import re
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
import os
import subprocess
import time

def crawl_site(url, city, task):
	#Path to your chromedriver.exe directory

    options = webdriver.ChromeOptions()
    #options.add_argument('headless')

	#Path to your chromedriver.exe directory
    browser = webdriver.Chrome("/home/boubou/Stage/chromedriver",chrome_options=options)
    # Load webpage
    browser.get(url)
    affiche('charge + url')
    browser.implicitly_wait(1)

    # Enter task and city
    browser.find_element_by_class_name('react-autosuggest__input').send_keys(task)
    browser.find_element_by_xpath("//input[@placeholder='Ville']").send_keys(city)
    time.sleep(3)
    browser.find_element_by_css_selector('button').click()

    affiche('charge page service')
    time.sleep(3)
    browser.find_element_by_class_name('filter-checkbox-photo-video').click()
    time.sleep(3)
    list_workers = []
    iteration_number = 0
    try:
        #If there is only one page of result than there is no button to go to the next page
        number_of_pages = int(browser.find_element_by_xpath("//button[@class='next']/preceding-sibling::button").text)
    except NoSuchElementException:
        number_of_pages = 1

    affiche('commence le crawling')
    for k in range(number_of_pages):
        i=iteration_number
        iteration_number=0
        try:
            while True:
                iteration_number+=1
                affiche(iteration_number)

                worker_dict = {
                    'page':i,
                    'rank': iteration_number,
                    'rating': '',
                    'picture': browser.find_element_by_xpath('(//div[@class="avatar-container"]/img)['+str(iteration_number)+']').get_attribute('src'),
                    'query': slugify(city + '_' + task),
                    'experience_time': browser.find_element_by_xpath('(//div[@class="xp"])['+str(iteration_number)+']').text,
                    }

                try:
                    worker_dict['rating'] = browser.find_element_by_xpath('(//div[@class="rating"])['+str(iteration_number)+']').text,
                except NoSuchElementException:
                    # No rating
                    worker_dict['rating'] = None
                list_workers.append(worker_dict)
                #urllib.request.urlretrieve(worker_dict['picture'], 'essai'+'/' + str(worker_dict['query'])+ str(worker_dict['page']) + str(worker_dict['rank']) + ".jpg")
        except NoSuchElementException:
            affiche("Plus d'éléments")
            affiche("Nouvelle Page")
            if number_of_pages !=1:
                browser.find_element_by_class_name('next').click()
            iteration_number+=i
            time.sleep(3)

    with open('essai'+'/' + slugify(city + '-' + task) + '.json', 'w') as fout:
        json.dump(list_workers, fout ,ensure_ascii=False)

    browser.close()

def affiche(s):
    if True:
        print(s)

def main():
    with open('./data/mistertemp/' + 'final_services.json') as f:
        entries = json.load(f)
    with open('./data/mistertemp/' + 'final_cities.json') as f:
        cities = json.load(f)
    compteur=1
    for entry in entries:
        for city in cities:
            affiche('query'+str(compteur))
            compteur+=1
            crawl_site('https://www.mistertemp.com/espace-recruteur/',city['city'],entry['service'])


main()
