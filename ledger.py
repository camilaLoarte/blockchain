"""
Simulación de la Capa Blockchain (Peers + Orderer Raft + World State)
=======================================================================
Reemplaza el ledger distribuido de Hyperledger Fabric por una cadena de
bloques enlazados por hash (misma propiedad de inmutabilidad y
trazabilidad descrita en la Fase I y II) y un diccionario en memoria que
hace las veces de "world state" (equivalente conceptual a CouchDB).
"""
import hashlib
import json
import time


class Bloque:
    def __init__(self, indice: int, transacciones: list, hash_anterior: str):
        self.indice = indice
        self.timestamp = time.time()
        self.transacciones = transacciones
        self.hash_anterior = hash_anterior
        self.hash = self._calcular_hash()

    def _calcular_hash(self) -> str:
        contenido = json.dumps(
            {
                "indice": self.indice,
                "timestamp": self.timestamp,
                "transacciones": self.transacciones,
                "hash_anterior": self.hash_anterior,
            },
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(contenido.encode()).hexdigest()

    def to_dict(self):
        return {
            "indice": self.indice,
            "hash": self.hash[:16] + "...",
            "hash_anterior": (self.hash_anterior[:16] + "...") if self.hash_anterior else "GENESIS",
            "transacciones": self.transacciones,
        }


class Ledger:
    """Ledger distribuido simulado (peers + orderer Raft)."""

    def __init__(self):
        self.cadena = [self._bloque_genesis()]
        self.world_state = {}   # equivalente a CouchDB: último estado por ID

    def _bloque_genesis(self) -> Bloque:
        return Bloque(0, [{"tipo": "GENESIS"}], hash_anterior="0" * 64)

    def registrar(self, tipo: str, datos_on_chain: dict) -> Bloque:
        """
        Simula: endoso de peers -> secuenciación por el orderer Raft ->
        commit en el ledger. Solo se aceptan aquí los datos ON-CHAIN
        definidos en la Tabla 1 del documento de Fase II (nunca datos
        personales ni el mapeo token-estudiante en claro).
        """
        tx = {"tipo": tipo, "timestamp": time.time(), **datos_on_chain}
        anterior = self.cadena[-1].hash
        bloque = Bloque(len(self.cadena), [tx], anterior)
        self.cadena.append(bloque)
        clave_estado = datos_on_chain.get("id") or datos_on_chain.get("token")
        if clave_estado:
            self.world_state[clave_estado] = tx
        return bloque

    def verificar_integridad(self) -> bool:
        """Recorre la cadena y confirma que ningún bloque fue alterado."""
        for i in range(1, len(self.cadena)):
            actual, previo = self.cadena[i], self.cadena[i - 1]
            if actual.hash_anterior != previo.hash:
                return False
            if actual.hash != actual._calcular_hash():
                return False
        return True

    def imprimir(self):
        print("\n=== LEDGER (cadena de bloques) ===")
        for b in self.cadena:
            print(f"Bloque #{b.indice} | hash={b.hash[:16]}... | anterior={b.hash_anterior[:16]}...")
            for tx in b.transacciones:
                print(f"    -> {tx}")
