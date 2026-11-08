"""
Generador y Visualizador de Hojas de Ruta (Roadmaps) COBIT 2019 [COB-TK10, COB-ST14, COB-ST15].
Organiza iniciativas por fases cronológicas, calcula matemáticamente Quick Wins mediante
análisis multi-criterio (MCDA / WSJF), programa dependencias bloqueantes, hitos (milestones)
y genera un Diagrama de Gantt interactivo con Plotly.
"""

import streamlit as st
import pandas as pd
from database.db_manager import (
    get_all_clients, get_assessments_by_client, get_assessment_scores,
    get_roadmap_by_assessment, get_roadmap_initiatives, save_roadmap,
    get_documents_by_client
)
from engine.roadmap_engine import (
    generate_roadmap_plan, create_interactive_gantt_chart,
    validate_roadmap_dependencies, generate_roadmap_milestones
)

def show_roadmap():
    st.title("🗺️ Hoja de Ruta de Transformación (Roadmap)")
    st.markdown("Plan estratégico secuenciado por fases, dependencias bloqueantes e hitos para elevar la madurez institucional.")

    clients = get_all_clients()
    if not clients:
        st.warning("No hay clientes registrados.")
        return

    client_ids = [c["id"] for c in clients]
    client_names = [f"{c['name']} ({c['sector']})" for c in clients]
    curr_c_idx = 0
    if st.session_state.get("active_client_id") in client_ids:
        curr_c_idx = client_ids.index(st.session_state["active_client_id"])

    # Validar rol de usuario para restringir cambio de empresa y regeneración en clientes corporativos
    user = st.session_state.get("user") or {}
    user_role = user.get("role", "consultant")

    if user_role == "client":
        active_client = clients[curr_c_idx]
        st.session_state["active_client_id"] = active_client["id"]
        st.markdown(f"""
        <div class="client-banner" style="margin: 8px 0 16px 0;">
            🏢 Empresa Cliente: {active_client['name']} 
            <span class="client-banner-tag">(Visualización de Plan Estratégico Aprobado)</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        selected_c_idx = st.selectbox("Empresa Cliente:", range(len(clients)), format_func=lambda i: client_names[i], index=curr_c_idx, key="road_client_picker")
        active_client = clients[selected_c_idx]
        st.session_state["active_client_id"] = active_client["id"]

    assessments = get_assessments_by_client(active_client["id"])
    if not assessments:
        st.info("No hay evaluaciones registradas para este cliente.")
        return

    active_eval = assessments[0]
    scores = get_assessment_scores(active_eval["id"])
    client_docs = get_documents_by_client(active_client["id"])

    # Consultar si ya existe un roadmap guardado
    existing_roadmap = get_roadmap_by_assessment(active_eval["id"])

    # Panel de Configuración y Regeneración Algorítmica (Administrador y Consultor Líder)
    if user_role in ["admin", "consultant"]:
        with st.expander("⚙️ Motor Algorítmico Multi-Criterio (Roadmap Engine)", expanded=not existing_roadmap):
            st.caption("Ajusta los parámetros de optimización multi-criterio (MCDA / WSJF) y estimación paramétrica:")
            col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
            with col_cfg1:
                strategy_choice = st.selectbox(
                    "Estrategia de Optimización:",
                    [
                        ("balanced", "Equilibrado (Holístico COBIT)"),
                        ("quick_wins", "Priorizar Quick Wins (< 90 Días)"),
                        ("security_risk", "Enfocado en Ciberseguridad y Continuidad"),
                        ("governance", "Enfocado en Gobierno Directivo (EDM/MEA)")
                    ],
                    format_func=lambda x: x[1],
                    key="road_strat"
                )
            with col_cfg2:
                horizon_choice = st.selectbox(
                    "Horizonte Temporal:",
                    [12, 18, 24],
                    index=1,
                    format_func=lambda m: f"{m} Meses de Ejecución",
                    key="road_horiz"
                )
            with col_cfg3:
                budget_tol = st.slider(
                    "Tolerancia de Inversión:",
                    min_value=0.7,
                    max_value=1.4,
                    value=1.0,
                    step=0.05,
                    format="%.2fx",
                    help="Multiplicador paramétrico de presupuesto según holgura financiera",
                    key="road_budg_tol"
                )

            btn_label = "⚡ Calcular y Guardar Hoja de Ruta" if not existing_roadmap else "🔄 Recalcular y Actualizar Hoja de Ruta"
            if st.button(btn_label, type="primary", use_container_width=True):
                new_plan = generate_roadmap_plan(
                    scores=scores,
                    client=active_client,
                    documents=client_docs,
                    horizon_months=horizon_choice,
                    focus_strategy=strategy_choice[0],
                    budget_tolerance=budget_tol
                )
                save_roadmap(
                    assessment_id=active_eval["id"],
                    client_id=active_client["id"],
                    title=new_plan["title"],
                    total_budget=new_plan["total_budget"],
                    horizon_months=new_plan["horizon_months"],
                    summary=new_plan["summary"],
                    initiatives=new_plan["initiatives"],
                    milestones=new_plan.get("milestones", [])
                )
                st.success("¡Hoja de ruta calculada, dependencias programadas y guardadas exitosamente!")
                st.rerun()

    if not existing_roadmap:
        st.info("ℹ️ Aún no se ha generado una hoja de ruta para esta evaluación. Utiliza el panel superior para calcularla.")
        return

    initiatives = get_roadmap_initiatives(existing_roadmap["id"])
    milestones = existing_roadmap.get("milestones") or generate_roadmap_milestones(existing_roadmap.get("horizon_months", 18))

    # Asegurar que las iniciativas tengan fechas y dependencias calculadas si provienen de versiones anteriores
    if initiatives and not initiatives[0].get("start_date"):
        temp_plan = generate_roadmap_plan(
            scores=scores,
            client=active_client,
            documents=client_docs,
            horizon_months=existing_roadmap.get("horizon_months", 18)
        )
        initiatives = temp_plan["initiatives"]
        milestones = temp_plan["milestones"]

    validation = validate_roadmap_dependencies(initiatives)

    # Tarjetas de Presupuesto y Plazos
    st.markdown("---")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Presupuesto Estimado", f"${existing_roadmap['total_budget']:,.0f} COP")
    with r2:
        st.metric("Horizonte de Ejecución", f"{existing_roadmap['horizon_months']} Meses")
    with r3:
        qw_count = len([i for i in initiatives if i.get("is_quick_win")])
        st.metric("Iniciativas Rápidas (Quick Wins)", f"{qw_count} proyectos")
    with r4:
        st.metric("Total de Iniciativas", f"{len(initiatives)} acciones")

    st.info(f"📌 **Resumen Estratégico:** {existing_roadmap['summary']}")

    # SECCIÓN DESTACADA: QUICK WINS CALCULADOS
    quick_wins = [i for i in initiatives if i.get("is_quick_win")]
    if quick_wins:
        st.markdown("### ⚡ Quick Wins Prioritarios (< 90 Días)")
        st.caption("Iniciativas identificadas por el algoritmo con alto impacto estratégico y rápida adopción operativa:")
        qw_cols = st.columns(min(3, len(quick_wins)))
        for idx, qw in enumerate(quick_wins[:3]):
            with qw_cols[idx]:
                st.markdown(f"""
                <div class="qw-card">
                    <span class="badge-qw">⚡ QUICK WIN</span>
                    <div class="qw-title">{qw['title']}</div>
                    <div class="qw-desc">{qw['description']}</div>
                    <div class="qw-role"><b>Responsable:</b> {qw['responsible_role']}</div>
                    <div class="qw-meta"><b>Inversión Estimada:</b> ${qw['estimated_cost']:,.0f} COP | <b>Plazo:</b> {qw['estimated_months']} meses</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # =====================================================================
    # SECCIÓN: DIAGRAMA DE GANTT INTERACTIVO (PLOTLY)
    # =====================================================================
    st.subheader("📊 Diagrama de Gantt Interactivo y Cronograma")
    st.caption("Visualización temporal con barras de duración, dependencias bloqueantes y líneas de hitos (milestones):")

    gantt_col1, gantt_col2 = st.columns([3, 1])
    with gantt_col2:
        color_mode = st.radio(
            "Colorear cronograma por:",
            options=["phase", "quick_win"],
            format_func=lambda x: "Fases Temporales" if x == "phase" else "Quick Wins vs Estándar",
            horizontal=True,
            key="gantt_color_picker"
        )

    gantt_fig = create_interactive_gantt_chart(
        initiatives=initiatives,
        milestones=milestones,
        color_by=color_mode
    )
    st.plotly_chart(gantt_fig, use_container_width=True)

    # =====================================================================
    # SECCIÓN: HITOS ESTRATÉGICOS (MILESTONES)
    # =====================================================================
    st.markdown("### 🚩 Hitos Estratégicos de Control (Milestones)")
    st.caption("Puntos de control formales y entregables de madurez COBIT a lo largo del horizonte:")
    m_cols = st.columns(len(milestones))
    for idx, m in enumerate(milestones):
        with m_cols[idx]:
            st.markdown(f"""
            <div class="report-card">
                <div style="font-size: 1.1rem; font-weight: 700; color: #0284C7;">🚩 {m['name']}</div>
                <div style="font-size: 0.85rem; color: #64748B; margin: 4px 0;"><b>Plazo:</b> Mes {m['target_month']} ({m['target_date']})</div>
                <div style="font-size: 0.88rem; margin-top: 6px;"><b>Entregables de Control:</b> {m['deliverables']}</div>
                <div style="margin-top: 8px;"><span class="badge-tag">FASE {m['phase']}</span> <span style="background: rgba(16, 185, 129, 0.15); color: #10B981; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">Programado</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # =====================================================================
    # SECCIÓN: AUDITORÍA DE DEPENDENCIAS Y RUTA CRÍTICA
    # =====================================================================
    with st.expander("🔗 Auditoría de Grafo de Dependencias Bloqueantes y Ruta Crítica", expanded=True):
        if validation["is_valid"]:
            st.success(f"✅ **Grafo de Precedencias COBIT Consistente:** {validation['total_dependencies']} dependencias activas evaluadas. No se detectaron dependencias circulares ni inversiones temporales.")
        else:
            st.warning("⚠️ Se detectaron inconsistencias en el cronograma:")
            for conf in validation["conflicts"]:
                st.write(f"- {conf}")

        aud1, aud2 = st.columns(2)
        with aud1:
            st.markdown("##### 🧱 Procesos Cuello de Botella (Mayor Bloqueo)")
            st.caption("Procesos que deben ejecutarse a tiempo porque desbloquean proyectos posteriores:")
            if validation["bottlenecks"]:
                for b in validation["bottlenecks"]:
                    st.markdown(f"- **`{b['process_id']}`**: Desbloquea **{b['blocked_tasks_count']}** proyectos ({b['title'][:35]}...)")
            else:
                st.info("No se identificaron cuellos de botella significativos.")

        with aud2:
            st.markdown("##### 🔥 Tareas en Ruta Crítica (Critical Path)")
            st.caption("Cadena de proyectos de mayor duración acumulada sin holgura:")
            crit_tasks = validation.get("critical_path_tasks", [])
            if crit_tasks:
                st.write("Procesos en ruta crítica: " + " ".join([f"`{t}`" for t in crit_tasks]))
            else:
                st.info("Distribución uniforme de holgura temporal.")

    st.markdown("---")

    # =====================================================================
    # SECCIÓN: FASES TEMPORALES DE LA HOJA DE RUTA
    # =====================================================================
    st.subheader("📅 Desglose Detallado por Fases de Madurez")
    f_tab1, f_tab2, f_tab3 = st.tabs([
        f"Fase 1: Cimientos y Quick Wins ({len([i for i in initiatives if i['phase'] == 1])} proyectos)",
        f"Fase 2: Consolidación y Procesos Core ({len([i for i in initiatives if i['phase'] == 2])} proyectos)",
        f"Fase 3: Optimización y Monitoreo ({len([i for i in initiatives if i['phase'] == 3])} proyectos)"
    ])

    for phase_num, f_tab in [(1, f_tab1), (2, f_tab2), (3, f_tab3)]:
        with f_tab:
            p_inits = [i for i in initiatives if i["phase"] == phase_num]
            if not p_inits:
                st.info(f"No hay iniciativas programadas para la Fase {phase_num}.")
                continue

            for init in p_inits:
                badge = "⚡ QUICK WIN" if init.get("is_quick_win") else f"Prioridad {init.get('priority', 'Media')}"
                crit_tag = " | 🔥 Ruta Crítica" if init.get("is_critical_path") else ""
                with st.expander(f"🔹 [{init.get('process_id') or 'TI'}] {init['title']} — {badge}{crit_tag}"):
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.markdown(f"**Alcance Técnico:** {init['description']}")
                        st.markdown(f"**Rol Institucional Responsable:** `{init['responsible_role']}`")
                        deps_arr = init.get("dependencies", [])
                        if deps_arr:
                            st.markdown(f"**Dependencias Bloqueantes:** " + " ".join([f"`{d}`" for d in deps_arr]))
                        else:
                            st.markdown("**Dependencias Bloqueantes:** *Ninguna (Iniciable de inmediato)*")
                        st.markdown(f"**Estado del Proyecto:** `{init.get('status', 'pending')}`")
                    with c2:
                        st.markdown(f"**Ventana Temporal:** Mes {init.get('start_month', 1)} → Mes {init.get('end_month', 3)} (`{init.get('start_date', '')}` a `{init.get('end_date', '')}`)")
                        st.markdown(f"**Duración Estimada:** `{init['estimated_months']} meses`")
                        st.markdown(f"**Inversión Presupuestal:** `${init['estimated_cost']:,.0f} COP`")
                        st.markdown(f"**Prioridad:** `{init.get('priority', 'Media')}`")
