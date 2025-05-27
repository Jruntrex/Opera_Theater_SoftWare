from PIL import Image, ImageDraw, ImageFont
import qrcode
import uuid
from datetime import datetime
from config import COLORS
import json
import os
import auth

class Order:
    def __init__(self, user, seats, total_price, theater_seating, performance_data=None):
        self.order_id = str(uuid.uuid4())
        self.user = user
        self.seats = seats
        self.total_price = total_price
        self.theater_seating = theater_seating
        self.performance_data = performance_data or {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_ticket(self) -> None:
        ticket_width = 600
        ticket_height = 300

        ticket = Image.new('RGB', (ticket_width, ticket_height), 'white')
        draw = ImageDraw.Draw(ticket)

        border_color = COLORS["primary"]
        border_width = 5
        draw.rectangle(
            [border_width, border_width, ticket_width - border_width, ticket_height - border_width],
            outline=border_color
        )

        try:
            title_font = ImageFont.truetype("georgia.ttf", 36)
            text_font = ImageFont.truetype("arial.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        seats_text = ", ".join(
            f"{seat['zone'].capitalize()} Ряд {seat['row']} Місце {seat['seat']}"
            for seat in self.seats
        )

        title = self.performance_data.get("title", "Березіль: " + (auth.PERFORMANCE_FOR_TICKET or "Live Night"))

        date_raw = self.performance_data.get("date", "30.06.2025")
        if " " in date_raw:
            date = date_raw.split()[0] + "." + date_raw.split()[1][:3].capitalize()
        else:
            try:
                date_obj = datetime.strptime(date_raw, "%Y-%m-%d")
                date = date_obj.strftime("%d.%m")
            except ValueError:
                date = "30.06"

        time_raw = self.performance_data.get("time", "20:00")
        time = time_raw.split(", ")[0] if ", " in time_raw else time_raw

        draw.text((30, 30), title, fill=COLORS["text"], font=title_font)
        draw.text((30, 90), f"Користувач: {self.user}", fill=COLORS["text"], font=text_font)
        draw.text((30, 130), f"Дата: {date}", fill=COLORS["text"], font=text_font)
        draw.text((30, 170), f"Час: {time}", fill=COLORS["text"], font=text_font)
        draw.text((30, 210), "Локація: UnderGround Hall", fill=COLORS["text"], font=text_font)
        draw.text((30, 250), f"Місця: {seats_text}", fill=COLORS["text"], font=text_font)

        qr_data = f"https://hadiastrum.com/ticket/{self.order_id}"
        qr = qrcode.make(qr_data)
        qr = qr.resize((150, 150))
        ticket.paste(qr, (ticket_width - 180, ticket_height - 180))

        # Просто прописуємо відносний шлях
        ticket_path = f"ui/tickets/ticket_{self.order_id}.png"
        ticket.save(ticket_path)

        print(f"Квиток збережено за шляхом: {ticket_path}")
        print(ticket_path)

    def save_order(self) -> None:
        MONTHS_UA = {
            "СІЧНЯ": "01", "ЛЮТОГО": "02", "БЕРЕЗНЯ": "03", "КВІТНЯ": "04",
            "ТРАВНЯ": "05", "ЧЕРВНЯ": "06", "ЛИПНЯ": "07", "СЕРПНЯ": "08",
            "ВЕРЕСНЯ": "09", "ЖОВТНЯ": "10", "ЛИСТОПАДА": "11", "ГРУДНЯ": "12"
        }

        # Нормалізація performance_data
        normalized_performance = self.performance_data.copy()
        if "date" in normalized_performance and " " in normalized_performance["date"]:
            date_parts = normalized_performance["date"].split()
            day, month = date_parts[0], date_parts[1]
            month_num = MONTHS_UA.get(month.upper(), "01")
            normalized_performance["date"] = f"2025-{month_num}-{day}"
        if "time" in normalized_performance and ", " in normalized_performance["time"]:
            normalized_performance["time"] = normalized_performance["time"].split(", ")[1]

        order_data = {
            "order_id": self.order_id,
            "user": self.user,
            "performance": normalized_performance,
            "seats": self.seats,
            "total_price": self.total_price,
            "timestamp": self.timestamp
        }

        try:
            if not os.path.exists("ui/orders.json") or os.path.getsize("ui/orders.json") == 0:
                with open("ui/orders.json", "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
                orders = []
            else:
                with open("ui/orders.json", "r", encoding="utf-8") as f:
                    orders = json.load(f)
        except json.JSONDecodeError:
            print("Помилка декодування JSON. Ініціалізація порожнім списком.")
            orders = []
            with open("ui/orders.json", "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        orders.append(order_data)

        with open("ui/orders.json", "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=4)