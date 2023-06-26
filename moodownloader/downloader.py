from bs4 import BeautifulSoup
import os.path

class PdfDownloader:
    def __init__(self, browser, course_dir: str) -> None:
        self.browser = browser
        self.course_dir = course_dir

    def download_pdf_from_link(self, pdf_link):
        # Descarga el archivo PDF y lo guarda en la carpeta del curso
        pdf_url = pdf_link['href']
        img_tags = pdf_link.find_all('img', {'src': True})
        for img_tag in img_tags:
            if 'pdf' in img_tag['src']:
                pdf_name = pdf_link.find("span", {"class": "instancename"}).text.strip()
                file_name = pdf_name.replace(" ", "_").replace("/", "").replace(".", "").replace("-", "_") + ".pdf"
                response = self.browser.session.get(pdf_url, stream=True)
                # La respuesta directamente es un pdf -> Lo descarga
                if response.headers.get('content-type') == 'application/pdf':
                    with open(os.path.join(self.course_dir, file_name), "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)
                    print(f"Archivo {file_name} guardado en la carpeta {self.course_dir}.")
                else:
                # La respuesta es una pagina que te lleva al pdf -> busca el link del pdf en la pagina y lo descarga
                    soup = BeautifulSoup(response.content, 'html.parser')
                    resource_tag = soup.find('div', {"class": "resourceworkaround"})
                    if resource_tag is not None:
                        pdf_a_tag = resource_tag.find('a', {'href': lambda x: x.endswith('.pdf')})
                        if pdf_a_tag is not None:
                            pdf_url = pdf_a_tag['href']
                            response = self.browser.session.get(pdf_url, stream=True)
                            with open(os.path.join(self.course_dir, file_name), "wb") as f:
                                for chunk in response.iter_content(chunk_size=1024):
                                    f.write(chunk)
                            print(f"Archivo {file_name} guardado en la carpeta {self.course_dir}.")
                        else:
                            print(f"No se pudo encontrar el enlace para el archivo PDF en {pdf_url}")
                    else:
                        print(f"No se pudo encontrar el enlace para el archivo PDF en {pdf_url}")                   


    def download_all_pdfs(self):
        pdf_links = self.browser.find_all('a', {'href': True})
        for pdf_link in pdf_links:
            self.download_pdf_from_link(pdf_link)