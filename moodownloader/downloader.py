class PdfDownloader:
    def __init__(self, browser, course_dir: str) -> None:
        self.browser = browser
        self.course_dir = course_dir