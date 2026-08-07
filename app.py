import streamlit as st
import pandas as pd

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
    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
    }
    /* Menú desplegable completo en claro */
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] [data-baseweb="popover"],
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #ffffff !important;
        border: 1px solid #c7d2fe !important;
        border-radius: 0.6rem !important;
    }
    [data-baseweb="popover"] [role="option"],
    li[data-testid="stSelectboxVirtualDropdownOption"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    [data-baseweb="popover"] [role="option"] *,
    li[data-testid="stSelectboxVirtualDropdownOption"] * {
        color: #0f172a !important;
    }
    [data-baseweb="popover"] [role="option"]:hover,
    li[data-testid="stSelectboxVirtualDropdownOption"]:hover {
        background-color: #eef3ff !important;
    }
    [data-baseweb="popover"] [role="option"][aria-selected="true"],
    li[data-testid="stSelectboxVirtualDropdownOption"]:focus {
        background-color: #dfe8ff !important;
    }
    /* Radio buttons: opciones en claro */
    [data-testid="stRadio"] * {
        color: #1e293b !important;
    }
    [data-testid="stRadio"] label {
        background-color: transparent !important;
    }
    /* Number input: botones +/- en claro */
    [data-testid="stNumberInput"] button {
        background-color: #eef3ff !important;
        color: #1e293b !important;
        border: 1px solid #c7d2fe !important;
    }
    [data-testid="stNumberInput"] button:hover {
        background-color: #dce6ff !important;
    }
    /* Metricas */
    [data-testid="stMetricLabel"] * {
        color: #334155 !important;
    }
    [data-testid="stMetric"] .st-ae,
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #334155 !important;
    }
    /* Captions / textos pequeños */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #5b6b8c !important;
    }
    /* Dataframe: tema claro */
    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        border-radius: 0.6rem !important;
        border: 1px solid #c7d2fe !important;
    }
    [data-testid="stDataFrame"] div[role="row"],
    [data-testid="stDataFrame"] thead th,
    [data-testid="stDataFrame"] tbody td {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    /* Título del menú hamburguesa y demás tooltips */
    [data-testid="stTooltip"],
    [data-testid="stTooltip"] * {
        background-color: #ffffff !important;
        color: #1e293b !important;
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

# ---- BACKEND REAL: importar las capas de la Fase II ----
from identity import FabricCA, MSP
from offchain import AlmacenOffChain
from ledger import Ledger
from chaincode import DAOChaincode, Propuesta


# Función auxiliar para extraer bloques del Ledger independientemente de su estructura
def obtener_bloques_ledger(ledger_obj):
    if hasattr(ledger_obj, 'get_blocks') and callable(getattr(ledger_obj, 'get_blocks')):
        return ledger_obj.get_blocks()
    elif hasattr(ledger_obj, 'cadena'):
        return ledger_obj.cadena
    elif hasattr(ledger_obj, 'chain'):
        return ledger_obj.chain
    elif hasattr(ledger_obj, 'blocks'):
        return ledger_obj.blocks
    elif hasattr(ledger_obj, 'ledger'):
        return ledger_obj.ledger
    return []


# Estado de la sesión: una sola instancia de la DAO completa (CA + Ledger + OffChain + Chaincode)
if 'dao' not in st.session_state:
    st.session_state.dao = DAOChaincode()
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'rol_usuario' not in st.session_state:
    st.session_state.rol_usuario = "estudiante"
if 'cert_actual' not in st.session_state:
    st.session_state.cert_actual = None

dao = st.session_state.dao

st.markdown("""
<div class="hero-header">
    <h1>🏛️ Portal de Gobernanza DAO Estudiantil UIDE</h1>
    <p>Sistema de toma de decisiones descentralizado sobre Hyperledger Fabric · Identidad SSO · Votación pseudónima</p>
    <span class="hero-badge">⚙️ On-Chain / Off-Chain · MSP · Raft Orderer</span>
</div>
""", unsafe_allow_html=True)

# BARRA LATERAL
st.sidebar.markdown('<div class="sidebar-brand">🪪 Identidad DAO · UIDE</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-label">🔐 Registro de Identidad (Fabric CA)</div>', unsafe_allow_html=True)
estudiante_id = st.sidebar.text_input("Usuario / Matrícula", value="2026-IT-001")
rol_sel = st.sidebar.selectbox("Rol", ["estudiante", "facultad", "consejo"])
facultad = st.sidebar.selectbox("Organización / Facultad", ["Ingeniería en TICs", "Administración", "Derecho", "Consejo Universitario"])

usuario = st.session_state.usuario
rol_usuario = st.session_state.rol_usuario
cert_actual = st.session_state.cert_actual

if st.sidebar.button("🪪 Emitir Certificado", use_container_width=True):
    try:
        cert = dao.registro_identidad(estudiante_id, rol_sel, facultad)
        st.session_state.usuario = estudiante_id
        st.session_state.rol_usuario = rol_sel
        st.session_state.cert_actual = cert
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"❌ {type(e).__name__}: {e}")

if cert_actual is not None:
    st.sidebar.success(f"✅ Certificado válido para **{usuario}**")
    st.sidebar.markdown('<div class="sidebar-label">Credenciales MSP</div>', unsafe_allow_html=True)
    st.sidebar.code(
        f"Usuario: {usuario}\n"
        f"Rol: {rol_usuario}\n"
        f"Serie: {cert_actual.numero_serie}\n"
        f"Huella: {cert_actual.huella[:20]}...",
        language="yaml",
    )
    permisos = MSP.PERMISOS.get(rol_usuario, set())
    st.sidebar.caption("Permisos: " + ", ".join(sorted(permisos)))
else:
    st.sidebar.info("ℹ️ Emite tu certificado para operar en la DAO.")

# ---- MÉTRICAS RESUMEN ----
_bloques_totales = max(len(obtener_bloques_ledger(dao.ledger)) - 1, 0)
_integridad = dao.ledger.verificar_integridad()
m1, m2, m3, m4 = st.columns(4)
m1.metric("🗳️ Propuestas Creadas", len(dao.propuestas))
m2.metric("📦 Bloques en el Ledger", _bloques_totales)
m3.metric("🔐 Identidades Emitidas", len(dao.ca._certificados))
m4.metric("🔎 Integridad del Ledger", "✅ ÍNTEGRO" if _integridad else "❌ ALTERADO")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# INTERFAZ PRINCIPAL
tab1, tab2, tab3 = st.tabs(["📝 Crear y Votar Propuestas", "📦 Explorador On-Chain (Ledger)", "🛡️ Arquitectura y Datos"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="st-card"><h3>📝 Crear Propuesta</h3><div class="card-sub">Solo usuarios con identidad válida (permiso: crear_propuesta)</div>', unsafe_allow_html=True)
        titulo = st.text_input("Título de la Iniciativa", value="Fondo para Proyectos de Robótica")
        contenido = st.text_area("Descripción Completa", value="Asignación presupuestaria para compra de kits y competencias.")

        if st.button("🚀 Enviar Propuesta a la DAO", use_container_width=True):
            if cert_actual is None:
                st.error("❌ Emite tu certificado en la barra lateral primero.")
            else:
                try:
                    propuesta = dao.crear_propuesta(usuario, titulo, contenido)
                    st.success(f"✅ Propuesta registrada: **{propuesta.id}**")
                    st.caption(f"🔗 Estado inicial: `{propuesta.estado}` · Autor hash: `{dao._hash_corto(usuario)}`")
                except Exception as e:
                    st.error(f"❌ {type(e).__name__}: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="st-card"><h3>🗳️ Gobernanza de Propuestas</h3><div class="card-sub">Endoso 2/3 → Apertura → Votación → Cierre y conteo</div>', unsafe_allow_html=True)
        ids_prop = list(dao.propuestas.keys())
        if not ids_prop:
            st.info("ℹ️ Aún no hay propuestas. Crea la primera.")
        else:
            prop_id_sel = st.selectbox("Seleccionar Propuesta", ids_prop)
            prop = dao.propuestas[prop_id_sel]

            # --- Indicador visual del ciclo de vida ---
            pasos = {"borrador": 0, "validada": 1, "en_votacion": 2, "cerrada": 3}
            paso_actual = pasos.get(prop.estado, 0)
            nombres = ["1. Borrador", "2. Validada", "3. En votación", "4. Cerrada"]
            cols_pasos = st.columns(4)
            for i, (col, nombre) in enumerate(zip(cols_pasos, nombres)):
                if i < paso_actual:
                    col.markdown(f"<div style='text-align:center;background:#dcfce7;color:#15803d;border:1px solid #86efac;border-radius:8px;padding:6px 4px;font-size:0.72rem;font-weight:700;'>✅ {nombre}</div>", unsafe_allow_html=True)
                elif i == paso_actual:
                    col.markdown(f"<div style='text-align:center;background:#1f3a93;color:#ffffff;border-radius:8px;padding:6px 4px;font-size:0.72rem;font-weight:800;'>⬤ {nombre}</div>", unsafe_allow_html=True)
                else:
                    col.markdown(f"<div style='text-align:center;background:#eef3ff;color:#64748b;border:1px solid #c7d2fe;border-radius:8px;padding:6px 4px;font-size:0.72rem;font-weight:700;'>○ {nombre}</div>", unsafe_allow_html=True)

            estado_clase = {
                "borrador": "abierta",
                "validada": "aprobada",
                "en_votacion": "abierta",
                "cerrada": "rechazada",
                "rechazada": "rechazada",
            }.get(prop.estado, "rechazada")
            st.markdown(f"<span class='status-chip {estado_clase}'>Estado: {prop.estado.upper()}</span>", unsafe_allow_html=True)

            st.write(f"**📌 Título:** {prop.titulo}")
            st.write(f"**👤 Autor:** {prop.autor}")

            endosos_faltantes = max(DAOChaincode.POLITICA_ENDOSO_MINIMA - len(prop.endosos), 0)
            st.write(f"**🤝 Endosos:** {len(prop.endosos)}/{DAOChaincode.POLITICA_ENDOSO_MINIMA} necesarios  ·  **⚖️ Quórum:** {prop.quorum if prop.quorum else 'N/D'}")
            if prop.estado == "borrador":
                if endosos_faltantes > 0:
                    st.caption(f"👉 Faltan **{endosos_faltantes}** endoso(s) para abrir la votación.")

            c_fav, c_con, c_abs = st.columns(3)
            c_fav.metric("✅ A favor", prop.votos["a_favor"])
            c_con.metric("❌ En contra", prop.votos["en_contra"])
            c_abs.metric("⬜ Abstención", prop.votos["abstencion"])

            # --- Acciones según el estado de la propuesta ---
            if prop.estado == "borrador":
                if rol_usuario in ("facultad", "consejo"):
                    st.info(f"👈 Ahora endosa la propuesta como **{usuario}** ({rol_usuario}), o recházala.")
                    col_end, col_rec = st.columns(2)
                    if col_end.button("🤝 Endosar / Validar", use_container_width=True):
                        try:
                            dao.validar(prop_id_sel, usuario, rol_usuario)
                            st.success(f"✅ Endoso registrado ({len(prop.endosos)}/{DAOChaincode.POLITICA_ENDOSO_MINIMA}).")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {type(e).__name__}: {e}")
                    motivo_rechazo = st.text_input("Motivo del rechazo (opcional)", key=f"motivo_{prop_id_sel}")
                    if col_rec.button("❌ Rechazar Propuesta", use_container_width=True):
                        try:
                            dao.rechazar(prop_id_sel, usuario, motivo_rechazo or "Sin justificación")
                            st.error(f"🚫 Propuesta {prop_id_sel} rechazada por {usuario}.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {type(e).__name__}: {e}")
                else:
                    st.warning(f"🔒 Tu rol es **estudiante**. Cambia a rol `facultad` o `consejo` en la barra lateral y emite un nuevo certificado para endosar.")

            elif prop.estado == "validada":
                if rol_usuario == "consejo":
                    st.info("👈 La propuesta ya está validada. Ábrela a votación como Consejo, o recházala.")
                    quorum_input = st.number_input("Quórum para abrir votación", min_value=1, value=2)
                    col_ab, col_rec2 = st.columns(2)
                    if col_ab.button("🗳️ Abrir Votación", use_container_width=True):
                        try:
                            dao.abrir_votacion(prop_id_sel, int(quorum_input), usuario)
                            st.success("✅ Votación abierta.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {type(e).__name__}: {e}")
                    motivo_rechazo2 = st.text_input("Motivo del rechazo (opcional)", key=f"motivo2_{prop_id_sel}")
                    if col_rec2.button("❌ Rechazar Propuesta", use_container_width=True):
                        try:
                            dao.rechazar(prop_id_sel, usuario, motivo_rechazo2 or "Sin justificación")
                            st.error(f"🚫 Propuesta {prop_id_sel} rechazada por {usuario}.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {type(e).__name__}: {e}")
                else:
                    st.warning("🔒 La propuesta está validada. Cambia a rol `consejo` en la barra lateral para abrir la votación.")

            elif prop.estado == "en_votacion":
                if rol_usuario == "estudiante":
                    st.info("👈 La votación está abierta. Emite tu voto como estudiante.")
                    opcion = st.radio("Selecciona tu voto:", ["a_favor", "en_contra", "abstencion"], horizontal=True)
                    if st.button("✍️ Firmar y Emitir Voto", use_container_width=True):
                        try:
                            token = dao.emitir_voto(prop_id_sel, usuario, opcion)
                            st.success(f"✅ Voto registrado con token pseudónimo `{token}`.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {type(e).__name__}: {e}")
                else:
                    st.warning("🔒 La votación está abierta: cambia a rol `estudiante` para votar.")
                    if rol_usuario in ("facultad", "consejo"):
                        st.info("👈 Cuando terminen de votar, cierra y cuenta como facultad o consejo.")
                        if st.button("🏁 Cerrar y Contar", use_container_width=True):
                            try:
                                resultado = dao.cerrar_y_contar(prop_id_sel)
                                st.success(f"✅ Resultado: **{resultado}**")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ {type(e).__name__}: {e}")

            elif prop.estado == "rechazada":
                st.markdown("""
                <div style="background:#fee2e2;color:#b91c1c;border:1px solid #fca5a5;border-radius:0.8rem;padding:1rem 1.2rem;">
                    <b>🚫 Propuesta rechazada por el Consejo / Facultad.</b><br>
                    <span style="font-size:0.85rem;">La propuesta no pasará a votación.</span>
                </div>
                """, unsafe_allow_html=True)

            elif prop.estado == "cerrada":
                total_votos = sum(prop.votos.values())
                if prop.quorum and total_votos < prop.quorum:
                    resultado = "NO_ALCANZA_QUORUM"
                elif prop.votos["a_favor"] > prop.votos["en_contra"]:
                    resultado = "APROBADA"
                else:
                    resultado = "RECHAZADA"
                resultado_clase = "aprobada" if resultado == "APROBADA" else "rechazada"
                st.markdown(f"<span class='status-chip {resultado_clase}'>🏁 {resultado}</span>", unsafe_allow_html=True)
                st.write(f"**Total de votos:** {total_votos} (quórum requerido: {prop.quorum})")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="st-card"><h3>📦 World State (Estado Actual)</h3><div class="card-sub">Equivalente conceptual a CouchDB: último estado de cada entidad on-chain</div>', unsafe_allow_html=True)
    world_state = dao.ledger.world_state
    if world_state:
        df_ws = pd.DataFrame.from_dict(world_state, orient='index')
        st.dataframe(df_ws, use_container_width=True)
    else:
        st.info("ℹ️ Aún no hay transacciones en el world state.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="st-card"><h3>🔗 Cadena de Bloques Inmutable (Raft Orderer)</h3><div class="card-sub">Cada transacción queda sellada criptográficamente en un bloque enlazado</div>', unsafe_allow_html=True)
    bloques = obtener_bloques_ledger(dao.ledger)

    if not bloques:
        st.info("ℹ️ No hay bloques registrados en el ledger aún.")
    else:
        integridad = dao.ledger.verificar_integridad()
        st.metric("🔎 Integridad de la cadena", "✅ ÍNTEGRA" if integridad else "❌ ALTERADA")
        st.caption("El hash de cada bloque depende del anterior: cualquier alteración se detecta al verificar.")

        for idx, block in enumerate(reversed(bloques)):
            b_hash = getattr(block, 'hash', 'N/A')
            b_prev = getattr(block, 'hash_anterior', '0')
            b_indice = getattr(block, 'indice', len(bloques) - 1 - idx)
            st.markdown(f"""
            <div class="block-card">
                <div class="block-title">⛓️ Bloque #{b_indice}</div>
                <div class="block-hash">Hash: {str(b_hash)}</div>
                <div class="block-hash">Hash anterior: {str(b_prev)}</div>
                <div class="block-hash">Transacciones: {len(getattr(block, 'transacciones', []))}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander(f"🔍 Ver detalle del bloque #{b_indice}"):
                st.json([{
                    "tipo": tx.get("tipo"),
                    "datos": {k: v for k, v in tx.items() if k not in ("tipo", "timestamp")},
                    "timestamp": tx.get("timestamp"),
                } for tx in getattr(block, 'transacciones', [])])
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="st-card"><h3>🛡️ Arquitectura Híbrida On-Chain / Off-Chain</h3><div class="card-sub">Datos sensibles off-chain (LOPDP) y verificabilidad on-chain</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🗄️ Almacenamiento Off-Chain (Privado - LOPDP):**")
        st.json({
            "perfiles_personales": dao.offchain.datos_personales,
            "textos_propuestas": {k: v[:80] + ("..." if len(v) > 80 else "") for k, v in dao.offchain.propuestas_texto.items()},
            "tokens_pseudonimos_emitidos": len(dao.offchain._mapeo_token_estudiante),
        })
        st.caption("El mapeo token ↔ estudiante NO se publica en el ledger (minimización de datos).")
    with c2:
        st.markdown("**🔐 Control de Accesos MSP / Fabric CA:**")
        st.json({
            sujeto: {
                "rol": cert.rol,
                "facultad": cert.facultad,
                "serie": cert.numero_serie,
                "huella": cert.huella[:16] + "...",
            }
            for sujeto, cert in dao.ca._certificados.items()
        })
        st.caption(f"Política de endoso: se requieren {DAOChaincode.POLITICA_ENDOSO_MINIMA} de 3 organizaciones.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:2rem; padding-top:1rem; border-top:1px solid #b8c7f5;">
    <span style="color:#4b5d85; font-size:0.75rem;">🏛️ DAO Estudiantil UIDE · Proyecto de Graduación · Hyperledger Fabric · Powered by Streamlit</span>
</div>
""", unsafe_allow_html=True)