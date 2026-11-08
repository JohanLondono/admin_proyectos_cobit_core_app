"""
Diagnóstico de Brechas e Inteligencia Artificial COBIT 2019 [COB-ST12, COB-ST13].
Proporciona alineación estratégica de negocio con NLP (TF-IDF + Coseno), análisis
cualitativo integrado y matriz cuantitativa de riesgos de gobernanza y TI.
"""

import streamlit as st
import pandas as pd
from database.db_manager import (
    get_all_clients, get_assessments_by_client, get_assessment_scores,
    get_documents_by_client
)
from engine.maturity_engine import calculate_assessment_metrics
from engine.ai_engine import align_business_goals, generate_heuristic_diagnosis

def show_diagnosis():
    st.title("🤖 Diagnóstico Inteligente de Brechas y Riesgos")
    st.markdown("Análisis estratégico cualitativo y cuantitativo potenciado por IA semántica (TF-IDF), NLP y alineación al negocio.")

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
    client_docs = get_documents_by_client(active_client["id"])

    tab_diag, tab_align, tab_risks = st.tabs(["📑 Diagnóstico Integral Multi-Fuente", "🎯 Alineación Estratégica con IA / NLP", "🛡️ Matriz de Riesgos Tecnológicos"])

    # TAB 1: DIAGNÓSTICO INTEGRAL
    with tab_diag:
        diag = generate_heuristic_diagnosis(active_client, metrics, scores, client_docs)
        st.markdown(diag["summary"])
        st.markdown("---")

        # Tarjeta resumen si hay documentos NLP procesados
        if client_docs:
            st.markdown(f"""
            <div class="info-box">
                <b>📚 Inteligencia Documental Activa:</b> Se incorporaron evidencias de <b>{len(client_docs)} documento(s)</b> institucional(es) cargados en el módulo NLP para corroborar los hallazgos de evaluación.
            </div>
            """, unsafe_allow_html=True)

        st.subheader("🔍 Hallazgos Clave por Dominio y Control")
        for f in diag["findings"]:
            st.markdown(f)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("⚡ Recomendaciones Inmediatas (Quick Wins & Prioridades)")
        for r in diag["recommendations"]:
            st.success(f"💡 {r}")

    # TAB 2: ALINEACIÓN ESTRATÉGICA DE NEGOCIO [COB-ST12]
    with tab_align:
        st.subheader("🎯 Asistente de Alineación Estratégica con NLP")
        st.markdown("Describe un reto, prioridad o meta estratégica del cliente. El motor semántico calculará la afinidad vectorial (TF-IDF + Coseno) con los 40 procesos COBIT 2019:")

        # Presets rápidos de retos estratégicos
        preset_choice = st.selectbox(
            "Selecciona un reto frecuente o escribe tu propio objetivo:",
            [
                "Personalizado (Escribir en el campo inferior)",
                "Expandir los canales digitales reduciendo fraudes y caídas de servicio",
                "Garantizar la continuidad operativa del centro de datos y copias de seguridad ante ransomware",
                "Cumplir con auditoría externa, SGSI y normatividad de protección de datos",
                "Optimizar el presupuesto de TI y alinear las inversiones tecnológicas al ROI del negocio"
            ]
        )

        default_text = "Expandir los canales digitales reduciendo fraudes y caídas de servicio"
        if preset_choice != "Personalizado (Escribir en el campo inferior)":
            default_text = preset_choice

        col_g1, col_g2 = st.columns([3, 1])
        with col_g1:
            strategic_input = st.text_input(
                "Meta o Reto Estratégico de la Empresa:",
                value=default_text,
                placeholder="Ej. Modernizar la arquitectura cloud, reducir tiempos de respuesta a incidentes..."
            )
        with col_g2:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            align_btn = st.button("🚀 Analizar Alineación Semántica", use_container_width=True)

        if strategic_input:
            recs = align_business_goals(strategic_input, active_client.get("sector", ""), top_k=6)
            st.markdown(f"**Procesos COBIT 2019 con mayor afinidad semántica y estratégica ({len(recs)} identificados):**")

            recs_table = []
            for r in recs:
                recs_table.append({
                    "Código": r["process_id"],
                    "Dominio": r.get("domain", ""),
                    "Nombre del Proceso": r.get("name", ""),
                    "Afinidad Semántica": f"{r.get('similarity_pct', 80.0):.1f}%",
                    "Criticidad": r.get("criticality", "Alta"),
                    "Justificación Semántica y Práctica Clave": r.get("reason", "")
                })
            st.dataframe(pd.DataFrame(recs_table), use_container_width=True, hide_index=True)

    # TAB 3: MATRIZ DE RIESGOS TECNOLÓGICOS Y GOBERNANZA
    with tab_risks:
        st.subheader("🛡️ Matriz Cuantitativa de Riesgos de Gobernanza y TI")
        st.caption("Evaluación calculada a partir de las brechas de madurez, evidencias ausentes y hallazgos documentales:")

        diag = generate_heuristic_diagnosis(active_client, metrics, scores, client_docs)
        for rk in diag["risks"]:
            lvl = rk["level"]
            if lvl == "Crítico":
                color = "#DC2626"
                badge_style = "background:rgba(220,38,38,0.15); color:#EF4444; border:1px solid #EF4444;"
            elif lvl == "Alto":
                color = "#EF4444"
                badge_style = "background:rgba(239,68,68,0.15); color:#EF4444; border:1px solid #EF4444;"
            elif lvl == "Medio":
                color = "#F59E0B"
                badge_style = "background:rgba(245,158,11,0.15); color:#F59E0B; border:1px solid #F59E0B;"
            else:
                color = "#10B981"
                badge_style = "background:rgba(16,185,129,0.15); color:#10B981; border:1px solid #10B981;"

            with st.container():
                st.markdown(f"""
                <div style="margin-bottom:6px;">
                    <span style="font-weight:700; font-size:1.1rem;">⚠️ {rk['category']}</span> — 
                    <span style="font-size:0.8rem; font-weight:700; padding:2px 8px; border-radius:6px; {badge_style}">Riesgo {lvl} ({rk.get('exposure_score', 50)}% Exposición)</span>
                    <span style="font-size:0.75rem; opacity:0.8; margin-left:8px;">[COBIT: {rk.get('cobit_ref', 'TI')}]</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Causa Raíz y Hallazgo:** {rk['description']}")
                st.info(f"**Acción de Mitigación Recomendada:** {rk['action']}")
                st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
