import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
from scipy.interpolate import CubicSpline
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def resize_image(image: cv2.typing.MatLike, scale_percent: int = 30):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


# Функция для загрузки и анализа изображения
def load_and_analyze_image(image_scale_percent: int = 30):
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(filename=file_path)
        image = resize_image(
            image=image,
            scale_percent=image_scale_percent,
        )

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )
        blurred = cv2.GaussianBlur(
            src=gray,
            ksize=(9, 9),
            sigmaX=0,
        )
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=100,
            param1=50,
            param2=30,
            minRadius=20,
            maxRadius=200,
        )

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for x, y, r in circles:
                cv2.circle(image, (x, y), r, (0, 255, 0), 4)
                # Вместо анализа центра круга здесь для демонстрации просто выделяем его

            # Конвертация изображения для отображения в Tkinter
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=im_pil)
            image_label.config(image=imgtk)
            image_label.photo = imgtk

            # Отображение оценочного значения pH (заглушка)
            value_color = "red"
            ph_value_label.config(text="TBD")
            ph_value_label.config(fg=value_color)

            # Построение графика
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

    # Создание фигуры Matplotlib
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.plot(ph_range, cs(ph_range), label="Зависимость цвета от pH")
    plot.scatter([7.0], [cs(7.0)], color="red")  # Примерное положение образца
    plot.set_xlabel("pH")
    plot.set_ylabel("Цвет")
    plot.set_title("Цвет / pH")
    plot.legend()

    # Создание холста Matplotlib для Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Создание главного окна
root = tk.Tk()
root.title("Анализатор pH")

# Кнопка для загрузки изображения
load_image_button = tk.Button(root, text="Загрузить изображение", command=load_and_analyze_image)
load_image_button.pack()

# Метка для отображения изображения
image_label = tk.Label(root)
image_label.pack()

# Frame для оценочного значения pH
ph_frame = tk.Frame(root)

# Метка для отображения оценочного значения pH
ph_value_text_label = tk.Label(ph_frame, text="Оценочное значение pH: ")
ph_value_label = tk.Label(ph_frame)

# place both labels in the same row under the image_label
ph_value_text_label.pack(side=tk.LEFT)
ph_value_label.pack(side=tk.LEFT)
ph_frame.pack()

root.mainloop()
