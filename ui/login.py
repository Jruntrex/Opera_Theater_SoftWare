import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from user import Signin, Signup
import auth

# Використовуємо ті самі COLORS і FONTS з TheaterHomeWindow
COLORS = {
    "primary": "#A71A1F",
    "primary_hover": "#871619",
    "background": "#FAFAFA",
    "white": "#FFFFFF",
    "text": "#111111",
    "secondary_text": "#555555",
    "accent": "#D4A017",
    "border": "#E0E0E0",
    "gradient_start": "#A71A1F",
    "gradient_end": "#D32F2F"
}

FONTS = {
    "header": ("Georgia", 36, "bold"),
    "title": ("Georgia", 24, "bold"),
    "regular": ("Arial", 14),
    "large": ("Arial", 16),
    "date": ("Arial", 32, "bold"),
    "highlight": ("Playfair Display", 18, "italic")
}

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_success, on_back):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success  # Callback для головного вікна
        self.on_back = on_back        # Callback для повернення до вступного вікна
        self.title("Увійти")
        self.geometry("800x430+400+250")
        self.configure(fg_color=COLORS["background"])
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Ліва панель
        self.left_frame = ctk.CTkFrame(self, width=400, height=400, fg_color=COLORS["white"], corner_radius=0)
        self.left_frame.pack(side="left", fill="both", expand=False)

        self.welcome_label = ctk.CTkLabel(
            self.left_frame,
            text="З Поверненням!",
            font=FONTS["header"],
            text_color=COLORS["text"],
            anchor="w"
        )
        self.welcome_label.place(relx=0.1, rely=0.4)

        self.skip_label = ctk.CTkLabel(
            self.left_frame,
            text="Пропустити вхід?",
            font=FONTS["regular"],
            text_color=COLORS["secondary_text"],
            anchor="w",
            cursor="hand2"
        )
        self.skip_label.place(relx=0.1, rely=0.5)
        self.skip_label.bind("<Button-1>", lambda e: self.skip_login())

        # Права панель
        self.right_frame = ctk.CTkFrame(self, width=400, height=400, fg_color=COLORS["white"], corner_radius=20)
        self.right_frame.pack(side="right", fill="both", expand=False)

        self.login_label = ctk.CTkLabel(
            self.right_frame,
            text="Вхід",
            font=FONTS["title"],
            text_color=COLORS["text"]
        )
        self.login_label.pack(pady=(30, 0))

        self.glad_label = ctk.CTkLabel(
            self.right_frame,
            text="Раді, що ви повернулися!",
            font=FONTS["regular"],
            text_color=COLORS["secondary_text"]
        )
        self.glad_label.pack(pady=(0, 20))

        self.username_entry = ctk.CTkEntry(
            self.right_frame,
            placeholder_text="Логін",
            placeholder_text_color=COLORS["secondary_text"],
            width=250,
            height=40,
            font=FONTS["regular"],
            fg_color=COLORS["background"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=5,
            text_color=COLORS["text"]
        )
        self.username_entry.pack(pady=5)
        self.username_entry.bind("<Return>", lambda e: self.login())  # Додаємо прив’язку Enter

        self.password_entry = ctk.CTkEntry(
            self.right_frame,
            placeholder_text="Пароль",
            placeholder_text_color=COLORS["secondary_text"],
            show="•",
            width=250,
            height=40,
            font=FONTS["regular"],
            fg_color=COLORS["background"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=5,
            text_color=COLORS["text"]
        )
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<Return>", lambda e: self.login())  # Додаємо прив’язку Enter

        self.remember_var = ctk.BooleanVar()
        self.remember_checkbox = ctk.CTkCheckBox(
            self.right_frame,
            text="Запам’ятати мене",
            variable=self.remember_var,
            font=FONTS["regular"],
            text_color=COLORS["text"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"]
        )
        # self.remember_checkbox.pack(pady=(10, 0), anchor="w", padx=75)

        self.login_button = ctk.CTkButton(
            self.right_frame,
            text="Увійти",
            width=250,
            height=40,
            font=FONTS["regular"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["white"],
            corner_radius=5,
            command=self.login
        )
        self.login_button.pack(pady=20)

        self.forgot_label = ctk.CTkLabel(
            self.right_frame,
            text="Забули пароль?",
            font=FONTS["regular"],
            text_color=COLORS["accent"],
            cursor="hand2"
        )
        self.forgot_label.pack(anchor="e", padx=75)
        self.forgot_label.bind("<Button-1>", lambda e: self.forgot_password())

        self.signup_label = ctk.CTkLabel(
            self.right_frame,
            text="Немає акаунту? Зареєструйтесь",
            font=FONTS["regular"],
            text_color=COLORS["accent"],
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
                auth.IS_USER_LOGGED_IN = True
                auth.USER = username
                print(username)
                print(auth.IS_USER_LOGGED_IN)
                if self.remember_var.get():
                    CTkMessagebox(
                        title="Інформація",
                        message="Дані для входу збережено!",
                        icon="info",
                        fg_color=COLORS["white"],
                        title_color=COLORS["text"],
                        button_color=COLORS["primary"],
                        button_hover_color=COLORS["primary_hover"]
                    )
                self.destroy()
                self.on_success()
                return True
            else:
                CTkMessagebox(
                    title="Помилка",
                    message="Невірний логін або пароль.",
                    icon="warning",
                    fg_color=COLORS["white"],
                    title_color=COLORS["text"],
                    button_color=COLORS["primary"],
                    button_hover_color=COLORS["primary_hover"]
                )
            return False
        else:
            CTkMessagebox(
                title="Помилка",
                message="Будь ласка, введіть логін і пароль.",
                icon="warning",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
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
                    fg_color=COLORS["white"],
                    title_color=COLORS["text"],
                    button_color=COLORS["primary"],
                    button_hover_color=COLORS["primary_hover"]
                )
            else:
                CTkMessagebox(
                    title="Помилка",
                    message=f"Користувача '{username}' не знайдено.",
                    icon="warning",
                    fg_color=COLORS["white"],
                    title_color=COLORS["text"],
                    button_color=COLORS["primary"],
                    button_hover_color=COLORS["primary_hover"]
                )
        else:
            CTkMessagebox(
                title="Помилка",
                message="Будь ласка, введіть логін.",
                icon="warning",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
            )

    def signup(self):
        signup_window = ctk.CTkToplevel(self)
        signup_window.grab_set()
        signup_window.title("Реєстрація")
        signup_window.geometry("400x500")
        signup_window.configure(fg_color=COLORS["white"])

        ctk.CTkLabel(
            signup_window,
            text="Реєстрація",
            font=FONTS["title"],
            text_color=COLORS["text"]
        ).pack(pady=(20, 10))

        username_entry = ctk.CTkEntry(
            signup_window,
            placeholder_text="Логін",
            placeholder_text_color=COLORS["secondary_text"],
            width=250,
            height=40,
            font=FONTS["regular"],
            fg_color=COLORS["background"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=5,
            text_color=COLORS["text"]
        )
        username_entry.pack(pady=5)
        username_entry.bind("<Return>", lambda e: signup_button.invoke())  # Додаємо прив’язку Enter

        password_entry = ctk.CTkEntry(
            signup_window,
            placeholder_text="Пароль",
            placeholder_text_color=COLORS["secondary_text"],
            show="•",
            width=250,
            height=40,
            font=FONTS["regular"],
            fg_color=COLORS["background"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=5,
            text_color=COLORS["text"]
        )
        password_entry.pack(pady=5)
        password_entry.bind("<Return>", lambda e: signup_button.invoke())  # Додаємо прив’язку Enter

        email_entry = ctk.CTkEntry(
            signup_window,
            placeholder_text="Електронна пошта",
            placeholder_text_color=COLORS["secondary_text"],
            width=250,
            height=40,
            font=FONTS["regular"],
            fg_color=COLORS["background"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=5,
            text_color=COLORS["text"]
        )
        email_entry.pack(pady=5)
        email_entry.bind("<Return>", lambda e: signup_button.invoke())  # Додаємо прив’язку Enter

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
                    fg_color=COLORS["white"],
                    title_color=COLORS["text"],
                    button_color=COLORS["primary"],
                    button_hover_color=COLORS["primary_hover"]
                )
                if "успішно" in result:
                    auth.IS_USER_LOGGED_IN = True  # Встановлюємо True після успішної реєстрації
                    auth.USER = username
                    signup_window.after(100, signup_window.destroy)
                    self.destroy()
                    self.on_success()
                    return True
            else:
                CTkMessagebox(
                    title="Помилка",
                    message="Будь ласка, заповніть усі поля.",
                    icon="warning",
                    fg_color=COLORS["white"],
                    title_color=COLORS["text"],
                    button_color=COLORS["primary"],
                    button_hover_color=COLORS["primary_hover"]
                )
            return False

        signup_button = ctk.CTkButton(
            signup_window,
            text="Зареєструватись",
            width=250,
            height=40,
            font=FONTS["regular"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["white"],
            corner_radius=5,
            command=perform_signup
        )
        signup_button.pack(pady=20)

    def skip_login(self):
        self.destroy()
        self.on_success()  # Змінено на on_success для переходу до афіші

    def on_closing(self):
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
            self.parent.destroy()