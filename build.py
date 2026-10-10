import PyInstaller.__main__
import os

if __name__ == '__main__':
    PyInstaller.__main__.run([
        'main.py',
        '--name=PajakEditor',
        '--onefile',
        '--windowed',
        # '--icon=assets/app.ico', # uncomment ini jika icon sudah tersedia
        '--clean',
    ])
