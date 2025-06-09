import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkImage
from PIL import Image
import os
from gui.side_window import SideWindow


class MainWindow:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = CTk()
        self.active_window = None

        self.root.attributes('-fullscreen', True)
        self.setup_background()
        self.create_interface()

    def setup_background(self):
        try:
            bg_path = os.path.join("assets", "bg_main.png")
            img = Image.open(bg_path)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            self.bg_image = CTkImage(
                light_image=img,
                dark_image=img,
                size=(screen_width, screen_height))

            bg_label = CTkLabel(self.root, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            self.root.configure(bg="white")

    def create_interface(self):
        # Блок аккаунта (восстановлен)
        self.account_frame = CTkFrame(self.root, width=100, height=90, fg_color="#6989e0")
        self.account_frame.place(relx=0.115, rely=0.181, anchor="ne")

        # Кнопка аккаунта
        self.account_btn = CTkButton(
            self.account_frame,
            text="Аккаунт",
            command=self.show_account_menu
        )
        self.account_btn.pack(pady=0)

        # Блок кнопок
        self.buttons_frame = CTkFrame(self.root, width=350, height=550, fg_color="#40486c")
        self.buttons_frame.pack_propagate(False)
        self.buttons_frame.place(relx=0.06, rely=0.51, anchor="center")

        # Блок контактов
        self.contacts_frame = CTkFrame(self.root, width=250, height=100, fg_color="#40336b")
        self.contacts_frame.place(relx=0.12, rely=0.92, anchor="se")

        # Контактные данные
        CTkLabel(
            self.contacts_frame,
            text="Контакты:\nТелефон: +7 (960) 003-96-86\nEmail: garagebook@gmail.com"
        ).pack(pady=0)

        # Основные кнопки
        buttons = [
            ("Гараж", self.open_garage_window),
            ("История поломок", self.open_repairs_window),
            ("Замена расходников", self.open_parts_window),
            ("Форумы", self.open_forums_window)
        ]

        for text, command in buttons:
            btn = CTkButton(
                self.buttons_frame,
                text=text,
                font=("Arial", 18),
                height=50,
                command=command
            )
            btn.pack(pady=15, fill="x")

    def show_account_menu(self):
        """Меню аккаунта (восстановлено)"""
        self.account_menu = CTkFrame(self.root, width=100, height=80, fg_color="#6989e0")
        self.account_menu.place(relx=0.115, rely=0.215, anchor="ne")

        CTkButton(
            self.account_menu,
            text="Выйти",
            fg_color="red",
            width=140,
            command=self.logout
        ).pack(pady=0)

    def logout(self):
        self.root.destroy()

    def open_window(self, title):
        if self.active_window:
            self.active_window.destroy()
        self.active_window = SideWindow(self.root, title, self.user_id)  # Передаем user_id
        self.active_window.focus_set()

    def open_garage_window(self):
        self.open_window("Гараж")

    def open_repairs_window(self):
        self.open_window("История поломок")

    def open_parts_window(self):
        self.open_window("Замена расходников")

    def open_forums_window(self):
        self.open_window("Форумы")

    def run(self):
        self.root.mainloop()

