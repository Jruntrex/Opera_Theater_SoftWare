import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from user import Signin, Signup

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Увійти")
        self.root.geometry("800x430")
        self.root.configure(bg="#F5F5F5")  # Світлий фон, як у TheaterMainWindow

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Ліва панель
        self.left_frame = ctk.CTkFrame(self.root, width=400, height=400, fg_color="#FFFFFF", corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=False)

        self.welcome_label = ctk.CTkLabel(
            self.left_frame,
            text="З Поверненням!",
            font=("Times New Roman", 40, "bold"),
            text_color="#000000",
            anchor="w"
        )
        self.welcome_label.place(relx=0.1, rely=0.4)

        self.skip_label = ctk.CTkLabel(
            self.left_frame,
            text="Пропустити вхід?",
            font=("Arial", 16),
            text_color="#666666",
            anchor="w",
            cursor="hand2"
        )
        self.skip_label.place(relx=0.1, rely=0.5)
        self.skip_label.bind("<Button-1>", lambda e: self.skip_login())

        # Права панель
        self.right_frame = ctk.CTkFrame(self.root, width=400, height=400, fg_color="#FFFFFF", corner_radius=20)
        self.right_frame.pack(side="right", fill="both", expand=False)

        self.login_label = ctk.CTkLabel(
            self.right_frame,
            text="Вхід",
            font=("Times New Roman", 24, "bold"),
            text_color="#000000"
        )
        self.login_label.pack(pady=(30, 0))

        self.glad_label = ctk.CTkLabel(
            self.right_frame,
            text="Раді, що ви повернулися!",
            font=("Arial", 14),
            text_color="#666666"
        )
        self.glad_label.pack(pady=(0, 20))

        self.username_entry = ctk.CTkEntry(
            self.right_frame,
            placeholder_text="Логін",
            placeholder_text_color="#A0A0A0",
            width=250,
            height=40,
            font=("Arial", 12),
            fg_color="#F5F5F5",
            border_color="#CCCCCC",
            border_width=1,
            corner_radius=5,
            text_color="#000000"
        )
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(
            self.right_frame,
            placeholder_text="Пароль",
            placeholder_text_color="#A0A0A0",
            show="•",
            width=250,
            height=40,
            font=("Arial", 12),
            fg_color="#F5F5F5",
            border_color="#CCCCCC",
            border_width=1,
            corner_radius=5,
            text_color="#000000"
        )
        self.password_entry.pack(pady=5)

        self.remember_var = ctk.BooleanVar()
        self.remember_checkbox = ctk.CTkCheckBox(
            self.right_frame,
            text="Запам’ятати мене",
            variable=self.remember_var,
            font=("Arial", 12),
            text_color="#000000",
            fg_color="#A71A1F",
            hover_color="#871619"
        )
        self.remember_checkbox.pack(pady=(10, 0), anchor="w", padx=75)

        self.login_button = ctk.CTkButton(
            self.right_frame,
            text="Увійти",
            width=250,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#A71A1F",
            hover_color="#871619",
            text_color="#FFFFFF",
            corner_radius=5,
            command=self.login
        )
        self.login_button.pack(pady=20)

        self.forgot_label = ctk.CTkLabel(
            self.right_frame,
            text="Забули пароль?",
            font=("Arial", 12),
            text_color="#D4A017",
            cursor="hand2"
        )
        self.forgot_label.pack(anchor="e", padx=75)
        self.forgot_label.bind("<Button-1>", lambda e: self.forgot_password())

        self.signup_label = ctk.CTkLabel(
            self.right_frame,
            text="Немає акаунту? Зареєструйтесь",
            font=("Arial", 12),
            text_color="#D4A017",
            cursor="hand2"
        )
        self.signup_label.pack(pady=(20, 0))
        self.signup_label.bind("<Button-1>", lambda e: self.signup())


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            user = Signin(username, password)
            if user.check_login():
                CTkMessagebox(
                    title="Успіх",
                    message="Вхід виконано успішно!",
                    icon="info",
                    option_1="Гаразд",
                    button_color="#A71A1F",
                    button_hover_color="#871619"
                )
                if self.remember_var.get():
                    CTkMessagebox(
                        title="Інформація",
                        message="Дані для входу збережено!",
                        icon="info",
                        option_1="Гаразд",
                        button_color="#A71A1F",
                        button_hover_color="#871619"
                    )
                return True
            else:
                CTkMessagebox(
                    title="Помилка",
                    message="Невірний логін або пароль.",
                    icon="warning",
                    option_1="Гаразд",
                    button_color="#A71A1F",
                    button_hover_color="#871619"
                )
            return False
        else:
            CTkMessagebox(
                title="Помилка",
                message="Будь ласка, введіть логін і пароль.",
                icon="warning",
                option_1="Гаразд",
                button_color="#A71A1F",
                button_hover_color="#871619"
            )
        return False


    def forgot_password(self):
        username = self.username_entry.get()
        if username:
            user = Signin(username, "")
            if user.download_data():
                CTkMessagebox(
                    title="Відновлення пароля",
                    message=f"Посилання для скидання пароля надіслано на {user.email}.",
                    icon="info",
                    option_1="Гаразд",
                    button_color="#A71A1F",
                    button_hover_color="#871619"
                )
            else:
                CTkMessagebox(
                    title="Помилка",
                    message=f"Користувача '{username}' не знайдено.",
                    icon="warning",
                    option_1="Гаразд",
                    button_color="#A71A1F",
                    button_hover_color="#871619"
                )
        else:
            CTkMessagebox(
                title="Помилка",
                message="Будь ласка, введіть логін.",
                icon="warning",
                option_1="Гаразд",
                button_color="#A71A1F",
                button_hover_color="#871619"
            )

    def signup(self):
        signup_window = ctk.CTkToplevel(self.root)
        signup_window.grab_set()
        signup_window.title("Реєстрація")
        signup_window.geometry("400x500")
        signup_window.configure(fg_color="#FFFFFF")  # Світлий фон

        ctk.CTkLabel(
            signup_window,
            text="Реєстрація",
            font=("Times New Roman", 24, "bold"),
            text_color="#000000"
        ).pack(pady=(20, 10))

        username_entry = ctk.CTkEntry(
            signup_window,
            placeholder_text="Логін",
            placeholder_text_color="#A0A0A0",
            width=250,
            height=40,
            font=("Arial", 12),
            fg_color="#F5F5F5",
            border_color="#CCCCCC",
            border_width=1,
            corner_radius=5,
            text_color="#000000"
        )
        username_entry.pack(pady=5)

        password_entry = ctk.CTkEntry(
            signup_window,
            placeholder_text="Пароль",
            placeholder_text_color="#A0A0A0",
            show="•",
            width=250,
            height=40,
            font=("Arial", 12),
            fg_color="#F5F5F5",
            border_color="#CCCCCC",
            border_width=1,
            corner_radius=5,
            text_color="#000000"
        )
        password_entry.pack(pady=5)

        email_entry = ctk.CTkEntry(
            signup_window,
            placeholder_text="Електронна пошта",
            placeholder_text_color="#A0A0A0",
            width=250,
            height=40,
            font=("Arial", 12),
            fg_color="#F5F5F5",
            border_color="#CCCCCC",
            border_width=1,
            corner_radius=5,
            text_color="#000000"
        )
        email_entry.pack(pady=5)

        def perform_signup():
            username = username_entry.get()
            password = password_entry.get()
            email = email_entry.get()
            if username and password and email:
                new_user = Signup(username, password, email)
                result = new_user.save_data()
                CTkMessagebox(
                    title="Результат реєстрації",
                    message=result,
                    icon="info" if "успішно" in result else "warning",
                    option_1="Гаразд",
                    button_color="#A71A1F",
                    button_hover_color="#871619"
                )
                if "успішно" in result:
                    signup_window.after(100, signup_window.destroy)
                    return True
            else:
                CTkMessagebox(
                    title="Помилка",
                    message="Будь ласка, заповніть усі поля.",
                    icon="warning",
                    option_1="Гаразд",
                    button_color="#A71A1F",
                    button_hover_color="#871619"
                )
            return False

        signup_button = ctk.CTkButton(
            signup_window,
            text="Зареєструватись",
            width=250,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#A71A1F",
            hover_color="#871619",
            text_color="#FFFFFF",
            corner_radius=5,
            command=perform_signup
        )
        signup_button.pack(pady=20)

    def skip_login(self):
        """Пропускає вхід (заглушка для переходу до основного вікна)."""
        CTkMessagebox(
            title="Пропуск входу",
            message="Пропуск входу... (Функція в розробці)",
            icon="info",
            option_1="Гаразд",
            button_color="#A71A1F",
            button_hover_color="#871619"
        )
        return True

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginWindow(root)
    root.mainloop()


