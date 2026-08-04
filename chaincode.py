"""
Chaincode simulado de la DAO Estudiantil
==========================================
Implementa las 8 transacciones de la Tabla 1 (Fase II, sección 2.6):
registro de identidad, creación de propuesta, validación (endoso),
apertura de votación, emisión de voto, cierre y conteo, consulta de
resultados y actualización de estado.
"""
import hashlib
import secrets

from identity import FabricCA, MSP
from ledger import Ledger
from offchain import AlmacenOffChain


class Propuesta:
    def __init__(self, id_propuesta: str, titulo: str, autor: str):
        self.id = id_propuesta
        self.titulo = titulo
        self.autor = autor
        self.estado = "borrador"        # borrador -> validada -> en_votacion -> cerrada
        self.endosos = set()            # facultades/consejo que endosaron
        self.votos = {"a_favor": 0, "en_contra": 0, "abstencion": 0}
        self.quorum = None
        self.tokens_usados = set()


class DAOChaincode:
    POLITICA_ENDOSO_MINIMA = 2   # 2 de 3 facultades/instancias, según Fase II

    def __init__(self):
        self.ca = FabricCA()
        self.ledger = Ledger()
        self.offchain = AlmacenOffChain()
        self.propuestas: dict[str, Propuesta] = {}

    # 1. Registro de identidad --------------------------------------------------
    def registro_identidad(self, sujeto: str, rol: str, facultad: str, correo: str = ""):
        if rol == "estudiante":
            self.ca.registrar_matricula(sujeto)
        cert = self.ca.emitir_certificado(sujeto, rol, facultad)
        self.offchain.guardar_perfil(sujeto, facultad, correo)
        self.ledger.registrar("REGISTRO_IDENTIDAD", {
            "id": cert.numero_serie,
            "rol": rol,
            "huella_cert": cert.huella[:16] + "...",
        })
        print(f"[OK] Identidad registrada: {cert}")
        return cert

    # 2. Creación de propuesta ---------------------------------------------------
    def crear_propuesta(self, autor: str, titulo: str, texto: str) -> Propuesta:
        if not self.ca.es_valido(autor):
            raise PermissionError(f"{autor} no tiene identidad válida.")
        if not MSP.autoriza(self.ca._certificados[autor], "crear_propuesta"):
            raise PermissionError(f"{autor} no tiene permiso para crear propuestas.")
        id_propuesta = secrets.token_hex(4)
        propuesta = Propuesta(id_propuesta, titulo, autor)
        self.propuestas[id_propuesta] = propuesta
        self.offchain.guardar_texto_propuesta(id_propuesta, texto)
        self.ledger.registrar("CREACION_PROPUESTA", {
            "id": id_propuesta,
            "estado": propuesta.estado,
            "autor_hash": self._hash_corto(autor),
        })
        print(f"[OK] Propuesta creada: {id_propuesta} - '{titulo}'")
        return propuesta

    # 3. Validación (endoso) ------------------------------------------------------
    def validar(self, id_propuesta: str, endosante: str, rol_endosante: str):
        propuesta = self._obtener(id_propuesta)
        if not self.ca.es_valido(endosante):
            raise PermissionError(f"{endosante} no tiene identidad válida.")
        cert = self.ca._certificados[endosante]
        if cert.rol != rol_endosante:
            raise PermissionError(
                f"El rol declarado ({rol_endosante}) no coincide con el certificado "
                f"del endosante ({cert.rol})."
            )
        if not MSP.autoriza(cert, "endosar"):
            raise PermissionError("Solo facultades/Consejo pueden endosar.")
        propuesta.endosos.add(endosante)
        if len(propuesta.endosos) >= self.POLITICA_ENDOSO_MINIMA:
            propuesta.estado = "validada"
        self.ledger.registrar("VALIDACION", {
            "id": id_propuesta,
            "endosante": endosante,
            "endosos_totales": len(propuesta.endosos),
            "estado": propuesta.estado,
        })
        print(f"[OK] Endoso de {endosante} para {id_propuesta} "
              f"({len(propuesta.endosos)} endosos) -> estado={propuesta.estado}")

    # 4. Apertura de votación -------------------------------------------------------
    def abrir_votacion(self, id_propuesta: str, quorum: int, admin: str):
        propuesta = self._obtener(id_propuesta)
        if not self.ca.es_valido(admin):
            raise PermissionError(f"{admin} no tiene identidad válida.")
        if not MSP.autoriza(self.ca._certificados[admin], "abrir_votacion"):
            raise PermissionError(
                "Solo facultades o el Consejo pueden abrir la votación (MSP)."
            )
        if propuesta.estado != "validada":
            raise ValueError("La propuesta debe estar validada antes de abrir votación.")
        propuesta.estado = "en_votacion"
        propuesta.quorum = quorum
        self.ledger.registrar("APERTURA_VOTACION", {
            "id": id_propuesta,
            "quorum": quorum,
            "canal": f"canal-{id_propuesta}",
            "estado": propuesta.estado,
        })
        print(f"[OK] Votación abierta para {id_propuesta} (quorum={quorum})")

    # 5. Emisión de voto ----------------------------------------------------------
    def emitir_voto(self, id_propuesta: str, votante: str, opcion: str) -> str:
        propuesta = self._obtener(id_propuesta)
        if propuesta.estado != "en_votacion":
            raise ValueError("La propuesta no está en periodo de votación.")
        if not self.ca.es_valido(votante):
            raise PermissionError(f"{votante} no tiene identidad válida.")
        if not MSP.autoriza(self.ca._certificados[votante], "votar"):
            raise PermissionError("Solo estudiantes con rol 'estudiante' pueden votar.")
        token = self.offchain.generar_token_pseudonimo(votante, id_propuesta)
        if token in propuesta.tokens_usados:
            raise PermissionError("Este token ya emitió su voto.")
        propuesta.tokens_usados.add(token)
        propuesta.votos[opcion] += 1
        self.ledger.registrar("EMISION_VOTO", {
            "id": id_propuesta,
            "token": token,
            "opcion": opcion,
        })
        print(f"[OK] Voto registrado con token {token} -> opción '{opcion}'")
        return token

    # 6. Cierre y conteo ------------------------------------------------------------
    def cerrar_y_contar(self, id_propuesta: str):
        propuesta = self._obtener(id_propuesta)
        total = sum(propuesta.votos.values())
        if propuesta.quorum and total < propuesta.quorum:
            resultado = "NO_ALCANZA_QUORUM"
        elif propuesta.votos["a_favor"] > propuesta.votos["en_contra"]:
            resultado = "APROBADA"
        else:
            resultado = "RECHAZADA"
        propuesta.estado = "cerrada"
        bloque = self.ledger.registrar("CIERRE_CONTEO", {
            "id": id_propuesta,
            "resultado": resultado,
            "votos": dict(propuesta.votos),
            "total_votos": total,
        })
        print(f"[OK] Votación cerrada para {id_propuesta}: {resultado} "
              f"(votos={propuesta.votos}) | hash_auditoria={bloque.hash[:16]}...")
        return resultado

    # 7. Consulta de resultados ------------------------------------------------------
    def consultar_resultados(self, id_propuesta: str) -> dict:
        propuesta = self._obtener(id_propuesta)
        return {
            "id": propuesta.id,
            "titulo": propuesta.titulo,
            "estado": propuesta.estado,
            "votos": dict(propuesta.votos),
        }

    # 8. Actualización de estado -----------------------------------------------------
    def actualizar_estado(self, id_propuesta: str, nuevo_estado: str, autoridad: str):
        propuesta = self._obtener(id_propuesta)
        if not self.ca.es_valido(autoridad):
            raise PermissionError(f"{autoridad} no tiene identidad válida.")
        if not MSP.autoriza(self.ca._certificados[autoridad], "actualizar_estado"):
            raise PermissionError(
                "Solo el Consejo Universitario puede actualizar el estado (MSP)."
            )
        propuesta.estado = nuevo_estado
        self.ledger.registrar("ACTUALIZACION_ESTADO", {
            "id": id_propuesta,
            "nuevo_estado": nuevo_estado,
            "autoridad": autoridad,
        })
        print(f"[OK] Estado de {id_propuesta} actualizado a '{nuevo_estado}' por {autoridad}")

    # 3b. Rechazo de propuesta (antes de votación) -------------------------------------
    def rechazar(self, id_propuesta: str, autoridad: str, motivo: str = "Sin justificación"):
        """Permite a facultad/consejo rechazar una propuesta antes de abrir la votación."""
        propuesta = self._obtener(id_propuesta)
        if not self.ca.es_valido(autoridad):
            raise PermissionError(f"{autoridad} no tiene identidad válida.")
        cert = self.ca._certificados[autoridad]
        if not MSP.autoriza(cert, "rechazar"):
            raise PermissionError("Solo facultad o el Consejo pueden rechazar propuestas.")
        if propuesta.estado not in ("borrador", "validada"):
            raise ValueError("Solo se pueden rechazar propuestas en borrador o validadas.")
        propuesta.estado = "rechazada"
        self.offchain.guardar_texto_propuesta(id_propuesta, propuesta.titulo + f"\n[RECHAZADA por {autoridad}]: {motivo}")  # noqa
        self.ledger.registrar("RECHAZO_PROPUESTA", {
            "id": id_propuesta,
            "autoridad": autoridad,
            "rol": cert.rol,
            "motivo": motivo,
            "estado": propuesta.estado,
        })
        print(f"[OK] Propuesta {id_propuesta} RECHAZADA por {autoridad} ({motivo})")

    # Utilidades -----------------------------------------------------------------------
    def _obtener(self, id_propuesta: str) -> Propuesta:
        if id_propuesta not in self.propuestas:
            raise KeyError(f"Propuesta {id_propuesta} no existe.")
        return self.propuestas[id_propuesta]

    @staticmethod
    def _hash_corto(texto: str) -> str:
        return hashlib.sha256(texto.encode()).hexdigest()[:12]
