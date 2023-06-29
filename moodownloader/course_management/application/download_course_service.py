from ..domain.navigator import Navigator
from ..domain.downloader import Downloader
from ..domain.course import Course
import os.path


class DownloadCourseService:
    def __init__(self, navigator: Navigator, downloader: Downloader) -> None:
        self.navigator = navigator
        self.downloader = downloader
    
    def download_all_course_pdfs(self) -> None:
        course_links = self.navigator.get_course_links()

        for link in course_links:
            course_name = link.find('h3', {'class': 'coursename'})
            if course_name is not None:
                course_dir = course_name.text.strip()
                if not os.path.exists(course_dir):
                    os.makedirs(course_dir)

                course_link = link.find('a', {'class': 'aalink'})
                if course_link is not None:
                    self.navigator.navigate_to_course(course_link)
                    self.downloader.course_dir = course_dir
                    self.downloader.download_all_pdfs()
                else:
                    print(f"No se pudo encontrar el enlace para el curso {course_dir}")
