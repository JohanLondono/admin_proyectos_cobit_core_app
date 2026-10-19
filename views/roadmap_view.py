"""
Generador y Visualizador de Hojas de Ruta (Roadmaps) COBIT 2019 [COB-TK10, COB-ST14, COB-ST15].
Organiza iniciativas por fases cronológicas, destaca Quick Wins y gestiona el presupuesto.
"""

import streamlit as st
import pandas as pd
from database.db_manager import (
    get_all_clients, get_assessments_by_client, get_assessment_scores,
    get_roadmap_by_assessment, get_roadmap_initiatives, save_roadmap
)
from engine.roadmap_engine import generate_roadmap_plan

def show_roadmap():
    st.title("🗺️ Hoja de Ruta de Transformación (Roadmap)")
    st.markdown("Plan estratégico secuenciado por fases para elevar el nivel de madurez institucional.")

    clients = get_all_clients()
    if not clients:
        st.warning("No hay clientes registrados.")
        return

    client_ids = [c["id"] for c in clients]
    client_names = [f"{c['name']} ({c['sector']})" for c in clients]
    curr_c_idx = 0
    if st.session_state.get("active_client_id") in client_ids:
        curr_c_idx = client_ids.index(st.session_state["active_client_id"])

    selected_c_idx = st.selectbox("Empresa Cliente:", range(len(clients)), format_func=lambda i: client_names[i], index=curr_c_idx, key="road_client_picker")
    active_client = clients[selected_c_idx]
    st.session_state["active_client_id"] = active_client["id"]

    assessments = get_assessments_by_client(active_client["id"])
    if not assessments:
        st.info("No hay evaluaciones registradas para este cliente.")
        return

    active_eval = assessments[0]
    scores = get_assessment_scores(active_eval["id"])

    # Consultar si ya existe un roadmap guardado
    existing_roadmap = get_roadmap_by_assessment(active_eval["id"])

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn2:
        if st.button("⚡ Regenerar Hoja de Ruta", help="Genera un plan optimizado usando el algoritmo multi-criterio COBIT"):
            new_plan = generate_roadmap_plan(scores, active_client["name"])
            save_roadmap(
                assessment_id=active_eval["id"],
                client_id=active_client["id"],
                title=new_plan["title"],
                total_budget=new_plan["total_budget"],
                horizon_months=new_plan["horizon_months"],
                summary=new_plan["summary"],
                initiatives=new_plan["initiatives"]
            )
            st.success("¡Hoja de ruta regenerada con éxito!")
            st.rerun()

    if not existing_roadmap:
        st.info("Aún no se ha generado una hoja de ruta para esta evaluación. Haz clic en 'Generar Hoja de Ruta'.")
        if st.button("🚀 Generar Hoja de Ruta Ahora", type="primary"):
            new_plan = generate_roadmap_plan(scores, active_client["name"])
            save_roadmap(
                assessment_id=active_eval["id"],
                client_id=active_client["id"],
                title=new_plan["title"],
                total_budget=new_plan["total_budget"],
                horizon_months=new_plan["horizon_months"],
                summary=new_plan["summary"],
                initiatives=new_plan["initiatives"]
            )
            st.rerun()
        return

    initiatives = get_roadmap_initiatives(existing_roadmap["id"])

    # Tarjetas de Presupuesto y Plazos
    st.markdown("---")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Presupuesto Estimado", f"${existing_roadmap['total_budget']:,.0f} COP")
    with r2:
        st.metric("Horizonte de Ejecución", f"{existing_roadmap['horizon_months']} Meses")
    with r3:
        qw_count = len([i for i in initiatives if i["is_quick_win"]])
        st.metric("Iniciativas Rápidas (Quick Wins)", f"{qw_count} proyectos")
    with r4:
        st.metric("Total de Iniciativas", f"{len(initiatives)} acciones")

    st.info(f"📌 **Resumen Estratégico:** {existing_roadmap['summary']}")

    # SECCIÓN DESTACADA: QUICK WINS
    quick_wins = [i for i in initiatives if i["is_quick_win"]]
    if quick_wins:
        st.markdown("### ⚡ Quick Wins Prioritarios (< 90 Días)")
        st.caption("Iniciativas de alto impacto y rápida implementación para generar victorias tempranas:")
        qw_cols = st.columns(min(3, len(quick_wins)))
        for idx, qw in enumerate(quick_wins[:3]):
            with qw_cols[idx]:
                st.markdown(f"""
                <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:12px; margin-bottom:10px;">
                    <span class="badge-qw">⚡ QUICK WIN</span>
                    <div style="font-weight:700; color:#14532D; margin-top:6px; font-size:0.95rem;">{qw['title']}</div>
                    <div style="font-size:0.82rem; color:#166534; margin:4px 0;">{qw['description']}</div>
                    <div style="font-size:0.8rem; color:#4B5563; margin-top:6px;"><b>Responsable:</b> {qw['responsible_role']}</div>
                    <div style="font-size:0.8rem; color:#15803D;"><b>Inversión:</b> ${qw['estimated_cost']:,.0f} COP | <b>Tiempo:</b> {qw['estimated_months']} meses</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # FASES TEMPORALES DE LA HOJA DE RUTA
    st.subheader("📅 Desglose del Plan por Fases")
    f_tab1, f_tab2, f_tab3 = st.tabs([
        "Fase 1: Cimientos y Quick Wins (Meses 1-3)",
        "Fase 2: Consolidación y Procesos Core (Meses 4-8)",
        "Fase 3: Optimización y Monitoreo (Meses 9-18)"
    ])

    for phase_num, f_tab in [(1, f_tab1), (2, f_tab2), (3, f_tab3)]:
        with f_tab:
            p_inits = [i for i in initiatives if i["phase"] == phase_num]
            if not p_inits:
                st.info(f"No hay iniciativas programadas para la Fase {phase_num}.")
                continue

            for init in p_inits:
                badge = "⚡ QUICK WIN" if init["is_quick_win"] else f"Prioridad {init['priority']}"
                with st.expander(f"🔹 [{init.get('process_id') or 'TI'}] {init['title']} — {badge}"):
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.markdown(f"**Descripción:** {init['description']}")
                        st.markdown(f"**Rol Responsable:** {init['responsible_role']}")
                    with c2:
                        st.markdown(f"**Duración Estimada:** {init['estimated_months']} meses")
                        st.markdown(f"**Presupuesto Sugerido:** ${init['estimated_cost']:,.0f} COP")
                        st.markdown(f"**Estado:** `{init.get('status', 'pending')}`")
