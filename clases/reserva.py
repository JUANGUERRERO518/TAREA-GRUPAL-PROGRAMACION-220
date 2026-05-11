#importo nuevamente
from clases.excepciones import ReservaInvalidaException, ErrorValidacionDatos
from utils.logger import GestorLogs

logger = GestorLogs()

# defino las constantes de estado 
ESTADO_PENDIENTE   = "pendiente"
ESTADO_CONFIRMADA  = "confirmada"
ESTADO_CANCELADA   = "cancelada"


class Reserva:
    # Esta clase representa una reserva en el sistema
    # Un cliente puede reservar uno o mas servicios

    # variable de clase para generar id automaticamente
    _contador_id = 1

    def __init__(self, cliente, servicio):
        # valido que me pasen un cliente y un servicio validos
        if cliente is None:
            raise ReservaInvalidaException("No se puede crear una reserva sin cliente")
        if servicio is None:
            raise ReservaInvalidaException("No se puede crear una reserva sin servicio")

        # asigno un id unico para cada reserva
        self._id = Reserva._contador_id
        Reserva._contador_id += 1

        self._cliente  = cliente
        # guardo los servicios en una lista para poder agregar mas despues
        self._servicios = [servicio]
        self._estado   = ESTADO_PENDIENTE  # toda reserva inicia pendiente

        logger.registrar_evento(
            f"Reserva #{self._id} creada para {cliente.get_nombre()} "
            f"- Estado: {self._estado}"
        )
        print(f"  Reserva #{self._id} creada para {cliente.get_nombre()} (pendiente)")

    #Estados 

    def confirmar(self):
        # solo se puede confirmar si esta pendiente
        if self._estado != ESTADO_PENDIENTE:
            logger.registrar_error(
                f"Intento de confirmar reserva #{self._id} en estado '{self._estado}'"
            )
            raise ReservaInvalidaException(
                f"No se puede confirmar, la reserva esta en estado '{self._estado}'"
            )
        self._estado = ESTADO_CONFIRMADA
        logger.registrar_evento(f"Reserva #{self._id} confirmada")
        print(f"  Reserva #{self._id} CONFIRMADA exitosamente")

    def cancelar(self):
        # no se puede cancelar algo que ya esta cancelado
        if self._estado == ESTADO_CANCELADA:
            raise ReservaInvalidaException("Esta reserva ya estaba cancelada")

        self._estado = ESTADO_CANCELADA
        logger.registrar_evento(f"Reserva #{self._id} cancelada")
        print(f"  Reserva #{self._id} CANCELADA")

    def get_estado(self):
        return self._estado

    def get_id(self):
        return self._id

    def get_cliente(self):
        return self._cliente

    def get_servicios(self):
        return self._servicios

    def agregar_servicio(self, servicio):
        # se pueden agrregar mas reservasa, solo si no se ha cancelado
        if self._estado == ESTADO_CANCELADA:
            raise ReservaInvalidaException(
                "No se pueden agregar servicios a una reserva cancelada"
            )
        if servicio is None:
            raise ErrorValidacionDatos("El servicio no puede ser None")

        self._servicios.append(servicio)
        logger.registrar_evento(
            f"Servicio '{servicio.get_nombre()}' agregado a reserva #{self._id}"
        )
        print(f"  Servicio '{servicio.get_nombre()}' agregado a reserva #{self._id}")

    def calcular_total(self):
        # sumo el precio de todos los servicios de la reserva
        total = 0
        for servicio in self._servicios:
            total += servicio.get_precio()
        return total

    # sobrecarga de operador

    def __str__(self):
        servicios_nombres = ", ".join([s.get_nombre() for s in self._servicios])
        return (f"Reserva #{self._id} | Cliente: {self._cliente.get_nombre()} "
                f"| Estado: {self._estado} | Servicios: {servicios_nombres} "
                f"| Total: ${self.calcular_total()}")

    def __eq__(self, otra):
        # sobrecargo == para comparar reservas por su id
        if not isinstance(otra, Reserva):
            return False
        return self._id == otra._id

    def __add__(self, otro_servicio):
     #sobrecarga de operadores
        self.agregar_servicio(otro_servicio)
        return self  

    def mostrar_detalle(self):
        # muestra toda la informacion de la reserva
        print(f"\n===== Detalle Reserva #{self._id} =====")
        print(f"Cliente : {self._cliente.get_nombre()} (ID: {self._cliente.get_identificacion()})")
        print(f"Estado  : {self._estado.upper()}")
        print(f"Servicios contratados:")
        for i, servicio in enumerate(self._servicios, 1):
            print(f"  {i}. {servicio.descripcion()}")
        print(f"Total   : ${self.calcular_total()}")
        print("=" * 35)
