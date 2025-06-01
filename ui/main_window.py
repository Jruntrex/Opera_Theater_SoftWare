import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox

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

class TheaterHomeWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_schedule, on_login):
        super().__init__(parent)
        self.parent = parent
        self.on_schedule = on_schedule
        self.on_login = on_login
        self.title("Театр Березіль")
        self.geometry("1200x840+200+0")
        self.configure(fg_color=COLORS["background"])
        self.resizable(False, False)
        # self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Додаємо ефект фону
        self.bg_canvas = ctk.CTkCanvas(self, bg=COLORS["background"], highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)

        # Хедер
        self.header_frame = ctk.CTkFrame(self.bg_canvas, fg_color=COLORS["white"], height=90, corner_radius=0,
                                         border_width=1, border_color=COLORS["border"])
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        self.header_frame.grid_columnconfigure((0, 2), weight=1)
        self.header_frame.grid_columnconfigure(1, weight=4)

        # Логотип
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

        # Головний контент
        self.main_frame = ctk.CTkFrame(self.bg_canvas, fg_color="transparent", corner_radius=0)
        self.main_frame.pack(pady=30, padx=40, fill="both", expand=True)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.main_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Банер
        try:
            self.banner_image = Image.open("ui/images_performance/theatre.png")
            self.banner_image = self.banner_image.resize((750, 375))
            self.banner_photo = ctk.CTkImage(self.banner_image, size=(750, 375))
            self.banner_label = ctk.CTkLabel(self.main_frame, image=self.banner_photo, text="")
            self.banner_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

            self.overlay_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.overlay_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
            self.overlay_frame.lower()

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

        # Вітальний блок
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

        # Кнопки
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

        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="🔐 Увійти",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.open_login,
            **button_style
        )
        self.login_button.grid(row=2, column=1, padx=20, pady=20)
        self.login_button.configure(fg_color=[COLORS["gradient_start"], COLORS["gradient_end"]])

        # Футер
        self.footer_frame = ctk.CTkFrame(self.bg_canvas, fg_color=COLORS["white"], height=70, corner_radius=0,
                                         border_width=1, border_color=COLORS["border"])
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
        self.destroy()
        self.on_schedule()

    def open_login(self):
        self.destroy()
        self.on_login()

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

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
