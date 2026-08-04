"""
Simulación de la Capa de Identidad y Seguridad (Fabric CA + MSP)
==================================================================
En Hyperledger Fabric real, cada usuario recibe un certificado X.509
emitido por una Autoridad Certificadora (Fabric CA) tras validar su
matrícula institucional. El MSP (Membership Service Provider) determina
el rol y los permisos de cada actor dentro de la red.

Esta simulación reemplaza la criptografía real (RSA/ECDSA + X.509) por
hashes SHA-256, suficientes para demostrar el flujo conceptual descrito
en la Fase II sin depender de librerías externas.
"""
import hashlib
import secrets
import time


class CertificadoDigital:
    """Representa un certificado X.509 simplificado."""

    def __init__(self, sujeto: str, rol: str, facultad: str):
        self.sujeto = sujeto
        self.rol = rol                # "estudiante", "facultad", "consejo"
        self.facultad = facultad
        self.emitido_en = time.time()
        self.numero_serie = secrets.token_hex(8)
        self.huella = self._calcular_huella()

    def _calcular_huella(self) -> str:
        base = f"{self.sujeto}|{self.rol}|{self.facultad}|{self.numero_serie}"
        return hashlib.sha256(base.encode()).hexdigest()

    def __repr__(self):
        return f"<Cert {self.sujeto} rol={self.rol} serie={self.numero_serie[:8]}>"


class FabricCA:
    """Autoridad Certificadora institucional (simulada)."""

    def __init__(self):
        self._matriculados = set()   # padrón de estudiantes activos
        self._certificados = {}      # sujeto -> CertificadoDigital

    def registrar_matricula(self, codigo_estudiante: str):
        """Soporte TI valida que el estudiante esté matriculado activo."""
        self._matriculados.add(codigo_estudiante)

    def emitir_certificado(self, sujeto: str, rol: str, facultad: str) -> CertificadoDigital:
        if rol == "estudiante" and sujeto not in self._matriculados:
            raise PermissionError(
                f"'{sujeto}' no consta en el padrón de matriculados activos."
            )
        cert = CertificadoDigital(sujeto, rol, facultad)
        self._certificados[sujeto] = cert
        return cert

    def revocar(self, sujeto: str):
        self._certificados.pop(sujeto, None)

    def es_valido(self, sujeto: str) -> bool:
        return sujeto in self._certificados


class MSP:
    """Membership Service Provider: qué transacciones puede firmar cada rol."""

    PERMISOS = {
        "estudiante": {"crear_propuesta", "votar"},
        "facultad": {"endosar", "abrir_votacion"},
        "consejo": {"endosar", "abrir_votacion", "actualizar_estado"},
    }

    @classmethod
    def autoriza(cls, cert: CertificadoDigital, accion: str) -> bool:
        return accion in cls.PERMISOS.get(cert.rol, set())
