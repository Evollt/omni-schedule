from datetime import datetime
import os
from controllers.login import Login
from flask import request

class Report:
    def get_report():
        login_ctrl = Login()
        token, error, status = login_ctrl.login()
        year = datetime.now().year
        month = request.args.get("month", default=datetime.now().month, type=int)


        if not token:
            return error, status

        # После успешного логина используем login_ctrl.session
        response = login_ctrl.session.post(
            os.getenv("BASE_URL") + "/report/get-report",
            json={
                "month": month,
                "year": year
            },
            headers={
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=UTF-8"
            },
            cookies={"PHPSESSID": token}
        )

        if response.status_code != 200:
            return {
                "error": "Schedule request failed",
                "details": response.text
            }, response.status_code

        return response