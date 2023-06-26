class MoodleAuthenticator:
    def __init__(self, url: str, username: str, password: str, browser) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.browser = browser
    
    def authenticate(self) -> bool:
        url_login = self.url + "login/index.php"
        self.browser.open(url_login)

        form = self.browser.get_form()
        if form is not None:
            form['username'].value = self.username
            form['password'].value = self.password
            self.browser.submit_form(form)
        else:
            print('No se pudo encontrar el formulario de inicio de sesión.')
            return False

        return True