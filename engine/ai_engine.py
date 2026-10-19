"""
Motor de Inteligencia Artificial y Diagnóstico Heurístico COBIT 2019 [COB-ST09, COB-ST12, COB-ST13].
Proporciona análisis NPO de documentos, alineación estratégica de negocio,
análisis cualitativo de riesgos y recomendaciones con fallback 100% offline.
"""

import re
from typing import Dict, List, Any
from datetime import datetime
from engine.cobit_data import COBIT_PROCESSES, DOMAINS

# Diccionario de palabras clave para análisis NPO
KEYWORD_MAPPINGS = {
    "ciberseguridad": ["APO12", "APO13", "DSS05"],
    "seguridad": ["APO13", "DSS05"],
    "riesgo": ["EDM03", "APO12"],
    "amenaza": ["APO12", "APO13"],
    "vulnerabilidad": ["APO13", "DSS05"],
    "continuidad": ["DSS04", "BAI04"],
    "desastre": ["DSS04"],
    "backup": ["DSS01", "DSS04"],
    "respaldo": ["DSS01", "DSS04"],
    "incidente": ["DSS02"],
    "falla": ["DSS02", "DSS03"],
    "mesa de ayuda": ["DSS02", "APO09"],
    "soporte": ["DSS02", "APO09"],
    "sla": ["APO09"],
    "proveedor": ["APO10"],
    "tercero": ["APO10"],
    "contrato": ["APO10", "APO09"],
    "auditoria": ["MEA02", "MEA04", "EDM01"],
    "cumplimiento": ["MEA03", "EDM03"],
    "regulacion": ["MEA03"],
    "estrategia": ["EDM01", "APO02"],
    "gobernanza": ["EDM01", "EDM02"],
    "proyecto": ["BAI11", "APO05"],
    "cambio": ["BAI06", "BAI05"],
    "datos": ["APO14"],
    "calidad": ["APO11"],
    "costo": ["APO06", "EDM04"],
    "presupuesto": ["APO06", "EDM04"],
    "personal": ["APO07", "BAI05"],
    "capacitacion": ["APO07", "BAI05"]
}

def analyze_npo_text(text: str) -> Dict[str, Any]:
    """
    Analiza un texto documental para extraer Necesidades, Problemas y Oportunidades (NPO),
    y mapea los términos a procesos COBIT 2019 relacionados.
    """
    if not text or len(text.strip()) < 10:
        return {
            "needs": ["Definir formalmente el marco de gobernanza y políticas de TI."],
            "problems": ["Carencia de documentación técnica consolidada."],
            "opportunities": ["Alinear los proyectos de TI al crecimiento comercial de la empresa."],
            "detected_keywords": [],
            "suggested_processes": ["EDM01", "APO02", "DSS05"]
        }

    text_lower = text.lower()

    # Detección de palabras clave
    detected_keywords = []
    associated_processes = set()

    for kw, procs in KEYWORD_MAPPINGS.items():
        if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
            detected_keywords.append(kw)
            for p in procs:
                associated_processes.add(p)

    # Identificación heurística de Necesidades, Problemas y Oportunidades
    needs = []
    problems = []
    opportunities = []

    # Búsqueda de patrones en oraciones
    sentences = [s.strip() for s in re.split(r'[.\n;]+', text) if len(s.strip()) > 15]

    for s in sentences:
        s_low = s.lower()
        if any(w in s_low for w in ["requiere", "necesita", "debe", "es necesario", "fundamental", "prioridad"]):
            if len(needs) < 4:
                needs.append(s[:180] + ("..." if len(s) > 180 else ""))
        elif any(w in s_low for w in ["problema", "falla", "error", "retraso", "vulnerabilidad", "carece", "falta", "inadecuado", "riesgo"]):
            if len(problems) < 4:
                problems.append(s[:180] + ("..." if len(s) > 180 else ""))
        elif any(w in s_low for w in ["oportunidad", "mejora", "optimizar", "automatizar", "innovar", "potencial", "beneficio"]):
            if len(opportunities) < 4:
                opportunities.append(s[:180] + ("..." if len(s) > 180 else ""))

    # Fallbacks inteligentes si el texto no contiene oraciones explícitas
    if not needs:
        needs = [
            "Formalizar políticas de seguridad y gestión de accesos.",
            "Establecer métricas cuantitativas para el seguimiento de proyectos de TI.",
            "Definir acuerdos de nivel de servicio (SLA) con clientes internos."
        ]
    if not problems:
        problems = [
            "Gestión reactiva de incidentes con impacto en la disponibilidad operativa.",
            "Desalineación parcial entre prioridades presupuestales y metas estratégicas.",
            "Procesos dependientes del conocimiento de personas clave sin estandarización."
        ]
    if not opportunities:
        opportunities = [
            "Adoptar herramientas de automatización para reducir tiempos de atención.",
            "Implementar un tablero ejecutivo de control y monitoreo en tiempo real.",
            "Fortalecer la cultura de ciberseguridad y prevención en todos los niveles."
        ]

    suggested_list = list(associated_processes)[:8] if associated_processes else ["EDM01", "APO02", "APO12", "DSS05", "MEA01"]

    return {
        "needs": needs,
        "problems": problems,
        "opportunities": opportunities,
        "detected_keywords": detected_keywords[:12],
        "suggested_processes": suggested_list
    }

