import os
import threading
import time
from tkinter import messagebox, simpledialog

from pynput import keyboard, mouse

correct_password = "1234"
time_left = 10
password_correct = threading.Event()
password_correct = False
countdown_started = False


def show_password_dialog():
    global password_correct
    password = simpledialog.askstring("Mot de passe requis", "Entrez le mot de passe:")

    if password == correct_password:
        messagebox.showinfo("Accès autorisé", "Mot de passe correct!")
        password_correct = True
        listener.stop()

    else:
        messagebox.showinfo("Accès refusé", "Explosion imminente!")


def countdown():
    time.sleep(10)

    if not password_correct:
        print("End of countdown. Rebooting computer.")
        put_to_sleep()


def on_press(key):
    global countdown_started, listener

    if not countdown_started:
        mouse_listener.stop()
        countdown_started = True
        main_thread = threading.Thread(target=countdown)
        main_thread.start()
        seconde_thread = threading.Thread(target=show_password_dialog)
        seconde_thread.start()


def start_keyboard_listener():
    global listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def put_to_sleep():
    if os.name == "nt":  # Pour Windows
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif (
        os.name == "posix"
    ):  # Pour macOS (et Linux, mais nécessite généralement l'installation supplémentaire pm-utils)
        os.system("pmset sleepnow")


def disable_mouse():
    def on_move(x, y):
        # Bloque le mouvement de la souris en la replaçant sur le même point

        mouse_controller.position = (0, 0)

        return False

    global mouse_listener
    mouse_listener = mouse.Listener(on_move=on_move)
    mouse_listener.start()


if __name__ == "__main__":
    mouse_controller = mouse.Controller()
    disable_mouse()
    start_keyboard_listener()
