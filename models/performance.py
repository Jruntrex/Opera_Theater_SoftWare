from datetime import datetime
import json
import os

# Словник для співставлення українських назв місяців
MONTHS_UA = {
    "СІЧНЯ": "01", "ЛЮТОГО": "02", "БЕРЕЗНЯ": "03", "КВІТНЯ": "04",
    "ТРАВНЯ": "05", "ЧЕРВНЯ": "06", "ЛИПНЯ": "07", "СЕРПНЯ": "08",
    "ВЕРЕСНЯ": "09", "ЖОВТНЯ": "10", "ЛИСТОПАДА": "11", "ГРУДНЯ": "12"
}

# Словник для співставлення англійських назв місяців
MONTHS_EN = {
    "JANUARY": "01", "FEBRUARY": "02", "MARCH": "03", "APRIL": "04",
    "MAY": "05", "JUNE": "06", "JULY": "07", "AUGUST": "08",
    "SEPTEMBER": "09", "OCTOBER": "10", "NOVEMBER": "11", "DECEMBER": "12"
}

# Словник для співставлення днів тижня (українська -> англійська)
DAYS_UA_TO_EN = {
    "ПН": "MON", "ВТ": "TUE", "СР": "WED", "ЧТ": "THU", "ПТ": "FRI",
    "СБ": "SAT", "НД": "SUN"
}

# Словник для співставлення англійських днів тижня
DAYS_EN = {
    "MON": "ПН", "TUE": "ВТ", "WED": "СР", "THU": "ЧТ", "FRI": "ПТ",
    "SAT": "СБ", "SUN": "НД"
}


