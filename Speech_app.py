from ttkthemes import ThemedStyle
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from ttkthemes.themed_tk import ThemedTk
from tkinter import filedialog
from PIL import Image, ImageTk

import threading
import speech_recognition as sr
import os
import time


splash_root = tk.Tk()

splash_root.title("Speech Recognition In Indian Languages")


splash_image = Image.open("S@T.png")
splash_photo = ImageTk.PhotoImage(splash_image)


splash_label = tk.Label(splash_root, image=splash_photo)
splash_label.pack()


splash_root.update()


screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()


image_width = splash_photo.width()
image_height = splash_photo.height()


x = (screen_width // 2) - (image_width // 2)
y = (screen_height // 2) - (image_height // 2)


splash_root.geometry(f"{image_width}x{image_height}+{x}+{y}")

time.sleep(4)

splash_root.destroy()


root = ThemedTk(theme="black")
root.title("Speech Recognition")
root.geometry("400x350")


bg_color = "#191970"  # Black color
fg_color = "#FFFFFF"  # White color
button_color = "#FFA500"
font_style = Font(family="Sans-serif", size=10, weight="bold")
title_font_style = Font(family="Sans-serif", size=16, weight="bold")


root.configure(bg=bg_color)


title_frame = tk.Frame(root, bg=bg_color)
title_frame.pack(fill="x", padx=20, pady=10)


title_label = ttk.Label(title_frame, text="Speech Recognition App", font=title_font_style, background=bg_color, foreground=fg_color)
title_label.pack()


style = ThemedStyle()
style.configure("TButton", background=button_color, foreground="white", font=font_style, relief="flat")


# Function definitions
def take_speech(language):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        update_status("Listening...", "yellow")
        r.pause_threshold = 0.7
        audio = r.listen(source)

        try:
            update_status("Recognizing...", "yellow")
            query = r.recognize_google(audio, language=language)
            update_result(f"Recognized Text: {query}", "white")

        except sr.UnknownValueError:
            update_result("Could not understand audio, please say that again.", "red")

        except sr.RequestError as e:
            update_result(f"Could not request results; {e}", "red")

        except Exception as e:
            update_result(f"An error occurred: {e}", "red")

        finally:
            progress.stop()


def on_select():
    language = language_var.get()
    if language in ["Hindi", "Kannada", "Tamil", "Bengali", "Marathi"]:
        progress.start()
        threading.Thread(target=take_speech, args=(language_codes[language],)).start()


def update_status(message, color):
    status_var.set(message)
    status_label.config(foreground=color)


def update_result(message, color):
    status_var.set("")
    result_var.set(message)
    result_label.config(foreground=color)


def clear_text():
    result_var.set("")
    status_var.set("")


# GUI elements
language_label = ttk.Label(root, text="Select a Language:", font=("Helvetica", 10, "bold"), background=bg_color, foreground=fg_color)
language_label.pack(pady=5)

language_var = tk.StringVar()
language_menu = ttk.Combobox(root, textvariable=language_var)
language_menu['values'] = ("Hindi", "Kannada", "Tamil", "Bengali", "Marathi", "Telugu")
language_menu.set("language..")


def on_combo_box_click(event):
    if language_var.get() == "language..":
        language_menu.set("")


def save_transcription():

    transcription = result_var.get()

    file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

    if file_path:
        with open(file_path, "w",encoding='utf-8') as file:
            file.write(transcription)


language_menu.bind("<FocusIn>",on_combo_box_click)
language_menu.pack(pady=5)

button = ttk.Button(root, text="Start Recognition", command=on_select)
button.pack(pady=10)

button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(side="bottom", fill="x")

# # Recognition button
# button = ttk.Button(button_frame, text="Start Recognition", command=on_select)
# button.pack(side="left", padx=(20, 10), pady=10)

save_button = ttk.Button(button_frame, text="Save Transcription", command=save_transcription)
save_button.pack(side="right", padx=(10, 130), pady=15)

status_var = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_var, font=("Arial", 10), foreground="white", background=bg_color)
status_label.pack(pady=5)

progress = ttk.Progressbar(root, mode='indeterminate')
progress.pack(pady=5)

result_var = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_var, font=("Arial", 12), wraplength=380, foreground="white", background=bg_color)
result_label.pack(pady=10)

clear_button = ttk.Button(root, text="Clear Text", command=clear_text)
clear_button.pack(pady=10)

language_codes = {
    "Hindi": "hi-IN",
    "Kannada": "kn-IN",
    "Tamil": "ta-IN",
    "Bengali": "bn-IN",
    "Telugu": "te-IN",
    "Marathi": "mr-IN"
}

root.mainloop()
