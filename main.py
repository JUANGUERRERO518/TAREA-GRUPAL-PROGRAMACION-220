"""
MÓDULO: main.py
FUNCIÓN: Punto de entrada del sistema - Integración y simulación
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clases.cliente import Cliente
from clases.servicios_concretos import (
    ReservaSalas,
    AlquilerEquipos,
    AsesoriaEspecializada
)
from clases.reserva import Reserva
from clases.excepciones import (
    ClienteInvalidoException,
    ReservaInvalidaException,
    ErrorValidacionDatos
)
from utils.logger import GestorLogs


def simular_operaciones():
    print("=" * 60)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 60)
    print("\n DEMOSTRACIÓN DE PROGRAMACIÓN ORIENTADA A OBJETOS")
    print("   - Abstracción (clase abstracta Servicio)")
    print("   - Herencia (3 servicios concretos)")
    print("   - Polimorfismo (mismo método, comportamientos diferentes)")
    print("   - Encapsulación (atributos privados en Cliente)")
    print("   - Manejo de excepciones (try/except/else/finally)")
    print("=" * 60)

    logger = GestorLogs()
    logger.registrar_evento("=== INICIO DE SIMULACIÓN ===")
    print("\n Sistema de logs inicializado")

    clientes_registrados = []
    reservas_registradas = []

    # ========== CREAR SERVICIOS ==========
    print("\n" + "-" * 40)
    print(" OPERACIONES 1-3: CREANDO SERVICIOS")
    print("-" * 40)
    
    sala = ReservaSalas("Sala VIP", 75.0)
    print(f"   Servicio creado: {sala.descripcion()} - ${sala.precio_base}/hora")
    logger.registrar_evento(f"Servicio creado: Sala VIP - ${sala.precio_base}/hora")
    
    equipo = AlquilerEquipos("Pack Proyectores", 30.0)
    print(f"   Servicio creado: {equipo.descripcion()} - ${equipo.precio_base}/hora")
    logger.registrar_evento(f"Servicio creado: Pack Proyectores - ${equipo.precio_base}/hora")
    
    asesoria = AsesoriaEspecializada("Consultoría Cloud", 120.0)
    print(f"   Servicio creado: {asesoria.descripcion()} - ${asesoria.precio_base}/hora")
    logger.registrar_evento(f"Servicio creado: Consultoría Cloud - ${asesoria.precio_base}/hora")

    # ========== REGISTRAR CLIENTES ==========
    print("\n" + "-" * 40)
    print(" OPERACIONES 4-10: REGISTRANDO CLIENTES")
    print("-" * 40)
    
    datos_clientes = [
        ("Ana María López", "ana.lopez@email.com", "3001234567", "C001"),
        ("Bo", "correo@valido.com", "3101111111", "C002"),
        ("Carlos Pérez", "carlos@", "3109876543", "C003"),
        ("", "vacio@email.com", "3111111111", "C004"),
        ("Diana Ríos", "diana.rios@empresa.com", "3205555555", "C005"),
        ("Ernesto Gil", "ernesto@mail.com", "telefono123", "C006"),
        ("Fernando Gómez", "fernando.gomez@mail.com", "3507777777", "C007"),
    ]

    for nombre, email, telefono, idc in datos_clientes:
        try:
            cliente = Cliente(nombre, email, telefono, idc)
            clientes_registrados.append(cliente)
            print(f"   Cliente registrado: {cliente}")
            logger.registrar_evento(f"Cliente registrado: {idc} - {nombre}")
        except ClienteInvalidoException as e:
            print(f"   Error al registrar '{nombre}': {e}")
            logger.registrar_error(f"Cliente inválido '{nombre}': {e}")
        except Exception as e:
            print(f"   Error inesperado con '{nombre}': {e}")
            logger.registrar_error(f"Error inesperado con cliente '{nombre}': {e}")

    print(f"\n   Resumen: {len(clientes_registrados)} clientes registrados exitosamente de {len(datos_clientes)} intentos")

    if len(clientes_registrados) < 2:
        print("\n   No hay suficientes clientes válidos. Creando cliente temporal...")
        cliente_temporal = Cliente("Usuario Temporal", "temp@temp.com", "3000000000", "TMP001")
        clientes_registrados.append(cliente_temporal)
        print(f"   Cliente temporal creado: {cliente_temporal}")

    cliente1 = clientes_registrados[0]
    cliente2 = clientes_registrados[-1]

    # ========== CREAR RESERVAS ==========
    print("\n" + "-" * 40)
    print(" OPERACIONES 11-22: CREANDO RESERVAS")
    print("-" * 40)
    
    intentos_reserva = [
        (cliente1, sala, 3, {"capacidad": 10}),
        (cliente1, equipo, 2, {"cantidad": -1}),
        (cliente2, asesoria, 4, {"tema": "Arquitectura de Software"}),
        (cliente1, asesoria, 1, {}),
        (cliente2, sala, 2, {"capacidad": 50}),
        (cliente1, sala, 2, {"capacidad": 100}),
        (cliente2, equipo, 5, {"cantidad": 3}),
        (cliente1, equipo, 1, {"cantidad": 0}),
        (cliente1, asesoria, 2, {"tema": "DevOps y CI/CD avanzado"}),
        (cliente2, asesoria, 1, {"tema": "IA"}),
        (cliente1, sala, 4, {"capacidad": 20}),
        (cliente2, equipo, 3, {"cantidad": 5}),
    ]

    for i, (cliente, servicio, duracion, params) in enumerate(intentos_reserva, 1):
        try:
            servicio.validar_parametros(**params)
            reserva = Reserva(cliente, servicio, duracion, "2025-06-15")
            costo = reserva.procesar()
            reservas_registradas.append(reserva)
            print(f"   Reserva {i:2d}: {reserva.id_reserva} - {servicio.nombre} - {duracion}h - Costo: ${costo:.2f}")
            logger.registrar_evento(f"Reserva exitosa: {reserva.id_reserva}")
        except ReservaInvalidaException as e:
            print(f"   Reserva {i:2d} fallida (ReservaInvalida): {e}")
            logger.registrar_error(f"Reserva fallida: {e}")
        except ErrorValidacionDatos as e:
            print(f"   Reserva {i:2d} fallida (Validación): {e}")
            logger.registrar_error(f"Validación fallida: {e}")
        except Exception as e:
            print(f"   Reserva {i:2d} fallida (Error inesperado): {e}")
            logger.registrar_error(f"Error inesperado: {e}")

    print(f"\n   Resumen: {len(reservas_registradas)} reservas exitosas de {len(intentos_reserva)} intentos")

    # ========== SOBRECARGA DE MÉTODOS ==========
    if reservas_registradas:
        print("\n" + "-" * 40)
        print(" DEMOSTRACIÓN DE SOBRECARGA DE MÉTODOS")
        print("-" * 40)
        
        r = reservas_registradas[0]
        print(f"  Servicio: {r.servicio.nombre}")
        print(f"  Duración: {r.duracion} horas")
        print(f"   Costo base: ${r.servicio.calcular_costo(r.duracion):.2f}")
        print(f"   Con descuento 15%: ${r.calcular_costo_con_descuento(15):.2f}")
        print(f"   Con impuesto 19%: ${r.calcular_costo_con_impuesto(19):.2f}")
        print(f"   Con descuento + impuesto: ${r.calcular_costo_completo(15, 19):.2f}")
        logger.registrar_evento("Demostración de sobrecarga de métodos completada")

    # ========== CANCELACIÓN ==========
    if reservas_registradas:
        print("\n" + "-" * 40)
        print("  DEMOSTRACIÓN DE CANCELACIÓN")
        print("-" * 40)
        
        r = reservas_registradas[0]
        print(f"  Reserva: {r.id_reserva}")
        print(f"  Estado actual: {r.estado}")
        
        try:
            r.cancelar()
            print(f"   Cancelación exitosa - Nuevo estado: {r.estado}")
            logger.registrar_evento(f"Reserva cancelada: {r.id_reserva}")
        except ReservaInvalidaException as e:
            print(f"   Error al cancelar: {e}")

    # ========== ENCADENAMIENTO DE EXCEPCIONES ==========
    print("\n" + "-" * 40)
    print(" DEMOSTRACIÓN DE ENCADENAMIENTO DE EXCEPCIONES")
    print("-" * 40)
    
    try:
        sala_invalida = ReservaSalas("Sala Test", 100)
        sala_invalida.validar_parametros(capacidad=200)
    except ErrorValidacionDatos as e:
        print(f"  Excepción capturada: {e}")
        if e.__cause__:
            print(f"  Causa original (encadenada): {e.__cause__}")
            print("   Esto es ENCADENAMIENTO DE EXCEPCIONES")
            logger.registrar_evento("Encadenamiento de excepciones demostrado")

    # ========== RESUMEN FINAL ==========
    print("\n" + "=" * 60)
    print(" RESUMEN FINAL DE LA SIMULACIÓN")
    print("=" * 60)
    print(f"  • Total de clientes intentados:     {len(datos_clientes)}")
    print(f"  • Clientes registrados exitosamente: {len(clientes_registrados)}")
    print(f"  • Total de reservas intentadas:     {len(intentos_reserva)}")
    print(f"  • Reservas exitosas:                {len(reservas_registradas)}")
    print(f"  • Reservas fallidas:                {len(intentos_reserva) - len(reservas_registradas)}")
    print(f"  • Archivo de logs:                  logs/eventos.log")
    print("=" * 60)
    print("\n" + "" * 20)
    print("SIMULACIÓN COMPLETADA - TODAS LAS OPERACIONES EJECUTADAS")
    print("El sistema manejó todos los errores sin detenerse")
    print("" * 20)
    
    logger.registrar_evento("=== FIN DE SIMULACIÓN ===")
    print("\n Revisa el archivo 'logs/eventos.log' para ver todos los eventos registrados.")


if __name__ == "__main__":
    simular_operaciones()