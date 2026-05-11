#importaciones
from abc import ABC, abstractmethod
from clases.excepciones import ServicioNoDisponibleException, ErrorValidacionDatos
from utils.logger import GestorLogs

logger = GestorLogs()

class Servicio(ABC):
    # Esta es la clase base para todos los servicios

    def __init__(self, nombre, precio, disponible=True):
        # todo servicio tiene un nombre, un precio y si esta disponible o no
        self._nombre = nombre
        self._precio = precio
        self._disponible = disponible
        logger.registrar_evento(f"Servicio registrado: {nombre} - Precio: ${precio}")

    @abstractmethod
    def ejecutar(self, cliente):
        pass

    # otro metodo abstracto para describir el servicio
    @abstractmethod
    def descripcion(self):
        pass

    def get_nombre(self):
        return self._nombre

    def get_precio(self):
        return self._precio

    def esta_disponible(self):
        return self._disponible

    def set_disponible(self, estado):
        # puedo activar o desactivar un servicio
        self._disponible = estado
        estado_str = "activado" if estado else "desactivado"
        logger.registrar_evento(f"Servicio '{self._nombre}' {estado_str}")

    def verificar_disponibilidad(self):
        # metodo reutilizable para verificar si el servicio se puede usar
        if not self._disponible:
            logger.registrar_error(f"Servicio no disponible: {self._nombre}")
            raise ServicioNoDisponibleException(
                f"El servicio '{self._nombre}' no esta disponible en este momento"
            )

    def __str__(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio: {self._nombre} | Precio: ${self._precio} | {estado}"
