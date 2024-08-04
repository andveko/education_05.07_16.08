from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

def load_image(url):
    try:
        # Отправляем GET-запрос с использованием requests.get()
        response = requests.get(url)

        # Проверяем успешность запроса (код ответа 200)
        response.raise_for_status()

        # Читаем байты из ответа в объект BytesIO
        image_data = BytesIO(response.content)

        # Открываем изображение с помощью PIL
        img = Image.open(image_data)
        # Изменяем размер изображения
        img.thumbnail((600, 480), Image.Resampling.LANCZOS)

        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

def set_image():
    # Вызываем функцию для загрузки изображения
    img = load_image(url)

    if img:
        # Устанавливаем изображение в метку
        label.config(image=img)
        label.image = img

window = Tk()
window.title("Cats!")
window.geometry("600x550")

# Создаем метку без изображения
label = Label()
label.pack()

# # Добавляем кнопку для обновления изображения
# update_button = Button(text="Обновить", command=set_image)
# update_button.pack()

# Создаем меню
menu_bar = Menu(window)
window.config(menu=menu_bar)

# Добавляем пункты меню
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Загрузить фото", command=set_image)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=exit)

# Кнопка "Выход"
exit_button = Button(text='Выход', command=window.destroy)
# Упаковываем кнопку "Выход".
# Кнопку устанавливаем в правом нижнем углу, окна программы.
# С отступами по горизонтали и вертикали.
exit_button.pack(side=RIGHT, padx=10, pady=10)

url = 'https://cataas.com/cat'
# Вызываем функцию для установки изображения в метку
set_image()

# img = load_image(url)

# if img:
#     # Устанавливаем изображение в метку
#     label.config(image=img)
#     # Необходимо сохранить ссылку на изображение, чтобы избежать сборки мусора
#     label.image = img

window.mainloop()
