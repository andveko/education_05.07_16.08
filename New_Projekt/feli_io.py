from tkinter import *
import requests
from tkinter import filedialog as fd
from tkinter import ttk

def upload():
    filepath = fd.askopenfilename()
    if filepath:
        files = {'file': open(filepath, 'rb')}
        response = requests.post('https://file.io', files=files)
        if response.status_code == 200:
            download_link = response.json()['link']
            link_entry.insert(0, download_link)

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