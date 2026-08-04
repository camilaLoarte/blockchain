"""
Simulación de la Capa Off-chain
=================================
Base de datos institucional donde viven los datos personales, el texto
completo de las propuestas y el mapeo cifrado token<->estudiante. Nada
de esto se publica jamás en el ledger, conforme al principio de
minimización de datos y a la LOPDP descritos en la Fase II.
"""
import hashlib


class AlmacenOffChain:
    def __init__(self):
        self.datos_personales = {}         # sujeto -> {facultad, correo...}
        self.propuestas_texto = {}         # id_propuesta -> texto completo
        self._mapeo_token_estudiante = {}  # token -> sujeto (cifrado simulado)

    def guardar_perfil(self, sujeto: str, facultad: str, correo: str):
        self.datos_personales[sujeto] = {"facultad": facultad, "correo": correo}

    def guardar_texto_propuesta(self, id_propuesta: str, texto: str):
        self.propuestas_texto[id_propuesta] = texto

    def generar_token_pseudonimo(self, sujeto: str, proceso: str) -> str:
        """Genera un token pseudónimo determinista por (estudiante, proceso).

        Al ser determinista, un mismo estudiante siempre obtiene el mismo
        token para el mismo proceso, lo que permite al chaincode rechazar
        votos duplicados. El mapeo token<->estudiante se guarda off-chain.
        """
        token = hashlib.sha256(
            f"{sujeto}|{proceso}".encode()
        ).hexdigest()[:16]
        self._mapeo_token_estudiante[token] = sujeto
        return token

    def resolver_token(self, token: str, autorizado: bool = False) -> str:
        """Acceso restringido: solo auditoría autorizada puede des-anonimizar."""
        if not autorizado:
            raise PermissionError("Acceso denegado: se requiere autorización de auditoría.")
        return self._mapeo_token_estudiante.get(token, "DESCONOCIDO")
