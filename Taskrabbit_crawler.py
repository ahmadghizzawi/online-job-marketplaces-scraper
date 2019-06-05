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

def crawl_site(url, city, task, output_path, pics_path):
	#Path to your chromedriver.exe directory
    browser = webdriver.Chrome("/Users/slide/Documents/GitHub/online-job-marketplaces-scraper/chromedriver")

    # Load webpage
    browser.get(url)
    browser.implicitly_wait(1)

    # dismiss cookie if it is displayed
    element = browser.find_element_by_css_selector('.js__cookie-banner-dismiss')
    if element.is_displayed():
        element.click()
    else:
        print('cookie banner hidden')
    #
    # # Click on the first task type
    # browser.find_element_by_css_selector('#metro-templates .btn.btn-secondary.btn-small.js__formEntry').click()

    # TASK INTEREST
    	# Task interest selected (i'm just browsing)
    browser.find_element_by_id("intent_level_low").click()

    browser.find_element_by_css_selector('.btn.btn-primary').click()

    # TASK LOCATION / START ADDRESS
    	#Location selected from the query
    browser.find_element_by_css_selector("input[name='location.freeform']").send_keys(city)
    	#Unit or Apt optional, we selected number 5
    browser.find_element_by_id("address2").send_keys("5")
    time.sleep(1)
    browser.find_element_by_css_selector('.btn.btn-primary').click()
    time.sleep(1)

    # TASK END ADDRESS (HELP MOVING CASE)
    # Condition for the case where we have 5 boxes (assembly task)
    boxes = browser.find_elements_by_css_selector(".build-group")
    if len(boxes) == 5:
        print('found 5 boxes')
        assembly = browser.find_elements_by_css_selector(".build-input-list li:last-of-type > input[type='radio']")
        for element in assembly:
            element.click()
        browser.find_element_by_css_selector('.btn.btn-primary').click()
    time.sleep(3)

    # TASK OPTIONS
    	#Loop to select the first option in each elements of the task options
    elements = browser.find_elements_by_css_selector(".build-input-list li:first-of-type > input[type='radio']")

    for element in elements:
        element.click()

    btn = browser.find_element_by_css_selector('.btn.btn-primary').click()
    time.sleep(1)

    # TASK DETAILS
    	# we fill the task details with one letter in order to be able to select the primary button
    browser.find_element_by_css_selector("textarea[name='description']").send_keys('t')
    time.sleep(1)

    browser.find_element_by_css_selector('.btn.btn-primary').click()
    time.sleep(1)

    # WORKERS LIST
    # Task date selected to within a week 
    browser.find_element_by_id("recommendations__schedule-option-next_week").click()

    # sleep time in order to load the whole page correctly
    time.sleep(3)

    workers = browser.find_elements_by_css_selector('.recommendations__result_wrapper')

    #Loop to build the list of workers
    list_workers = []
    iteration_number = 1
    for worker in workers:
        # worker build
        worker_dict = {
            'id': worker.find_element_by_css_selector('.recommendations__result.recommendations__result--tasker').get_attribute('data-user-id'),
            'rank': iteration_number,
            'picture': worker.find_element_by_css_selector('.recommendations__avatar__circular').get_attribute('src'),
            'positive_rating': worker.find_elements_by_xpath("//i[@class='ss-lnr-star']/following-sibling::span")[iteration_number - 1].text,
            'number_of_relevant_tasks': worker.find_elements_by_xpath("//i[@class='ss-lnr-check-circle']/following-sibling::span")[iteration_number - 1].text,
            'great_value_badge': '',
            'elite_tasker': '',
            'new_tasker': '',
            'how_can_help': worker.find_element_by_css_selector('.recommendations__blurb').text,
            'right_person': '',
            'when_tasking': '',
            'number_of_reviews_received': '',
            'number_of_relevant_reviews_received': '',
            #Return the string of per_hour_rate
            'per_hour_rate': float(re.findall(r"[-+]?\d*\.\d+|\d+", worker.find_element_by_css_selector('strong').text)[0]),
            #City and the task separated by '_' 
            'query': slugify(city + '_' + task),
            'reviews': []
        }

        # positive rating
        try:
        	# Return the float of the percentage of Positve rating
            worker_dict['positive_rating'] = float(int(re.findall(r"[-+]?\d*\.\d+|\d+",
                                                               worker_dict['positive_rating'])[0]) / 100)
        except IndexError:
        	# Case of positive rating not found
            worker_dict['positive_rating'] = None

        # number of relevant tasks

        try:
        	# Return the number of relevant tasks
            worker_dict['number_of_relevant_tasks'] = int(re.findall(r"[-+]?\d*\.\d+|\d+",
                                                                  worker_dict['number_of_relevant_tasks'])[0])
        except IndexError:
        	# Case of relevant tasks not found
            worker_dict['number_of_relevant_tasks'] = None

        # worker has great value badge?
        try:
        	# Boolean for value_badge 
            worker.find_element_by_css_selector('.recommendations__great-value-badge')
            worker_dict['great_value_badge'] = True
        except NoSuchElementException:
        	# Case of value_badge not found
            worker_dict['great_value_badge'] = False

        # worker is an elite tasker?
        try:
        	# Boolean for elite_tasker 
            worker.find_element_by_css_selector('.ss-medal-star')
            worker_dict['elite_tasker'] = True
        except NoSuchElementException:
        	# Case of elite_tasker not found
            worker_dict['elite_tasker'] = False

        # worker is a new tasker?
        try:
        	# Boolean for new_tasker
            worker.find_element_by_css_selector('.ss-happy-lined')
            worker_dict['new_tasker'] = True
        except NoSuchElementException:
        	# Case of new_tasker not found (ss-happy-lined)
            worker_dict['new_tasker'] = False

        # open user popup (Profile & reviews)
        worker.find_element_by_css_selector('.recommendations__result-name').click()

        # retrieve the first free text
        try:
            worker_dict['right_person'] = browser.find_elements_by_css_selector('.tasker--bio-responses')[0].text
        except:
            print('no right person')

        # retrieve the second free text
        try:
            worker_dict['when_tasking'] = browser.find_elements_by_css_selector('.tasker--bio-responses')[1].text
        except:
            print('no when tasking')

        # retrieve number of reviews
        reviews_dropdown = browser.find_elements_by_css_selector('.reviews__filter--select option')
        if len(reviews_dropdown) > 0:
            worker_dict['number_of_reviews_received'] = int(re.findall(r"[-+]?\d*\.\d+|\d+", reviews_dropdown[-1].text)[0])
            worker_dict['number_of_relevant_reviews_received'] = int(
                re.findall(r"[-+]?\d*\.\d+|\d+", reviews_dropdown[0].text)[0])

            # select all reviews
            reviews_dropdown[-1].click()
        else:
        	# If worker have no review
            worker_dict['number_of_reviews_received'] = 0
            worker_dict['number_of_relevant_reviews_received'] = 0

        # while clicking on right arrow is permissible, retrieve the next page of reviews
        next_page = browser.find_elements_by_xpath(
            "//span[@class='current']/following-sibling::a")
        while True:
            # Retrieve reviews
            reviews = browser.find_elements_by_css_selector('.tasker-review')
            if len(reviews) > 0:
                for review in reviews:
                    worker_dict['reviews'].append({
                        'text': review.find_element_by_css_selector('.exterior__bottom--sm').text,
                        'date': review.find_element_by_css_selector('.review-author').text.split(',', 1)[1]
                    })
            if len(next_page) > 0:
                next_page[0].click()
                next_page = browser.find_elements_by_xpath(
                "//span[@class='current']/following-sibling::a")
                time.sleep(0.5)
            if len(next_page) == 0:
                break

        # close popup of the worker profile & reviews
        browser.find_element_by_css_selector('.lightbox--dismiss').click()

        # Add the worker to the list of workers
        list_workers.append(worker_dict)
        # Save users pictures
        # Must create pics folder in your directory
        
        urllib.request.urlretrieve(worker_dict['picture'], pics+'/' + str(worker_dict['id']) + ".jpg")
        iteration_number += 1

        time.sleep(0.5)

    # Write the list of workers found in a json file 
    # Must create results folder in the directory of datasets
    with open(output+'/' + slugify(city + '-' + task) + '.json', 'w') as fout:
        json.dump(list_workers, fout)

    # Query finished close the browser
    browser.close()


