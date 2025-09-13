import uuid
from datetime import datetime
from controllers.date import Date

class Calendar:
    def __init__(self):
        self.filename = "./result/demo.ics"

    def get(self, schedule):
        result = []
        body = schedule['body']
        dates = schedule['dates']

        for key in body:
            for innerKey in body[key]:
                item = body[key][innerKey]
                start_formatted = Date.get_start_and_end_time(dates[innerKey], item['l_start'])
                end_formatted = Date.get_start_and_end_time(dates[innerKey], item['l_end'])
                uid = f"evt-{uuid.uuid4()}"

                result.append(f"""
BEGIN:VEVENT
SUMMARY:{item['name_spec']}
DESCRIPTION:Группа - {item['groups']}, Кабинет - {item['num_rooms']}
DTSTART:{start_formatted}
DTEND:{end_formatted}
UID:{uid}
SEQUENCE:0
STATUS:CONFIRMED
BEGIN:VALARM
TRIGGER:-PT5M
DESCRIPTION:Напоминание о событии
ACTION:DISPLAY
END:VALARM
BEGIN:VALARM
TRIGGER:-PT5M
RELATED=END
DESCRIPTION:Напоминание о завершении события
ACTION:DISPLAY
END:VALARM
END:VEVENT
""")

        return f"""
BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
{''.join(result)}
END:VCALENDAR
"""