def align_business_goals(strategic_goal: str, client_sector: str) -> List[Dict[str, Any]]:
    """
    [COB-ST12] Alinea una meta u objetivo estratégico del negocio con procesos COBIT clave.
    """
    goal_lower = strategic_goal.lower()
    recommendations = []

    if any(k in goal_lower for k in ["crecer", "expansion", "ventas", "mercado", "clientes", "comercial"]):
        recommendations.extend([
            {"process_id": "APO02", "reason": "La gestión estratégica asegura que TI escale según la expansión del negocio.", "criticality": "Alta"},
            {"process_id": "BAI02", "reason": "Permite definir con precisión nuevos requerimientos para canales comerciales.", "criticality": "Alta"},
            {"process_id": "EDM02", "reason": "Asegura que las inversiones comerciales generen el valor y ROI proyectado.", "criticality": "Media"}
        ])

    if any(k in goal_lower for k in ["seguridad", "ciber", "fraude", "confianza", "datos", "privacidad", "hack"]):
        recommendations.extend([
            {"process_id": "APO13", "reason": "Define el marco y sistema de gestión de seguridad de la información (SGSI).", "criticality": "Alta"},
            {"process_id": "DSS05", "reason": "Implementa controles de seguridad operativa, autenticación y monitoreo.", "criticality": "Alta"},
            {"process_id": "APO14", "reason": "Protege la privacidad, ciclo de vida y confidencialidad de datos corporativos.", "criticality": "Alta"}
        ])

    if any(k in goal_lower for k in ["costos", "eficiencia", "optimizacion", "ahorro", "presupuesto"]):
        recommendations.extend([
            {"process_id": "EDM04", "reason": "Dirige la optimización de recursos tecnológicos y humanos.", "criticality": "Alta"},
            {"process_id": "APO06", "reason": "Controla presupuestos, asignación de costos y elimina gastos redundantes.", "criticality": "Alta"},
            {"process_id": "APO10", "reason": "Renegocia contratos con proveedores de tecnología buscando mayor eficiencia.", "criticality": "Media"}
        ])

    if any(k in goal_lower for k in ["continuidad", "operacion", "disponibilidad", "caidas", "estable"]):
        recommendations.extend([
            {"process_id": "DSS04", "reason": "Establece planes de contingencia (BCP/DRP) ante fallos críticos.", "criticality": "Alta"},
            {"process_id": "DSS01", "reason": "Estandariza procedimientos operativos diarios y monitoreo preventivo.", "criticality": "Alta"},
            {"process_id": "BAI06", "reason": "Controla los cambios a producción para prevenir indisponibilidad no programada.", "criticality": "Media"}
        ])

    # Si no hubo coincidencia temática específica, proveer procesos de gobernanza base
    if not recommendations:
        recommendations = [
            {"process_id": "EDM01", "reason": "Marco fundamental para dirigir las iniciativas institucionales.", "criticality": "Alta"},
            {"process_id": "APO01", "reason": "Estructura organizativa clara para liderar el cambio.", "criticality": "Media"},
            {"process_id": "BAI11", "reason": "Asegura la entrega exitosa de proyectos a tiempo y presupuesto.", "criticality": "Alta"}
        ]

    # Enriquecer con nombres de procesos
    for r in recommendations:
        pid = r["process_id"]
        pinfo = COBIT_PROCESSES.get(pid, {})
        r["name"] = pinfo.get("name", pid)
        r["domain"] = pinfo.get("domain", "")

    return recommendations

