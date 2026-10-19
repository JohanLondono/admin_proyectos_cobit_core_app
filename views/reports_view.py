"""
Generación y Exportación de Reportes Ejecutivos (PDF y Excel) [COB-ST19, COB-ST20].
Proporciona descargas instantáneas para entrega a juntas directivas y auditores.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database.db_manager import (
    get_all_clients, get_assessments_by_client, get_assessment_scores,
    get_roadmap_by_assessment, get_roadmap_initiatives
)
from engine.maturity_engine import calculate_assessment_metrics
from engine.export_engine import generate_pdf_report, generate_excel_report

def show_reports():
    st.title("📥 Reportes Ejecutivos y Exportación")
    st.markdown("Genera informes ejecutivos en formato PDF profesional y exporta matrices completas a Excel.")

    clients = get_all_clients()
    if not clients:
        st.warning("No hay clientes registrados.")
        return

    client_ids = [c["id"] for c in clients]
    client_names = [f"{c['name']} ({c['sector']})" for c in clients]
    curr_c_idx = 0
    if st.session_state.get("active_client_id") in client_ids:
        curr_c_idx = client_ids.index(st.session_state["active_client_id"])

    col1, col2 = st.columns(2)
    with col1:
        selected_c_idx = st.selectbox("Empresa Cliente:", range(len(clients)), format_func=lambda i: client_names[i], index=curr_c_idx, key="rep_client_picker")
        active_client = clients[selected_c_idx]
        st.session_state["active_client_id"] = active_client["id"]

    assessments = get_assessments_by_client(active_client["id"])
    if not assessments:
        st.info("No hay evaluaciones disponibles para exportar.")
        return

    eval_titles = [f"{a['title']} [{a['code']}]" for a in assessments]
    with col2:
        selected_eval_idx = st.selectbox("Evaluación a Exportar:", range(len(assessments)), format_func=lambda i: eval_titles[i], key="rep_eval_picker")
        active_eval = assessments[selected_eval_idx]

    scores = get_assessment_scores(active_eval["id"])
    metrics = calculate_assessment_metrics(scores)

    # Cargar hoja de ruta si existe
    roadmap_plan = None
    existing_roadmap = get_roadmap_by_assessment(active_eval["id"])
    if existing_roadmap:
        inits = get_roadmap_initiatives(existing_roadmap["id"])
        roadmap_plan = {
            "title": existing_roadmap["title"],
            "total_budget": existing_roadmap["total_budget"],
            "horizon_months": existing_roadmap["horizon_months"],
            "initiatives": inits
        }

    st.markdown("---")

    # Botones de Descarga en 2 columnas destacadas
    c_pdf, c_xlsx = st.columns(2)

    with c_pdf:
        st.markdown("""
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:20px; text-align:center;">
            <div style="font-size:2.5rem;">📄</div>
            <div style="font-weight:700; font-size:1.15rem; color:#1E3A8A; margin-top:8px;">Informe Ejecutivo en PDF</div>
            <div style="font-size:0.85rem; color:#64748B; margin:8px 0 16px 0;">
                Documento formal con portada, ficha técnica, resumen de madurez, desglose por dominios, brechas críticas y cronograma.
            </div>
        </div>
        """, unsafe_allow_html=True)

        pdf_bytes = generate_pdf_report(active_client, active_eval, metrics, roadmap_plan)
        filename_pdf = f"Informe_COBIT_{active_client['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

        st.download_button(
            label="⬇️ Descargar Informe PDF",
            data=pdf_bytes,
            file_name=filename_pdf,
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )

    with c_xlsx:
        st.markdown("""
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:20px; text-align:center;">
            <div style="font-size:2.5rem;">📊</div>
            <div style="font-weight:700; font-size:1.15rem; color:#059669; margin-top:8px;">Matriz Completa en Excel (.xlsx)</div>
            <div style="font-size:0.85rem; color:#64748B; margin:8px 0 16px 0;">
                Libro de cálculo con 3 pestañas: Resumen Ejecutivo, Calificaciones individuales de los procesos y Métricas por dominio.
            </div>
        </div>
        """, unsafe_allow_html=True)

        excel_bytes = generate_excel_report(active_client, active_eval, scores, metrics)
        filename_xlsx = f"Matriz_COBIT_{active_client['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx"

        st.download_button(
            label="⬇️ Descargar Libro Excel (.xlsx)",
            data=excel_bytes,
            file_name=filename_xlsx,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="secondary",
            use_container_width=True
        )

    # Vista previa de datos
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("👁️ Vista Previa del Resumen a Exportar")
    st.markdown(f"**Cliente:** {active_client['name']} | **NIT:** {active_client.get('tax_id')} | **Sector:** {active_client['sector']}")
    st.markdown(f"**IMO Calculado:** `{metrics['imo']:.2f} / 5.00` | **Nivel:** `{metrics['level_label']}` | **Salud:** `{metrics['health_score']:.1f}%`")

    st.markdown("#### Desglose de Dominios:")
    dom_preview = []
    for d_code, d_info in metrics.get("domains", {}).items():
        dom_preview.append({
            "Dominio": d_code,
            "Nombre": d_info.get("name", ""),
            "Nivel Actual": d_info.get("current", 0.0),
            "Nivel Meta": d_info.get("target", 3.0),
            "Brecha": d_info.get("gap", 0.0),
            "Procesos": d_info.get("count", 0)
        })
    st.dataframe(pd.DataFrame(dom_preview), use_container_width=True, hide_index=True)
