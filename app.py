import streamlit as st
import pandas as pd
import hashlib
import json

# Configuración de la página
st.set_page_config(
    page_title="DAO Estudiantil - UIDE",
    page_icon="🏛️",
    layout="wide"
)

# ---- ESTILOS CSS PERSONALIZADOS (solo mejora visual) ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --uide-primary: #1f3a93;
        --uide-primary-light: #2a5cbf;
        --uide-accent: #00b4d8;
        --uide-gold: #f4a300;
        --uide-green: #2ecc71;
        --uide-red: #e74c3c;
        --uide-bg-soft: #eef3ff;
        --uide-card-border: #c7d2fe;

        /* Forzar variables de tema claro de Streamlit */
        --text-color: #1e293b !important;
        --text-color-disabled: #64748b !important;
        --background-color: #eef3ff !important;
        --secondary-background-color: #f4f8ff !important;
        --primary-color: #1f3a93 !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #eef3ff !important;
        color: #1e293b !important;
    }

    /* FORZAR TEMA CLARO: texto oscuro en toda la interfaz */
    [data-testid="stAppViewContainer"] {
        color: #1e293b !important;
    }
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] div,
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4 {
        color: #1e293b !important;
    }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {
        color: #1e293b !important;
    }
    /* Inputs: texto oscuro dentro */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        color: #0f172a !important;
    }
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }
    /* Selectbox: texto de la opción y del menú */
    [data-baseweb="select"] * {
        color: #0f172a !important;
    }
    [data-baseweb="popover"] [role="option"] * {
        color: #0f172a !important;
    }
    [data-baseweb="popover"] [role="option"]:hover {
        background-color: #eef3ff !important;
    }
    /* Radio buttons */
    [data-testid="stRadio"] * {
        color: #1e293b !important;
    }
    /* Metricas */
    [data-testid="stMetricLabel"] * {
        color: #334155 !important;
    }
    /* Expander */
    [data-testid="stExpander"] * {
        color: #1e293b !important;
    }
    /* Sidebar */
    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] * {
        color: #1e293b !important;
    }
    /* Alertas / info / success */
    [data-testid="stAlert"] * {
        color: inherit !important;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #334155;
    }

    /* Fondo general: azul suave en vez de blanco */
    .stApp {
        background: linear-gradient(160deg, #e8eefc 0%, #dfe9fa 45%, #d6e4f8 100%) !important;
    }

    /* Encabezado principal */
    .hero-header {
        background: linear-gradient(135deg, #1f3a93 0%, #2a5cbf 55%, #00b4d8 100%);
        padding: 1.6rem 2.2rem;
        border-radius: 1.2rem;
        margin-bottom: 1.5rem;
        color: #ffffff;
        box-shadow: 0 10px 28px rgba(31, 58, 147, 0.3);
        border: 1px solid rgba(255,255,255,0.15);
    }
    .hero-header h1 {
        margin: 0;
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .hero-header p {
        margin: 0.35rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.92;
        font-weight: 400;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.4);
        padding: 0.25rem 0.9rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.7rem;
    }

    /* Tarjetas (cards): fondo claro con tinte azulado */
    .st-card {
        background: linear-gradient(180deg, #ffffff 0%, #f4f8ff 100%);
        border: 1px solid var(--uide-card-border);
        border-radius: 1rem;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 6px 18px rgba(31, 58, 147, 0.1);
        margin-bottom: 1rem;
    }
    .st-card h3 {
        margin-top: 0;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--uide-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .st-card .card-sub {
        color: #5b6b8c;
        font-size: 0.82rem;
        margin-top: -0.4rem;
    }

    /* Chips / badges de estado */
    .status-chip {
        display: inline-block;
        padding: 0.18rem 0.8rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }
    .status-chip.abierta { background: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }
    .status-chip.aprobada { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .status-chip.rechazada { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }

    /* Bloques del ledger */
    .block-card {
        background: linear-gradient(180deg, #ffffff 0%, #f4f8ff 100%);
        border: 1px solid var(--uide-card-border);
        border-left: 5px solid var(--uide-primary);
        border-radius: 0.8rem;
        padding: 1rem 1.2rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 3px 12px rgba(31, 58, 147, 0.08);
    }
    .block-card .block-title {
        font-weight: 700;
        color: var(--uide-primary);
        margin-bottom: 0.4rem;
    }
    .block-card code {
        font-family: 'JetBrains Mono', monospace;
        background: #e8eefb;
        padding: 0.15rem 0.5rem;
        border-radius: 0.4rem;
        font-size: 0.75rem;
        color: #1e3a8a;
    }
    .block-hash {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #5b6b8c;
        word-break: break-all;
    }

    /* Separador decorativo */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #8aa4f0, transparent);
        margin: 1.4rem 0;
        opacity: 0.7;
    }

    /* Metricas */
    [data-testid="stMetric"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f5ff 100%);
        border: 1px solid var(--uide-card-border);
        border-radius: 0.9rem;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 4px 12px rgba(31, 58, 147, 0.1);
    }
    [data-testid="stMetricLabel"] { font-weight: 600; color: #334155; }
    [data-testid="stMetricValue"] { color: var(--uide-primary); font-weight: 800; }

    /* Botones: azules y visibles */
    .stButton > button {
        background: linear-gradient(135deg, #1f3a93 0%, #2a5cbf 60%, #00b4d8 130%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 0.7rem;
        font-weight: 700;
        padding: 0.55rem 1.2rem;
        box-shadow: 0 5px 14px rgba(31, 58, 147, 0.35);
        transition: all 0.15s ease;
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(31, 58, 147, 0.45);
        background: linear-gradient(135deg, #17307e 0%, #2453a8 60%, #0094b8 130%) !important;
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Inputs: fondo blanco con borde azul visible */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        border: 1.5px solid #b8c7f5 !important;
        border-radius: 0.6rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--uide-primary) !important;
        box-shadow: 0 0 0 3px rgba(42, 92, 191, 0.2) !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1.5px solid #b8c7f5 !important;
        border-radius: 0.6rem !important;
    }
    .stNumberInput input {
        background-color: #ffffff !important;
        border: 1.5px solid #b8c7f5 !important;
        border-radius: 0.6rem !important;
    }

    /* Bloque de código: MODO CLARO, sin franjas negras */
    [data-testid="stCodeBlock"] {
        background-color: #f1f5ff !important;
        border: 1px solid #c7d2fe !important;
        border-radius: 0.8rem !important;
    }
    [data-testid="stCodeBlock"] pre {
        background-color: transparent !important;
        color: #1e3a8a !important;
    }
    [data-testid="stCodeBlock"] code, [data-testid="stCodeBlock"] .language-yaml {
        color: #1e3a8a !important;
    }

    /* JSON: MODO CLARO, sin franjas negras */
    [data-testid="stJson"] {
        background-color: #f4f8ff !important;
        border: 1px solid #c7d2fe !important;
        border-radius: 0.8rem !important;
        padding: 0.6rem !important;
    }
    [data-testid="stJson"] .stJson {
        background: transparent !important;
    }

    /* Sidebar: claro con tinte */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f4f8ff 0%, #e6eefb 100%);
        border-right: 1px solid #b8c7f5;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        background: transparent;
    }
    .sidebar-brand {
        background: linear-gradient(135deg, #1f3a93, #00b4d8);
        color: #ffffff;
        border-radius: 0.9rem;
        padding: 0.9rem 1.1rem;
        margin-bottom: 1rem;
        font-weight: 800;
        font-size: 1rem;
        text-align: center;
        box-shadow: 0 6px 16px rgba(31, 58, 147, 0.3);
    }
    .sidebar-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #4b5d85;
        margin-bottom: 0.2rem;
    }

    /* Cajas de éxito/info/error: claras y suaves */
    [data-testid="stAlert"] {
        border-radius: 0.8rem;
        border: 1px solid rgba(0,0,0,0.06);
    }

    /* Tabs: claras */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.6rem;
        background: #ffffff;
        border-radius: 0.9rem;
        padding: 0.4rem 0.4rem;
        border: 1px solid var(--uide-card-border);
        box-shadow: 0 3px 10px rgba(31, 58, 147, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.6rem;
        padding: 0.45rem 1.2rem;
        font-weight: 600;
        color: #334155;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #eef3ff;
    }
    .stTabs [aria-selected="true"] {
        background: var(--uide-primary) !important;
        color: #ffffff !important;
    }

    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    @media (max-width: 700px) {
        .hero-header h1 { font-size: 1.4rem; }
    }
</style>
""", unsafe_allow_html=True)

# Intentar importar los módulos existentes
try:
    from identity import IdentityManager
except ImportError:
    class IdentityManager:
        def __init__(self): self.identities = {}
        def register_identity(self, estudiante_id, facultad):
            self.identities[estudiante_id] = facultad
            return f"CERT-X509-{estudiante_id}"
        def get_registered_identities(self): return self.identities

try:
    from offchain import OffChainDB
except ImportError:
    class OffChainDB:
        def __init__(self):
            self.proposals = {}
            self.tokens = {}
        def get_or_create_token(self, estudiante_id, eleccion):
            token = hashlib.sha256(f"{estudiante_id}_{eleccion}".encode()).hexdigest()
            self.tokens[estudiante_id] = token[:16]
            return token[:16]
        def store_proposal_doc(self, prop_id, titulo, contenido):
            hash_doc = hashlib.sha256(contenido.encode()).hexdigest()
            self.proposals[prop_id] = {"titulo": titulo, "contenido": contenido, "hash": hash_doc}
            return hash_doc
        def get_proposal_doc(self, prop_id): return self.proposals.get(prop_id, {})
        def get_debug_data(self): return self.proposals

try:
    from ledger import Ledger
except ImportError:
    class Ledger:
        def __init__(self):
            self.chain = []
            self.create_genesis()
        def create_genesis(self):
            self.chain.append({"index": 0, "hash": "0000000000", "txs": ["Bloque Génesis DAO UIDE"]})
        def add_block(self, tx):
            idx = len(self.chain)
            prev_hash = self.chain[-1].get("hash", "0") if isinstance(self.chain[-1], dict) else getattr(self.chain[-1], "hash", "0")
            block_hash = hashlib.sha256(f"{idx}{tx}{prev_hash}".encode()).hexdigest()
            self.chain.append({"index": idx, "hash": block_hash, "previous_hash": prev_hash, "txs": [tx]})

try:
    from chaincode import Chaincode
except ImportError:
    class Chaincode:
        def __init__(self, ledger):
            self.ledger = ledger
            self.state = {}
            self.votos = set()
        def invoke(self, fn, args):
            if fn == "CrearPropuesta":
                p_id = args["id"]
                if p_id in self.state:
                    return {"error": "La propuesta ya existe"}
                self.state[p_id] = {
                    "hash_doc": args["hash_doc"],
                    "votos_favor": 0,
                    "votos_contra": 0,
                    "quorum": args["quorum"],
                    "estado": "ABIERTA"
                }
                if hasattr(self.ledger, "add_block"):
                    self.ledger.add_block({"type": "CREAR_PROPUESTA", "id": p_id})
                return {"success": True}
            elif fn == "EmitirVoto":
                p_id = args["propuesta_id"]
                token = args["token_votante"]
                clave = f"{p_id}_{token}"
                if clave in self.votos:
                    return {"error": "Este token ya ha registrado un voto para esta propuesta."}
                if p_id not in self.state or self.state[p_id]["estado"] != "ABIERTA":
                    return {"error": "La propuesta no está abierta para votación."}
                
                if args["opcion"] == "FAVOR":
                    self.state[p_id]["votos_favor"] += 1
                else:
                    self.state[p_id]["votos_contra"] += 1
                
                self.votos.add(clave)
                if hasattr(self.ledger, "add_block"):
                    self.ledger.add_block({"type": "EMITIR_VOTO", "id": p_id, "token": token})
                
                total = self.state[p_id]["votos_favor"] + self.state[p_id]["votos_contra"]
                if total >= self.state[p_id]["quorum"]:
                    self.state[p_id]["estado"] = "APROBADA" if self.state[p_id]["votos_favor"] > self.state[p_id]["votos_contra"] else "RECHAZADA"
                return {"success": True}
        def get_all_proposals(self):
            return self.state

# Función auxiliar para extraer bloques del Ledger independientemente de su estructura
def obtener_bloques_ledger(ledger_obj):
    if hasattr(ledger_obj, 'get_blocks') and callable(getattr(ledger_obj, 'get_blocks')):
        return ledger_obj.get_blocks()
    elif hasattr(ledger_obj, 'chain'):
        return ledger_obj.chain
    elif hasattr(ledger_obj, 'blocks'):
        return ledger_obj.blocks
    elif hasattr(ledger_obj, 'ledger'):
        return ledger_obj.ledger
    return []

# Inicializar componentes en el estado de la sesión
if 'identity_mgr' not in st.session_state:
    st.session_state.identity_mgr = IdentityManager()
if 'offchain_db' not in st.session_state:
    st.session_state.offchain_db = OffChainDB()
if 'ledger' not in st.session_state:
    st.session_state.ledger = Ledger()
if 'chaincode' not in st.session_state:
    st.session_state.chaincode = Chaincode(st.session_state.ledger)

st.markdown("""
<div class="hero-header">
    <h1>🏛️ Portal de Gobernanza DAO Estudiantil UIDE</h1>
    <p>Sistema de toma de decisiones descentralizado sobre Hyperledger Fabric · Identidad SSO · Votación pseudónima</p>
    <span class="hero-badge">⚙️ On-Chain / Off-Chain · MSP · Raft Orderer</span>
</div>
""", unsafe_allow_html=True)

# BARRA LATERAL
st.sidebar.markdown('<div class="sidebar-brand">🪪 Identidad DAO · UIDE</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-label">🔐 Autenticación e Identidad (Fabric CA)</div>', unsafe_allow_html=True)
estudiante_id = st.sidebar.text_input("Matrícula Estudiantil", value="2026-IT-001")
facultad = st.sidebar.selectbox("Organización / Facultad", ["Ingeniería en TIs", "Administración", "Derecho", "Consejo Universitario"])

cert = st.session_state.identity_mgr.register_identity(estudiante_id, facultad) if hasattr(st.session_state.identity_mgr, 'register_identity') else "CERT-X509"
token_pseudonimo = st.session_state.offchain_db.get_or_create_token(estudiante_id, "ELECCION_2026") if hasattr(st.session_state.offchain_db, 'get_or_create_token') else "TOKEN-12345"

st.sidebar.success("✅ Autenticación SSO Verificada")
st.sidebar.markdown('<div class="sidebar-label">Credenciales MSP</div>', unsafe_allow_html=True)
st.sidebar.code(f"Org: {facultad}\nToken Pseudónimo:\n{token_pseudonimo}", language="yaml")

# ---- MÉTRICAS RESUMEN ----
_props_totales = len(st.session_state.chaincode.get_all_proposals()) if hasattr(st.session_state.chaincode, 'get_all_proposals') else 0
_bloques_totales = len(obtener_bloques_ledger(st.session_state.ledger)) - 1 if obtener_bloques_ledger(st.session_state.ledger) else 0
m1, m2, m3, m4 = st.columns(4)
m1.metric("🗳️ Propuestas Activas", _props_totales)
m2.metric("📦 Bloques en el Ledger", max(_bloques_totales, 0))
m3.metric("🔐 Identidades MSP", len(st.session_state.identity_mgr.get_registered_identities()) if hasattr(st.session_state.identity_mgr, 'get_registered_identities') else 0)
m4.metric("🆔 Token Pseudónimo", token_pseudonimo[:8] + "...")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# INTERFAZ PRINCIPAL
tab1, tab2, tab3 = st.tabs(["📝 Crear y Votar Propuestas", "📦 Explorador On-Chain (Ledger)", "🛡️ Arquitectura y Datos"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="st-card"><h3>📝 Crear Propuesta Estudiantil</h3><div class="card-sub">Registra una iniciativa y envíala a votación de la comunidad</div>', unsafe_allow_html=True)
        prop_id = st.text_input("ID de Propuesta", value="PROP-2026-01")
        titulo = st.text_input("Título de la Iniciativa", value="Fondo para Proyectos de Robótica")
        contenido = st.text_area("Descripción Completa", value="Asignación presupuestaria para compra de kits y competencias.")
        quorum = st.number_input("Quórum Mínimo de Votos", min_value=1, value=3)

        if st.button("🚀 Enviar Propuesta a la DAO", use_container_width=True):
            hash_doc = st.session_state.offchain_db.store_proposal_doc(prop_id, titulo, contenido) if hasattr(st.session_state.offchain_db, 'store_proposal_doc') else "hash_123"
            res = st.session_state.chaincode.invoke("CrearPropuesta", {
                "id": prop_id,
                "hash_doc": hash_doc,
                "quorum": quorum,
                "org": facultad
            })
            if isinstance(res, dict) and "error" in res:
                st.error(res["error"])
            else:
                st.success(f"✅ Propuesta {prop_id} registrada en el ledger on-chain!")
                st.caption(f"🔗 Hash de auditoría: `{str(hash_doc)[:20]}...`")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="st-card"><h3>🗳️ Emitir Voto Pseudónimo</h3><div class="card-sub">Tu identidad queda oculta tras un token criptográfico</div>', unsafe_allow_html=True)
        propuestas = st.session_state.chaincode.get_all_proposals() if hasattr(st.session_state.chaincode, 'get_all_proposals') else {}
        if not propuestas:
            st.info("ℹ️ No hay propuestas activas en este momento.")
        else:
            prop_id_sel = st.selectbox("Seleccionar Propuesta para Votar", list(propuestas.keys()))
            datos_p = propuestas[prop_id_sel]
            doc_offchain = st.session_state.offchain_db.get_proposal_doc(prop_id_sel) if hasattr(st.session_state.offchain_db, 'get_proposal_doc') else {}

            estado = datos_p.get('estado', 'N/A').lower()
            estado_clase = 'abierta' if estado == 'abierta' else ('aprobada' if estado == 'aprobada' else 'rechazada')
            st.markdown(f"<span class='status-chip {estado_clase}'>{datos_p.get('estado', 'N/A')}</span>", unsafe_allow_html=True)

            st.write(f"**📌 Título:** {doc_offchain.get('titulo', '')}")
            st.write(f"**⚖️ Quórum:** {datos_p.get('quorum', 'N/A')} votos requeridos")
            st.write(f"**🔑 Hash de Auditoría (Doc):** `{str(datos_p.get('hash_doc', ''))[:24]}...`")

            c_fav, c_con = st.columns(2)
            c_fav.metric("✅ Favor", datos_p.get('votos_favor', 0))
            c_con.metric("❌ Contra", datos_p.get('votos_contra', 0))

            opcion = st.radio("Selecciona tu voto:", ["FAVOR", "CONTRA"], horizontal=True)

            if st.button("✍️ Firmar y Emitir Transacción", use_container_width=True):
                res_voto = st.session_state.chaincode.invoke("EmitirVoto", {
                    "propuesta_id": prop_id_sel,
                    "token_votante": token_pseudonimo,
                    "opcion": opcion
                })

                if isinstance(res_voto, dict) and "error" in res_voto:
                    st.error(f"❌ Transacción Rechazada: {res_voto['error']}")
                else:
                    st.success("✅ Voto endosado y registrado inmutablemente en el bloque.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="st-card"><h3>📦 Estado del Ledger Distribuido (World State)</h3><div class="card-sub">Vista global del estado actual de todas las propuestas en la red</div>', unsafe_allow_html=True)
    propuestas_dict = st.session_state.chaincode.get_all_proposals() if hasattr(st.session_state.chaincode, 'get_all_proposals') else {}
    if propuestas_dict:
        df_prop = pd.DataFrame.from_dict(propuestas_dict, orient='index')
        st.dataframe(df_prop, use_container_width=True)
    else:
        st.info("ℹ️ Aún no hay propuestas registradas.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="st-card"><h3>🔗 Cadena de Bloques Inmutable (Raft Orderer)</h3><div class="card-sub">Cada transacción queda sellada criptográficamente en un bloque</div>', unsafe_allow_html=True)
    bloques = obtener_bloques_ledger(st.session_state.ledger)
    
    if not bloques:
        st.info("ℹ️ No hay bloques registrados en el ledger aún.")
    else:
        for idx, block in enumerate(reversed(bloques)):
            b_hash = block.get('hash', 'N/A') if isinstance(block, dict) else getattr(block, 'hash', 'N/A')
            st.markdown(f"""
            <div class="block-card">
                <div class="block-title">⛓️ Bloque #{len(bloques) - 1 - idx}</div>
                <div class="block-hash">Hash: {str(b_hash)}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander(f"🔍 Ver detalle del bloque #{len(bloques) - 1 - idx}"):
                st.code(str(block), language="json")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="st-card"><h3>🛡️ Arquitectura Híbrida On-Chain / Off-Chain</h3><div class="card-sub">Datos sensibles off-chain (LOPDP) y verificabilidad on-chain</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🗄️ Almacenamiento Off-Chain (Privado - LOPDP):**")
        if hasattr(st.session_state.offchain_db, 'get_debug_data'):
            st.json(st.session_state.offchain_db.get_debug_data())
    with c2:
        st.markdown("**🔐 Control de Accesos MSP / Fabric CA:**")
        if hasattr(st.session_state.identity_mgr, 'get_registered_identities'):
            st.json(st.session_state.identity_mgr.get_registered_identities())
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:2rem; padding-top:1rem; border-top:1px solid #b8c7f5;">
    <span style="color:#4b5d85; font-size:0.75rem;">🏛️ DAO Estudiantil UIDE · Proyecto de Graduación · Hyperledger Fabric · Powered by Streamlit</span>
</div>
""", unsafe_allow_html=True)