import re
import time
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify

from src.crawler import RankingItem, OJMCrawler


class PeoplePerHour(OJMCrawler):
    def crawl(self):
        query = self.query
        # Load webpage

        self.browser.get(query.url)
        self.browser.implicitly_wait(1)
        try:
            element = self.browser.find_element_by_css_selector(
                "div.pull-right.drop-filters-trigger"
            )
            element.find_elements_by_tag_name("a")[0].click()
        except NoSuchElementException:
            element = self.browser.find_element_by_css_selector(
                "ul.filters__list"
            )
            element.find_elements_by_tag_name("li")[
                3
            ].find_elements_by_tag_name("a")[0].click()
        suite = self.browser.find_elements_by_xpath(
            '//input[@id="location-input"]'
        )[0]
        suite.send_keys(query.city)
        chopper_list = self.browser.find_elements_by_css_selector(
            "div.tt-dataset-location-input-typeahead"
        )[0]
        time.sleep(2)
        city_pos = chopper_list.find_element_by_css_selector("p")
        city_pos.click()
        time.sleep(2)
        list_url = []
        list_element = self.browser.find_elements_by_css_selector(
            "div.items.clearfix.items-results"
        )[0].find_elements_by_xpath("child::*")
        for element in list_element:
            list_url.append(
                element.find_elements_by_tag_name("a")[0].get_attribute("href")
            )
        last_page = (
            self.browser.find_element_by_id("freelancer-listing-pager")
            .find_elements_by_xpath("child::*")[-2]
            .find_elements_by_tag_name("a")[0]
            .get_attribute("data-page")
        )
        url_base = self.browser.current_url
        for i in range(2, int(last_page) + 1):
            self.browser.get(url_base + "&page=" + str(i))
            time.sleep(1)
            list_element = self.browser.find_elements_by_css_selector(
                "div.items.clearfix.items-results"
            )[0].find_elements_by_xpath("child::*")
            for element in list_element:
                list_url.append(
                    element.find_elements_by_tag_name("a")[0].get_attribute(
                        "href"
                    )
                )

        ranking = 1
        list_workers = []
        for url in list_url:
            self.browser.get(url)
            time.sleep(1)
            worker_dict = RankingItem(
                self.browser.find_element_by_class_name("action-buttons-inner")
                .find_elements_by_tag_name("a")[0]
                .get_attribute("href")
                .split("=")[1],
                self.browser.find_elements_by_xpath(
                    '//div[@class="profile-pic"]/img'
                )[0].get_attribute("src"),
                ranking,
                {
                    "city": query.city,
                    "rating": "",
                    # "service": service,
                    "language": [
                        element.text
                        for element in self.browser.find_element_by_css_selector(
                            "div.member-languages.clearfix"
                        ).find_elements_by_tag_name(
                            "a"
                        )
                    ],
                    "number_of_project": "",
                },
            )
            ranking += 1
            try:
                worker_dict.metadata[
                    "rating"
                ] = self.browser.find_element_by_class_name(
                    "total-rating"
                ).text
            except NoSuchElementException:
                worker_dict.metadata["rating"] = None
            list_workers.append(worker_dict)

        self.browser.close()
        return list_workers
        # Query finished close the self.browser