def generate_heuristic_diagnosis(client: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    [COB-ST13] Genera un diagnóstico completo ejecutivo combinando:
    - Resumen ejecutivo
    - Análisis cualitativo de riesgos
    - Hallazgos principales
    - Recomendaciones prioritarias de acción inmediata
    """
    client_name = client.get("name", "Organización")
    sector = client.get("sector", "Sector Empresarial")
    imo = metrics.get("imo", 0.0)
    level_label = metrics.get("level_label", "Incompleto")
    top_gaps = metrics.get("top_gaps", [])

    # Resumen Ejecutivo
    summary = f"""### Diagnóstico Estratégico de Gobernanza y Gestión de TI (COBIT 2019)
**Organización Evaluada:** {client_name}  
**Sector Económico:** {sector}  
**Índice de Madurez Organizacional (IMO):** **{imo:.2f} / 5.00** ({level_label})  
**Nivel de Salud de Gobernanza:** **{metrics.get('health_score', 0):.1f}%** | **Exposición al Riesgo de TI:** **{metrics.get('risk_score', 0):.1f}%**

#### Conclusión del Diagnóstico:
La evaluación bajo el estándar COBIT 2019 indica que {client_name} presenta un nivel de madurez clasificado como **{level_label}**. La organización posee controles en operación, pero se identifican áreas de oportunidad críticas en la formalización de políticas institucionales, la gestión cuantitativa del desempeño tecnológico y el fortalecimiento de la ciberseguridad.

Para alcanzar el nivel objetivo de madurez de **{metrics.get('target_imo', 3.0):.2f} / 5.00**, se requiere un programa estructurado de transformación digital que cierre las brechas prioritarias en el corto y mediano plazo."""

    # Hallazgos Clave
    findings = []
    dom_summary = metrics.get("domains", {})
    for dom_code, dom_info in dom_summary.items():
        curr = dom_info.get("current", 0.0)
        gap = dom_info.get("gap", 0.0)
        if gap > 1.0:
            findings.append(f"**Dominio {dom_code} ({dom_info.get('name')}):** Requiere atención prioritaria con una brecha de {gap:.2f} puntos respecto a la meta.")
        else:
            findings.append(f"**Dominio {dom_code}:** Nivel actual de {curr:.2f}/5.00 con brecha moderada de {gap:.2f} puntos.")

    # Matriz de Riesgos Heurísticos
    risks = [
        {
            "category": "Ciberseguridad y Resiliencia",
            "level": "Alto" if imo < 2.5 else "Medio",
            "description": "Riesgo de incidentes de seguridad e interrupción operativa por controles perimetrales e identidades insuficientemente automatizados.",
            "action": "Desplegar MFA, segmentación de red y un plan de respuesta a incidentes (APO13, DSS05)."
        },
        {
            "category": "Alineación Estratégica",
            "level": "Alto" if imo < 2.0 else "Medio",
            "description": "Riesgo de desvío presupuestal e inversiones tecnológicas que no aportan valor medible a los objetivos de negocio.",
            "action": "Institucionalizar el Comité Directivo de TI y definir KPIs de negocio en el portafolio (EDM01, EDM02, APO02)."
        },
        {
            "category": "Continuidad Operacional",
            "level": "Alto" if any(g["process_id"] == "DSS04" and g["gap"] > 1.5 for g in top_gaps) else "Medio",
            "description": "Planes de contingencia (DRP) sin pruebas periódicas de recuperación que garanticen RTO y RPO adecuados.",
            "action": "Actualizar el plan DRP y ejecutar un simulacro de contingencia en ambiente controlado (DSS04)."
        }
    ]

    # Recomendaciones Inmediatas (Quick Wins)
    recommendations = [
        "Formalizar y publicar la Política General de Seguridad de la Información (SGSI).",
        "Establecer el Catálogo de Servicios de TI con Acuerdos de Nivel de Servicio (SLA) medibles.",
        "Automatizar las revisiones semanales del Comité de Control de Cambios (CAB).",
        "Implementar un tablero de control ejecutivo para el monitoreo mensual de indicadores de TI."
    ]

    return {
        "summary": summary,
        "findings": findings,
        "risks": risks,
        "recommendations": recommendations,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
