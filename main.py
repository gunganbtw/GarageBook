# В файле main.txt:

from gui.autentefication_window import AuthWindow
from gui.mainwindow import MainWindow

def on_login_success(user_data):
    auth_window.root.destroy()
    # user_data - это кортеж (user_id, username, full_name, email)
    main_window = MainWindow(user_data[0])  # передаем user_id
    main_window.run()

if __name__ == "__main__":
    try:
        auth_window = AuthWindow(on_login_success)
        auth_window.run()
    except Exception as e:
        print(f"Ошибка в программе: {e}")
        import sys
        sys.exit(1)