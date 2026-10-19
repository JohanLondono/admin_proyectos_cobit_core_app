"""
Catálogo Interactivo de Procesos COBIT 2019 [COB-TK05, COB-ST07].
Explorador oficial de los 5 dominios y 40 objetivos de gobierno y gestión.
"""

import streamlit as st
from engine.cobit_data import DOMAINS, COBIT_PROCESSES, get_all_processes_list

def show_catalog():
    st.title("📖 Catálogo Interactivo COBIT 2019")
    st.markdown("Guía oficial de consulta con los 5 dominios de ISACA y sus 40 objetivos de gobierno y gestión.")

    # Buscador y filtros rápidos
    col_search, col_filter = st.columns([3, 2])
    with col_search:
        search_kw = st.text_input("🔍 Buscar proceso por código o palabra clave:", placeholder="Ej. seguridad, riesgo, BAI06, datos...")
    with col_filter:
        domain_choice = st.selectbox("Filtrar por Dominio:", ["Todos los Dominios (40 procesos)"] + [f"{k} - {v['name']}" for k, v in DOMAINS.items()])

    all_procs = get_all_processes_list()

    # Aplicar filtros
    filtered = all_procs
    if domain_choice != "Todos los Dominios (40 procesos)":
        d_code = domain_choice.split(" - ")[0]
        filtered = [p for p in filtered if p["domain"] == d_code]

    if search_kw.strip():
        kw = search_kw.strip().lower()
        filtered = [
            p for p in filtered
            if kw in p["id"].lower()
            or kw in p["name"].lower()
            or kw in p["purpose"].lower()
            or any(kw in prac.lower() for prac in p["practices"])
        ]

    st.caption(f"Mostrando **{len(filtered)}** de 40 objetivos COBIT.")

    # Resumen de Dominios en tarjetas de color
    st.markdown("### 🏛️ Dominios del Marco COBIT 2019")
    dom_cols = st.columns(5)
    for idx, (d_code, d_info) in enumerate(DOMAINS.items()):
        with dom_cols[idx]:
            count = len([p for p in all_procs if p["domain"] == d_code])
            st.markdown(f"""
            <div style="background-color:{d_info['color']}; color:white; padding:10px; border-radius:8px; text-align:center;">
                <div style="font-weight:800; font-size:1.1rem;">{d_code}</div>
                <div style="font-size:0.75rem; margin-top:2px;">{d_info['type']}</div>
                <div style="font-size:0.8rem; font-weight:700; margin-top:4px;">{count} procesos</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Listado de Procesos
    st.markdown("### 📋 Objetivos de Gobierno y Gestión")
    if not filtered:
        st.info("No se encontraron procesos que coincidan con la búsqueda.")
        return

    for p in filtered:
        dom_meta = DOMAINS.get(p["domain"], {})
        badge_core = "🔥 PROCESO CORE / ESENCIAL" if p.get("core") else ""
        
        with st.expander(f"🔹 **{p['id']}**: {p['name']} ({p['domain']}) {badge_core}"):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"**Dominio:** {dom_meta.get('name', p['domain'])}")
                st.markdown(f"**Propósito Oficial:**")
                st.info(p["purpose"])
            with c2:
                st.markdown("**Prácticas Clave Recomendadas:**")
                for prac in p["practices"]:
                    st.markdown(f"- ✅ {prac}")
