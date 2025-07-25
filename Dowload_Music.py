import time
import yt_dlp
import os
import tkinter as tk
from tkinter import messagebox,ttk,filedialog


def descargar_musica(url, carpeta="Mi_Musica", label=None, barra=None):
    try:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        def hook(d):
            if barra:
                status = d.get('status','')
                if status == 'downloading':
                    total_bytes =  d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    downloaded_bytes = d.get('downloaded_bytes', 0)
                    progreso= int((downloaded_bytes / total_bytes) * 100) if total_bytes else 0
                    barra['value'] = progreso
                    ventana.update_idletasks()     
                elif d['status'] == 'finished':
                    barra['value'] = 100
                    if label:
                        label.config(text="Convirtiendo mp4 a mp3...")   

        opciones = {
            'format': 'bestaudio/best',
            'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'progress_hooks':[hook]
        }

        if label:
            label.config(text="Iniciando descarga...")
        
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        messagebox.showinfo("Éxito", "¡Descarga completada!")

        if label:
            label.config(text="Descarga completada")
            label.after(2000,lambda: label.config(text=""))

        if barra:
            barra['value'] = 0

        url_var.set("")
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        if label:
            label.config(text="Error al descargar")
            label.after(2000,lambda:label.config(text=""))

        if barra:
            barra['value'] = 0


def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_var.set(carpeta)

def iniciar_descarga():
    url = url_var.get()
    carpeta = carpeta_var.get() or "Mi_Musica"
    if not url:
        messagebox.showwarning("Aviso", "Por favor, ingrese un enlace de YouTube.")
        return
    descargar_musica(url, carpeta,label=estado_label,barra=progress_bar)





# Crear ventana
ventana = tk.Tk()
ventana.title("Descargador de Música de YouTube")

# Variables
url_var = tk.StringVar()
carpeta_var = tk.StringVar()



# Layout
tk.Label(ventana, text="Enlace de YouTube:").pack(pady=5)
tk.Entry(ventana, textvariable=url_var, width=50,).pack(pady=5)


tk.Label(ventana, text="Carpeta de destino (opcional):").pack(pady=5)
tk.Entry(ventana, textvariable=carpeta_var, width=50).pack(pady=5)
tk.Button(ventana, text="Seleccionar carpeta", command=seleccionar_carpeta).pack(pady=5)

tk.Button(ventana, text="Descargar", command=iniciar_descarga, bg="green", fg="white").pack(pady=20)

#barra estado
progress_bar = ttk.Progressbar(ventana,length=400, mode='determinate')
progress_bar.pack(pady=5)

#Estado
estado_label=tk.Label(ventana,text="")
estado_label.pack(pady=5)

tk.Label(ventana,text="Desarrollado por Erwin Baldera").pack(pady=3)

ventana.mainloop()
