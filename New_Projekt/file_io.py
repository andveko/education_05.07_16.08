from tkinter import *
import requests
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk

def upload():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()  # Проверка на ошибки HTTP
                download_link = response.json().get('link')
                if download_link:
                    link_entry.delete(0, END)
                    link_entry.insert(0, download_link)
                else:
                    raise ValueError("Не удалось получить ссылку для скачивания")
    except ValueError as ve:
        mb.showerror("Ошибка", f"Произошла ошибка: {ve}")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")


window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry('400x200')

upload_button = ttk.Button(text="Загрузить файл", width=29, command=upload)
upload_button.pack(padx=10, pady=10)

link_entry = ttk.Entry(width=30)
link_entry.pack(padx=10, pady=10)

# Кнопка "Выход"
exit_button = ttk.Button(text='Выход', command=window.destroy)
# Упаковываем кнопку "Выход".
# Кнопку устанавливаем в правом нижнем углу, окна программы.
# С отступами по горизонтали и вертикали.
exit_button.pack(side=BOTTOM,padx=10, pady=(0, 10))

window.mainloop()