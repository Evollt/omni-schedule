from flask import Flask
import requests
import os
from controllers.calendar import Calendar

app = Flask(__name__)

@app.route("/getcal")
def getcal():
    url = os.getenv("BASE_URL")

    session = requests.Session()
    session.get(url)
    cookies = session.cookies.get_dict()

    csrf_token = cookies.get('_csrf')
    if not csrf_token:
        return {"error": "CSRF token not found"}, 400

    login_response = session.post(
        url + "/auth/login",
        json={  # Используем json вместо data
            "LoginForm": {
                "id_city": None,
                "password": os.getenv("PASSWORD"),
                "username": os.getenv("USERNAME"),
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
        return {"error": "Login failed", "details": login_response.text}, login_response.status_code

    session_cookies = session.cookies.get_dict()
    token = session_cookies.get('PHPSESSID')

    if not token:
        return {"error": "Session token not found"}, 400

    schedule_response = session.post(
        url + "/schedule/get-schedule",
        json={"week": 0},
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8"
        },
        cookies={"PHPSESSID": token}
    )

    if schedule_response.status_code != 200:
        return {"error": "Schedule request failed", "details": schedule_response.text}, schedule_response.status_code

    calendar = Calendar()
    return calendar.get(schedule_response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
