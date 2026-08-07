# Prototipo DAO Estudiantil — Demo en Python (Fase III)

Prototipo funcional que simula, sin dependencias externas, el ciclo de vida
completo de una decisión dentro de la DAO estudiantil diseñada en la **Fase I**
(conceptual) y la **Fase II** (arquitectura técnica sobre Hyperledger Fabric).

## 1. Qué simula y por qué

Hyperledger Fabric real requiere Docker, contenedores por organización, un
orderer Raft, canales, CouchDB, etc. Para una **demo académica en Python**, este
prototipo reproduce el *comportamiento* de cada capa de la arquitectura de la
Fase II usando únicamente la librería estándar:

| Capa de la Fase II                          | Cómo se simula aquí                                           | Archivo         |
|----------------------------------------------|-----------------------------------------------------------------|------------------|
| Identidad y seguridad (Fabric CA + MSP)      | Certificados con hash SHA-256 + control de roles/permisos      | `identity.py`    |
| Blockchain on-chain (peers + orderer Raft)   | Cadena de bloques enlazados por hash (inmutable y verificable) | `ledger.py`      |
| Off-chain (BD institucional, LOPDP)          | Diccionarios en memoria separados del ledger                    | `offchain.py`    |
| Chaincode (las 8 transacciones de la Tabla 1)| Clase `DAOChaincode` con un método por transacción              | `chaincode.py`   |
| Flujo completo end-to-end                    | Escenario de ejemplo (propuesta, endoso, votación, conteo)     | `demo.py`        |

No requiere Hyperledger Fabric instalado ni ninguna librería de terceros —
solo Python 3.9+ y su librería estándar (`hashlib`, `json`, `secrets`, `time`).

## 2. Estructura de archivos

```
dao-estudiantil/
├── identity.py    # Fabric CA + MSP simulados
├── ledger.py       # Cadena de bloques (peers + orderer Raft + world state)
├── offchain.py      # Base de datos institucional off-chain
├── chaincode.py       # Las 8 transacciones de la Tabla 1 (Fase II, 2.6)
├── demo.py              # Script que ejecuta el flujo completo
└── README.md
```

## 3. Cómo ejecutarlo

```bash
# 1. Verificar Python 3.9 o superior
python3 --version

# 2. Ejecutar la demo completa
cd dao-estudiantil
python3 demo.py
```

No hace falta `pip install` nada.

## 4. Qué muestra la demo (`demo.py`)

1. **Registro de identidades**: 3 estudiantes, 2 facultades y el Consejo
   Universitario reciben su certificado digital simulado.
2. **Creación de propuesta**: una estudiante crea una propuesta de
   presupuesto (ej. Club de Robótica).
3. **Validación / endoso multi-organización**: se requieren endosos de al
   menos 2 de 3 facultades para que la propuesta pase a "validada" —tal como
   describe la política de endoso de Fabric en la Fase II (2 de 3).
4. **Apertura de votación**: el Consejo abre la votación con un quórum
   mínimo.
5. **Emisión de votos pseudónimos**: cada estudiante vota con un token
   pseudónimo distinto (el mapeo token↔estudiante queda off-chain, cifrado y
   de acceso restringido, igual que en el modelo de datos de la Fase II).
6. **Cierre y conteo automático**: el propio "chaincode" calcula el
   resultado (`APROBADA`, `RECHAZADA` o `NO_ALCANZA_QUORUM`).
7. **Consulta pública de resultados**.
8. **Verificación de integridad del ledger**: recorre toda la cadena y
   confirma que los hashes encajan (`True`).
9. **Intento de voto duplicado**: se muestra que el sistema lo rechaza.
10. **Prueba de inmutabilidad**: se altera a la fuerza un bloque ya
    confirmado y se vuelve a verificar la cadena — el resultado cambia a
    `False`, demostrando en código la propiedad de "transparencia e
    inmutabilidad" mencionada como justificación en la Fase I.

## 5. Relación con las 8 transacciones de la Tabla 1 (Fase II)

| # | Transacción             | Método en `chaincode.py`     |
|---|---------------------------|-------------------------------|
| 1 | Registro de identidad     | `registro_identidad()`        |
| 2 | Creación de propuesta     | `crear_propuesta()`           |
| 3 | Validación (endoso)       | `validar()`                   |
| 4 | Apertura de votación      | `abrir_votacion()`            |
| 5 | Emisión de voto           | `emitir_voto()`               |
| 6 | Cierre y conteo           | `cerrar_y_contar()`           |
| 7 | Consulta de resultados    | `consultar_resultados()`      |
| 8 | Actualización de estado   | `actualizar_estado()`         |

