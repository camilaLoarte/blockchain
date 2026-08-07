# 🎓 DAO Estudiantil — Prototipo de votación descentralizada

Una plataforma que simula una **DAO (Organización Autónoma Descentralizada)**
universitaria: permite crear propuestas, obtener endosos de varias "facultades"
(a manera de consenso), abrir votaciones y contar resultados sobre un **ledger
distribuido** (cadena de bloques).

> **Para verla corriendo:** hay dos formas. La más vistosa es la **versión web**
> (React + TypeScript con backend en Python). Acompáñate de la sección
> [3. Cómo probar la versión web](#3-cómo-probar-la-versión-web).

---

## 1. Qué es y qué simula

Hyperledger Fabric real necesita Docker, contenedores por organización, orderer
Raft, canales, etc. Este prototipo **reproduce el comportamiento** de esa
arquitectura usando herramientas simples, para que se entienda el conceptos sin
complejidad:

| Capa (arquitectura real)              | Cómo se simula aquí                    | Archivo        |
|---------------------------------------|----------------------------------------|----------------|
| Identidad y seguridad (Fabric CA+MSP) | Certificados con hash + control de roles | `identity.py` |
| Blockchain on-chain (peers/orderer)   | Cadena de bloques enlazados por hash   | `ledger.py`    |
| Off-chain (BD institucional, LOPDP)   | Diccionario en memoria separado        | `offchain.py`  |
| Chaincode (las transacciones)         | Clase `DAOChaincode` (un método por transacción) | `chaincode.py` |
| Flujo completo end-to-end             | Escenario de ejemplo (demo)            | `demo.py`      |

---

## 2. Estructura

```
dao-estudiantil/
├── identity.py        # Fabric CA + MSP (roles y permisos)
├── ledger.py          # Cadena de bloques + verificación de integridad
├── offchain.py        # Datos personales fuera de la cadena (privacidad)
├── chaincode.py       # Las 8 transacciones (crear, endosar, votar, cerrar…)
├── demo.py            # Demo en terminal (sin interface gráfica)
├── app.py             # (legado) interfaz Streamlit
├── server/
│   ├── api.py         # API REST (FastAPI) que reutiliza la lógica
│   └── usuarios.json  # Cuentas de demostración (clave 1234)
└── frontend/
    └── src/           # App web: Login, Dashboard, Ledger, Arquitectura
```

---

## 3. Cómo probar la versión web

Necesitas **Python 3.9+** y **Node.js 18+** instalados.

### Paso 1 — Arrancar el backend (API)

```bash
# (una sola vez) instala las librerías de Python
pip install -r requirements.txt
# hay que tener actualizado typing_extensions (>=4.8)
pip install --upgrade typing_extensions

# arrancar el servidor en http://127.0.0.1:8000
python -m uvicorn server.api:app --host 127.0.0.1 --port 8000
```

Lo correcto es ver algo como `Application startup complete`.

### Paso 2 — Arrancar el frontend (React)

```bash
cd frontend
npm install     # una sola vez
npm run dev     # queda corriendo el servidor de desarrollo
```

### Paso 3 — Abrir la app

En el navegador entra a **http://localhost:5173**.

Entra con cualquiera de estas cuentas (todas con contraseña **`1234`**):

| Usuario    | Rol         | Qué puede hacer                              |
|------------|-------------|----------------------------------------------|
| `camila`   | estudiante  | Crear propuestas y votar                   |
| `alumno`   | estudiante  | Crear propuestas y votar                   |
| `profesor` | facultad    | Endosar, abrir votación, rechazar         |
| `facadm`   | facultad    | Endosar, abrir votación, rechazar         |
| `rector`   | consejo     | Endosar, abrir, cerrar y rechazar                |

> 💡 *Escenario típico:* entra como **estudiante** y crea una propuesta, luego
> cambia a **facultad** para endosarla (necesitas 2 endosos), abre la votación
> con **consejo**, vota con los estudiantes y cierra para ver el resultado en el
> **Ledger**.

---

## 4. Tributos de roles (permisos por identidad)

| Permiso            | estudiante | facultad | consejo |
|--------------------|------------|----------|---------|
| Crear propuesta     | ✅         | ❌       | ❌      |
| Votar              | ✅         | ❌       | ❌      |
| Endosar            | ❌         | ✅       | ✅      |
| Abrir votación     | ❌         | ✅       | ✅      |
| Rechazar           | ❌         | ✅       | ✅      |
| Cerrar y contar    | ❌         | ~        | ✅      |

Distintas acciones se permiten o bloquean en función del rol que se obtiene al
iniciar sesión (la API responde `403` si un rol intenta algo que no le toca).

---

## 5. API REST (para integrar)

| Método | Ruta                     | Descripción                       |
|--------|--------------------------|-----------------------------------|
| POST   | `/api/login`             | Inicia sesión, devuelve token      |
| GET    | `/api/propuestas`        | Lista propuestas                   |
| POST   | `/api/propuestas/crear`    | Crea propuesta (estudiante)        |
| POST   | `/api/propuestas/endosar`  | Endosa (facultad/consejo)          |
| POST   | `/api/propuestas/rechazar` | Rechaza (facultad/consejo)         |
| POST   | `/api/propuestas/abrir`    | Abre votación (facultad/consejo)   |
| POST   | `/api/propuestas/votar`    | Vota (estudiante, token pseudónimo) |
| POST   | `/api/propuestas/cerrar`   | Cierra y cuenta                    |
| GET    | `/api/ledger`           | Cadena de bloques + integridad     |
| GET    | `/api/arquitectura`     | Permisos, identidades, off-chain   |

Cada petición autenticada se hace con `?token=<token>`. El backend valida los
permisos por rol mediante el `MSP`.

---

## 6. Demo en terminal (opcional)

```bash
python demo.py
```

Muestra el ciclo completo con prints: registro de identidades, creación,
endoso de 2/3 facultades, apertura, votos pseudónimos, conteo y verificación de
integridad del ledger (incluye una prueba de que si se modifica un bloque, la
cadena deja de ser válida).

---

## 7. Relación con las 8 transacciones

| # | Transacción             | Método en `chaincode.py`      |
|---|---------------------------|-------------------------------|
| 1 | Registro de identidad     | `registro_identidad()`         |
| 2 | Creación de propuesta     | `crear_propuesta()`            |
| 3 | Validación (endoso)       | `validar()`                    |
| 4 | Apertura de votación      | `abrir_votacion()`             |
| 5 | Emisión de voto           | `emitir_voto()`                |
| 6 | Cierre y conteo           | `cerrar_y_contar()`            |
| 7 | Consulta de resultados    | `consultar_resultados()`       |
| 8 | Actualización de estado   | `actualizar_estado()`          |

---

## 8. Límites del prototipo

- No usa criptografía real (RSA/ECDSA) ni certificados X.509 → se usan hashes
  SHA-256 para simplificar.
- No hay red distribuida real: el consenso Raft y el endoso se simulan en un
  solo proceso.
- Los datos se guardan en memoria (se pierden al cerrar el programa).
- Es una buena base para migrar `chaincode.py` a un chaincode real de
  Hyperledger Fabric.