from gui.autentefication_window import AuthWindow
from gui.mainwindow import MainWindow

def on_login_success(user_id):
    auth_window.root.destroy()
    main_window = MainWindow(user_id)
    main_window.run()

if __name__ == "__main__":
    auth_window = AuthWindow(on_login_success)
    auth_window.run()