from PIL import Image

# Колірна гама (залишаємо ту саму, але додаємо градієнти)
COLORS = {
    "primary": "#A71A1F",
    "primary_hover": "#871619",
    "background": "#FAFAFA",
    "white": "#FFFFFF",
    "text": "#111111",
    "secondary_text": "#555555",
    "accent": "#D4A017",
    "border": "#E0E0E0",
    "gradient_start": "#A71A1F",  # Початок градієнта
    "gradient_end": "#D32F2F"     # Кінець градієнта
}

# Шрифти (додаємо кілька нових для вишуканості)
FONTS = {
    "header": ("Georgia", 36, "bold"),
    "title": ("Georgia", 24, "bold"),
    "regular": ("Arial", 14),
    "large": ("Arial", 16),
    "date": ("Arial", 32, "bold"),
    "highlight": ("Playfair Display", 18, "italic")
}

class TheaterHomeWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Налаштування вікна
        self.title("Театр Березіль")
        self.geometry("1200x840+200+0")
        self.configure(fg_color=COLORS["background"])
        self.resizable(False, False)  # Фіксований розмір для кращого вигляду

        # Додаємо обробник закриття вікна
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Додаємо ефект фону з легким градієнтом
        self.bg_canvas = ctk.CTkCanvas(self, bg=COLORS["background"], highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.configure(bg="#2A2A2A")

        # ===== Хедер =====
        self.header_frame = ctk.CTkFrame(self.bg_canvas, fg_color=COLORS["white"], height=90, corner_radius=0, border_width=1, border_color=COLORS["border"])
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        self.header_frame.grid_columnconfigure((0, 2), weight=1)
        self.header_frame.grid_columnconfigure(1, weight=4)

        # Логотип з анімацією при наведенні
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text="ТЕАТР БЕРЕЗІЛЬ",
            font=FONTS["header"],
            text_color=COLORS["primary"],
            cursor="hand2"
        )
        self.logo_label.grid(row=0, column=1, pady=20)
        self.logo_label.bind("<Enter>", lambda e: self.logo_label.configure(text_color=COLORS["accent"]))
        self.logo_label.bind("<Leave>", lambda e: self.logo_label.configure(text_color=COLORS["primary"]))

        # ===== Головний контент із ефектом паралаксу =====
        self.main_frame = ctk.CTkFrame(self.bg_canvas, fg_color="transparent", corner_radius=0)
        self.main_frame.pack(pady=30, padx=40, fill="both", expand=True)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.main_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Банер із затемненням і текстом поверх
        try:
            self.banner_image = Image.open("images_performance/theatre.png")
            self.banner_image = self.banner_image.resize((750, 375))
            self.banner_photo = ctk.CTkImage(self.banner_image, self.banner_image, size=(750, 375))
            self.banner_label = ctk.CTkLabel(self.main_frame, image=self.banner_photo, text="")
            self.banner_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

            # Затемнення для банера
            self.overlay_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.overlay_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
            self.overlay_frame.lower()

            # Текст поверх банера
            self.banner_text = ctk.CTkLabel(
                self.overlay_frame,
                text="Відчуйте магію мистецтва!",
                font=FONTS["title"],
                text_color=COLORS["white"],
                bg_color="transparent",
                wraplength=600
            )
            self.banner_text.place(relx=0.5, rely=0.8, anchor="center")
        except FileNotFoundError:
            self.banner_label = ctk.CTkLabel(
                self.main_frame,
                text="(Зображення не знайдено)",
                font=FONTS["regular"],
                text_color=COLORS["secondary_text"]
            )
            self.banner_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Вітальний блок із тінню та градієнтом
        self.welcome_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS["white"],
            corner_radius=20,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.welcome_card.grid(row=1, column=0, columnspan=2, pady=10, padx=60, sticky="nsew")
        self.welcome_card.grid_columnconfigure(0, weight=1)

        self.welcome_label = ctk.CTkLabel(
            self.welcome_card,
            text="Ласкаво просимо до Театру Березіль!",
            font=FONTS["title"],
            text_color=COLORS["primary"]
        )
        self.welcome_label.grid(row=0, column=0, pady=(20, 5))

        self.description_label = ctk.CTkLabel(
            self.welcome_card,
            text="Оперні шедеври, балетні вистави та концерти у серці Львова",
            font=FONTS["highlight"],
            text_color=COLORS["secondary_text"],
            wraplength=800
        )
        self.description_label.grid(row=1, column=0, pady=(0, 20))

        # Кнопки з анімацією та градієнтом
        button_style = {
            "text_color": COLORS["white"],
            "font": FONTS["regular"],
            "corner_radius": 15,
            "width": 250,
            "height": 60,
            "border_width": 1,
            "border_color": COLORS["border"]
        }

        self.schedule_button = ctk.CTkButton(
            self.main_frame,
            text="🎭 Афіша вистав",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.open_schedule,
            **button_style
        )
        self.schedule_button.grid(row=2, column=0, padx=20, pady=20)
        self.schedule_button.configure(fg_color=[COLORS["gradient_start"], COLORS["gradient_end"]])

        self.about_button = ctk.CTkButton(
            self.main_frame,
            text="ℹ️ Про театр",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.open_about,
            **button_style
        )
        self.about_button.grid(row=2, column=1, padx=20, pady=20)
        self.about_button.configure(fg_color=[COLORS["gradient_start"], COLORS["gradient_end"]])

        # Додаткові інтерактивні кнопки
        # self.contact_button = ctk.CTkButton(
        #     self.main_frame,
        #     text="📞 Контакти",
        #     fg_color="transparent",
        #     hover_color=COLORS["border"],
        #     text_color=COLORS["accent"],
        #     font=FONTS["regular"],
        #     corner_radius=10,
        #     width=150,
        #     height=40,
        #     command=self.open_contacts
        # )
        # self.contact_button.grid(row=3, column=0, columnspan=2, pady=10)

        # ===== Футер з іконками соціальних мереж =====
        self.footer_frame = ctk.CTkFrame(self.bg_canvas, fg_color=COLORS["white"], height=70, corner_radius=0, border_width=1, border_color=COLORS["border"])
        self.footer_frame.pack(fill="x")
        self.footer_frame.pack_propagate(False)
        self.footer_frame.grid_columnconfigure((0, 2), weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=4)

        self.contact_label = ctk.CTkLabel(
            self.footer_frame,
            text="📍 вул. Театральна, 1, Львів  |  ☎️ +380 123 456 789  |  ✉️ info@berezil.ua",
            font=FONTS["regular"],
            text_color=COLORS["secondary_text"]
        )
        self.contact_label.grid(row=0, column=1)

        # Соціальні мережі
        self.social_frame = ctk.CTkFrame(self.footer_frame, fg_color=COLORS["white"])
        self.social_frame.grid(row=0, column=2, padx=20, pady=15, sticky="e")

        social_buttons = [
            ("📘", "https://facebook.com"),
            ("📸", "https://instagram.com"),
            ("🐦", "https://twitter.com")
        ]
        for idx, (icon, url) in enumerate(social_buttons):
            btn = ctk.CTkButton(
                self.social_frame,
                text=icon,
                fg_color="transparent",
                hover_color=COLORS["border"],
                text_color=COLORS["accent"],
                font=FONTS["regular"],
                width=40,
                height=40,
                corner_radius=10,
                command=lambda u=url: self.open_link(u)
            )
            btn.grid(row=0, column=idx, padx=5)

    def open_schedule(self):
        return True

    def open_about(self):
        CTkMessagebox(
            title="Про театр",
            message="Театр Березіль — культурна перлина Львова, що об’єднує оперу, балет та концерти. (Функція в розробці)",
            icon="info",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )

    def open_contacts(self):
        CTkMessagebox(
            title="Контакти",
            message="вул. Театральна, 1, Львів\n+380 123 456 789\ninfo@berezil.ua",
            icon="info",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )

    def open_settings(self):
        CTkMessagebox(
            title="Налаштування",
            message="Налаштування програми (Функція в розробці)",
            icon="info",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

    def on_closing(self):
        """Обробник закриття вікна"""
        if CTkMessagebox(
            title="Вихід",
            message="Ви впевнені, що хочете вийти?",
            icon="question",
            option_1="Так",
            option_2="Ні",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        ).get() == "Так":
            self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = TheaterHomeWindow()
    app.mainloop()





import json
from datetime import datetime, timedelta

# Константи для стилів
COLORS = {
    "primary": "#A71A1F",  # Червоний колір, як на opera.lviv.ua
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

class TheaterMainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Налаштування головного вікна
        self.title("Театр Березіль")
        self.geometry("1200x800")
        self.configure(fg_color=COLORS["background"])

        # Хедер
        self.header_frame = ctk.CTkFrame(self, fg_color=COLORS["white"], height=80, corner_radius=0)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=4)
        self.header_frame.grid_columnconfigure(2, weight=1)

        # Кнопка "Назад"
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

        # Кнопка "Налаштування"
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

        # Логотип/заголовок афіші
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text="АФІША ТЕАТРУ",
            font=FONTS["header"],
            text_color=COLORS["text"]
        )
        self.logo_label.pack(pady=20)

        # Панель навігації
        self.nav_frame = ctk.CTkFrame(self, fg_color=COLORS["white"], height=100)
        self.nav_frame.pack(fill="x", pady=(0, 10))

        # Календар
        self.calendar_frame = ctk.CTkFrame(self.nav_frame, fg_color=COLORS["white"], height=40)
        self.calendar_frame.pack(fill="x", padx=20, pady=(5, 0))

        # Змінна для обраної дати
        self.selected_date = None
        self.calendar_buttons = []

        # Календар на 7 днів
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

        # Кнопка "Скинути"
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

        # Вкладки
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

        self.tab_opera = ctk.CTkButton(
            self.tab_frame,
            text="Опера",
            command=lambda: self.show_tab("opera"),
            **button_style
        )
        self.tab_opera.grid(row=0, column=1, padx=10, pady=5)

        self.tab_ballet = ctk.CTkButton(
            self.tab_frame,
            text="Балет",
            command=lambda: self.show_tab("ballet"),
            **button_style
        )
        self.tab_ballet.grid(row=0, column=2, padx=10, pady=5)

        self.tab_concert = ctk.CTkButton(
            self.tab_frame,
            text="Концерти",
            command=lambda: self.show_tab("concert"),
            **button_style
        )
        self.tab_concert.grid(row=0, column=3, padx=10, pady=5)

        self.filter_button = ctk.CTkButton(
            self.tab_frame,
            text="Фільтр",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["white"],
            font=FONTS["regular"],
            corner_radius=5,
            width=100,
            height=30,
            command=self.open_filter
        )
        self.filter_button.grid(row=0, column=4, padx=10, pady=5)

        # Контент
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"], corner_radius=0)
        self.content_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Завантаження даних
        try:
            with open("data_performance.json", "r", encoding="utf-8") as file:
                self.performances = json.load(file)
        except FileNotFoundError:
            CTkMessagebox(
                title="Помилка",
                message="Файл data_performance.json не знайдено!",
                icon="warning",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
            )
            self.performances = {"opera": [], "ballet": [], "concert": []}

        self.current_tab = "opera"
        self.show_tab(self.current_tab)

    def select_date(self, date):
        """Оновлює обрану дату і відображає відфільтровані події."""
        self.selected_date = date
        for button in self.calendar_buttons:
            if button.cget("text").startswith(str(date.day)):
                button.configure(fg_color=COLORS["primary"], text_color=COLORS["white"])
            else:
                button.configure(fg_color=COLORS["white"], text_color=COLORS["text"])
        self.show_tab(self.current_tab)

    def reset_filter(self):
        """Скидає фільтр і повертається до вкладки 'Опера'."""
        self.selected_date = None
        self.current_tab = "opera"
        for button in self.calendar_buttons:
            button.configure(fg_color=COLORS["white"], text_color=COLORS["text"])
        self.show_tab(self.current_tab)

    def show_tab(self, tab_name):
        """Відображає події для обраного табу з фільтрацією за датою."""
        self.current_tab = tab_name
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        MONTHS_UA = {
            "СІЧНЯ": "01", "ЛЮТОГО": "02", "БЕРЕЗНЯ": "03", "КВІТНЯ": "04",
            "ТРАВНЯ": "05", "ЧЕРВНЯ": "06", "ЛИПНЯ": "07", "СЕРПНЯ": "08",
            "ВЕРЕСНЯ": "09", "ЖОВТНЯ": "10", "ЛИСТОПАДА": "11", "ГРУДНЯ": "12"
        }

        for item in self.performances.get(tab_name, []):
            try:
                date_parts = item.get("date", "22 ТРАВНЯ ЧТ").split()
                day, month, _ = date_parts
                month_num = MONTHS_UA.get(month.upper())
                if not month_num:
                    continue
                item_date = datetime.strptime(f"2025-{month_num}-{day}", "%Y-%m-%d").date()
            except Exception:
                continue

            if self.selected_date and item_date != self.selected_date:
                continue

            # Карта афіші
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

            # Дата
            date_frame = ctk.CTkFrame(card_frame, fg_color=COLORS["white"])
            date_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

            date_parts = item.get("date", "22 ТРАВНЯ ЧТ").split()
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

            # Інформація
            info_frame = ctk.CTkFrame(card_frame, fg_color=COLORS["white"])
            info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

            title_label = ctk.CTkLabel(
                info_frame,
                text=item["title"],
                font=FONTS["title"],
                text_color=COLORS["text"],
                anchor="w"
            )
            title_label.pack(fill="x")

            time_label = ctk.CTkLabel(
                info_frame,
                text=f"{item['time']} | {tab_name.capitalize()}",
                font=FONTS["regular"],
                text_color=COLORS["secondary_text"],
                anchor="w"
            )
            time_label.pack(fill="x")

            author_label = ctk.CTkLabel(
                info_frame,
                text=f"Автор: {item['author']}",
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

            # Кнопки
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
                command=lambda t=item["title"]: self.buy_ticket(t)
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
                command=lambda t=item["title"]: self.show_details(t)
            )
            details_button.pack(side="left")

            # Зображення
            try:
                image_path = item["image"]
                image = ctk.CTkImage(Image.open(image_path), size=(300, 200))
                image_label = ctk.CTkLabel(
                    card_frame,
                    image=image,
                    text="",
                    corner_radius=10
                )
                image_label.grid(row=0, column=2, padx=10, pady=10)
            except FileNotFoundError:
                image_label = ctk.CTkLabel(
                    card_frame,
                    text="Зображення відсутнє",
                    font=FONTS["regular"],
                    text_color=COLORS["secondary_text"]
                )
                image_label.grid(row=0, column=2, padx=10, pady=10)

    def buy_ticket(self, performance_title):
        """Відображає повідомлення про покупку квитка."""
        CTkMessagebox(
            title="Успіх",
            message=f"Ви обрали квиток на {performance_title}! (Функція в розробці)",
            icon="check",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )

    def show_details(self, performance_title):
        """Відображає деталі події."""
        CTkMessagebox(
            title="Деталі",
            message=f"Детальна інформація про {performance_title} (Функція в розробці)",
            icon="info",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )

    def go_back(self):
        """Логіка для кнопки 'Назад'."""
        CTkMessagebox(
            title="Повернення",
            message="Повернення до головного меню (Функція в розробці)",
            icon="info",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )

    def open_settings(self):
        """Логіка для кнопки 'Налаштування'."""
        CTkMessagebox(
            title="Налаштування",
            message="Налаштування програми (Функція в розробці)",
            icon="info",
            fg_color=COLORS["white"],
            title_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )

    def open_filter(self):
        """Логіка для кнопки 'Фільтр'."""
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
    app = TheaterMainWindow()
    app.mainloop()