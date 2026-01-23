registro_alumnos = []

def calculo_promedio(calificaciones):
    if not calificaciones:
        return 0.0
    return sum(calificaciones) / len(calificaciones)

def registrar_alumno():
    calificaciones = []
    nombre = input("Ingrese el nombre del alumno: ")
    materia = input("Ingrese la materia: ")
    numero_tareas = int(input("Número de calificaciones a ingresar: "))

    for i in range (numero_tareas):
        calificacion = float(input(f"Ingrese la calificación {i+1}: "))
        calificaciones.append(calificacion)

    promedio = calculo_promedio(calificaciones)
    registro_alumnos.append((nombre, materia, calificaciones, promedio))
    print(f"Alumno {nombre} registrado con promedio {promedio}")

print("Bienvenido al sistema de registro de calificaciones")
while True:
    registrar_alumno()
    continuar = input("¿Desea registrar otro alumno? s/n: ")
    if continuar != 's':
        break