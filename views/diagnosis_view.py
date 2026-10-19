"""
Diagnóstico de Brechas e Inteligencia Artificial COBIT 2019 [COB-ST12, COB-ST13].
Proporciona alineación estratégica de negocio, análisis cualitativo y matriz de riesgos.
"""

import streamlit as st
import pandas as pd
from database.db_manager import (
    get_all_clients, get_assessments_by_client, get_assessment_scores
)
from engine.maturity_engine import calculate_assessment_metrics
from engine.ai_engine import align_business_goals, generate_heuristic_diagnosis

def show_diagnosis():
    st.title("🤖 Diagnóstico Inteligente de Brechas y Riesgos")
    st.markdown("Análisis estratégico cualitativo potenciado por IA heurística y alineación al negocio.")

    clients = get_all_clients()
    if not clients:
        st.warning("No hay clientes registrados.")
        return

    client_ids = [c["id"] for c in clients]
    client_names = [f"{c['name']} ({c['sector']})" for c in clients]
    curr_c_idx = 0
    if st.session_state.get("active_client_id") in client_ids:
        curr_c_idx = client_ids.index(st.session_state["active_client_id"])

    selected_c_idx = st.selectbox("Selecciona la Empresa para Diagnóstico:", range(len(clients)), format_func=lambda i: client_names[i], index=curr_c_idx)
    active_client = clients[selected_c_idx]
    st.session_state["active_client_id"] = active_client["id"]

    assessments = get_assessments_by_client(active_client["id"])
    if not assessments:
        st.info("Este cliente no cuenta con evaluaciones. Por favor crea una en 'Evaluación COBIT'.")
        return

    active_eval = assessments[0]
    scores = get_assessment_scores(active_eval["id"])
    metrics = calculate_assessment_metrics(scores)

    tab_diag, tab_align, tab_risks = st.tabs(["📑 Diagnóstico Integral", "🎯 Alineación Estratégica", "🛡️ Matriz de Riesgos"])

    # TAB 1: DIAGNÓSTICO INTEGRAL
    with tab_diag:
        diag = generate_heuristic_diagnosis(active_client, metrics)
        st.markdown(diag["summary"])
        st.markdown("---")

        st.subheader("🔍 Hallazgos Clave por Dominio")
        for f in diag["findings"]:
            st.markdown(f"- {f}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("⚡ Recomendaciones Inmediatas (Quick Wins)")
        for r in diag["recommendations"]:
            st.success(f"💡 {r}")

    # TAB 2: ALINEACIÓN ESTRATÉGICA DE NEGOCIO [COB-ST12]
    with tab_align:
        st.subheader("🎯 Asistente de Alineación Estratégica")
        st.markdown("Ingresa una prioridad o meta estratégica del negocio del cliente para que la IA sugiera los procesos COBIT 2019 prioritarios:")

        col_g1, col_g2 = st.columns([3, 1])
        with col_g1:
            strategic_input = st.text_input(
                "Meta o Reto Estratégico de la Empresa:",
                value="Expandir los canales digitales reduciendo fraudes y caídas de servicio",
                placeholder="Ej. Reducir costos operativos, cumplir normatividad bancaria..."
            )
        with col_g2:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            align_btn = st.button("Analizar Alineación", use_container_width=True)

        if strategic_input:
            recs = align_business_goals(strategic_input, active_client.get("sector", ""))
            st.markdown(f"**Procesos COBIT 2019 recomendados para soportar este objetivo ({len(recs)}):**")

            recs_table = []
            for r in recs:
                recs_table.append({
                    "Código": r["process_id"],
                    "Dominio": r.get("domain", ""),
                    "Nombre del Proceso": r.get("name", ""),
                    "Criticidad": r.get("criticality", "Alta"),
                    "Justificación Semántica": r.get("reason", "")
                })
            st.dataframe(pd.DataFrame(recs_table), use_container_width=True, hide_index=True)

    # TAB 3: MATRIZ DE RIESGOS TECNOLÓGICOS
    with tab_risks:
        st.subheader("🛡️ Matriz de Riesgos de Gobernanza y TI")
        st.caption("Identificación de amenazas inherentes derivadas de las brechas de madurez.")

        diag = generate_heuristic_diagnosis(active_client, metrics)
        for rk in diag["risks"]:
            color = "#DC2626" if rk["level"] == "Alto" else "#D97706"
            with st.container():
                st.markdown(f"#### ⚠️ {rk['category']} — <span style='color:{color}; font-size:0.9rem;'>Riesgo {rk['level']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Descripción del Riesgo:** {rk['description']}")
                st.info(f"**Acción de Mitigación Recomendada:** {rk['action']}")
                st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
