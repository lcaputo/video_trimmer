import os
import pdb
import datetime
import subprocess
import tkinter as tk
from tkinter import END
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# Variables
video_title: str = ''
video_path: str = ''
video_length: int = 0
num_of_cuts: int = 0
video_extract_start: list = []
video_extract_end: list = []


# Inicair Tkinter
first_window = tk.Tk()


def exit_event():
    os.sys.exit()


first_window.resizable(False, False)
first_window.protocol("WM_DELETE_WINDOW", exit_event)
first_window.title("Recorta tus videos")
first_window.geometry("300x230")

# Funciones


def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    # ASIGNAR VARIABLE CON NOMBRE DEL VIDEO
    video_path = filename
    video_clip_file = VideoFileClip(video_path)
    # ASIGNAR VARIABLE CON DURACION DEL VIDEO
    video_length = video_clip_file.duration
    print('Selected:', video_path)
    # ASIGNAR VARIABLE NUMERO DE CORTES
    try:
        num_of_cuts = int(cuts.get())
        if (video_path != '' and video_length != 0 and num_of_cuts != 0):
            # DESTRUIR VENTANA ANTERIOR
            first_window.withdraw()
            # NUEVA VENTANA
            second_window = tk.Tk()
            second_window.resizable(False, False)
            second_window.protocol("WM_DELETE_WINDOW", exit_event)
            video_title = video_path.split('/')[-1:][0]
            second_window.title(video_title)

            # BOTON SALIR
            exit_button = tk.Button(second_window, text="Salir",
                                    command=lambda: os.sys.exit())
            exit_button.grid(row=1, column=0)

            sections_label = tk.Label(
                second_window, text="Duración: " + str(datetime.timedelta(seconds=round(video_length))))
            sections_label.grid(row=1, column=1)

            start_label = tk.Label(second_window, text="Inicio")
            start_label.grid(row=2, column=1)
            end_label = tk.Label(second_window, text="Fin")
            end_label.grid(row=2, column=2)
            # CICLO PARA AGREGAR ENTRADAs DE TIEMPO
            for i in range(0, int(num_of_cuts)):
                label = tk.Label(second_window, text='video %s' % (i+1))
                label.grid(row=3+i, column=0, pady=2)
                video_extract_start.append(
                    tk.Entry(second_window, justify='center'))
                video_extract_start[i].grid(row=3+i, column=1)
                video_extract_end.append(
                    tk.Entry(second_window, justify='center'))
                video_extract_end[i].grid(row=3+i, column=2)

            # BOTON EXPORTAR
            export_button = tk.Button(
                second_window, text="Exportar", command=lambda: cut_video(video_clip_file, num_of_cuts, video_length))
            export_button.grid(row=4+num_of_cuts+1, column=2, pady=10)
        else:
            messagebox.showerror(title="Error", message="Verifica los campos")
    except:
        messagebox.showerror(
            title="Error", message="Solo puede introducir números")


def time_to_secs(time_input: str):
    time: str = time_input.split(':') if time_input.split(':') else ''
    hours_and_minutes: list = time[:-1]
    seconds: int = int(time[-1:][0])
    result: int = seconds
    if len(hours_and_minutes) == 1:
        result = result + int(hours_and_minutes[0])*60
    if len(hours_and_minutes) == 2:
        result += hours_and_minutes[0]*60
        result += (hours_and_minutes[1]*60)*60
    return result


def cut_video(video_clip_file, num_of_cuts, video_length):
    try:
        for i in range(0, int(num_of_cuts)):
            start = time_to_secs(video_extract_start[i].get())
            end = time_to_secs(video_extract_end[i].get())
            time = '%s: %s' % (str(start), str(end))
            if end <= video_length:
                output = video_clip_file.subclip(start, end)
                output = output.set_duration(end-start)
                directory = 'exports'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                output.write_videofile("%s/%s.mp4" % (directory, i+1))
                messagebox.showinfo(
                    title="Exito", message="Se exporto correctamente")
                os.startfile(os.getcwd()+'/exports')
                """ ffmpeg_extract_subclip(
                    video_clip_file, start, end, targetname="exports/%s.mp4" % i) """
            else:
                print('max length exceeded')
                messagebox.showwarning(
                    title="Advertencia", message="Los valores no puedes sobre pasar la duración maxima del video")
        video_clip_file.close()
        if video_clip_file.audio and video_clip_file.audio.reader:
            video_clip_file.audio.reader.close_proc()
    except:
        messagebox.showerror(
            title="Error", message="Falló al convertir revise las configuraciónes")


def set_text(entry, value):
    entry.delete(0, END)
    entry.insert(0, (float(value) / 60, 0))


def CalcWindow():
    try:
        calc_window = tk.Tk()
        calc_window.resizable(False, False)
        calc_window.title("Calculadora")
        calc_window.geometry("250x150")
        calc_label = tk.Label(calc_window, text="Minutos a Segundos")
        calc_label.pack()
        calc_input = tk.Entry(calc_window, justify='center')
        calc_input.pack()
        calc_button = tk.Button(calc_window, text="Calcular",
                                command=lambda: set_text(
                                    calc_result, calc_input.get()
                                ))
        calc_button.pack(pady=10)
        calc_result = tk.Entry(calc_window, justify='center')
        calc_result.pack()
        quit_button = tk.Button(calc_window, text="Salir",
                                command=lambda: calc_window.destroy())
        quit_button.pack(pady=10)
    except:
        entry.delete(0, END)


# Añadir ventana principal
label = tk.Label(first_window, text="Recortar Videos \nFacilmente.")
label.pack(side="top", fill="x", pady=10)

cuts_label = tk.Label(first_window, text="1) Número de recortes: ")
cuts_label.pack()
cuts = tk.Entry(first_window, justify='center')
cuts.pack(pady=10)
upload_label = tk.Label(first_window, text="2) Subir Video: ")
upload_label.pack()
button = tk.Button(first_window, text='Examinar...',
                   command=lambda: UploadAction())
button.pack(pady=10)
tk.Button(first_window, text="Salir",
          command=lambda: os.sys.exit()).pack(pady=5)

first_window.mainloop()
