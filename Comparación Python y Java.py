# Python es relajado
class Usuario:
    def __init__(self, nombre, password):
        self.nombre = nombre       # Cualquiera lo ve
        self.__password = password # El guion bajo lo hace "privado" (más o menos)