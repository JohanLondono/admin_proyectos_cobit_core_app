"""
Vista del Dashboard Ejecutivo COBIT 2019 [COB-ST16, COB-ST17].
Presenta gráficos radar Plotly comparativos, KPIs de madurez, desglose por dominios y alertas.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from database.db_manager import (
    get_all_clients, get_client_by_id, get_assessments_by_client,
    get_assessment_scores
)
from engine.maturity_engine import calculate_assessment_metrics
from engine.cobit_data import DOMAINS

def render_radar_chart(domains_data: dict) -> go.Figure:
    """Genera un gráfico Radar interactivo con Plotly comparando Actual vs Meta."""
    categories = list(DOMAINS.keys())
    cat_names = [f"{d} - {DOMAINS[d]['name'][:15]}" for d in categories]

    current_vals = [domains_data.get(d, {}).get("current", 0.0) for d in categories]
    target_vals = [domains_data.get(d, {}).get("target", 3.0) for d in categories]

    # Cerrar el polígono
    cat_names_closed = cat_names + [cat_names[0]]
    current_closed = current_vals + [current_vals[0]]
    target_closed = target_vals + [target_vals[0]]

    fig = go.Figure()

    # Capa 1: Nivel Actual
    fig.add_trace(go.Scatterpolar(
        r=current_closed,
        theta=cat_names_closed,
        fill='toself',
        fillcolor='rgba(2, 132, 199, 0.25)',
        line=dict(color='#0284C7', width=3),
        name='Nivel Actual (Evaluado)'
    ))

    # Capa 2: Meta Deseada
    fig.add_trace(go.Scatterpolar(
        r=target_closed,
        theta=cat_names_closed,
        fill='toself',
        fillcolor='rgba(5, 150, 105, 0.15)',
        line=dict(color='#059669', width=2.5, dash='dash'),
        name='Nivel Objetivo (Meta)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[0, 1, 2, 3, 4, 5],
                ticktext=["0 - Incompleto", "1 - Inicial", "2 - Gestionado", "3 - Establecido", "4 - Predecible", "5 - Optimizado"],
                tickfont=dict(size=9, color="#475569")
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#0F172A", family="Outfit")
            )
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=30, b=50),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def show_dashboard():
    st.title("📊 Dashboard Ejecutivo de Gobernanza TI")
    st.markdown("Visualización integral de madurez COBIT 2019, radar de dominios y brechas clave.")

    # Selección de Cliente
    clients = get_all_clients()
    if not clients:
        st.warning("⚠️ No hay empresas clientes registradas aún. Dirígete a 'Gestión de Clientes' para crear una.")
        return

    # Buscar cliente activo en sesión
    client_ids = [c["id"] for c in clients]
    client_names = [f"{c['name']} ({c['sector']})" for c in clients]

    current_idx = 0
    if st.session_state.get("active_client_id") in client_ids:
        current_idx = client_ids.index(st.session_state["active_client_id"])

    col_sel1, col_sel2 = st.columns([2, 2])
    with col_sel1:
        selected_client_idx = st.selectbox(
            "🏢 Selecciona la Empresa Cliente:",
            range(len(clients)),
            format_func=lambda i: client_names[i],
            index=current_idx,
            key="dash_client_select"
        )
        active_client = clients[selected_client_idx]
        st.session_state["active_client_id"] = active_client["id"]

    # Evaluaciones del cliente
    assessments = get_assessments_by_client(active_client["id"])
    if not assessments:
        st.info(f"ℹ️ El cliente '{active_client['name']}' no tiene evaluaciones registradas. Crea una en la sección 'Evaluación COBIT'.")
        return

    eval_titles = [f"{a['title']} [{a['code']}]" for a in assessments]
    with col_sel2:
        selected_eval_idx = st.selectbox(
            "📋 Selecciona la Evaluación:",
            range(len(assessments)),
            format_func=lambda i: eval_titles[i],
            key="dash_eval_select"
        )
        active_eval = assessments[selected_eval_idx]
        st.session_state["active_assessment_id"] = active_eval["id"]

    # Cargar puntajes y calcular métricas
    scores = get_assessment_scores(active_eval["id"])
    metrics = calculate_assessment_metrics(scores)

    st.markdown("---")

    # 4 KPI Cards Principales
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Índice Madurez (IMO)</div>
            <div class="metric-value">{metrics['imo']:.2f} <span style="font-size:1.1rem; color:#64748B;">/ 5.0</span></div>
            <div class="metric-sub">Nivel: <b>{metrics['level_label']}</b></div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Meta Propuesta</div>
            <div class="metric-value">{metrics['target_imo']:.2f} <span style="font-size:1.1rem; color:#64748B;">/ 5.0</span></div>
            <div class="metric-sub">Brecha: <b>{metrics['overall_gap']:.2f} pts</b></div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Salud de Gobernanza</div>
            <div class="metric-value" style="color:#059669;">{metrics['health_score']:.1f}%</div>
            <div class="metric-sub">Efectividad del Marco TI</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        risk_color = "#DC2626" if metrics['risk_score'] > 50 else "#D97706"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Exposición al Riesgo</div>
            <div class="metric-value" style="color:{risk_color};">{metrics['risk_score']:.1f}%</div>
            <div class="metric-sub">Brecha no mitigada</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico Radar y Detalle por Dominio
    col_chart, col_doms = st.columns([3, 2])

    with col_chart:
        st.subheader("🕸️ Gráfico Radar de Madurez por Dominio")
        st.caption("Comparación visual de los 5 dominios COBIT: Estado Actual vs Meta")
        radar_fig = render_radar_chart(metrics["domains"])
        st.plotly_chart(radar_fig, use_container_width=True)

    with col_doms:
        st.subheader("📑 Desempeño por Dominio")
        st.caption("Puntaje promedio obtenido en cada área del marco")
        for dom_code, dom_info in metrics["domains"].items():
            curr = dom_info["current"]
            targ = dom_info["target"]
            pct = min(1.0, max(0.0, curr / 5.0))
            st.markdown(f"**{dom_code}** - {DOMAINS[dom_code]['name'][:30]}...")
            st.progress(pct, text=f"Actual: {curr:.2f} | Meta: {targ:.2f} (Brecha: {dom_info['gap']:.2f})")

    st.markdown("---")

    # Top 5 Brechas Críticas
    st.subheader("⚠️ Top 5 Procesos con Mayor Brecha de Madurez")
    st.caption("Procesos prioritarios que requieren atención inmediata en la hoja de ruta")

    if metrics["top_gaps"]:
        gap_records = []
        for g in metrics["top_gaps"]:
            gap_records.append({
                "Proceso": g["process_id"],
                "Dominio": g["domain"],
                "Nombre": g["name"],
                "Nivel Actual": f"{g['current_score']:.1f} / 5.0",
                "Nivel Meta": f"{g['target_score']:.1f} / 5.0",
                "Brecha (Gap)": f"+{g['gap']:.1f} pts",
                "Evidencias Registradas": g.get("evidence", "Sin evidencia") or "Pendiente de justificación"
            })
        st.dataframe(pd.DataFrame(gap_records), use_container_width=True, hide_index=True)
    else:
        st.success("🎉 Todos los procesos evaluados alcanzan el nivel objetivo.")

    # Accesos rápidos
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚀 Acciones Rápidas")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        if st.button("📝 Continuar Evaluación", use_container_width=True):
            st.session_state["current_view"] = "assessment"
            st.rerun()
    with r2:
        if st.button("🔍 Ver Diagnóstico e IA", use_container_width=True):
            st.session_state["current_view"] = "diagnosis"
            st.rerun()
    with r3:
        if st.button("🗺️ Consultar Hoja de Ruta", use_container_width=True):
            st.session_state["current_view"] = "roadmap"
            st.rerun()
    with r4:
        if st.button("📥 Descargar Reportes", use_container_width=True):
            st.session_state["current_view"] = "reports"
            st.rerun()
