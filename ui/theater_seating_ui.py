import customtkinter as ctk
from models.theater_seating import TheaterSeating
from CTkMessagebox import CTkMessagebox
from models.order import Order
import auth
from config import COLORS
import json
import os
from datetime import datetime

FONTS = {
    "header": ("Arial", 24, "bold"),
    "title": ("Arial", 18, "bold"),
    "large": ("Arial", 16, "bold"),
    "regular": ("Arial", 16)
}

class TheaterSeatingUI(ctk.CTkToplevel):
    def __init__(self, parent, theater_seating, reserved_seats_file="ui/orders.json", performance_data=None):
        super().__init__(parent)
        self.title(f"Схема залу театру: {performance_data.get('title', 'Вистави') if performance_data else 'Вистави'}")
        self.geometry("1200x840+200+0")
        self.grab_set()
        self.configure(fg_color=COLORS["background"])

        # Нормалізуємо performance_data
        self.performance_data = performance_data or {}
        self.performance_data = self._normalize_performance_data(self.performance_data)

        # Завантажуємо заброньовані місця
        self.reserved_seats = self._load_reserved_seats(reserved_seats_file)
        print(
            f"Завантажені заброньовані місця для {self.performance_data.get('title', 'невідома вистава')}: {self.reserved_seats}")

        # Ініціалізуємо TheaterSeating з нормалізованими даними
        self.theater_seating = TheaterSeating(performance_data=self.performance_data)
        self.theater_seating.load_reserved_seats(self.reserved_seats)

        self.selected_seats = []
        self.buttons = {}
        self.price_colors = {
            "синій": "#64B5F6",
            "жовтий": "#FFD54F",
            "фіолетовий": "#BA68C8"
        }
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS["background"])
        self.main_container.pack(fill="both", expand=True)
        self.main_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS["background"])
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.info_panel = ctk.CTkFrame(self.main_container, fg_color=COLORS["white"], width=250)
        self.info_panel.pack(side="right", fill="y", padx=10, pady=10)
        self.info_panel.pack_propagate(False)
        self.price_label = None
        self.selected_seats_label = None

        # Додаємо кнопку "← Назад" у верхньому лівому куті
        self.arrow_back_button = ctk.CTkButton(
            self,
            text="← Назад",
            command=self.go_back,
            fg_color=COLORS["white"],
            hover_color="#E0E0E0",
            text_color=COLORS["text"],
            font=FONTS["regular"],
            corner_radius=5,
            width=120,
            height=40,
        )
        self.arrow_back_button.place(x=20, y=20)

        self._create_info_panel()
        self._create_seating_layout()
        self.confirm_button = ctk.CTkButton(
            self.main_frame,
            text="Підтвердити вибір",
            command=self.confirm_selection,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["white"],
            font=FONTS["large"],
            width=200,
            height=40,
            corner_radius=10
        )
        self.confirm_button.pack(pady=15)
        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="Повернутися",
            command=self.go_back,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["white"],
            font=FONTS["large"],
            width=200,
            height=40,
            corner_radius=10
        )
        self.back_button.pack(pady=15)
        self._update_info_panel()

    def _normalize_performance_data(self, performance_data):
        """Нормалізує дату і час у performance_data до формату orders.json."""
        normalized = performance_data.copy()
        MONTHS_UA = {
            "СІЧНЯ": "01", "ЛЮТОГО": "02", "БЕРЕЗНЯ": "03", "КВІТНЯ": "04",
            "ТРАВНЯ": "05", "ЧЕРВНЯ": "06", "ЛИПНЯ": "07", "СЕРПНЯ": "08",
            "ВЕРЕСНЯ": "09", "ЖОВТНЯ": "10", "ЛИСТОПАДА": "11", "ГРУДНЯ": "12"
        }

        date_raw = performance_data.get("date", "30.06.2025")
        if " " in date_raw:
            date_parts = date_raw.split()
            day, month = date_parts[0], date_parts[1]
            month_num = MONTHS_UA.get(month.upper(), "06")
            normalized["date"] = f"2025-{month_num}-{day.zfill(2)}"
        else:
            try:
                date_obj = datetime.strptime(date_raw, "%d.%m.%Y")
                normalized["date"] = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                normalized["date"] = "2025-06-30"

        time_raw = performance_data.get("time", "20:00")
        if ", " in time_raw:
            normalized["time"] = time_raw.split(", ")[1]
        else:
            normalized["time"] = time_raw

        return normalized

    def _load_reserved_seats(self, filename):
        try:
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                print(f"Файл {filename} не існує або порожній. Ініціалізація порожнім списком.")
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
                return []
            with open(filename, 'r', encoding='utf-8') as f:
                orders = json.load(f)
        except json.JSONDecodeError:
            print(f"Помилка декодування JSON у файлі {filename}. Ініціалізація порожнім списком.")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            return []
        except Exception as e:
            print(f"Помилка при завантаженні {filename}: {str(e)}")
            return []

        reserved_seats = []
        current_title = self.performance_data.get("title", "")
        current_date = self.performance_data.get("date", "")
        current_time = self.performance_data.get("time", "")

        for order in orders:
            order_performance = order.get("performance", {})
            order_title = order_performance.get("title", "")
            order_date = order_performance.get("date", "")
            order_time = order_performance.get("time", "")

            if order_title == current_title and order_date == current_date and order_time == current_time:
                for seat in order.get("seats", []):
                    reserved_seats.append((seat["zone"], seat["row"], seat["seat"]))

        return reserved_seats

    def _create_info_panel(self):
        ctk.CTkLabel(
            self.info_panel,
            text="ІНФОРМАЦІЯ",
            font=FONTS["header"],
            text_color=COLORS["text"]
        ).pack(pady=10)
        ctk.CTkLabel(
            self.info_panel,
            text="ЦІНИ",
            font=FONTS["title"],
            text_color=COLORS["text"]
        ).pack(pady=5)
        for category, color in self.price_colors.items():
            frame = ctk.CTkFrame(self.info_panel, fg_color="transparent")
            frame.pack(fill="x", padx=10, pady=2)
            sample = ctk.CTkFrame(frame, width=15, height=15, fg_color=color)
            sample.pack(side="left", padx=5)
            ctk.CTkLabel(
                frame,
                text=f"{category.capitalize()}: {self.theater_seating.get_price_by_category(category)} грн",
                font=FONTS["regular"],
                text_color=COLORS["text"]
            ).pack(side="left", padx=5)
        ctk.CTkLabel(
            self.info_panel,
            text="ОБРАНІ МІСЦЯ",
            font=FONTS["title"],
            text_color=COLORS["text"],
            pady=10
        ).pack()
        self.selected_seats_label = ctk.CTkLabel(
            self.info_panel,
            text="",
            font=FONTS["regular"],
            text_color=COLORS["text"],
            justify="left"
        )
        self.selected_seats_label.pack(padx=10, fill="x")
        ctk.CTkLabel(
            self.info_panel,
            text="ЗАГАЛЬНА СУМА:",
            font=FONTS["title"],
            text_color=COLORS["text"],
            pady=5
        ).pack()
        self.price_label = ctk.CTkLabel(
            self.info_panel,
            text="0 грн",
            font=FONTS["large"],
            text_color=COLORS["primary"]
        )
        self.price_label.pack(padx=10, pady=5)

    def _create_seating_layout(self):
        scene_label = ctk.CTkLabel(
            self.main_frame,
            text="СЦЕНА",
            font=FONTS["header"],
            fg_color=COLORS["gradient_start"],
            corner_radius=8,
            width=300,
            height=50,
            text_color=COLORS["white"]
        )
        scene_label.pack(pady=10)
        for balcony, zone in [(1, "балкон_1"), (2, "балкон_2"), (3, "балкон_3")]:
            balcony_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["white"], corner_radius=8, width=400)
            balcony_frame.pack(fill="x", padx=200 - (balcony * 30), pady=10, anchor="center")
            balcony_frame.pack_propagate(False)
            ctk.CTkLabel(
                balcony_frame,
                text=f"БАЛКОН {balcony}",
                font=FONTS["title"],
                text_color=COLORS["text"]
            ).pack(pady=5)
            for row in range(1, 4):
                row_frame = ctk.CTkFrame(balcony_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=2)
                ctk.CTkLabel(
                    row_frame,
                    text=f"Ряд {row}",
                    width=50,
                    font=FONTS["regular"],
                    text_color=COLORS["text"]
                ).pack(side="left", padx=5)
                seats_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                seats_frame.pack(anchor="center")
                for seat in range(1, 11):
                    seat_info = next(
                        (s for s in self.theater_seating.get_seats_in_zone(zone) if
                         s["row"] == row and s["seat"] == seat),
                        None
                    )
                    if seat_info:
                        is_reserved = self.theater_seating.is_seat_reserved(zone, row, seat)
                        self._create_seat_button(seats_frame, zone, row, seat, seat_info, is_reserved)

    def _create_seat_button(self, parent, zone, row, seat, seat_info, is_reserved=False):
        color = self.price_colors[seat_info["price_category"]]
        button = ctk.CTkButton(
            parent,
            text=str(seat),
            width=30,
            height=30,
            fg_color="#616161" if is_reserved else color,
            hover_color=COLORS["primary_hover"] if not is_reserved else "#616161",
            text_color=COLORS["white"],
            font=FONTS["regular"],
            corner_radius=5,
            command=lambda: self._toggle_seat(zone, row, seat) if not is_reserved else None,
            state="disabled" if is_reserved else "normal"
        )
        button.pack(side="left", padx=3, pady=3)
        self.buttons[(zone, row, seat)] = button

    def _update_info_panel(self):
        selected_seats_text = "\n".join(
            [f"{s['zone'].capitalize()}, ряд {s['row']}, місце {s['seat']}" for s in self.selected_seats])
        self.selected_seats_label.configure(text=selected_seats_text if selected_seats_text else "Немає обраних місць")
        total_price = sum(self.theater_seating.get_price(s["zone"], s["row"], s["seat"]) for s in self.selected_seats)
        if self.price_label:
            self.price_label.configure(text=f"{total_price} грн")

    def _toggle_seat(self, zone, row, seat):
        seat_info = next(
            (s for s in self.theater_seating.get_seats_in_zone(zone) if s["row"] == row and s["seat"] == seat),
            None
        )
        if not seat_info:
            CTkMessagebox(
                title="Помилка",
                message=f"Місце {row}-{seat} у зоні {zone} не знайдено.",
                icon="warning"
            )
            return
        button = self.buttons[(zone, row, seat)]
        seat_key = (zone, row, seat)
        if seat_key in [(s["zone"], s["row"], s["seat"]) for s in self.selected_seats]:
            self.selected_seats = [s for s in self.selected_seats if
                                   not (s["zone"] == zone and s["row"] == row and s["seat"] == seat)]
            button.configure(fg_color=self.price_colors[seat_info["price_category"]], state="normal")
        else:
            self.selected_seats.append({"zone": zone, "row": row, "seat": seat})
            button.configure(fg_color=COLORS["primary"], state="normal")
        self._update_info_panel()

    def confirm_selection(self):
        if not auth.IS_USER_LOGGED_IN:
            CTkMessagebox(
                title="Помилка",
                message="Увійдіть у систему, щоб зробити замовлення!",
                icon="warning"
            )
            return
        if not self.selected_seats:
            CTkMessagebox(
                title="Помилка",
                message="Оберіть хоча б одне місце!",
                icon="warning"
            )
            return
        total_price = 0
        for seat in self.selected_seats:
            zone, row, seat_num = seat["zone"], seat["row"], seat["seat"]
            try:
                price = self.theater_seating.get_price(zone, row, seat_num)
                total_price += price
                self.theater_seating.reserve_seat(zone, row, seat_num)
                self.buttons[(zone, row, seat_num)].configure(fg_color="#616161", state="disabled")
            except ValueError as e:
                CTkMessagebox(
                    title="Помилка",
                    message=str(e),
                    icon="warning"
                )
                return
        order = Order(
            user=auth.USER,
            seats=self.selected_seats,
            total_price=total_price,
            theater_seating=self.theater_seating,
            performance_data=self.performance_data
        )
        order.save_order()
        order.generate_ticket()

        ticket_path = f"ui/tickets/ticket_{order.order_id}.png"

        try:
            os.system(f'start "" "{ticket_path}"')
            print("qwerty")
        except Exception as e:
            CTkMessagebox(
                title="Помилка",
                message=f"Не вдалося відкрити квиток: {str(e)}",
                icon="warning"
            )

        CTkMessagebox(
            title="Успіх",
            message=f"Місця зарезервовано! Загальна сума: {total_price} грн\nКвиток збережено як 'ticket_{order.order_id}.png'",
            icon="info"
        )
        self.selected_seats = []
        self._update_info_panel()

    def go_back(self):
        if self.selected_seats:
            response = CTkMessagebox(
                title="Попередження",
                message="Ви обрали місця, але не підтвердили. Закрити вікно?",
                icon="warning",
                option_1="Так",
                option_2="Ні",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
            )
            if response.get() != "Так":
                return
        self.destroy()

if __name__ == '__main__':
    root = ctk.CTk()
    theater_seating = TheaterSeating()
    app = TheaterSeatingUI(root, theater_seating, "ui/orders.json")
    root.mainloop()