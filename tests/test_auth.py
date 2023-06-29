import unittest
from unittest.mock import Mock, MagicMock, PropertyMock
from moodownloader.authentication.infrastructure.moodle_authenticator import MoodleAuthenticator

class MoodleAuthenticatorTests(unittest.TestCase):

    def test_successful_authentication(self):
        browser = Mock()
        form = MagicMock()
        type(form).__getitem__ = PropertyMock(side_effect=lambda : Mock())
        type(form).__setitem__ = PropertyMock(side_effect=lambda : Mock())
        browser.get_form.return_value = form
        browser.submit_form.return_value = None

        authenticator = MoodleAuthenticator("https://moodle.example.com/", "username", "password", browser)
        result = authenticator.authenticate()

        self.assertTrue(result)
        browser.open.assert_called_with("https://moodle.example.com/login/index.php")
        browser.submit_form.assert_called_once_with(form)

    def test_failed_authentication(self):
        browser = Mock()
        browser.get_form.return_value = None

        authenticator = MoodleAuthenticator("https://moodle.example.com/", "username", "wrong_password", browser)
        result = authenticator.authenticate()

        self.assertFalse(result)
        browser.open.assert_called_with("https://moodle.example.com/login/index.php")
        browser.get_form.assert_called_once()

    def test_missing_login_form(self):
        browser = Mock()
        browser.get_form.return_value = None

        authenticator = MoodleAuthenticator("https://moodle.example.com/", "username", "password", browser)
        result = authenticator.authenticate()

        self.assertFalse(result)
        browser.open.assert_called_with("https://moodle.example.com/login/index.php")
        browser.get_form.assert_called_once()

    def test_incorrect_website_url(self):
        browser = Mock()
        browser.get_form.return_value = None

        authenticator = MoodleAuthenticator("https://moodle.example.net/", "username", "password", browser)
        result = authenticator.authenticate()

        self.assertFalse(result)
        browser.open.assert_called_with("https://moodle.example.net/login/index.php")
        browser.get_form.assert_called_once()


if __name__ == '__main__':
    unittest.main()