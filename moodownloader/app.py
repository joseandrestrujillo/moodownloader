from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import getpass
import os.path

from authenticator import MoodleAuthenticator

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
                            response = browser.session.get(pdf_url, stream=True)
                            # La respuesta directamente es un pdf -> Lo descarga
                            if response.headers.get('content-type') == 'application/pdf':
                                with open(os.path.join(course_dir, file_name), "wb") as f:
                                    for chunk in response.iter_content(chunk_size=1024):
                                        f.write(chunk)
                                print(f"Archivo {file_name} guardado en la carpeta {course_dir}.")
                            else:
                            # La respuesta es una pagina que te lleva al pdf -> busca el link del pdf en la pagina y lo descarga
                                soup = BeautifulSoup(response.content, 'html.parser')
                                resource_tag = soup.find('div', {"class": "resourceworkaround"})
                                if resource_tag is not None:
                                    pdf_a_tag = resource_tag.find('a', {'href': lambda x: x.endswith('.pdf')})
                                    if pdf_a_tag is not None:
                                        pdf_url = pdf_a_tag['href']
                                        response = browser.session.get(pdf_url, stream=True)
                                        with open(os.path.join(course_dir, file_name), "wb") as f:
                                            for chunk in response.iter_content(chunk_size=1024):
                                                f.write(chunk)
                                        print(f"Archivo {file_name} guardado en la carpeta {course_dir}.")
                                    else:
                                        print(f"No se pudo encontrar el enlace para el archivo PDF en {pdf_url}")
                                else:
                                    print(f"No se pudo encontrar el enlace para el archivo PDF en {pdf_url}")                   

            else:
                print(f"No se pudo encontrar el enlace para el curso {course_dir}")

    print("Descarga completada.")


if __name__ == '__main__':
    main()