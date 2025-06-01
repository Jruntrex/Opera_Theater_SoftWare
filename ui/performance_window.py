import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import json
from datetime import datetime, timedelta
from ui.performance_details import PerformanceDetailsWindow
import auth
from models.theater_seating import TheaterSeating
from ui.theater_seating_ui import TheaterSeatingUI
from ui.admin_performance_manager import AdminPerformanceManager

COLORS = {
    "primary": "#A71A1F",
    "primary_hover": "#871619",
    "background": "#F5F5F5",
    "white": "#FFFFFF",
    "text": "#000000",
    "secondary_text": "#666666",
    "accent": "#D4A017"
}
FONTS = {
    "header": ("Times New Roman", 32, "bold"),
    "title": ("Times New Roman", 22, "bold"),
    "regular": ("Arial", 14),
    "large": ("Arial", 16),
    "date": ("Arial", 32, "bold")
}


class TheaterMainWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_back):
        super().__init__(parent)
        self.on_back = on_back
        self.title("Театр Березіль")
        self.geometry("1200x840+200+0")
        self.configure(fg_color=COLORS["background"])
        self.protocol("WM_DELETE_WINDOW", self.go_back)  # Обробка закриття вікна

        # Ініціалізація основних фреймів
        self._setup_header_frame()
        self._setup_nav_frame()
        self._setup_content_frame()
        self._load_performance_data()
        self.current_tab = "opera"
        self.show_tab(self.current_tab)

    def _setup_header_frame(self):
        self.header_frame = ctk.CTkFrame(self, fg_color=COLORS["white"], height=80, corner_radius=0)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=2)
        if auth.USER == "admin":
            self.header_frame.grid_columnconfigure(2, weight=1)
        else:
            self.header_frame.grid_columnconfigure(2, weight=2)

        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="← Назад",
            fg_color=COLORS["white"],
            hover_color="#E0E0E0",
            text_color=COLORS["text"],
            font=FONTS["regular"],
            corner_radius=5,
            width=120,
            height=40,
            command=self.go_back
        )
        self.back_button.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        if auth.USER == "admin":
            self.settings_button = ctk.CTkButton(
                self.header_frame,
                text="⚙️",
                fg_color=COLORS["white"],
                hover_color="#E0E0E0",
                text_color=COLORS["text"],
                font=FONTS["large"],
                corner_radius=5,
                width=50,
                height=40,
                command=self.open_settings
            )
            self.settings_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text="АФІША ТЕАТРУ",
            font=FONTS["header"],
            text_color=COLORS["text"]
        )
        self.logo_label.grid(row=0, column=1, pady=20, sticky="nsew")

    def _setup_nav_frame(self):
        self.nav_frame = ctk.CTkFrame(self, fg_color=COLORS["white"], height=100)
        self.nav_frame.pack(fill="x", pady=(0, 10))
        self.calendar_frame = ctk.CTkFrame(self.nav_frame, fg_color=COLORS["white"], height=40)
        self.calendar_frame.pack(fill="x", padx=20, pady=(5, 0))
        self.selected_date = None
        self.calendar_buttons = []
        today = datetime.now().date()
        days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "НД"]

        for i in range(7):
            date = today + timedelta(days=i)
            day_label = ctk.CTkButton(
                self.calendar_frame,
                text=f"{date.day} {days[date.weekday()]}",
                fg_color=COLORS["white"],
                hover_color="#E0E0E0",
                text_color=COLORS["text"],
                font=FONTS["regular"],
                width=80,
                height=30,
                corner_radius=5,
                border_width=1,
                border_color="#CCCCCC",
                command=lambda d=date: self.select_date(d)
            )
            day_label.pack(side="left", padx=5)
            self.calendar_buttons.append(day_label)

        self.reset_button = ctk.CTkButton(
            self.calendar_frame,
            text="Скинути",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["white"],
            font=FONTS["regular"],
            width=80,
            height=30,
            corner_radius=5,
            command=self.reset_filter
        )
        self.reset_button.pack(side="left", padx=5)

        self.tab_frame = ctk.CTkFrame(self.nav_frame, fg_color=COLORS["white"], height=40)
        self.tab_frame.pack(fill="x", padx=20, pady=(5, 0))
        self.tab_frame.grid_columnconfigure((0, 5), weight=1)
        self.tab_frame.grid_columnconfigure((1, 2, 3, 4), weight=0)

        button_style = {
            "fg_color": COLORS["white"],
            "hover_color": "#E0E0E0",
            "text_color": COLORS["text"],
            "font": FONTS["regular"],
            "corner_radius": 5,
            "width": 100,
            "height": 30
        }

        self.tabs = {
            "opera": ctk.CTkButton(
                self.tab_frame,
                text="Опера",
                command=lambda: self.show_tab("opera"),
                **button_style
            ),
            "ballet": ctk.CTkButton(
                self.tab_frame,
                text="Балет",
                command=lambda: self.show_tab("ballet"),
                **button_style
            ),
            "concert": ctk.CTkButton(
                self.tab_frame,
                text="Концерти",
                command=lambda: self.show_tab("concert"),
                **button_style
            )
        }
        self.tabs["opera"].grid(row=0, column=1, padx=10, pady=5)
        self.tabs["ballet"].grid(row=0, column=2, padx=10, pady=5)
        self.tabs["concert"].grid(row=0, column=3, padx=10, pady=5)

    def _setup_content_frame(self):
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"], corner_radius=0)
        self.content_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def _load_performance_data(self):
        try:
            with open("ui/data_performance.json", "r", encoding="utf-8") as file:
                self.performance = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            CTkMessagebox(
                title="Помилка",
                message=f"Не вдалося завантажити дані: {str(e)}",
                icon="warning",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
            )
            self.performance = {"opera": [], "ballet": [], "concert": []}

    def select_date(self, date):
        self.selected_date = date
        for button in self.calendar_buttons:
            if button.cget("text").startswith(str(date.day)):
                button.configure(fg_color=COLORS["primary"], text_color=COLORS["white"])
            else:
                button.configure(fg_color=COLORS["white"], text_color=COLORS["text"])
        self.show_tab(self.current_tab)

    def reset_filter(self):
        self.selected_date = None
        self.current_tab = "opera"
        for button in self.calendar_buttons:
            button.configure(fg_color=COLORS["white"], text_color=COLORS["text"])
        self.show_tab(self.current_tab)

    def show_tab(self, tab_name):
        self.current_tab = tab_name
        for name, button in self.tabs.items():
            button.configure(
                fg_color=COLORS["primary"] if name == tab_name else COLORS["white"],
                text_color=COLORS["white"] if name == tab_name else COLORS["text"]
            )

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        MONTHS_UA = {
            "СІЧНЯ": "01", "ЛЮТОГО": "02", "БЕРЕЗНЯ": "03", "КВІТНЯ": "04",
            "ТРАВНЯ": "05", "ЧЕРВНЯ": "06", "ЛИПНЯ": "07", "СЕРПНЯ": "08",
            "ВЕРЕСНЯ": "09", "ЖОВТНЯ": "10", "ЛИСТОПАДА": "11", "ГРУДНЯ": "12"
        }

        for item in self.performance.get(tab_name, []):
            try:
                date_parts = item.get("date", "26 ТРАВНЯ ПН").split()
                day, month, _ = date_parts
                month_num = MONTHS_UA.get(month.upper())
                if not month_num:
                    continue
                item_date = datetime.strptime(f"2025-{month_num}-{day}", "%Y-%m-%d").date()
                if self.selected_date and item_date != self.selected_date:
                    continue
            except (ValueError, KeyError):
                continue

            card_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color=COLORS["white"],
                corner_radius=10,
                border_width=1,
                border_color="#E0E0E0"
            )
            card_frame.pack(fill="x", padx=20, pady=10)
            card_frame.grid_columnconfigure(0, weight=0)
            card_frame.grid_columnconfigure(1, weight=1)
            card_frame.grid_columnconfigure(2, weight=0)

            date_frame = ctk.CTkFrame(card_frame, fg_color=COLORS["white"])
            date_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
            date_parts = item.get("date", "26 ТРАВНЯ ПН").split()
            date_label = ctk.CTkLabel(
                date_frame,
                text=date_parts[0],
                font=FONTS["date"],
                text_color=COLORS["primary"]
            )
            date_label.pack()
            month_label = ctk.CTkLabel(
                date_frame,
                text=date_parts[1],
                font=FONTS["regular"],
                text_color=COLORS["text"]
            )
            month_label.pack()
            day_label = ctk.CTkLabel(
                date_frame,
                text=date_parts[2],
                font=FONTS["regular"],
                text_color=COLORS["text"]
            )
            day_label.pack()

            info_frame = ctk.CTkFrame(card_frame, fg_color=COLORS["white"])
            info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            title_label = ctk.CTkLabel(
                info_frame,
                text=item.get("title", "Без назви"),
                font=FONTS["title"],
                text_color=COLORS["text"],
                anchor="w"
            )
            title_label.pack(fill="x")
            time_label = ctk.CTkLabel(
                info_frame,
                text=f"{item.get('time', 'Час не вказано')} | {tab_name.capitalize()}",
                font=FONTS["regular"],
                text_color=COLORS["secondary_text"],
                anchor="w"
            )
            time_label.pack(fill="x")
            author_label = ctk.CTkLabel(
                info_frame,
                text=f"Автор: {item.get('author', 'Невідомий')}",
                font=FONTS["regular"],
                text_color=COLORS["secondary_text"],
                anchor="w"
            )
            author_label.pack(fill="x")
            description_label = ctk.CTkLabel(
                info_frame,
                text=item.get("description", "Опис відсутній"),
                font=FONTS["regular"],
                text_color=COLORS["secondary_text"],
                anchor="w",
                wraplength=600
            )
            description_label.pack(fill="x", pady=(5, 0))

            button_frame = ctk.CTkFrame(info_frame, fg_color=COLORS["white"])
            button_frame.pack(fill="x", pady=(10, 0))
            buy_button = ctk.CTkButton(
                button_frame,
                text="Купити квиток",
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                text_color=COLORS["white"],
                font=FONTS["regular"],
                corner_radius=5,
                width=150,
                height=35,
                command=lambda i=item: self.buy_ticket(i)
            )
            buy_button.pack(side="left", padx=(0, 10))
            details_button = ctk.CTkButton(
                button_frame,
                text="Детальніше",
                fg_color=COLORS["white"],
                hover_color=COLORS["background"],
                text_color=COLORS["accent"],
                font=FONTS["regular"],
                corner_radius=5,
                width=100,
                height=35,
                command=lambda i=item: self.show_details(i)
            )
            details_button.pack(side="left")

            try:
                image_path = item.get("image")
                if image_path:
                    image = ctk.CTkImage(Image.open(image_path), size=(300, 200))
                    image_label = ctk.CTkLabel(
                        card_frame,
                        image=image,
                        text="",
                        corner_radius=10
                    )
                    image_label.grid(row=0, column=2, padx=10, pady=10)
                else:
                    raise FileNotFoundError("Image path not provided")
            except FileNotFoundError:
                image_label = ctk.CTkLabel(
                    card_frame,
                    text="Зображення відсутнє",
                    font=FONTS["regular"],
                    text_color=COLORS["secondary_text"]
                )
                image_label.grid(row=0, column=2, padx=10, pady=10)

    def buy_ticket(self, performance_data):
        print(f"Відкривається TheaterSeatingUI для {performance_data.get('title', 'Без назви')}")
        if not auth.IS_USER_LOGGED_IN:
            CTkMessagebox(
                title="Помилка",
                message="Будь ласка, увійдіть в систему, щоб купити квиток!",
                icon="warning",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
            )
            return False

        try:
            auth.PERFORMANCE_FOR_TICKET = performance_data.get("title", "Без назви")
            theater_seating = TheaterSeating(performance_data)
            TheaterSeatingUI(self, theater_seating, "ui/orders.json", performance_data)
            return True
        except Exception as e:
            CTkMessagebox(
                title="Помилка",
                message=f"Не вдалося відкрити схему залу: {str(e)}",
                icon="warning",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
            )
            return False

    def show_details(self, performance_data):
        PerformanceDetailsWindow(self, performance_data, self.show_tab_wrapper)

    def show_tab_wrapper(self):
        self.show_tab(self.current_tab)

    def go_back(self):
        self.destroy()
        self.on_back()

    def open_settings(self):
        admin_window = AdminPerformanceManager(self)
        self.wait_for_admin_window(admin_window)

    def wait_for_admin_window(self, admin_window):
        if admin_window.winfo_exists():
            self.after(100, lambda: self.wait_for_admin_window(admin_window))
        else:
            self._load_performance_data()
            self.show_tab(self.current_tab)

    def open_filter(self):
        CTkMessagebox(
            title="Фільтр",
            message="Фільтрація подій за параметрами (Функція в розробці)",
            icon="info",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.withdraw()
    app = TheaterMainWindow(root, lambda: print("Back to Home"))
    app.mainloop()