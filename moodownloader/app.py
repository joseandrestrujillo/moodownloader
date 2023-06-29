from robobrowser import RoboBrowser
import getpass
import os.path


from authentication.infrastructure.moodle_authenticator import MoodleAuthenticator
from authentication.application.authentication_service import AuthenticationService
from course_management.application.download_course_service import DownloadCourseService
from course_management.infrastructure.moodle_navigator import MoodleNavigator
from course_management.infrastructure.pdf_downloader import PdfDownloader

def main():
    url = input("Introduzca la url del moodle que quieres descargar: ")
    username = input("Introduzca el nombre de usuario de moodle: ")
    password = getpass.getpass('Introduzca la contrasena de moodle: ') 

    url = "https://" + url
    browser = RoboBrowser(parser='html.parser')
       
    authenticator = MoodleAuthenticator(url, username, password, browser)
    if not AuthenticationService(authenticator).authenticate_user():
        return
    
    navigator = MoodleNavigator(authenticator.browser)
    downloader = PdfDownloader(navigator.browser)
    DownloadCourseService(navigator, downloader).download_all_course_pdfs()
    
    print("Descarga completada.")   


if __name__ == '__main__':
    main()