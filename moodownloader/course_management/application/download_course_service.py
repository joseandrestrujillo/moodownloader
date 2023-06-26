from ..domain.navigator import Navigator
from ..domain.downloader import Downloader
from ..domain.course import Course


class DownloadCourseService:
    def __init__(self, navigator: Navigator, downloader: Downloader) -> None:
        self.navigator = navigator
        self.downloader = downloader
    
    def download_all_course_pdfs(self) -> None:
        course_links = self.navigator.get_course_links()
        for course_link in course_links:
            course = Course(course_link.text.strip(), course_link['href'])
            self.navigator.navigate_to_course(course_link)
            self.downloader.download_all_pdfs(course.name)