#importaciones
from clases.servicio import Servicio
from clases.excepciones import ServicioNoDisponibleException, ErrorValidacionDatos
from utils.logger import GestorLogs

logger = GestorLogs()


# Servicio 1: Servicio de Habitacion

class ServicioHabitacion(Servicio):
    # Este servicio es para reservar una habitacion de hotel

    def __init__(self, tipo_habitacion, precio, disponible=True):
        # llamo al constructor del padre
        super().__init__(f"Habitacion {tipo_habitacion}", precio, disponible)
        self._tipo = tipo_habitacion  # puede ser: simple, doble, suite

    def descripcion(self):
        # implemento el metodo abstracto
        return f"Habitacion tipo {self._tipo} por ${self._precio} la noche"

    def ejecutar(self, cliente):
        # primero verifico que este disponible, si no lanza excepcion
        self.verificar_disponibilidad()

        # valido que el cliente no sea none
        if cliente is None:
            raise ErrorValidacionDatos("Se necesita un cliente para ejecutar el servicio")

        logger.registrar_evento(
            f"Servicio habitacion '{self._tipo}' asignado a {cliente.get_nombre()}"
        )
        print(f"  Habitacion {self._tipo} reservada para {cliente.get_nombre()} - Precio: ${self._precio}")
        return True

# Servicio 2: Servicio de Restaurante

class ServicioRestaurante(Servicio):
    def __init__(self, numero_personas, precio_por_persona, disponible=True):
        # calculo el precio total segun cuantas personas son
        precio_total = numero_personas * precio_por_persona
        super().__init__("Restaurante", precio_total, disponible)
        self._numero_personas = numero_personas
        self._precio_por_persona = precio_por_persona

    def descripcion(self):
        return (f"Reserva en restaurante para {self._numero_personas} personas "
                f"a ${self._precio_por_persona} por persona")

    def ejecutar(self, cliente):
        self.verificar_disponibilidad()

        if cliente is None:
            raise ErrorValidacionDatos("Se necesita un cliente para el restaurante")

        # valido que el numero de personas sea razonable
        if self._numero_personas <= 0:
            raise ErrorValidacionDatos("El numero de personas debe ser mayor a 0")

        if self._numero_personas > 20:
            # si son muchas personas, se les avisa que necesita una reserva diferente 
            raise ErrorValidacionDatos("Para grupos mayores a 20 personas contactar directamente")

        logger.registrar_evento(
            f"Restaurante reservado para {cliente.get_nombre()} - {self._numero_personas} personas"
        )
        print(f"  Restaurante reservado para {cliente.get_nombre()} "
              f"({self._numero_personas} personas) - Total: ${self._precio}")
        return True


# Servicio 3: Servicio de Spa

class ServicioSpa(Servicio):
    # Este servicio es para reservar tratamientos de spa

    def __init__(self, tipo_tratamiento, duracion_minutos, precio, disponible=True):
        super().__init__(f"Spa - {tipo_tratamiento}", precio, disponible)
        self._tratamiento = tipo_tratamiento
        self._duracion = duracion_minutos  # duracion en minutos

    def descripcion(self):
        return (f"Tratamiento de spa: {self._tratamiento} "
                f"- Duracion: {self._duracion} minutos - Precio: ${self._precio}")

    def ejecutar(self, cliente):
        self.verificar_disponibilidad()

        if cliente is None:
            raise ErrorValidacionDatos("Se necesita un cliente para el spa")

        # valido que la duracion sea positiva
        if self._duracion <= 0:
            raise ErrorValidacionDatos("La duracion del tratamiento debe ser mayor a 0")

        logger.registrar_evento(
            f"Spa '{self._tratamiento}' reservado para {cliente.get_nombre()} "
            f"- {self._duracion} min"
        )
        print(f"  Spa '{self._tratamiento}' reservado para {cliente.get_nombre()} "
              f"- {self._duracion} min - Precio: ${self._precio}")
        return True
