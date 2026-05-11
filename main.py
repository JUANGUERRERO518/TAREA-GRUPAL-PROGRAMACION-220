"""
MÓDULO: main.py
FUNCIÓN: Punto de entrada del sistema - Integración y simulación
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clases.cliente import Cliente
from clases.servicios_concretos import ServicioHabitacion, ServicioRestaurante, ServicioSpa
from clases.reserva import Reserva
from clases.excepciones import (
    ClienteInvalidoException,
    ReservaInvalidaException,
    ErrorValidacionDatos,
    ServicioNoDisponibleException
)
from utils.logger import GestorLogs


def simular_operaciones():
    print("=" * 60)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 60)

    logger = GestorLogs()
    logger.registrar_evento("=== INICIO DE SIMULACIÓN ===")
    print("\n Sistema de logs inicializado")

    clientes_registrados = []
    reservas_registradas = []

    # ========== CREAR SERVICIOS ==========
    print("\n CREANDO SERVICIOS...")
    
    habitacion = ServicioHabitacion("Suite", 150.0, True)
    print(f"   {habitacion.descripcion()}")
    
    restaurante = ServicioRestaurante(4, 35.0, True)
    print(f"   {restaurante.descripcion()}")
    
    spa = ServicioSpa("Masaje Relajante", 60, 80.0, True)
    print(f"   {spa.descripcion()}")

    # ========== REGISTRAR CLIENTES ==========
    print("\n REGISTRANDO CLIENTES...")
    
    datos_clientes = [
        ("Ana María López", "ana.lopez@email.com", "3001234567", "C001"),
        ("Bo", "correo@valido.com", "3101111111", "C002"),
        ("Carlos Pérez", "carlos@", "3109876543", "C003"),
        ("", "vacio@email.com", "3111111111", "C004"),
        ("Diana Ríos", "diana.rios@empresa.com", "3205555555", "C005"),
    ]

    for nombre, email, telefono, idc in datos_clientes:
        try:
            cliente = Cliente(nombre, email, telefono, idc)
            clientes_registrados.append(cliente)
            print(f"   Cliente registrado: {cliente}")
            logger.registrar_evento(f"Cliente registrado: {idc}")
        except (ClienteInvalidoException, ErrorValidacionDatos) as e:
            print(f"   Error: {e}")
            logger.registrar_error(f"Error: {e}")

    print(f"\n   Clientes válidos: {len(clientes_registrados)}")

    if len(clientes_registrados) == 0:
        cliente_temp = Cliente("Usuario Temporal", "temp@temp.com", "3000000000", "TMP001")
        clientes_registrados.append(cliente_temp)

    cliente1 = clientes_registrados[0]
    cliente2 = clientes_registrados[-1]

    # ========== CREAR RESERVAS ==========
    print("\n CREANDO RESERVAS...")
    
    intentos = [
        (cliente1, habitacion, True),
        (cliente2, restaurante, True),
        (cliente1, spa, True),
        (None, habitacion, True),
        (cliente1, None, True),
        (cliente2, habitacion, False),
    ]

    for i, (cliente, servicio, disponible) in enumerate(intentos, 1):
        try:
            if servicio:
                servicio.set_disponible(disponible)
            
            if cliente is None:
                raise ReservaInvalidaException("Cliente nulo")
            if servicio is None:
                raise ErrorValidacionDatos("Servicio nulo")
            
            reserva = Reserva(cliente, servicio)
            reservas_registradas.append(reserva)
            servicio.ejecutar(cliente)
            
            print(f"   Reserva {i}: #{reserva.get_id()} - Total: ${reserva.calcular_total():.2f}")
            logger.registrar_evento(f"Reserva exitosa: #{reserva.get_id()}")
            
        except (ReservaInvalidaException, ErrorValidacionDatos, ServicioNoDisponibleException) as e:
            print(f"   Reserva {i} fallida: {e}")
            logger.registrar_error(f"Reserva fallida: {e}")

    # ========== DEMOSTRACIÓN DE ESTADOS ==========
    if reservas_registradas:
        print("\n CAMBIANDO ESTADOS...")
        r = reservas_registradas[0]
        print(f"  Reserva #{r.get_id()} - Estado: {r.get_estado()}")
        r.confirmar()
        r.cancelar()

    # ========== DEMOSTRACIÓN DE SOBRECARGA ==========
    if reservas_registradas:
        print("\n SOBRECARGA DE OPERADOR '+'...")
        r = reservas_registradas[0]
        print(f"  Total inicial: ${r.calcular_total():.2f}")
        nuevo = ServicioSpa("Piedras Calientes", 45, 65.0, True)
        r + nuevo
        print(f"  Nuevo total: ${r.calcular_total():.2f}")

    # ========== RESUMEN ==========
    print("\n" + "=" * 60)
    print(" RESUMEN FINAL")
    print("=" * 60)
    print(f"  Clientes válidos: {len(clientes_registrados)}")
    print(f"  Reservas exitosas: {len(reservas_registradas)}")
    print(f"  Logs: logs/eventos.log")
    print("=" * 60)
    print("\n SIMULACIÓN COMPLETADA")
    logger.registrar_evento("=== FIN DE SIMULACIÓN ===")


if __name__ == "__main__":
    simular_operaciones()