import re
import time
from selenium.common.exceptions import NoSuchElementException
from slugify import slugify

from src.crawler import RankingItem, OJMCrawler


class TaskrabbitCrawler(OJMCrawler):
    def __hide_cookies_banner(self, element):
        if element.is_displayed():
            element.click()
        else:
            print("cookie banner hidden")

    # TODO: USE self.browser INSTEAD OF PASSING browser AS A PARAMETER
    def __assembly(self, boxes, browser):
        if len(boxes) == 5:
            print("found 5 boxes")
            assembly = browser.find_elements_by_css_selector(
                ".build-input-list li:last-of-type > input[type='radio']"
            )
            for element in assembly:
                element.click()
            browser.find_element_by_css_selector(".btn.btn-primary").click()
        time.sleep(3)

    def __task_option(self, elements, browser):
        for element in elements:
            element.click()
        self.browser.find_element_by_css_selector(".btn.btn-primary").click()
        time.sleep(1)

    def __reviews_retiever(self, browser, worker_dict, next_page):
        while True:
            # Retrieve reviews
            reviews = self.browser.find_elements_by_css_selector(
                ".tasker-review"
            )
            if len(reviews) > 0:
                for review in reviews:
                    worker_dict.metadata["reviews"].append(
                        {
                            "text": review.find_element_by_css_selector(
                                ".exterior__bottom--sm"
                            ).text,
                            "date": review.find_element_by_css_selector(
                                ".review-author"
                            ).text.split(",", 1)[1],
                        }
                    )
            if len(next_page) > 0:
                next_page[0].click()
                next_page = self.browser.find_elements_by_xpath(
                    "//span[@class='current']/following-sibling::a"
                )
                time.sleep(0.5)
            if len(next_page) == 0:
                break

    def __promotion_remover(self):
        try:
            self.browser.execute_script(
                "var elem = document.querySelector('.tr-promo-container');elem.parentNode.removeChild(elem);"
            )
            print("Promotion banner removed")
        except Exception:
            print("No promotion banner")

    def crawl(self):
        query = self.query

        # Load webpage
        self.browser.get(query.url)
        self.browser.implicitly_wait(1)

        # dismiss cookie if it is displayed
        element = self.browser.find_element_by_css_selector(
            ".js__cookie-banner-dismiss"
        )
        self.__hide_cookies_banner(element)
        time.sleep(2)
        self.__promotion_remover()

        # TASK INTEREST
        # Task interest selected (i'm just browsing)
        self.browser.find_element_by_id("intent_level_low").click()

        self.browser.find_element_by_css_selector(".btn.btn-primary").click()

        # TASK LOCATION / START ADDRESS
        # Location selected from the query
        self.browser.find_element_by_css_selector(
            "input[name='location.freeform']"
        ).send_keys(query.city)
        # Unit or Apt optional, we selected number 5
        self.browser.find_element_by_id("address2").send_keys("5")
        time.sleep(1)
        self.browser.find_element_by_css_selector(".btn.btn-primary").click()
        time.sleep(1)

        # TASK END ADDRESS (HELP MOVING CASE)
        # Condition for the case where we have 5 boxes (assembly task)
        boxes = self.browser.find_elements_by_css_selector(".build-group")
        self.__assembly(boxes, self.browser)

        # TASK OPTIONS
        # Loop to select the first option in each elements of the task options
        elements = self.browser.find_elements_by_css_selector(
            ".build-input-list li:first-of-type > input[type='radio']"
        )
        self.__task_option(elements, self.browser)

        # TASK DETAILS
        # we fill the task details with one letter in order to be able to select
        # the primary button
        self.browser.find_element_by_css_selector(
            "textarea[name='description']"
        ).send_keys("t")
        time.sleep(1)

        self.browser.find_element_by_css_selector(".btn.btn-primary").click()
        time.sleep(1)

        # WORKERS LIST
        # Task date selected to within a week
        # self.browser.execute_script("var elem = document.querySelector('.tr-promo-container');elem.parentNode.removeChild(elem);")
        self.browser.find_element_by_id(
            "recommendations__schedule-option-next_week"
        ).click()

        # sleep time in order to load the whole page correctly
        time.sleep(3)

        workers = self.browser.find_elements_by_css_selector(
            ".recommendations__result_wrapper"
        )

        # Loop to build the list of workers
        list_workers = []
        iteration_number = 1
        for worker in workers:
            # worker build
            worker_dict = RankingItem(
                worker.find_element_by_css_selector(
                    ".recommendations__result.recommendations__result--tasker"
                ).get_attribute("data-user-id"),
                worker.find_element_by_css_selector(
                    ".recommendations__avatar__circular"
                ).get_attribute("src"),
                iteration_number,
                {
                    "positive_rating": worker.find_elements_by_xpath(
                        "//i[@class='ss-lnr-star']/following-sibling::span"
                    )[iteration_number - 1].text,
                    "number_of_relevant_tasks": worker.find_elements_by_xpath(
                        "//i[@class='ss-lnr-check-circle']/following-sibling::span"
                    )[iteration_number - 1].text,
                    "great_value_badge": "",
                    "elite_tasker": "",
                    "new_tasker": "",
                    "how_can_help": worker.find_element_by_css_selector(
                        ".recommendations__blurb"
                    ).text,
                    "right_person": "",
                    "when_tasking": "",
                    "number_of_reviews_received": "",
                    "number_of_relevant_reviews_received": "",
                    # Return the string of per_hour_rate
                    "per_hour_rate": float(
                        re.findall(
                            r"[-+]?\d*\.\d+|\d+",
                            worker.find_element_by_css_selector("strong").text,
                        )[0]
                    ),
                    # City and the task separated by '_'
                    "query": slugify(query.city + "_" + query.title),
                    "reviews": [],
                },
            )
            # positive rating
            try:
                # Return the float of the percentage of Positve rating
                worker_dict.metadata["positive_rating"] = float(
                    int(
                        re.findall(
                            r"[-+]?\d*\.\d+|\d+",
                            worker_dict.metadata["positive_rating"],
                        )[0]
                    )
                    / 100
                )
            except IndexError:
                # Case of positive rating not found
                worker_dict.metadata["positive_rating"] = None

            # number of relevant tasks

            try:
                # Return the number of relevant tasks
                worker_dict.metadata["number_of_relevant_tasks"] = int(
                    re.findall(
                        r"[-+]?\d*\.\d+|\d+",
                        worker_dict.metadata["number_of_relevant_tasks"],
                    )[0]
                )
            except IndexError:
                # Case of relevant tasks not found
                worker_dict.metadata["number_of_relevant_tasks"] = None

            # worker has great value badge?
            try:
                # Boolean for value_badge
                worker.find_element_by_css_selector(
                    ".recommendations__great-value-badge"
                )
                worker_dict.metadata["great_value_badge"] = True
            except NoSuchElementException:
                # Case of value_badge not found
                worker_dict.metadata["great_value_badge"] = False

            # worker is an elite tasker?
            try:
                # Boolean for elite_tasker
                worker.find_element_by_css_selector(".ss-medal-star")
                worker_dict.metadata["elite_tasker"] = True
            except NoSuchElementException:
                # Case of elite_tasker not found
                worker_dict.metadata["elite_tasker"] = False

            # worker is a new tasker?
            try:
                # Boolean for new_tasker
                worker.find_element_by_css_selector(".ss-happy-lined")
                worker_dict.metadata["new_tasker"] = True
            except NoSuchElementException:
                # Case of new_tasker not found (ss-happy-lined)
                worker_dict.metadata["new_tasker"] = False

            # open user popup (Profile & reviews)
            worker.find_element_by_css_selector(
                ".recommendations__result-name"
            ).click()
            # retrieve the first free text
            try:
                worker_dict.metadata[
                    "right_person"
                ] = self.browser.find_elements_by_css_selector(
                    ".tasker--bio-responses"
                )[
                    0
                ].text
            except Exception:
                print("no right person")

            # retrieve the second free text
            try:
                worker_dict.metadata[
                    "when_tasking"
                ] = self.browser.find_elements_by_css_selector(
                    ".tasker--bio-responses"
                )[
                    1
                ].text
            except Exception:
                print("no when tasking")
            # retrieve number of reviews
            reviews_dropdown = self.browser.find_elements_by_css_selector(
                ".reviews__filter--select option"
            )
            if len(reviews_dropdown) > 0:
                worker_dict.metadata["number_of_reviews_received"] = int(
                    re.findall(
                        r"[-+]?\d*\.\d+|\d+", reviews_dropdown[-1].text
                    )[0]
                )
                worker_dict.metadata[
                    "number_of_relevant_reviews_received"
                ] = int(
                    re.findall(r"[-+]?\d*\.\d+|\d+", reviews_dropdown[0].text)[
                        0
                    ]
                )

                # select all reviews
                reviews_dropdown[-1].click()
            else:
                # If worker have no review
                worker_dict.metadata["number_of_reviews_received"] = 0
                worker_dict.metadata["number_of_relevant_reviews_received"] = 0
            # while clicking on right arrow is permissible, retrieve the next page
            # of reviews
            next_page = self.browser.find_elements_by_xpath(
                "//span[@class='current']/following-sibling::a"
            )
            self.__reviews_retiever(self.browser, worker_dict, next_page)

            # close popup of the worker profile & reviews
            self.browser.find_element_by_css_selector(
                ".lightbox--dismiss"
            ).click()

            # Add the worker to the list of workers
            list_workers.append(worker_dict)
            # Save users pictures
            iteration_number += 1

            time.sleep(0.5)
        # Query finished close the self.browser
        self.browser.close()
        return list_workers
