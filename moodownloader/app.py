from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import getpass
import os.path

def main():
    url = input("Introduzca la url del moodle que quieres descargar: ")
    url = "https://" + url

    if os.path.isfile('cookies.txt'):
        browser = RoboBrowser(parser='html.parser')
        browser.session.cookies.load('cookies.txt', ignore_discard=True)
    else:
        url_login = url + "login/index.php"    

        browser = RoboBrowser(parser='html.parser')
        browser.open(url_login)

        form = browser.get_form()
        if form is not None:
            username = input("Introduzca el nombre de usuario de moodle: ")
            password = getpass.getpass('Introduzca la contrasena de moodle: ') 
            form['username'].value = username
            form['password'].value = password
            browser.submit_form(form)
            browser.session.cookies.save(ignore_discard=True)
        else:
            print('No se pudo encontrar el formulario de inicio de sesión.')
            return
        
    browser.open(url)
    soup = BeautifulSoup(browser.response.content, 'html.parser')
    course_links = soup.find_all('div', {'class': 'coursebox'})

    for link in course_links:
        course_name = link.find('h3', {'class': 'coursename'})
        if course_name is not None:
            print(course_name.text)



if __name__ == '__main__':
    main()