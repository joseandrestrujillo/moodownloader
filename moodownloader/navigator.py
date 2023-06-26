from bs4 import BeautifulSoup, ResultSet

class MoodleNavigator:
    def __init__(self, browser) -> None:
        self.browser = browser

    def get_course_links(self) -> ResultSet[any]:
        soup = BeautifulSoup(self.browser.response.content, 'html.parser')
        course_links = soup.find_all('div', {'class': 'coursebox'})
        return course_links

    def navigate_to_course(self, course_link) -> None:
        self.browser.follow_link(course_link)
    