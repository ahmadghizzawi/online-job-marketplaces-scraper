from selenium import webdriver
import json
import urllib.request
import time
import re
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify


def crawl_site(url, city, task):
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
    browser.find_element_by_id("intent_level_low").click()

    browser.find_element_by_css_selector('.btn.btn-primary').click()

    # TASK LOCATION / START ADDRESS
    browser.find_element_by_css_selector("input[name='location.freeform']").send_keys(city)

    browser.find_element_by_id("address2").send_keys("5")
    time.sleep(1)
    browser.find_element_by_css_selector('.btn.btn-primary').click()
    time.sleep(1)

    # TASK END ADDRESS (HELP MOVING CASE)
    boxes = browser.find_elements_by_css_selector(".build-group")
    if len(boxes) == 5:
        print('found 5 boxes')
        assembly = browser.find_elements_by_css_selector(".build-input-list li:last-of-type > input[type='radio']")
        for element in assembly:
            element.click()
        browser.find_element_by_css_selector('.btn.btn-primary').click()
    time.sleep(3)

    # TASK OPTIONS
    elements = browser.find_elements_by_css_selector(".build-input-list li:first-of-type > input[type='radio']")

    for element in elements:
        element.click()

    btn = browser.find_element_by_css_selector('.btn.btn-primary').click()
    time.sleep(1)
    # TASK DETAILS
    browser.find_element_by_css_selector("textarea[name='description']").send_keys('t')
    time.sleep(1)

    browser.find_element_by_css_selector('.btn.btn-primary').click()
    time.sleep(1)

    # WORKERS LIST
    # Set time to next week
    browser.find_element_by_id("recommendations__schedule-option-next_week").click()

    time.sleep(3)

    workers = browser.find_elements_by_css_selector('.recommendations__result_wrapper')

    list_workers = []
    iteration_number = 1
    for worker in workers:
        # build worker.
        worker_dict = {
            'id': worker.find_element_by_css_selector(
                '.recommendations__result.recommendations__result--tasker').get_attribute('data-user-id'),
            'rank': iteration_number,
            'picture': worker.find_element_by_css_selector('.recommendations__avatar__circular').get_attribute('src'),
            # todo: investigate why these seem to stay the same all the time
            'positive_rating': worker.find_elements_by_xpath(
                "//i[@class='ss-lnr-star']/following-sibling::span")[iteration_number - 1].text,
            'number_of_relevant_tasks': worker.find_elements_by_xpath(
                "//i[@class='ss-lnr-check-circle']/following-sibling::span")[iteration_number - 1].text,
            'great_value_badge': '',
            'elite_tasker': '',
            'new_tasker': '',
            'how_can_help': worker.find_element_by_css_selector('.recommendations__blurb').text,
            'right_person': '',
            'when_tasking': '',
            'number_of_reviews_received': '',
            'number_of_relevant_reviews_received': '',
            'per_hour_rate': float(
                re.findall(r"[-+]?\d*\.\d+|\d+", worker.find_element_by_css_selector('strong').text)[0]),
            'query': slugify(city + '-' + task),
            'reviews': []
        }

        # positive rating
        try:
            worker_dict['positive_rating'] = float(int(re.findall(r"[-+]?\d*\.\d+|\d+",
                                                               worker_dict['positive_rating'])[0]) / 100)
        except IndexError:
            worker_dict['positive_rating'] = None

        # number of relevant tasks
        try:
            worker_dict['number_of_relevant_tasks'] = int(re.findall(r"[-+]?\d*\.\d+|\d+",
                                                                  worker_dict['number_of_relevant_tasks'])[0])
        except IndexError:
            worker_dict['number_of_relevant_tasks'] = None

        # worker has great value badge?
        try:
            worker.find_element_by_css_selector('.recommendations__great-value-badge')
            worker_dict['great_value_badge'] = True
        except NoSuchElementException:
            worker_dict['great_value_badge'] = False

        # worker is a new tasker?
        try:
            worker.find_element_by_css_selector('.ss-happy-lined')
            worker_dict['new_tasker'] = True
        except NoSuchElementException:
            worker_dict['new_tasker'] = False

        # worker is an elite tasker?
        try:
            worker.find_element_by_css_selector('.ss-medal-star')
            worker_dict['elite_tasker'] = True
        except NoSuchElementException:
            worker_dict['elite_tasker'] = False

        # open user popup
        worker.find_element_by_css_selector('.recommendations__result-name').click()

        # retrieve the first free textc
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
            worker_dict['number_of_reviews_received'] = 0
            worker_dict['number_of_relevant_reviews_received'] = 0

        # while clicking on right arrow is permissible, retrieve reviews
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
        # close popup
        browser.find_element_by_css_selector('.lightbox--dismiss').click()

        list_workers.append(worker_dict)
        # Save user picture
        urllib.request.urlretrieve(worker_dict['picture'], 'pics/' + str(worker_dict['id']) + ".jpg")
        iteration_number += 1

        time.sleep(0.5)

    with open('results/' + slugify(city + '-' + task) + '.json', 'w') as fout:
        json.dump(list_workers, fout)

    browser.close()


def main():
    with open('queries.json') as f:
        entries = json.load(f)
    counter = 1
    failed = []
    for entry in entries:
        print('Crawling query #', counter, 'out of', len(entries))
        try:
            if entry['city'].endswith('UK'):
                website = 'https://www.taskrabbit.co.uk'
            elif entry['city'] in ['Toronto, CA', 'Vancouver, CA']:
                website = 'https://www.taskrabbit.ca'
            else:
                website = 'https://www.taskrabbit.com'
            crawl_site(website + entry['url'], entry['city'], entry['task_title'])
        except Exception as error:
            print('query #', counter, 'failed.')
            print('Error:', error)
            failed.append(entry)
        counter += 1
        time.sleep(5)
        with open('failed_queries.json', 'w') as f:
            json.dump(failed, f)

main()