def main():
    parser = argparse.ArgumentParser(description= 'taskrabbit crawler')
    parser.add_argument('-f', '--file', type =str, metavar='', help=' The files containing the queries you wish to work with')
    parser.add_argument('-r', '--results', type= str,metavar='',default='results/',help='The output directory containing the result')
    parser.add_argument('-p', '--pics', type= str,metavar='',default='pics/',help='The output directory containing the pics')

    args = parser.parse_args()
    if args.file is None:
        print('No input file passed \nAutomatic crawl Taskrabbit.com')
        subprocess.call('scrapy crawl cities -o cities.json', shell=True ,cwd='./src/Taskrabbit/spider/Taskrabbit/')
        subprocess.call('mv cities.json ./../../cities.json',shell=True ,cwd='./src/Taskrabbit/spider/Taskrabbit/')
        subprocess.call('python3 clean_cities.py',shell=True ,cwd='./src/Taskrabbit/')
        subprocess.call('cp final_cities.json ./../../data/taskrabbit/final_cities.json',shell=True ,cwd='./src/Taskrabbit/')
        subprocess.call('scrapy crawl allqueries -o allqueries.json', shell=True ,cwd='./src/Taskrabbit/spider/Taskrabbit/')
        subprocess.call('scrapy crawl task_urls -o final.json', shell=True ,cwd='./src/Taskrabbit/spider/Taskrabbit/')
        subprocess.call('mv final.json ./../../final.json',shell=True ,cwd='./src/Taskrabbit/spider/Taskrabbit/')
        subprocess.call('rm allqueries.json',shell=True ,cwd='./src/Taskrabbit/spider/Taskrabbit/')
        subprocess.call('python3 helpers.py',shell=True ,cwd='./src/Taskrabbit/')
        subprocess.call('python3 final_queries.py',shell=True ,cwd='./src/Taskrabbit/')
        subprocess.call('cp final_queries.json ./../../data/taskrabbit/final_queries.json',shell=True ,cwd='./src/Taskrabbit/')
        subprocess.call('rm *.json',shell=True ,cwd='./src/Taskrabbit/')
        args.file = 'final_queries.json'

    # Creation of the sub folder pics and results with the timestamp of the program execution where we store the results
    timestr = time.strftime("%m%d-%H-%M")
    source = './Datasets/Taskrabbit/'+args.pics
    pic = os.path.join(source+'pics '+timestr)
    if not os.path.exists(pic):
    	os.makedirs(pic)

    source2 = './Datasets/Taskrabbit/'+args.results
    res = os.path.join(source2+'results '+timestr)
    if not os.path.exists(res):
    	os.makedirs(res)


    with open('./Data/taskrabbit/'+args.file) as f:
        entries = json.load(f)
    # Counter used to know the number of query 
    counter = 1
    failed = []
    for entry in entries:
        print('Crawling query #', counter, 'out of', len(entries))
        try:
            if entry['city'].endswith('UK'):
            	# UK cities, UK taskrabbit
                website = 'https://www.taskrabbit.co.uk'
            elif entry['city'] in ['Toronto, CA', 'Vancouver, CA']:
            	# Canada cities, Canadien taskrabbit
                website = 'https://www.taskrabbit.ca'
            else:
            	# USA taskrabbit
                website = 'https://www.taskrabbit.com'
            # List of attrbute for crawl_site fonction
            crawl_site(website + entry['url'], entry['city'], entry['task_title'],res,pic)
        except Exception as error:
            print('query #', counter, 'failed.')
            print('Error:', error)
            failed.append(entry)
        counter += 1
        time.sleep(5)
        with open('./Datasets/Taskrabbit/failed_queries.json', 'w') as f:
            json.dump(failed, f)
if __name__ == "__main__":
    main()
