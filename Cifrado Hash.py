import hashlib
import tkinter as tk
from tkinter import filedialog

def sha256_de_archivo(ruta_archivo, tam_bloque=4096):
    sha256 = hashlib.sha256()

    try:
        with open(ruta_archivo, "rb") as archivo:
            while True:
                datos = archivo.read(tam_bloque)
                if not datos:
                    break
                sha256.update(datos)
        return sha256.hexdigest()

    except FileNotFoundError:
        return "Error: El archivo no existe."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    print("Selecciona un archivo...")
    ruta = filedialog.askopenfilename(title="Selecciona el archivo para generar SHA-256")

    if ruta:
        hash_resultado = sha256_de_archivo(ruta)
        print("Archivo seleccionado:", ruta)
        print("SHA-256:", hash_resultado)
    else:
        print("No se seleccionó ningún archivo.")