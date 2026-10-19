"""
Cuestionario Interactivo de Evaluación de Madurez COBIT 2019 [COB-ST10, COB-ST11].
Permite calificar procesos en escala 0-5, registrar evidencias y calcular el IMO en tiempo real.
"""

import streamlit as st
from datetime import datetime
from database.db_manager import (
    get_all_clients, get_assessments_by_client, create_assessment,
    get_assessment_scores, save_all_assessment_scores
)
from engine.cobit_data import DOMAINS, MATURITY_LEVELS, COBIT_PROCESSES
from engine.maturity_engine import calculate_assessment_metrics

def show_assessment():
    st.title("📝 Evaluación de Madurez COBIT 2019")
    st.markdown("Cuestionario formal para diagnosticar el nivel de capacidad de los procesos en la escala 0 a 5.")

    clients = get_all_clients()
    if not clients:
        st.warning("⚠️ Primero registra una empresa en 'Gestión de Clientes'.")
        return

    # Selección de Cliente
    client_ids = [c["id"] for c in clients]
    client_names = [f"{c['name']} ({c['sector']})" for c in clients]

    current_c_idx = 0
    if st.session_state.get("active_client_id") in client_ids:
        current_c_idx = client_ids.index(st.session_state["active_client_id"])

    col_c1, col_c2 = st.columns([2, 2])
    with col_c1:
        selected_client_idx = st.selectbox(
            "🏢 Cliente para Evaluar:",
            range(len(clients)),
            format_func=lambda i: client_names[i],
            index=current_c_idx,
            key="eval_client_picker"
        )
        active_client = clients[selected_client_idx]
        st.session_state["active_client_id"] = active_client["id"]

    # Evaluaciones existentes
    assessments = get_assessments_by_client(active_client["id"])

    with col_c2:
        # Opción para crear nueva evaluación o seleccionar existente
        eval_options = ["➕ Crear Nueva Evaluación"] + [f"{a['title']} [{a['code']}]" for a in assessments]
        selected_eval_choice = st.selectbox("📋 Expediente de Evaluación:", eval_options, key="eval_picker")

    # Si seleccionó crear nueva evaluación
    if selected_eval_choice == "➕ Crear Nueva Evaluación":
        st.markdown("### 🆕 Configurar Nueva Evaluación COBIT")
        with st.form("new_assessment_form"):
            new_title = st.text_input("Título de la Evaluación *", value=f"Diagnóstico de Madurez COBIT 2019 — {datetime.now().strftime('%B %Y')}")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                eval_type = st.radio("Alcance de la Evaluación:", [
                    ("comprehensive", "Diagnóstico Integral (40 Procesos COBIT)"),
                    ("quick", "Diagnóstico Rápido / Quick Assessment (18 Procesos Core)")
                ], format_func=lambda x: x[1])
                consultant = st.text_input("Consultor Líder Responsable", value=st.session_state.get("user", {}).get("full_name", "Ing. Johan Londoño"))
            with col_t2:
                target_date = st.date_input("Fecha Objetivo de Cierre")
                notes = st.text_area("Objetivo y Alcance Preliminar", placeholder="Propósito del diagnóstico, áreas involucradas...")

            if st.form_submit_button("🚀 Iniciar Expediente de Evaluación"):
                new_eval_id = create_assessment(
                    client_id=active_client["id"],
                    title=new_title,
                    assessment_type=eval_type[0],
                    lead_consultant=consultant,
                    target_date=str(target_date),
                    notes=notes
                )
                st.session_state["active_assessment_id"] = new_eval_id
                st.success("¡Evaluación creada con éxito! Ahora puedes calificar los procesos a continuación.")
                st.rerun()
        return

    # Si seleccionó una evaluación existente
    eval_index = eval_options.index(selected_eval_choice) - 1
    current_assessment = assessments[eval_index]
    st.session_state["active_assessment_id"] = current_assessment["id"]

    # Cargar los puntajes de la evaluación activa
    scores = get_assessment_scores(current_assessment["id"])
    if not scores:
        st.info("No se encontraron registros de puntuación para esta evaluación.")
        return

    # Calcular métricas actuales
    metrics = calculate_assessment_metrics(scores)

    # Barra superior de estado y métricas en vivo
    st.markdown("---")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("IMO Actual", f"{metrics['imo']:.2f} / 5.0", delta=metrics['level_label'])
    with m_col2:
        st.metric("Meta Deseada", f"{metrics['target_imo']:.2f} / 5.0")
    with m_col3:
        st.metric("Brecha Global", f"{metrics['overall_gap']:.2f} pts")
    with m_col4:
        st.metric("Procesos Evaluados", f"{metrics['processes_count']} procesos")

    st.markdown("<br>", unsafe_allow_html=True)

    # Cuestionario por Dominios en Pestañas
    st.subheader("📊 Cuestionario de Madurez por Dominio")
    st.caption("Ajusta el Nivel Actual (0-5), la Meta y documenta la evidencia observada.")

    domain_tabs = st.tabs([f"{d} ({len([s for s in scores if s['domain'] == d])})" for d in DOMAINS.keys()])

    updated_scores = []

    for tab_idx, d_code in enumerate(DOMAINS.keys()):
        with domain_tabs[tab_idx]:
            dom_meta = DOMAINS[d_code]
            st.markdown(f"#### {dom_meta['name']}")
            st.caption(dom_meta['description'])

            dom_scores = [s for s in scores if s['domain'] == d_code]
            if not dom_scores:
                st.info(f"No hay procesos asignados al dominio {d_code} en este tipo de evaluación.")
                continue

            for s in dom_scores:
                pid = s["process_id"]
                p_info = COBIT_PROCESSES.get(pid, {})
                curr_score = float(s.get("current_score", 0.0))
                targ_score = float(s.get("target_score", 3.0))

                with st.expander(f"🔹 **{pid}**: {p_info.get('name', pid)} (Actual: {curr_score:.1f} | Meta: {targ_score:.1f})"):
                    st.caption(f"**Propósito:** {p_info.get('purpose', '')}")

                    c_score, c_target = st.columns(2)
                    with c_score:
                        new_curr = st.select_slider(
                            f"Nivel Actual para {pid}:",
                            options=[0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                            value=curr_score,
                            key=f"curr_{pid}"
                        )
                        lvl_int = int(min(5, max(0, new_curr)))
                        st.caption(f"*{MATURITY_LEVELS[lvl_int]['label']}*: {MATURITY_LEVELS[lvl_int]['short_desc']}")

                    with c_target:
                        new_targ = st.select_slider(
                            f"Nivel Meta para {pid}:",
                            options=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                            value=targ_score,
                            key=f"targ_{pid}"
                        )

                    new_evidence = st.text_input(
                        "Evidencias Probatorias / Hallazgos:",
                        value=s.get("evidence", "") or "",
                        placeholder="Ej. Política documentada en 2024, actas de comité, logs de auditoría...",
                        key=f"evid_{pid}"
                    )
                    new_obs = st.text_input(
                        "Observaciones y Plan Inmediato:",
                        value=s.get("observations", "") or "",
                        placeholder="Ej. Se requiere formalizar el procedimiento antes del Q3...",
                        key=f"obs_{pid}"
                    )

                    updated_scores.append({
                        "process_id": pid,
                        "domain": d_code,
                        "current_score": new_curr,
                        "target_score": new_targ,
                        "evidence": new_evidence,
                        "observations": new_obs
                    })

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Guardar Todas las Calificaciones y Recalcular IMO", type="primary", use_container_width=True):
        new_metrics = calculate_assessment_metrics(updated_scores)
        save_all_assessment_scores(current_assessment["id"], updated_scores, new_metrics["imo"])
        st.success(f"¡Calificaciones guardadas exitosamente! Nuevo IMO: {new_metrics['imo']:.2f} / 5.0 ({new_metrics['level_label']}).")
        st.rerun()
