import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkImage
from PIL import Image
import os


class MainWindow:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = CTk()


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
        # Блок аккаунта
        self.account_frame = CTkFrame(self.root, width=200, height=80, fg_color="grey")
        self.account_frame.place(
            relx=0.115,
            rely=0.095,
            anchor="ne"
        )

        self.buttons_frame = CTkFrame(
            self.root,
            width=350,
            height=550,
            fg_color="grey"
        )
        self.buttons_frame.pack_propagate(False)
        self.buttons_frame.place(
            relx=0.06,
            rely=0.51,
            anchor="center"
        )

        # Блок контактов
        self.contacts_frame = CTkFrame(self.root, width=250, height=100, fg_color="grey")
        self.contacts_frame.place(
            relx=0.12,
            rely=0.92,
            anchor="se"
        )

        # Добавляем элементы в блоки
        self.add_account_elements()
        self.add_buttons_elements()
        self.add_contacts_elements()

    def add_account_elements(self):
        CTkButton(
            self.account_frame,
            text="Аккаунт",
            command=self.show_account_menu
        ).pack(pady=10)

    def add_buttons_elements(self):
        CTkLabel(
            self.buttons_frame,
            text="Основные кнопки",
            font=("Arial", 24)
        ).pack(pady=50)

    def add_contacts_elements(self):
        CTkLabel(
            self.contacts_frame,
            text="Контакты:\nТелефон: +7 (960) 003-96-86\nEmail: garagebook@gmail.com"
        ).pack(pady=10)

    def show_account_menu(self):
        menu = CTkFrame(self.root, width=200, height=120, fg_color="white")
        menu.place(
            relx=0.115,
            rely=0.15,
            anchor="ne"
        )

        CTkButton(menu, text="Настройки").pack(pady=5)
        CTkButton(
            menu,
            text="Выйти",
            fg_color="red",
            command=self.logout
        ).pack(pady=5)

    def logout(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()