class Performance:
    def __init__(self, title: str, date: str, time: str, description: str, ticket_price: float, author: str,
                 image: str = "") -> None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Назва має бути непорожнім рядком.")
        try:
            self.date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Некоректний формат дати. Використовуйте РРРР-ММ-ДД.")
        try:
            self.time = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            raise ValueError("Некоректний формат часу. Використовуйте ГГ:ХХ.")
        if not isinstance(description, str):
            raise ValueError("Опис має бути рядком.")
        if not isinstance(ticket_price, (int, float)) or ticket_price < 0:
            raise ValueError("Вартість квитка має бути невід'ємним числом.")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Автор має бути непорожнім рядком.")
        if not isinstance(image, str):
            raise ValueError("Зображення має бути рядком.")

        self.title = title
        self.description = description
        self.ticket_price = float(ticket_price)
        self.author = author
        self.image = image

    def __str__(self) -> str:
        return f"{self.title} ({self.date}, {self.time})"

    def get_info(self):
        day = self.date.strftime("%d")
        month = self.date.strftime("%B").upper()
        for ua_month, num in MONTHS_UA.items():
            if num == self.date.strftime("%m"):
                month = ua_month
                break
        day_of_week = self.date.strftime("%a").upper()
        for ua_day, en_day in DAYS_UA_TO_EN.items():
            if en_day == day_of_week:
                day_of_week = ua_day
                break
        return {
            "title": self.title,
            "date": f"{day} {month} {day_of_week}",
            "time": f"{self.date.strftime('%m.%d')}, {self.time.strftime('%H:%M')}",
            "description": self.description,
            "price": self.ticket_price,
            "author": self.author,
            "image": self.image
        }

    @classmethod
    def from_json_dict(cls, data) -> 'Performance':
        try:
            date_str = data["date"]
            date_parts = date_str.split()
            day, month, day_of_week = date_parts[0], date_parts[1], date_parts[2]
            month_num = MONTHS_UA.get(month.upper()) or MONTHS_EN.get(month.upper())
            if not month_num:
                raise ValueError(f"Невідома назва місяця: {month}")
            date_obj = datetime.strptime(f"2025-{month_num}-{day}", "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Некоректний формат дати у полі 'date'. Використовуйте 'ДД ММММ ДД'.")

        try:
            time_part = data["time"].split(", ")[1]
        except Exception:
            raise ValueError("Некоректний формат часу у полі 'time'.")

        return cls(
            title=data["title"],
            date=date_obj.isoformat(),
            time=time_part,
            description=data["description"],
            ticket_price=data.get("price", 0.0),
            author=data["author"],
            image=data.get("image", "")
        )

    @classmethod
    def add_performance(cls, title: str, date: str, time: str, description: str, ticket_price: float, author: str,
                        image: str, category: str, file_path: str = None) -> None:
        if category not in ["opera", "concert", "ballet"]:
            raise ValueError("Категорія має бути 'opera', 'concert' або 'ballet'.")

        file_path = file_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui",
                                              "data_performance.json")

        if cls.find_performance(title, date, time, category, file_path):
            raise ValueError(f"Вистава '{title}' на {date} {time} у категорії '{category}' уже існує.")

        performance = cls(title, date, time, description, ticket_price, author, image)
        file_path = os.path.abspath(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"opera": [], "concert": [], "ballet": []}
        except Exception as e:
            raise ValueError(f"Помилка при читанні файлу JSON: {e}")

        data[category].append(performance.get_info())

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ValueError(f"Помилка при записі у файл JSON: {e}")

    @classmethod
    def delete_performance(cls, title: str, date: str, time: str, category: str, file_path: str = None) -> None:
        if category not in ["opera", "concert", "ballet"]:
            raise ValueError("Категорія має бути 'opera', 'concert' або 'ballet'.")

        file_path = file_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui",
                                              "data_performance.json")
        file_path = os.path.abspath(file_path)
        try:
            if not os.path.exists(file_path):
                raise ValueError("Файл JSON не існує.")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise ValueError(f"Помилка при читанні файлу JSON: {e}")

        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            time_obj = datetime.strptime(time, "%H:%M").time()
            day = date_obj.strftime("%d")
            month = date_obj.strftime("%B").upper()
            for ua_month, num in MONTHS_UA.items():
                if num == date_obj.strftime("%m"):
                    month = ua_month
                    break
            day_of_week = date_obj.strftime("%a").upper()
            for ua_day, en_day in DAYS_UA_TO_EN.items():
                if en_day == day_of_week:
                    day_of_week = ua_day
                    break
            json_date = f"{day} {month} {day_of_week}"
            json_time = f"{date_obj.strftime('%m.%d')}, {time_obj.strftime('%H:%M')}"
        except ValueError:
            raise ValueError("Некоректний формат дати або часу.")

        updated_performances = []
        found = False
        for perf in data.get(category, []):
            if perf["title"] == title and perf["date"] == json_date and perf["time"] == json_time:
                found = True
                continue
            updated_performances.append(perf)

        if not found:
            raise ValueError(f"Виставу '{title}' на {date} {time} у категорії '{category}' не знайдено.")

        data[category] = updated_performances

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ValueError(f"Помилка при записі у файл JSON: {e}")

    @classmethod
    def edit_performance(cls, old_title: str, old_date: str, old_time: str, category: str, new_title: str,
                         new_date: str, new_time: str, new_description: str, new_ticket_price: float, new_author: str,
                         new_image: str, file_path: str = None) -> None:
        if category not in ["opera", "concert", "ballet"]:
            raise ValueError("Категорія має бути 'opera', 'concert' або 'ballet'.")

        file_path = file_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui",
                                              "data_performance.json")
        cls.delete_performance(old_title, old_date, old_time, category, file_path)
        cls.add_performance(new_title, new_date, new_time, new_description, new_ticket_price, new_author, new_image,
                            category, file_path)

    @classmethod
    def find_performance(cls, title: str, date: str, time: str, category: str, file_path: str = None) -> dict:
        if category not in ["opera", "concert", "ballet"]:
            raise ValueError("Категорія має бути 'opera', 'concert' або 'ballet'.")

        file_path = file_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui",
                                              "data_performance.json")
        file_path = os.path.abspath(file_path)
        try:
            if not os.path.exists(file_path):
                return None
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return None

        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            time_obj = datetime.strptime(time, "%H:%M").time()
            day = date_obj.strftime("%d")
            month = date_obj.strftime("%B").upper()
            for ua_month, num in MONTHS_UA.items():
                if num == date_obj.strftime("%m"):
                    month = ua_month
                    break
            day_of_week = date_obj.strftime("%a").upper()
            for ua_day, en_day in DAYS_UA_TO_EN.items():
                if en_day == day_of_week:
                    day_of_week = ua_day
                    break
            json_date = f"{day} {month} {day_of_week}"
            json_time = f"{date_obj.strftime('%m.%d')}, {time_obj.strftime('%H:%M')}"
        except ValueError:
            return None

        for perf in data.get(category, []):
            if perf["title"] == title and perf["date"] == json_date and perf["time"] == json_time:
                return perf
        return None

    @classmethod
    def load_performances(cls, file_path: str = None) -> list:
        file_path = file_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui",
                                              "data_performance.json")
        file_path = os.path.abspath(file_path)
        try:
            if not os.path.exists(file_path):
                return []
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return []

        if not isinstance(data, dict) or not all(key in data for key in ["opera", "concert", "ballet"]):
            return []

        performances = []
        seen = set()
        for category in ["opera", "concert", "ballet"]:
            category_data = data.get(category, [])
            if not isinstance(category_data, list):
                continue
            for perf in category_data:
                if not isinstance(perf, dict):
                    continue
                perf_key = (perf["title"], perf["date"], perf["time"])
                if perf_key not in seen:
                    perf["category"] = category
                    performances.append(perf)
                    seen.add(perf_key)
        return performances

    @classmethod
    def convert_json_date(cls, json_date: str) -> str:
        try:
            date_parts = json_date.split()
            if len(date_parts) < 2:
                raise ValueError("Некоректний формат дати")
            day, month = date_parts[0], date_parts[1]
            month_num = MONTHS_UA.get(month.upper()) or MONTHS_EN.get(month.upper())
            if not month_num:
                raise ValueError(f"Невідома назва місяця: {month}")
            return f"2025-{month_num}-{day.zfill(2)}"
        except Exception as e:
            raise ValueError(f"Помилка конвертації дати: {str(e)}")