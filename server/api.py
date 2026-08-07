"""
API HTTP (FastAPI) para la DAO Estudiantil.

Reutiliza la lógica completa del prototipo (chaincode, ledger, identity,
offchain) exponiéndola como endpoints JSON para el frontend React.
"""
import json
import os
import secrets
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# La lógica de negocio importa los módulos ya existentes del prototipo
from chaincode import DAOChaincode
from identity import MSP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USUARIOS_PATH = os.path.join(BASE_DIR, "usuarios.json")

app = FastAPI(title="DAO Estudiantil API", version="1.0.0")

# CORS: permitir que el frontend React (local) consuma esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Estado del servidor (en memoria, igual que el prototipo) ----
dao = DAOChaincode()
SESIONES: dict[str, dict] = {}          # token -> {usuario, rol}


def cargar_usuarios() -> list[dict]:
    with open(USUARIOS_PATH, encoding="utf-8") as f:
        return json.load(f)["usuarios"]


def registrar_todos():
    """Registra las identidades iniciales en la Autoridad Certificadora."""
    for u in cargar_usuarios():
        try:
            dao.registro_identidad(u["usuario"], u["rol"], u["facultad"], u.get("correo", ""))
        except Exception:
            pass  # ya registrado


registrar_todos()


def usuario_por_token(token: str) -> dict:
    usuario_id = SESIONES.get(token)
    if not usuario_id:
        raise HTTPException(status_code=401, detail="Sesión no válida o expirada.")
    for u in cargar_usuarios():
        if u["usuario"] == usuario_id:
            return u
    raise HTTPException(status_code=401, detail="Usuario no encontrado.")


def es_rol(token: str, *roles) -> bool:
    u = usuario_por_token(token)
    return u["rol"] in roles


# ---- Esquemas de petición ----
class LoginBody(BaseModel):
    usuario: str
    contrasena: str


class CrearPropuestaBody(BaseModel):
    titulo: str
    descripcion: str


class EndosoBody(BaseModel):
    propuesta_id: str


class RechazoBody(BaseModel):
    propuesta_id: str
    motivo: str = "Sin justificación"


class AbrirVotacionBody(BaseModel):
    propuesta_id: str
    quorum: int


class VotoBody(BaseModel):
    propuesta_id: str
    opcion: str  # a_favor | en_contra | abstencion


# ---- Endpoints de autenticación ----
@app.post("/api/login")
def login(body: LoginBody):
    for u in cargar_usuarios():
        if u["usuario"] == body.usuario and u["contrasena"] == body.contrasena:
            token = secrets.token_hex(16)
            SESIONES[token] = u["usuario"]
            return {
                "token": token,
                "usuario": u["usuario"],
                "nombre": u["nombre"],
                "rol": u["rol"],
                "facultad": u["facultad"],
                "permisos": sorted(MSP.PERMISOS.get(u["rol"], set())),
            }
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos.")


@app.post("/api/logout")
def logout(token: str):
    SESIONES.pop(token, None)
    return {"ok": True}


# ---- Propuestas ----
@app.get("/api/propuestas")
def listar_propuestas(token: str):
    usuario_por_token(token)
    result = []
    for pid, prop in dao.propuestas.items():
        result.append({
            "id": pid,
            "titulo": prop.titulo,
            "autor": prop.autor,
            "estado": prop.estado,
            "endosos": len(prop.endosos),
            "endosos_minimo": DAOChaincode.POLITICA_ENDOSO_MINIMA,
            "quorum": prop.quorum,
            "votos": dict(prop.votos),
            "descripcion": dao.offchain.propuestas_texto.get(pid, ""),
            "motivo_rechazo": dao.offchain.propuestas_texto.get(pid, "").split("[RECHAZADA]")[-1]
            if "RECHAZADA" in dao.offchain.propuestas_texto.get(pid, "")
            else None,
        })
    return result


@app.post("/api/propuestas/crear")
def crear_propuesta(token: str, body: CrearPropuestaBody):
    u = usuario_por_token(token)
    if "crear_propuesta" not in MSP.PERMISOS.get(u["rol"], set()):
        raise HTTPException(status_code=403, detail="Tu rol no puede crear propuestas.")
    propuesta = dao.crear_propuesta(u["usuario"], body.titulo, body.descripcion)
    return {"id": propuesta.id, "estado": propuesta.estado}


@app.post("/api/propuestas/endosar")
def endosar(token: str, body: EndosoBody):
    u = usuario_por_token(token)
    try:
        dao.validar(body.propuesta_id, u["usuario"], u["rol"])
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    prop = dao.propuestas[body.propuesta_id]
    return {"endosos": len(prop.endosos), "estado": prop.estado}


@app.post("/api/propuestas/rechazar")
def rechazar(token: str, body: RechazoBody):
    u = usuario_por_token(token)
    try:
        dao.rechazar(body.propuesta_id, u["usuario"], body.motivo)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    prop = dao.propuestas[body.propuesta_id]
    return {"estado": prop.estado}


@app.post("/api/propuestas/abrir")
def abrir_votacion(token: str, body: AbrirVotacionBody):
    u = usuario_por_token(token)
    try:
        dao.abrir_votacion(body.propuesta_id, body.quorum, u["usuario"])
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    prop = dao.propuestas[body.propuesta_id]
    return {"estado": prop.estado, "quorum": prop.quorum}


@app.post("/api/propuestas/votar")
def votar(token: str, body: VotoBody):
    u = usuario_por_token(token)
    try:
        t = dao.emitir_voto(body.propuesta_id, u["usuario"], body.opcion)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    prop = dao.propuestas[body.propuesta_id]
    return {"token": t, "votos": dict(prop.votos)}


@app.post("/api/propuestas/cerrar")
def cerrar(token: str, body: EndosoBody):
    u = usuario_por_token(token)
    if u["rol"] not in ("facultad", "consejo"):
        raise HTTPException(status_code=403, detail="Tu rol no puede cerrar las votaciones.")
    resultado = dao.cerrar_y_contar(body.propuesta_id)
    return {"resultado": resultado}


# ---- Ledger ----
@app.get("/api/ledger")
def obtener_ledger(token: str):
    usuario_por_token(token)
    bloques = []
    for b in dao.ledger.cadena:
        bloques.append({
            "indice": b.indice,
            "hash": b.hash,
            "hash_anterior": b.hash_anterior or "0",
            "transacciones": b.transacciones,
        })
    return {
        "bloques": bloques,
        "world_state": dao.ledger.world_state,
        "integridad": dao.ledger.verificar_integridad(),
    }


# ---- Arquitectura / datos ----
@app.get("/api/arquitectura")
def obtener_arquitectura(token: str):
    usuario_por_token(token)
    return {
        "permisos_msp": MSP.PERMISOS,
        "identidades": {
            s: {"rol": c.rol, "facultad": c.facultad, "serie": c.numero_serie}
            for s, c in dao.ca._certificados.items()
        },
        "offchain_perfiles": dao.offchain.datos_personales,
        "politica_endoso": DAOChaincode.POLITICA_ENDOSO_MINIMA,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}