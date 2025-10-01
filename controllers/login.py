import os
import requests

class Login:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.session = requests.Session()

    def login(self):
        # Инициализация сессии (для получения CSRF)
        self.session.get(self.base_url)
        cookies = self.session.cookies.get_dict()

        csrf_token = cookies.get('_csrf')
        if not csrf_token:
            return None, {"error": "CSRF token not found"}, 400

        # Логин
        login_response = self.session.post(
            self.base_url + "/auth/login",
            json={
                "LoginForm": {
                    "id_city": None,
                    "password": self.password,
                    "username": self.username,
                }
            },
            headers={
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=UTF-8",
                "X-CSRF-Token": csrf_token,
                "X-Requested-With": "XMLHttpRequest"
            }
        )

        if login_response.status_code != 200:
            return None, {
                "error": "Login failed",
                "details": login_response.text
            }, login_response.status_code

        # Получаем PHPSESSID
        session_cookies = self.session.cookies.get_dict()
        token = session_cookies.get('PHPSESSID')

        if not token:
            return None, {"error": "Session token not found"}, 400

        return token, None, 200
