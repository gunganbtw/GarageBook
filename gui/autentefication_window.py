import customtkinter as ctk
from database.GarageBase import verify_user, add_user


class AuthWindow:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success

        self.root = ctk.CTk()
        self.root.title("GarageBook - Авторизация")
        self.root.geometry("400x700")

        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame,
            text="GarageBook",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(20, 10))

        # Переключатель между входом и регистрацией
        self.auth_mode = ctk.StringVar(value="login")
        login_radio = ctk.CTkRadioButton(
            main_frame,
            text="Вход",
            variable=self.auth_mode,
            value="login",
            command=self.toggle_auth_mode
        )
        register_radio = ctk.CTkRadioButton(
            main_frame,
            text="Регистрация",
            variable=self.auth_mode,
            value="register",
            command=self.toggle_auth_mode
        )
        login_radio.pack(pady=5)
        register_radio.pack(pady=5)

        # Поля для ввода
        self.username_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Имя пользователя"
        )
        self.username_entry.pack(pady=10, padx=20, fill="x")

        self.password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Пароль",
            show="*"
        )
        self.password_entry.pack(pady=10, padx=20, fill="x")

        # Дополнительные поля для регистрации
        self.full_name_label = ctk.CTkLabel(
            main_frame,
            text="Полное имя:",
            state="disabled"
        )
        self.full_name_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Иванов Иван Иванович",
            state="disabled"
        )

        self.email_label = ctk.CTkLabel(
            main_frame,
            text="Email (необязательно):",
            state="disabled"
        )
        self.email_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="example@mail.com",
            state="disabled"
        )

        # Кнопка подтверждения
        self.submit_btn = ctk.CTkButton(
            main_frame,
            text="Войти",
            command=self.handle_submit
        )
        self.submit_btn.pack(pady=20, padx=20, fill="x")

        # Сообщение об ошибке/успехе
        self.message_label = ctk.CTkLabel(
            main_frame,
            text="",
            text_color="red"
        )
        self.message_label.pack(pady=5)

    def toggle_auth_mode(self):
        mode = self.auth_mode.get()

        if mode == "register":
            self.full_name_label.pack(pady=(10, 0), padx=20, anchor="w")
            self.full_name_entry.pack(pady=(0, 10), padx=20, fill="x")
            self.full_name_entry.configure(state="normal")
            self.full_name_label.configure(state="normal")

            self.email_label.pack(pady=(10, 0), padx=20, anchor="w")
            self.email_entry.pack(pady=(0, 10), padx=20, fill="x")
            self.email_entry.configure(state="normal")
            self.email_label.configure(state="normal")

            self.submit_btn.configure(text="Зарегистрироваться")
        else:
            self.full_name_label.pack_forget()
            self.full_name_entry.pack_forget()
            self.email_label.pack_forget()
            self.email_entry.pack_forget()

            self.submit_btn.configure(text="Войти")

    def handle_submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.show_message("Имя пользователя и пароль обязательны!")
            return

        if self.auth_mode.get() == "login":
            user = verify_user(username, password)
            if user:
                self.show_message("Успешный вход!", is_error=False)
                self.root.after(1000, lambda: self.on_login_success(user[0]))
            else:
                self.show_message("Неверное имя пользователя или пароль")
        else:
            full_name = self.full_name_entry.get()
            if not full_name:
                self.show_message("Полное имя обязательно для регистрации")
                return

            email = self.email_entry.get()
            success = add_user(username, password, full_name, email)

            if success:
                self.show_message("Регистрация успешна! Теперь вы можете войти.", is_error=False)
                self.auth_mode.set("login")
                self.toggle_auth_mode()
            else:
                self.show_message("Имя пользователя уже занято")

    def show_message(self, text, is_error=True):
        self.message_label.configure(
            text=text,
            text_color="red" if is_error else "green"
        )
        self.root.after(3000, lambda: self.message_label.configure(text=""))

    def run(self):
        self.root.mainloop()