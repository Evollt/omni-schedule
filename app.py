from datetime import datetime
from flask import Flask, request, url_for, send_file
from pathlib import Path
import os
from controllers.calendar import Calendar
from controllers.login import Login
from controllers.report import Report
from controllers.document import Document
from num2words import num2words
import locale

app = Flask(__name__)

url = os.getenv("BASE_URL")
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

@app.route("/getcal")
def getcal():
    login_ctrl = Login()
    token, error, status = login_ctrl.login()

    if not token:
        return error, status

    # После успешного логина используем login_ctrl.session
    schedule_response = login_ctrl.session.post(
        url + "/schedule/get-schedule",
        json={"week": 0},
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8"
        },
        cookies={"PHPSESSID": token}
    )

    if schedule_response.status_code != 200:
        return {
            "error": "Schedule request failed",
            "details": schedule_response.text
        }, schedule_response.status_code

    calendar = Calendar()
    return calendar.get(schedule_response.json())


@app.route("/getreport")
def getreport():
    response = Report.get_report()

    return response.json()

@app.route("/generate-act")
def generate_act():
    response = Report.get_report().json();
    end_date = datetime.fromisoformat(response['end'])
    start_date = datetime.fromisoformat(response['start'])
    price = response['total_pairs'] * 1500
    price_text = num2words(price, lang="ru")
    products = []

    for index, (name, info) in enumerate(response['spec_reports'].items()):
        product_hours = info['count_lenta']  # или duration/часа, уточни что считать

        products.append({
            "product_index": index + 1,
            "product": name,
            "product_hours": product_hours
        })

    context = {
        "end_date": end_date.day,
        "start_date": start_date.day,
        "month": end_date.strftime("%B").lower(),
        "year": end_date.year,
        "academy_hours": response['total_hours'],
        "products": products,
        "full_hours": f"{response['total_pairs']} ",
        "price": response['total_pairs'] * 1500,
        "price_text": price_text + " рублей"
    }
    month = request.args.get("month", default=datetime.now().month, type=int)

    doc = Document()
    save_path = doc.create_act(context, month)

    download_url = f"{os.getenv('APP_URL')}/download/{save_path.name}"


    return {
        "success": True,
        "url": download_url
    }

@app.route("/download/<filename>")
def download_file(filename):
    file_path = Path(f"./acts/{filename}")
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    return {"error": "File not found"}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
