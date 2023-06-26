from robobrowser import RoboBrowser
import getpass
import os.path

from authenticator import MoodleAuthenticator
from navigator import MoodleNavigator
from downloader import PdfDownloader

def main():
    # User input
    url = input("Introduzca la url del moodle que quieres descargar: ")
    username = input("Introduzca el nombre de usuario de moodle: ")
    password = getpass.getpass('Introduzca la contrasena de moodle: ') 


    url = "https://" + url

    browser = RoboBrowser(parser='html.parser')
    
    authenticator = MoodleAuthenticator(url, username, password, browser)
    if not authenticator.authenticate():
        return
    

    navigator = MoodleNavigator(authenticator.browser)
    course_links = navigator.get_course_links()

    for link in course_links:
        course_name = link.find('h3', {'class': 'coursename'})
        if course_name is not None:
            course_dir = course_name.text.strip()
            if not os.path.exists(course_dir):
                os.makedirs(course_dir)

            course_link = link.find('a', {'class': 'aalink'})
            if course_link is not None:
                navigator.navigate_to_course(course_link)

                downloader = PdfDownloader(navigator.browser, course_dir)
                downloader.download_all_pdfs()

            else:
                print(f"No se pudo encontrar el enlace para el curso {course_dir}")

    print("Descarga completada.")   


if __name__ == '__main__':
    main()