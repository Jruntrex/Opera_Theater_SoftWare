import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from ui.main_window import TheaterHomeWindow
from ui.login import LoginWindow
from ui.performance_window import TheaterMainWindow

# Константи стилів
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

class TheaterApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Ініціалізація змінних для вікон
        self.login_window = None
        self.home_window = None
        self.main_window = None
        self.temp_root = ctk.CTk()
        self.temp_root.withdraw()  # Ховаємо тимчасове кореневе вікно

        # Відкриваємо домашню сторінку
        self.show_home_window()

    def show_login_window(self):
        print("Відкривається LoginWindow")
        # Закриваємо інші Toplevel-вікна
        if self.home_window:
            self.home_window.destroy()
            self.home_window = None
        if self.main_window:
            self.main_window.destroy()
            self.main_window = None

        # Перевіряємо, чи попередні вікна закрито, і створюємо LoginWindow з затримкою
        self.temp_root.after(100, self._create_login_window)

    def _create_login_window(self):
        # Перевіряємо, чи HomeWindow або MainWindow повністю закрито
        if (self.home_window and self.home_window.winfo_exists()) or \
                (self.main_window and self.main_window.winfo_exists()):
            print("Чекаємо закриття HomeWindow або MainWindow")
            self.temp_root.after(100, self._create_login_window)
            return

        # Створюємо LoginWindow
        self.login_window = LoginWindow(
            self.temp_root,
            on_success=self.on_login_success,
            on_back=self.show_home_window  # Повернення до Home
        )

    def on_login_success(self):
        print("Вхід успішний, перехід до TheaterMainWindow")
        # Знищуємо LoginWindow
        if self.login_window:
            self.login_window.destroy()
            self.login_window = None
        # Переходимо до MainWindow з затримкою
        self.temp_root.after(100, self._create_main_window)

    def show_home_window(self):
        print("Відкривається TheaterHomeWindow")
        # Закриваємо інші Toplevel-вікна
        if self.login_window:
            self.login_window.destroy()
            self.login_window = None
        if self.main_window:
            self.main_window.destroy()
            self.main_window = None

        # Перевіряємо, чи попередні вікна закрито, і створюємо HomeWindow з затримкою
        self.temp_root.after(100, self._create_home_window)

    def _create_home_window(self):
        # Перевіряємо, чи LoginWindow або MainWindow повністю закрито
        if (self.login_window and self.login_window.winfo_exists()) or \
                (self.main_window and self.main_window.winfo_exists()):
            print("Чекаємо закриття LoginWindow або MainWindow")
            self.temp_root.after(100, self._create_home_window)
            return

        # Створюємо HomeWindow
        self.home_window = TheaterHomeWindow(
            self.temp_root,
            on_schedule=self.show_main_window,
            on_login=self.show_login_window
        )

    def show_main_window(self):
        print("Відкривається TheaterMainWindow")
        # Закриваємо інші Toplevel-вікна
        if self.login_window:
            self.login_window.destroy()
            self.login_window = None
        if self.home_window:
            self.home_window.destroy()
            self.home_window = None

        # Переходимо до створення MainWindow з затримкою
        self.temp_root.after(100, self._create_main_window)

    def _create_main_window(self):
        # Перевіряємо, чи попередні вікна закрито
        if (self.login_window and self.login_window.winfo_exists()) or \
                (self.home_window and self.home_window.winfo_exists()):
            print("Чекаємо закриття LoginWindow або HomeWindow")
            self.temp_root.after(100, self._create_main_window)
            return

        # Створюємо MainWindow
        self.main_window = TheaterMainWindow(
            self.temp_root,  # Передаємо temp_root як батьківське вікно
            on_back=self.show_home_window  # Повернення до Home
        )

    def close_app(self):
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
            # Закриваємо всі вікна
            if self.main_window:
                self.main_window.destroy()
                self.main_window = None
            if self.login_window:
                self.login_window.destroy()
                self.login_window = None
            if self.home_window:
                self.home_window.destroy()
                self.home_window = None
            if self.temp_root:
                self.temp_root.destroy()
                self.temp_root = None

    def run(self):
        # Запускаємо цикл подій
        self.temp_root.mainloop()

if __name__ == "__main__":
    app = TheaterApp()
    app.run()