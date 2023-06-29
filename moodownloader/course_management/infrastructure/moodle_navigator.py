from bs4 import BeautifulSoup
from typing import List

from .dom_element import DomElement


class MoodleNavigator:
    def __init__(self, browser) -> None:
        self.browser = browser

    def get_course_links(self) -> List["DomElement"]:
        dom_element = DomElement(BeautifulSoup(self.browser.response.content, 'html.parser'))
        course_links = dom_element.find_all('div', {'class': 'coursebox'})
        return course_links

    def navigate_to_course(self, course_link) -> None:
        self.browser.follow_link(course_link.soup)
    