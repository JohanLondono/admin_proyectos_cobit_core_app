"""
Motor de Exportación de Reportes Ejecutivos (PDF, Excel y CSV) [COB-ST19, COB-ST20].
Genera documentos descargables profesionales para comités directivos y auditoría.
"""

import io
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

# Importación segura de ReportLab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch

def generate_excel_report(client: Dict[str, Any], assessment: Dict[str, Any], scores: List[Dict[str, Any]], metrics: Dict[str, Any]) -> bytes:
    """
    [COB-ST20] Genera un archivo Excel (.xlsx) con hojas separadas para:
    1. Resumen Ejecutivo y Métricas
    2. Detalle de Procesos y Calificaciones COBIT
    3. Resumen por Dominios
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Hoja 1: Resumen
        resumen_data = {
            "Parámetro": [
                "Cliente", "NIT", "Sector", "Tamaño de Empresa",
                "Código de Evaluación", "Tipo de Evaluación", "Consultor Líder",
                "Índice de Madurez Organizacional (IMO)", "Nivel Verbal",
                "Meta Promedio Deseada", "Brecha Global",
                "Salud de Gobernanza", "Exposición al Riesgo", "Fecha de Generación"
            ],
            "Valor": [
                client.get("name", "N/A"),
                client.get("tax_id", "N/A"),
                client.get("sector", "N/A"),
                client.get("size", "N/A"),
                assessment.get("code", "N/A"),
                assessment.get("assessment_type", "comprehensive").capitalize(),
                assessment.get("lead_consultant", "N/A"),
                f"{metrics.get('imo', 0.0):.2f} / 5.00",
                metrics.get("level_label", "Incompleto"),
                f"{metrics.get('target_imo', 3.0):.2f} / 5.00",
                f"{metrics.get('overall_gap', 0.0):.2f} puntos",
                f"{metrics.get('health_score', 0.0):.1f}%",
                f"{metrics.get('risk_score', 0.0):.1f}%",
                datetime.now().strftime("%d/%m/%Y %H:%M")
            ]
        }
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name="Resumen Ejecutivo", index=False)

        # Hoja 2: Procesos Evaluados
        procesos_data = []
        for s in metrics.get("all_scored_processes", []):
            procesos_data.append({
                "Código": s["process_id"],
                "Dominio": s["domain"],
                "Nombre del Proceso": s["name"],
                "Nivel Actual (0-5)": s["current_score"],
                "Nivel Meta (0-5)": s["target_score"],
                "Brecha (Gap)": s["gap"],
                "Evidencias": s.get("evidence", ""),
                "Observaciones": s.get("observations", "")
            })
        df_proc = pd.DataFrame(procesos_data)
        df_proc.to_excel(writer, sheet_name="Calificaciones COBIT", index=False)

        # Hoja 3: Dominios
        dom_data = []
        for d_code, d_info in metrics.get("domains", {}).items():
            dom_data.append({
                "Dominio": d_code,
                "Descripción": d_info.get("name", ""),
                "Nivel Actual Promedio": d_info.get("current", 0.0),
                "Nivel Meta Promedio": d_info.get("target", 3.0),
                "Brecha": d_info.get("gap", 0.0),
                "Cantidad Procesos": d_info.get("count", 0)
            })
        df_dom = pd.DataFrame(dom_data)
        df_dom.to_excel(writer, sheet_name="Resumen por Dominio", index=False)

    return output.getvalue()

def generate_pdf_report(client: Dict[str, Any], assessment: Dict[str, Any], metrics: Dict[str, Any], roadmap_plan: Dict[str, Any] = None) -> bytes:
    """
    [COB-ST19] Genera un informe PDF ejecutivo formal con ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1, # Center
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=20
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    elements = []

    # Encabezado
    elements.append(Paragraph("SISTEMA DE CONSULTORÍA EN GOBIERNO DE TI", title_style))
    elements.append(Paragraph(f"INFORME EJECUTIVO DE MADUREZ COBIT 2019 — {client.get('name', 'EMPRESA CLIENTE').upper()}", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=15))

    # Ficha Técnica
    ficha_data = [
        [
            Paragraph("<b>Empresa:</b> " + client.get("name", "N/A"), body_style),
            Paragraph("<b>NIT/RUT:</b> " + client.get("tax_id", "N/A"), body_style)
        ],
        [
            Paragraph("<b>Sector:</b> " + client.get("sector", "N/A"), body_style),
            Paragraph("<b>Tamaño:</b> " + client.get("size", "N/A"), body_style)
        ],
        [
            Paragraph("<b>Código Evaluación:</b> " + assessment.get("code", "N/A"), body_style),
            Paragraph("<b>Fecha:</b> " + datetime.now().strftime("%d/%m/%Y"), body_style)
        ],
        [
            Paragraph("<b>Consultor Líder:</b> " + assessment.get("lead_consultant", "Consultor Certificado"), body_style),
            Paragraph(f"<b>IMO Obtenido:</b> <b>{metrics.get('imo', 0.0):.2f} / 5.00</b> ({metrics.get('level_label')})", body_style)
        ]
    ]
    t_ficha = Table(ficha_data, colWidths=[260, 260])
    t_ficha.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_ficha)
    elements.append(Spacer(1, 12))

    # Resumen de Dominios
    elements.append(Paragraph("1. Resultados de Madurez por Dominio COBIT 2019", h2_style))
    dom_headers = ["Dominio", "Nombre", "Nivel Actual", "Meta", "Brecha", "Estado"]
    dom_rows = [[Paragraph(f"<b>{h}</b>", table_header) for h in dom_headers]]

    for d_code, d_info in metrics.get("domains", {}).items():
        curr = d_info.get("current", 0.0)
        gap = d_info.get("gap", 0.0)
        status_txt = "Crítico" if gap > 1.2 else ("Requiere Atención" if gap > 0.6 else "Adecuado")
        dom_rows.append([
            Paragraph(d_code, table_cell),
            Paragraph(d_info.get("name", ""), table_cell),
            Paragraph(f"{curr:.2f}", table_cell),
            Paragraph(f"{d_info.get('target', 3.0):.2f}", table_cell),
            Paragraph(f"{gap:.2f}", table_cell),
            Paragraph(status_txt, table_cell)
        ])

    t_dom = Table(dom_rows, colWidths=[45, 235, 60, 50, 50, 80])
    t_dom.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_dom)
    elements.append(Spacer(1, 12))

    # Top Brechas Críticas
    elements.append(Paragraph("2. Principales Brechas Tecnológicas Detectadas (Top 5)", h2_style))
    gap_headers = ["Proceso", "Nombre", "Actual", "Meta", "Brecha", "Evidencia"]
    gap_rows = [[Paragraph(f"<b>{h}</b>", table_header) for h in gap_headers]]

    for g in metrics.get("top_gaps", []):
        gap_rows.append([
            Paragraph(g["process_id"], table_cell),
            Paragraph(g["name"][:35], table_cell),
            Paragraph(f"{g['current_score']:.1f}", table_cell),
            Paragraph(f"{g['target_score']:.1f}", table_cell),
            Paragraph(f"{g['gap']:.1f}", table_cell),
            Paragraph(g.get("evidence", "Pendiente")[:40] or "Sin evidencia", table_cell)
        ])

    t_gaps = Table(gap_rows, colWidths=[45, 160, 45, 45, 45, 180])
    t_gaps.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284C7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_gaps)
    elements.append(Spacer(1, 12))

    # Resumen de Hoja de Ruta
    if roadmap_plan and roadmap_plan.get("initiatives"):
        elements.append(Paragraph("3. Resumen de la Hoja de Ruta de Transformación (Roadmap)", h2_style))
        r_headers = ["Fase", "Iniciativa", "Proceso", "Meses", "Costo Aprox. (COP)", "Tipo"]
        r_rows = [[Paragraph(f"<b>{h}</b>", table_header) for h in r_headers]]

        for init in roadmap_plan["initiatives"][:6]:
            tipo = "Quick Win" if init.get("is_quick_win") else "Estratégica"
            costo_fmt = f"${init.get('estimated_cost', 0):,.0f}"
            r_rows.append([
                Paragraph(f"Fase {init.get('phase', 1)}", table_cell),
                Paragraph(init.get("title", "")[:45], table_cell),
                Paragraph(init.get("process_id", "-"), table_cell),
                Paragraph(f"{init.get('estimated_months', 3)} m", table_cell),
                Paragraph(costo_fmt, table_cell),
                Paragraph(tipo, table_cell)
            ])

        t_road = Table(r_rows, colWidths=[45, 215, 50, 45, 95, 70])
        t_road.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(t_road)

    doc.build(elements)
    return buffer.getvalue()
