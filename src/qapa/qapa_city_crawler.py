from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify
import json



def main():
    browser = webdriver.Chrome("/Users/slide/Documents/GitHub/online-job-marketplaces-scraper/chromedriver")
    url = 'https://www.qapa.fr/localites/a'
    cities = []
    for i in range(26):
        browser.get("https://www.qapa.fr/localites/" + chr(i+97))
        browser.implicitly_wait(5)
        counter = 2
        while True:
            city = browser.find_elements_by_css_selector('#seo-locality > div > div.row > div:nth-child(2) > ul.list-item > li')
            if len(city) > 0:
                for ville in city:
                    work = {
                    #cities['city'].append(ville.find_elements_by_css_selector('a')[0].text.replace("Emploi",""))
                    'city': ville.find_elements_by_css_selector('a')[0].text.replace("Emploi ","")
                    }
                    cities.append(work)
                browser.get("https://www.qapa.fr/localites/" + chr(i+97)+"/"+str(counter))
                counter += 1
            else:
                break
    browser.close()
    with open('cities.json','w') as f:
        json.dump(cities , f, ensure_ascii=False)
main()