

# se Importan las excepciones que hizo el compañero juan para usarlas cuando algo salga mal
from clases.excepciones import ClienteInvalidoException, ErrorValidacionDatos
from utils.logger import GestorLogs

# Creo el logger para registrar lo que pasa
logger = GestorLogs()

class Cliente:
    # Esta clase representa a un cliente del sistema
    # los atributos son privados_


    def __init__(self, nombre, correo, telefono, identificacion):

        # uso los setters para que se validen los datos 
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)
        self.set_identificacion(identificacion)

        # registro que se creo el cliente
        logger.registrar_evento(f"Cliente creado: {nombre} - ID: {identificacion}")


    def set_nombre(self, nombre):
        # el nombre no puede estar vacio ni ser solo espacios
        if not nombre or not nombre.strip():
            logger.registrar_error("Se intento crear cliente sin nombre")
            raise ClienteInvalidoException("El nombre del cliente no puede estar vacio")
        # guardo el nombre con _ al inicio para indicar que es privado
        self._nombre = nombre.strip()

    def set_correo(self, correo):
        # valido que el correo tenga @ y un punto
        if not correo or "@" not in correo or "." not in correo:
            logger.registrar_error(f"Correo invalido: {correo}")
            raise ErrorValidacionDatos(f"El correo '{correo}' no parece valido")
        self._correo = correo.strip()

    def set_telefono(self, telefono):
        # el telefono debe tener solo numeros y al menos 7 dig9tos
        telefono_str = str(telefono).strip()
        if not telefono_str.isdigit() or len(telefono_str) < 7:
            logger.registrar_error(f"Telefono invalido: {telefono}")
            raise ErrorValidacionDatos("El telefono debe tener solo numeros y minimo 7 digitos")
        self._telefono = telefono_str

    def set_identificacion(self, identificacion):
        # la identificacion no puede ser vacia
        identificacion_str = str(identificacion).strip()
        if not identificacion_str:
            logger.registrar_error("Identificacion vacia al crear cliente")
            raise ClienteInvalidoException("La identificacion no puede estar vacia")
        self._identificacion = identificacion_str

    #  get para leer los valores

    def get_nombre(self):
        return self._nombre

    def get_correo(self):
        return self._correo

    def get_telefono(self):
        return self._telefono

    def get_identificacion(self):
        return self._identificacion

    # metodo para mostrar la info del cliente
    def mostrar_info(self):
        print(f"--- Info del Cliente ---")
        print(f"Nombre        : {self._nombre}")
        print(f"Identificacion: {self._identificacion}")
        print(f"Correo        : {self._correo}")
        print(f"Telefono      : {self._telefono}")

    # represantacion en texto del objeto
    def __str__(self):
        return f"Cliente({self._nombre}, ID: {self._identificacion})"
