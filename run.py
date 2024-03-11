import subprocess
import os

if __name__ == "__main__":
    # Ejecutar dependencies.py
    ruta_install = os.path.join('src', 'dependencies.py')
    subprocess.run(['python', ruta_install])

    # Ejecutar downloader.py
    ruta_app = os.path.join('src', 'downloader.py')
    subprocess.run(['python', ruta_app])
