from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
import json

def main():
    browser = webdriver.Chrome("/Users/slide/Documents/GitHub/online-job-marketplaces-scraper/chromedriver")
    url = 'https://www.qapa.fr/metiers/a'
    services = []
    for i in range(26):
        browser.get("https://www.qapa.fr/metiers/" + chr(i+97))
        browser.implicitly_wait(3)
        counter = 2
        while True:
            service = browser.find_elements_by_css_selector('#seo-trade > div > div.row > div:nth-child(3) > ul.list-item > li')
            if len(service) > 0:
                for job in service:
                    services.append({'task': job.find_elements_by_css_selector('a')[0].text})
                browser.get("https://www.qapa.fr/metiers/" + chr(i+97)+"/"+str(counter))
                counter += 1
            else:
                break
    browser.close()
    with open('qapa_services.json','w') as f:
        json.dump(services , f, ensure_ascii=False)
main()