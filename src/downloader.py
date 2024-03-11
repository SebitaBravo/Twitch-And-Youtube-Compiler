from pytube import YouTube
import streamlink
import requests
from moviepy.editor import VideoFileClip
import os


# Crear una variable con el nombre de la carpeta donde quieres guardar las descargas
carpeta = "Downloads"
# Verificar si la carpeta existe, y si no, crearla
if not os.path.exists(carpeta):
    os.mkdir(carpeta)


def convert_to_mp4(binary_file, output_file):
    clip = VideoFileClip(binary_file)
    clip.write_videofile(output_file, codec='libx264')


def descargar_video(url):
    print("Procesando url")
    # Crear un objeto YouTube con la url del video
    video = YouTube(url)
    # Obtener el stream de mayor resolución disponible
    # Por alguna razon solo me descarga como maximo 720p
    stream = video.streams.get_highest_resolution()
    # Descargar el video en la carpeta actual
    stream.download(output_path=carpeta)
    # Imprimir un mensaje de éxito
    print("Video descargado con éxito")


def descargar_twitch(url, archivo):
    print("Procesando url")
    # Obtener el stream de la url con la mejor calidad disponible
    streams = streamlink.streams(url)
    stream = streams.get("best", None)
    # Si el stream no existe, imprimir un mensaje de error y salir de la función
    if stream is None:
        print("No se pudo obtener el stream de la url")
        return
    # Hacer una petición GET al stream
    response = requests.get(stream.url, stream=True)
    # Si la petición no tiene éxito, imprimir un mensaje de error y salir de la función
    if not response.ok:
        print("No se pudo hacer la petición al stream")
        return
    # Abrir el archivo de salida como un archivo binario
    with open(os.path.join(carpeta, archivo), "wb") as output_file:
        # Leer el contenido del stream en fragmentos de 1024 bytes
        for chunk in response.iter_content(1024):
            # Si el fragmento no está vacío, escribirlo en el archivo
            if chunk:
                output_file.write(chunk)
            # Si ocurre algún error al escribir el archivo, imprimir un mensaje de error y salir de la función
            else:
                print("No se pudo escribir el archivo")
                return
    # Imprimir un mensaje de éxito
    print("Contenido descargado con éxito")


# Pedir al usuario que elija qué quiere hacer
opcion = input(
    "¿Qué quieres hacer? (1) Descargar un video de YouTube, (2) Descargar un directo de Twitch: ")
# Validar la opción ingresada
if opcion == "1":
    # Pedir la url del video de YouTube
    url = input("Ingrese la url del video de YouTube: ")
    # Llamar a la función para descargar el video
    descargar_video(url)
elif opcion == "2":
    # Pedir la url del canal de Twitch
    url = input("Ingrese la url del canal de Twitch: ")
    # Pedir al usuario que ingrese el nombre del archivo de salida
    archivo = input("Ingrese el nombre del archivo de salida: ")
    # Llamar a la función para descargar el directo
    descargar_twitch(url, archivo)
    # Convertir archivo binario a mp4
    binary_file = os.path.join(carpeta, archivo)
    output_file = os.path.join(carpeta, archivo + ".mp4")
    convert_to_mp4(binary_file, output_file)
    # Borrar archivo antiguo
    os.remove(binary_file)
else:
    # Imprimir un mensaje de error
    print("Opción inválida. Por favor, ingrese 1 o 2.")
