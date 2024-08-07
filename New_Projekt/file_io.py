from tkinter import *
import requests
import pyperclip
from tkinter import filedialog, messagebox
from tkinter import ttk
import json
import os


history_file = "upload_history.json"


def save_history(file_path, download_link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            history = json.load(file)

    history.append({"file_path": os.path.basename(file_path), "download_link": download_link})

    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)


def show_history():
    if not os.path.exists(history_file):
        messagebox.showinfo("История", "История загрузок пуста")
        return

    history_window = Toplevel(window)
    history_window.title("История Загрузок")

    files_listbox = Listbox(history_window, width=50, height=20)
    files_listbox.grid(row=0, column=0, padx=(10,0), pady=10)

    links_listbox = Listbox(history_window, width=50, height=20)
    links_listbox.grid(row=0, column=1, padx=(0,10), pady=10)

    with open(history_file, "r") as file:
        history = json.load(file)
        for item in history:
            files_listbox.insert(END, item['file_path'])
            links_listbox.insert(END, item['download_link'])


def upload():
    try:
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()  # Проверка на ошибки HTTP
                download_link = response.json().get('link')
                if download_link:
                    link_entry.delete(0, END)
                    link_entry.insert(0, download_link)
                    pyperclip.copy(download_link)  # Копирование ссылки в буфер обмена
                    save_history(filepath, download_link)
                    messagebox.showinfo("Ссылка скопирована", "Ссылка успешно скопирована в буфер обмена")
                else:
                    raise ValueError("Не удалось получить ссылку для скачивания")
    except ValueError as ve:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {ve}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry('300x200')

upload_button = ttk.Button(text="Загрузить файл", width=27, command=upload)
upload_button.pack(padx=10, pady=10)

link_entry = ttk.Entry(width=28)
link_entry.pack(padx=10, pady=10)

history_button = ttk.Button(window, text="Показать Историю", width=27, command=show_history)
history_button.pack(padx=10, pady=10)

# Кнопка "Выход"
exit_button = ttk.Button(text='Выход', command=window.destroy)
# Упаковываем кнопку "Выход".
# Кнопку устанавливаем в правом нижнем углу, окна программы.
# С отступами по горизонтали и вертикали.
exit_button.pack(side=BOTTOM, padx=10, pady=(0, 10))

window.mainloop()