## 6. Límites del prototipo (a mencionar en tu informe)

- No usa criptografía real (RSA/ECDSA) ni certificados X.509 reales — se
  reemplazan por hashes SHA-256 para simplificar la demo.
- No hay red distribuida real: el "consenso Raft" y el "endoso de peers" se
  simulan de forma secuencial en un solo proceso, no con nodos físicos
  separados por facultad.
- Los datos se guardan en memoria (se pierden al cerrar el programa); una
  versión posterior podría persistirlos en SQLite o JSON para que la demo
  sobreviva entre ejecuciones.
- Es una base ideal para, en una siguiente iteración, migrar la lógica de
  `chaincode.py` a un chaincode real de Hyperledger Fabric (Go/JS), como
  se planteó como siguiente paso en la conclusión de la Fase II.

## 7. Posibles extensiones para la sustentación

- Agregar una interfaz de línea de comandos (`argparse`) para correr
  escenarios interactivos en vivo.
- Guardar el ledger en un archivo JSON para inspeccionarlo con un cliente
  aparte (simulando una "consulta pública" real).
- Añadir un segundo escenario donde una propuesta es `RECHAZADA` o no
  alcanza `quorum`.

## 8. Versión web (React + TypeScript + FastAPI)

La lógica de `chaincode.py` se expone como una API REST (FastAPI) que consume
un frontend en React con TypeScript. La DAO vive como instancia única en
memoria del servidor (igual que el prototipo).

### Estructura

```
dao-estudiantil/
├── server/
│   ├── api.py            # Endpoints REST (login, propuestas, ledger, arquitectura)
│   └── usuarios.json     # Credenciales y roles de la demo
├── frontend/
│   ├── src/
│   │   ├── pages/        # Login, Dashboard, Ledger, Arquitectura
│   │   ├── components/   # Layout (barra superior con navegación)
│   │   ├── auth.tsx      # Contexto de sesión (token + rol)
│   │   ├── api.ts        # Cliente axios con token en cada petición
│   │   └── types.ts      # Tipos compartidos (Propuesta, Bloque, etc.)
│   ├── vite.config.ts    # Proxy /api → http://127.0.0.1:8000
│   └── package.json
```

### Requisitos

- Python 3.9+ con `fastapi` y `uvicorn` (`pip install -r requirements.txt`)
- Node.js 18+ (el frontend usa Vite)

### Cómo ejecutar

```bash
# 1. Terminal 1 — backend en http://127.0.0.1:8000
python -m uvicorn server.api:app --host 127.0.0.1 --port 8000

# 2. Terminal 2 — frontend en http://localhost:5173
cd frontend
npm install
npm run dev
```

Abrir `http://localhost:5173` y entrar con un usuario de `server/usuarios.json`
(por defecto todos usan la contraseña `1234`):

| Usuario   | Rol         |
|-----------|-------------|
| `camila`  | estudiante  |
| `alumno`  | estudiante  |
| `profesor`| facultad    |
| `facadm`  | facultad    |
| `rector`  | consejo     |

### API REST

| Método | Ruta                    | Descripción                       |
|--------|-------------------------|-----------------------------------|
| POST   | `/api/login`            | Inicia sesión, devuelve token     |
| GET    | `/api/propuestas`       | Lista propuestas                  |
| POST   | `/api/propuestas/crear` | Crea propuesta (estudiante)       |
| POST   | `/api/propuestas/endosar`| Endosa (facultad/consejo)        |
| POST   | `/api/propuestas/rechazar`| Rechaza (facultad/consejo)      |
| POST   | `/api/propuestas/abrir` | Abre votación (facultad/consejo)  |
| POST   | `/api/propuestas/votar` | Vota (estudiante, token pseudónimo)|
| POST   | `/api/propuestas/cerrar`| Cierra y cuenta                   |
| GET    | `/api/ledger`           | Cadena de bloques + integridad    |
| GET    | `/api/arquitectura`     | Permisos, identidades, off-chain  |

Cada petición autenticada se hace con `?token=<token>` (o cabecera). El
backend valida los permisos por rol mediante el `MSP` del `identity.py`.
