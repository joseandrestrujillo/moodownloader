from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import getpass
import os.path
import http.cookiejar
import requests

def main():
    url = input("Introduzca la url del moodle que quieres descargar: ")
    url = "https://" + url
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
    else:
        print('No se pudo encontrar el formulario de inicio de sesión.')
        return
        
    browser.open(url)
    soup = BeautifulSoup(browser.response.content, 'html.parser')
    course_links = soup.find_all('div', {'class': 'coursebox'})

    for link in course_links:
        course_name = link.find('h3', {'class': 'coursename'})
        if course_name is not None:
            # Obtiene el nombre del curso
            course_dir = course_name.text.strip()
            # Crea una carpeta con el nombre del curso si no existe
            if not os.path.exists(course_dir):
                os.makedirs(course_dir)
            # Entra en el curso si encuentra el link
            course_link = link.find('a', {'class': 'aalink'})
            if course_link is not None:  # Verificar si el link fue encontrado
                browser.follow_link(course_link)
                # Busca todos los enlaces que contengan la cadena "pdf" en el atributo src de la etiqueta img
                pdf_links = browser.find_all('a', {'href': True})
                for pdf_link in pdf_links:
                    # Descarga el archivo PDF y lo guarda en la carpeta del curso
                    pdf_url = pdf_link['href']
                    img_tags = pdf_link.find_all('img', {'src': True})
                    for img_tag in img_tags:
                        if 'pdf' in img_tag['src']:
                            pdf_name = pdf_link.find("span", {"class": "instancename"}).text.strip()
                            file_name = pdf_name.replace(" ", "_").replace("/", "").replace(".", "").replace("-", "_") + ".pdf"
                            # Descargar el archivo al que te redirije pdf_url y guardarlo en la carpeta del curso con el nombre file_name 
                            # Solo modificar aqui dentro !!!
                            browser.follow_link(pdf_link)
                            try:
                                # Si el PDF se abre en una ventana emergente, cambia al controlador de ventana
                                browser.switch_to.window(browser.windows[-1])
                                response = browser.session.get(browser.url, stream=True)                            
                                with open(os.path.join(course_dir, file_name), "wb") as f:
                                    for chunk in response.iter_content(chunk_size=1024):
                                        f.write(chunk)
                                print(f"Archivo {file_name} guardado en la carpeta {course_dir}.")
                            except:
                                # Si el PDF se descarga directamente, descárgalo y guárdalo como antes
                                response = browser.session.get(pdf_url, stream=True)
                                with open(os.path.join(course_dir, file_name), "wb") as f:
                                    for chunk in response.iter_content(chunk_size=1024):
                                        f.write(chunk)
                                print(f"Archivo {file_name} guardado en la carpeta {course_dir}.")

            else:
                print(f"No se pudo encontrar el enlace para el curso {course_dir}")

    print("Descarga completada.")


if __name__ == '__main__':
    main()