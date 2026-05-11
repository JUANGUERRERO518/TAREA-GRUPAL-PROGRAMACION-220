"""Excepciones personalizadas para el sistema"""

class ErrorValidacionDatos(Exception):
    """Se lanza cuando los datos no pasan las validaciones"""
    pass

class ServicioNoDisponibleException(Exception):
    """Se lanza cuando un servicio no está disponible"""
    pass

class ReservaInvalidaException(Exception):
    """Se lanza cuando una reserva no es válida"""
    pass

class ClienteInvalidoException(Exception):
    """Se lanza cuando los datos del cliente son inválidos"""
    pass 
