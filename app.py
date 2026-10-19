"""
Sistema de Consultoría en Gobierno y Gestión de TI (COBIT 2019 + IA) - Core App
Universidad del Quindío - Formulación de Proyectos - 8vo Semestre
Punto de Entrada Principal y Router de Navegación.
"""

import streamlit as st
import os
from pathlib import Path

# Configuración inicial de Streamlit (debe ser la primera llamada de Streamlit)
st.set_page_config(
    page_title="COBIT 2019 Core Consulting",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialización de la base de datos y datos semilla
from database.db_manager import init_db, authenticate_user, get_all_clients
init_db()

# Cargar estilos CSS personalizados
def load_custom_css():
    css_path = Path(__file__).parent / "static" / "custom.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()

# Inicialización de variables de sesión
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "dashboard"
if "active_client_id" not in st.session_state:
    clients = get_all_clients()
    if clients:
        st.session_state["active_client_id"] = clients[0]["id"]

# =====================================================================
# VISTA DE LOGIN Y AUTENTICACIÓN [COB-ST01, COB-ST03]
# =====================================================================
def show_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c_left, c_center, c_right = st.columns([1, 2, 1])

    with c_center:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); color:white; padding:28px; border-radius:14px; text-align:center; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);">
            <div style="font-size:3rem;">🏛️</div>
            <h2 style="color:white !important; margin:10px 0 4px 0;">COBIT 2019 Core Consulting</h2>
            <div style="font-size:0.9rem; opacity:0.85;">Sistema de Evaluación de Madurez y Gobernanza de TI</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("#### Iniciar Sesión Segura")
            username = st.text_input("Usuario:", placeholder="admin, consultor, o cliente")
            password = st.text_input("Contraseña:", type="password", placeholder="••••••••")

            col_sub1, col_sub2 = st.columns([1, 1])
            with col_sub1:
                submitted = st.form_submit_button("🔑 Entrar al Sistema", type="primary", use_container_width=True)

            if submitted:
                user = authenticate_user(username.strip(), password.strip())
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = user
                    st.success(f"¡Bienvenido, {user['full_name']}!")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas. Por favor verifica usuario y contraseña.")

        # Acceso Rápido / Demo credentials helper
        st.markdown("""
        <div style="background:#F1F5F9; border-left:4px solid #0284C7; padding:12px 16px; border-radius:0 8px 8px 0; margin-top:16px; font-size:0.82rem; color:#334155;">
            <b>Credenciales de demostración preconfiguradas:</b><br>
            • <b>Administrador:</b> usuario <code>admin</code> / clave <code>admin123</code><br>
            • <b>Consultor Líder:</b> usuario <code>consultor</code> / clave <code>cobit2019</code><br>
            • <b>Cliente (CIO):</b> usuario <code>cliente</code> / clave <code>cliente2019</code>
        </div>
        """, unsafe_allow_html=True)

# Si el usuario no está autenticado, renderizar login
if not st.session_state["authenticated"]:
    show_login()
    st.stop()

# =====================================================================
# SIDEBAR DE NAVEGACIÓN Y CONTEXTO
# =====================================================================
user = st.session_state["user"]
role_label = {
    "admin": "👑 Administrador",
    "consultant": "💼 Consultor Líder",
    "client": "🏢 Cliente Corporativo"
}.get(user.get("role"), "Usuario")

with st.sidebar:
    st.markdown(f"""
    <div style="padding:10px 0 16px 0; border-bottom:1px solid #E2E8F0;">
        <div style="font-size:1.4rem; font-weight:800; color:#1E3A8A; display:flex; align-items:center; gap:8px;">
            <span>🏛️</span> COBIT Core
        </div>
        <div style="font-size:0.78rem; color:#64748B;">Marco COBIT 2019 + IA</div>
    </div>
    """, unsafe_allow_html=True)

    # Tarjeta de usuario
    st.markdown(f"""
    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px; margin:14px 0 18px 0;">
        <div style="font-weight:700; font-size:0.88rem; color:#0F172A;">{user['full_name']}</div>
        <div style="font-size:0.75rem; color:#0284C7; font-weight:600;">{role_label}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**MENÚ PRINCIPAL**")

    # Botones de navegación
    nav_items = [
        ("📊", "dashboard", "Dashboard Principal"),
        ("🏢", "clients", "Gestión de Clientes"),
        ("📖", "catalog", "Catálogo COBIT 2019"),
        ("📝", "assessment", "Evaluación de Madurez"),
        ("🤖", "diagnosis", "Diagnóstico e IA"),
        ("🗺️", "roadmap", "Hoja de Ruta (Roadmap)"),
        ("📄", "documents", "Ingesta Documental (NLP)"),
        ("📥", "reports", "Reportes y Descargas")
    ]

    for icon, key, label in nav_items:
        is_current = (st.session_state["current_view"] == key)
        btn_type = "primary" if is_current else "secondary"
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True, type=btn_type):
            st.session_state["current_view"] = key
            st.rerun()

    st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)

    # Botón Cerrar Sesión
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.rerun()

    st.caption("Universidad del Quindío • 8vo Semestre")

# =====================================================================
# ENRUTADOR DE VISTAS (ROUTER)
# =====================================================================
view = st.session_state["current_view"]

if view == "dashboard":
    from views.dashboard_view import show_dashboard
    show_dashboard()
elif view == "clients":
    from views.clients_view import show_clients
    show_clients()
elif view == "catalog":
    from views.catalog_view import show_catalog
    show_catalog()
elif view == "assessment":
    from views.assessment_view import show_assessment
    show_assessment()
elif view == "diagnosis":
    from views.diagnosis_view import show_diagnosis
    show_diagnosis()
elif view == "roadmap":
    from views.roadmap_view import show_roadmap
    show_roadmap()
elif view == "documents":
    from views.documents_view import show_documents
    show_documents()
elif view == "reports":
    from views.reports_view import show_reports
    show_reports()
else:
    st.error("Vista no encontrada.")
