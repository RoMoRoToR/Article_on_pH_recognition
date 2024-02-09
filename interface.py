import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Функция для загрузки и анализа изображения
def load_and_analyze_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=50, param2=30, minRadius=20, maxRadius=200)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(image, (x, y), r, (0, 255, 0), 4)
                # Вместо анализа центра круга здесь для демонстрации просто выделяем его

            # Конвертация изображения для отображения в Tkinter
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=im_pil)
            image_label.config(image=imgtk)
            image_label.photo = imgtk

            # Отображение оценочного значения pH (заглушка)
            ph_value_label.config(text="Оценочное значение pH: TBD")

            # Построение графика (заглушка)
            plot_ph_curve()
        else:
            ph_value_label.config(text="Круги не обнаружены.")

# Функция для построения графика зависимости цвета от pH
def plot_ph_curve():
    # Заглушка для графика
    ph_values = np.array([5.7, 6.3, 6.9, 7.5, 8.0])
    color_values = np.array([50, 100, 150, 200, 250])  # Примерные значения цвета
    cs = CubicSpline(ph_values, color_values)
    ph_range = np.linspace(min(ph_values), max(ph_values), 100)
    plt.figure()
    plt.plot(ph_range, cs(ph_range), label='Зависимость цвета от pH')
    plt.scatter([7.0], [cs(7.0)], color='red')  # Примерное положение образца
    plt.xlabel('pH')
    plt.ylabel('Цвет')
    plt.title('Цвет / pH')
    plt.legend()
    plt.show()

# Создание главного окна
root = tk.Tk()
root.title("Анализатор pH")

# Кнопка для загрузки изображения
load_image_button = tk.Button(root, text="Загрузить изображение", command=load_and_analyze_image)
load_image_button.pack()

# Метка для отображения изображения
image_label = tk.Label(root)
image_label.pack()

# Метка для отображения оценочного значения pH
ph_value_label = tk.Label(root, text="Оценочное значение pH: ")
ph_value_label.pack()

root.mainloop()
