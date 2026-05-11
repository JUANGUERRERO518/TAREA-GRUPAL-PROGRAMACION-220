"""Sistema de logs con manejo de archivos y finally"""

import logging
import os

class GestorLogs:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar_logger()
        return cls._instancia

    def _inicializar_logger(self):
        os.makedirs('logs', exist_ok=True)
        self.logger = logging.getLogger('SoftwareFJ')
        self.logger.setLevel(logging.INFO)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        file_handler = logging.FileHandler('logs/eventos.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def registrar_con_finally(self, mensaje, nivel="INFO"):
        archivo = None
        try:
            archivo = open("logs/eventos.log", "a", encoding="utf-8")
            archivo.write(f"{mensaje}\n")
            if nivel == "INFO":
                self.logger.info(mensaje)
            else:
                self.logger.error(mensaje)
        except Exception as e:
            print(f"Error crítico escribiendo en log: {e}")
        finally:
            if archivo:
                archivo.close()

    def registrar_evento(self, mensaje):
        self.registrar_con_finally(mensaje, "INFO")

    def registrar_error(self, mensaje):
        self.registrar_con_finally(f"ERROR: {mensaje}", "ERROR")