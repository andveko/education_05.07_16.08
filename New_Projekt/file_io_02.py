# Импортируем модуль tkinter и все его компоненты.
# Для создания графического пользовательского интерфейса.
from tkinter import *
# Импортируем модуль requests. Для
# взаимодействия со страницами в интернете.
import requests
# Импортируем модуль pyperclip. Этот модуль
# позволяет копировать и вставлять текст в буфер обмена.
import pyperclip
# Из tkinter импортируем filedialog и messagebox.
# Модуль filedialog позволяет открывать файлы.
# Модуль messagebox, для создания окон
# с сообщениями пользователю.
from tkinter import filedialog, messagebox
# Импортируем модуль ttk.
# Расширяем стандартную библиотеку tkinter.
from tkinter import ttk
# Импортируем модуль json.
# Модуль json позволят кодировать и
# декодировать данные в удобном формате.
import json
# Импортируем модуль os. Предоставляет различные
# функции для взаимодействия с операционной системой.
import os


# Файл с историей загрузок.
# Файл содержит данные в формате json.
history_file = "upload_history.json"


# Функция сохранения истории загрузок файлов. В качестве
# аргументов функция принимает путь к файлу и ссылку на файл.
def save_history(file_path, download_link):
    # Список для хранения истории загрузок.
    history = []
    # Проверяем, чтобы путь к файлу существует.
    if os.path.exists(history_file):
        # Если путь к файлу существует, то открываем файл для чтения.
        with open(history_file, "r") as file:
            # Загружаем в переменную содержания файла.
            history = json.load(file)
    # Добавляем новую информацию в имеющиеся у нас данные.
    history.append({"file_path": os.path.basename(file_path), "download_link": download_link})
    # Открываем файл истории загрузок.
    # Файл открываем для перезаписи.
    with open(history_file, "w") as file:
        # Записываем историю загрузок в файл в формате json.
        json.dump(history, file, indent=4)


# Функция для показа истории, в отдельном окне.
def show_history():
    # Делаем проверку существования истории загрузок.
    if not os.path.exists(history_file):
        # Если история пустая, то выводим сообщение пользователю.
        messagebox.showinfo("История", "История загрузок пуста")
        # Выходим из функции.
        return

    # Создаем вторичное окно.
    history_window = Toplevel(window)
    # Заголовок вторичного окна
    history_window.title("История Загрузок")

    # Виджет многострочного окна Text.
    # Цвет заднего фона окна белый, цвет текста черный.
    files_listbox = Text(history_window, bg='white', fg='black')
    # Упаковываем виджет с отступами со всех сторон.
    files_listbox.pack(padx=10, pady=10)
    # Открываем файл с историей загрузок.
    # Файл открываем для чтения.
    with open(history_file, "r") as file:
        # В переменную history загружаем
        # содержимое файла истории, в формате json.
        history = json.load(file)
        # Цикл для перебора данных файла.
        for item in history:
            # Присваиваем переменной значение
            # содержащиеся в значении item['file_path'].
            file_path = item['file_path']
            # Присваиваем переменной значение
            # содержащиеся в значении item['download_link'].
            download_link = item['download_link']
            # Из полученных значений, с помощью f-строки создаем строку.
            # В конце строки вставляем управляющий символ переноса строки.
            create_string = f'Файл: {file_path},  Ссылка: {download_link}\n'
            # Вставляем полученную строку в виджет Text.
            files_listbox.insert(END, create_string)
    # С помощью виджета ttk создаем кнопку закрытия вторичного окна.
    close_button = ttk.Button(history_window, text='Закрыть', command=history_window.destroy)
    # Упаковываем кнопку закрытия вторичного окна, и размещаем её внизу окна.
    close_button.pack(side=BOTTOM, padx=10, pady=(0, 10))


# Функция для загрузки фалов на сайт.
def upload():
    # Для обработки возможных возникших ошибок применяем конструкцию: try...except
    try:
        # Получаем путь к файлу который хотим загрузить на сайт.
        # Выбор файла открывается в новом отдельном окне.
        filepath = filedialog.askopenfilename()
        # Если файл существует,
        if filepath:
            # то открываем файл в бинарном режиме для чтения.
            with open(filepath, 'rb') as f:
                files = {'file': f}
                # Отправляем запрос post на сайт.
                response = requests.post('https://file.io', files=files)
                # Проверка на ошибки HTTP.
                response.raise_for_status()
                # Из ответа сервера получаем ссылку на загруженный файл.
                download_link = response.json().get('link')
                if download_link:
                    # Очищаем поле вывода ссылки на файл для загрузки.
                    link_entry.delete(0, END)
                    # Вставляем новую полученную ссылку.
                    link_entry.insert(0, download_link)
                    # Копирование ссылки в буфер обмена.
                    pyperclip.copy(download_link)
                    # Вызов функции сохранения истории загрузок.
                    save_history(filepath, download_link)
                    # Выводим сообщение пользователю, о том, что ссылка скопирована в буфер обмена.
                    messagebox.showinfo("Ссылка скопирована", "Ссылка успешно скопирована в буфер обмена")
    # Обработка возникающих исключений.
    except Exception as e:
        # Выводим в отдельном окне сообщение о возникшей ошибке, с описанием самой ошибки.
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


# Создаем окно программы.
window = Tk()
# Заголовок окна программы.
window.title("Сохранение файлов в облаке")
# Размеры окна программы.
window.geometry('400x250')
# Создаем метку с предупреждением,
# что файл не должен быть более 2 Гб.
label_1 = Label(text='Загрузите файлы, размером до 2 ГБ')
# Упаковываем метку, с отступом сверху и без отступа снизу.
label_1.pack(padx=10, pady=(10, 0))
# Создаем метку для продолжения фразы с предупреждением.
label_2 = Label(text='и получите ссылку, которой можно поделиться')
# Упаковываем метку, чтобы фраза смотрелась хорошо, убираем отступ сверху.
label_2.pack(padx=10, pady=(0, 10))
# С помощью расширенного модуля ttk создаем кнопку
# для загрузки файлов на сайт 'https://file.io'.
upload_button = ttk.Button(text="Загрузить файл", width=27, command=upload)
# Упаковываем кнопку загрузки файлов.
upload_button.pack(padx=10, pady=10)
# Создаем поле для вставки ссылки полученной после загрузки файла.
link_entry = ttk.Entry(width=28)
# Упаковываем поле.
link_entry.pack(padx=10, pady=10)
# Кнопка для показа истории загруженных файлов.
history_button = ttk.Button(window, text="Показать Историю", width=27, command=show_history)
# Упаковываем кнопку.
history_button.pack(padx=10, pady=10)
# Кнопка "Выход"
exit_button = ttk.Button(text='Выход', command=window.destroy)
# Упаковываем кнопку "Выход".
# Кнопку устанавливаем внизу окна программы.
# С отступами по горизонтали и вертикали.
exit_button.pack(side=BOTTOM, padx=10, pady=(0, 10))
# Запускаем главный цикл программы.
window.mainloop()
