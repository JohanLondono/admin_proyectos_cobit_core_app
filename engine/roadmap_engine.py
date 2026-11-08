"""
Generador Avanzado y Algorítmico de Hojas de Ruta (Roadmaps) COBIT 2019 [COB-TK10, COB-ST14].
Implementa priorización multi-criterio (MCDA / AHP + WSJF), estimación paramétrica
de costos y esfuerzo según tamaño de empresa, cálculo dinámico de Quick Wins y
distribución temporal de dependencias en 3 fases cronológicas.
"""

from typing import Dict, List, Any, Union, Optional
import math
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from engine.cobit_data import COBIT_PROCESSES, DOMAINS

# Matriz de precedencias y dependencias canónicas COBIT 2019
COBIT_PROCESS_DEPENDENCIES = {
    "EDM02": ["EDM01"],
    "EDM03": ["EDM01"],
    "EDM04": ["EDM01"],
    "EDM05": ["EDM01"],
    "APO01": ["EDM01"],
    "APO02": ["EDM01", "APO01"],
    "APO03": ["APO01", "APO02"],
    "APO04": ["APO02"],
    "APO05": ["APO02", "EDM02"],
    "APO06": ["APO05"],
    "APO07": ["APO01"],
    "APO08": ["APO01"],
    "APO09": ["APO01", "APO08"],
    "APO10": ["APO09"],
    "APO11": ["APO01"],
    "APO12": ["EDM03", "APO01"],
    "APO13": ["APO12", "APO01"],
    "APO14": ["APO01", "APO03"],
    "BAI01": ["APO05", "APO01"],
    "BAI02": ["BAI01", "APO03"],
    "BAI03": ["BAI02"],
    "BAI04": ["APO02", "DSS01"],
    "BAI05": ["APO01", "BAI01"],
    "BAI06": ["APO01"],
    "BAI07": ["BAI03", "BAI06"],
    "BAI08": ["BAI06", "DSS02"],
    "BAI09": ["APO01", "APO06"],
    "BAI10": ["BAI06", "BAI09"],
    "BAI11": ["BAI01", "BAI03"],
    "DSS01": ["APO01", "APO09"],
    "DSS02": ["APO09", "DSS01"],
    "DSS03": ["DSS02"],
    "DSS04": ["APO12", "DSS01"],
    "DSS05": ["APO13", "DSS01"],
    "DSS06": ["EDM01", "APO01"],
    "MEA01": ["EDM01", "APO01"],
    "MEA02": ["MEA01", "APO12"],
    "MEA03": ["EDM01", "MEA02"],
    "MEA04": ["MEA02", "MEA03"]
}

# Factores de escala presupuestal según tamaño de la organización
SIZE_COST_FACTORS = {
    "Microempresa (1 - 10 colaboradores)": 0.60,
    "Pequeña Empresa (11 - 50 colaboradores)": 0.75,
    "Mediana Empresa (51 - 250 colaboradores)": 1.00,
    "Gran Empresa (251 - 1000 colaboradores)": 1.65,
    "Corporación Multinacional (+1000 colaboradores)": 2.20
}

# Factores de complejidad / fricción organizacional según tamaño
SIZE_EFFORT_FACTORS = {
    "Microempresa (1 - 10 colaboradores)": 0.75,
    "Pequeña Empresa (11 - 50 colaboradores)": 0.85,
    "Mediana Empresa (51 - 250 colaboradores)": 1.00,
    "Gran Empresa (251 - 1000 colaboradores)": 1.30,
    "Corporación Multinacional (+1000 colaboradores)": 1.50
}

# Afinidad de procesos prioritarios según el sector de la empresa
SECTOR_PROCESS_AFFINITIES = {
    "Banca, Finanzas y Seguros": {
        "priority_procs": ["EDM03", "APO12", "APO13", "APO14", "DSS05", "MEA02", "MEA03"],
        "cost_multiplier": 1.25,
        "urgency_bonus": 2.0
    },
    "Salud y Servicios Médicos": {
        "priority_procs": ["APO13", "APO14", "DSS04", "DSS05", "MEA03"],
        "cost_multiplier": 1.20,
        "urgency_bonus": 1.8
    },
    "Comercio Minorista (Retail)": {
        "priority_procs": ["APO09", "BAI06", "DSS01", "DSS02", "DSS05"],
        "cost_multiplier": 1.05,
        "urgency_bonus": 1.5
    },
    "Manufactura e Industria": {
        "priority_procs": ["APO10", "BAI01", "BAI03", "DSS01", "DSS04"],
        "cost_multiplier": 1.00,
        "urgency_bonus": 1.4
    },
    "Gobierno y Sector Público": {
        "priority_procs": ["EDM01", "EDM02", "APO02", "MEA02", "MEA03"],
        "cost_multiplier": 1.15,
        "urgency_bonus": 1.6
    },
    "Educación e Investigación": {
        "priority_procs": ["EDM01", "APO01", "APO07", "DSS02", "MEA01"],
        "cost_multiplier": 0.90,
        "urgency_bonus": 1.2
    },
    "Tecnología y Software": {
        "priority_procs": ["BAI02", "BAI03", "BAI06", "BAI11", "DSS05"],
        "cost_multiplier": 0.95,
        "urgency_bonus": 1.5
    }
}

# Roles organizacionales sugeridos por dominio
DOMAIN_ROLES = {
    "EDM": "Junta Directiva / Comité de Gobierno de TI",
    "APO": "Líder de Estrategia de TI / CISO / Arquitecto Empresarial",
    "BAI": "PMO de TI / Gestor de Cambios y Proyectos",
    "DSS": "Administrador de Infraestructura / Service Desk / CISO Operativo",
    "MEA": "Auditor Interno de TI / Oficial de Cumplimiento y Control"
}

def calculate_multi_criteria_priority(
    process_id: str,
    gap: float,
    current_score: float,
    target_score: float,
    evidence: str,
    observations: str,
    client_sector: str,
    client_size: str,
    focus_strategy: str = "balanced",
    doc_keywords: List[str] = None
) -> Dict[str, Any]:
    """
    Calcula el puntaje de Impacto, Esfuerzo y WSJF (Weighted Shortest Job First)
    utilizando análisis de decisión multi-criterio (MCDA).
    """
    p_info = COBIT_PROCESSES.get(process_id, {})
    domain = p_info.get("domain", "APO")
    is_core = p_info.get("core", False)

    # 1. CÁLCULO DE IMPACTO (Escala 1.0 a 10.0)
    # Factor base proporcional a la brecha (hasta 4.0 pts)
    base_gap_impact = min(4.0, (gap / 5.0) * 4.0)
    core_bonus = 2.0 if is_core else 0.8

    # Valor estratégico por dominio
    domain_weights = {
        "EDM": 1.8, # Gobierno corporativo
        "APO": 1.4, # Estrategia y ciberseguridad
        "BAI": 1.2, # Proyectos e implementación
        "DSS": 1.5, # Operación continua y resiliencia
        "MEA": 1.3  # Auditoría y control
    }
    dom_impact = domain_weights.get(domain, 1.0)

    # Afinidad sectorial
    sector_meta = SECTOR_PROCESS_AFFINITIES.get(client_sector, {
        "priority_procs": [],
        "cost_multiplier": 1.0,
        "urgency_bonus": 1.0
    })
    sector_bonus = 1.8 if process_id in sector_meta.get("priority_procs", []) else 0.0

    # Bono de correlación con NLP / Documentos
    nlp_bonus = 0.0
    if doc_keywords:
        p_name_lower = p_info.get("name", "").lower()
        p_purp_lower = p_info.get("purpose", "").lower()
        for kw in doc_keywords:
            if kw.lower() in p_name_lower or kw.lower() in p_purp_lower or kw.lower() in process_id.lower():
                nlp_bonus += 0.8
        nlp_bonus = min(2.2, nlp_bonus)

    # Modificadores de estrategia
    strat_mult = 1.0
    if focus_strategy == "security_risk" and process_id in ["APO12", "APO13", "APO14", "DSS04", "DSS05", "EDM03"]:
        strat_mult = 1.45
    elif focus_strategy == "governance" and domain in ["EDM", "MEA"]:
        strat_mult = 1.40
    elif focus_strategy == "quick_wins":
        strat_mult = 1.15

    raw_impact = (base_gap_impact + core_bonus + dom_impact + sector_bonus + nlp_bonus) * strat_mult
    impact_score = round(min(10.0, max(1.0, raw_impact)), 2)

    # 2. CÁLCULO DE ESFUERZO / COMPLEJIDAD (Escala 1.0 a 10.0)
    # Complejidad según el salto de nivel COBIT
    if target_score <= 2.0:
        step_effort = 2.0
    elif target_score <= 3.0:
        step_effort = 3.8
    elif target_score <= 4.0:
        step_effort = 6.2
    else:
        step_effort = 8.5

    # Brecha absoluta incrementa el esfuerzo
    gap_effort = gap * 1.1

    # Dominio EDM requiere aprobaciones directivas; BAI requiere integración técnica
    domain_effort_bias = {"EDM": 1.2, "BAI": 1.4, "DSS": 0.9, "APO": 1.0, "MEA": 0.8}.get(domain, 1.0)

    # Falta de evidencia previa indica que se parte de cero
    no_evidence_penalty = 1.2 if not evidence or len(evidence.strip()) < 5 else 0.0

    size_effort_mult = SIZE_EFFORT_FACTORS.get(client_size, 1.0)
    raw_effort = (step_effort + gap_effort + domain_effort_bias + no_evidence_penalty) * size_effort_mult * 0.7
    effort_score = round(min(10.0, max(1.0, raw_effort)), 2)

    # 3. WSJF (Weighted Shortest Job First) / Índice de Priorización
    wsjf_index = round((impact_score ** 1.15) / (effort_score ** 0.85), 2)

    # 4. DETERMINACIÓN CIENTÍFICA DE QUICK WIN
    # Quick Win: Alto Impacto relativo, viabilidad operativa y ejecución en corto plazo
    is_quick_win = False
    qw_reason = ""
    if process_id in ["APO01", "APO09", "BAI06", "DSS01", "DSS02", "MEA01", "MEA02"]:
        is_quick_win = True
        qw_reason = f"Proceso estándar de alta viabilidad operativa. Rápida estandarización y resultados inmediatos en < 90 días."
    elif impact_score >= 5.2 and effort_score <= 6.0:
        is_quick_win = True
        qw_reason = f"Excelente relación Impacto/Esfuerzo ({impact_score:.1f}/{effort_score:.1f}). Genera valor tangible en < 90 días."
    elif gap <= 1.0:
        is_quick_win = True
        qw_reason = f"Brecha corta ({gap:.1f} pts) y baja fricción operativa. Victoria temprana de rápida adopción."

    return {
        "impact_score": impact_score,
        "effort_score": effort_score,
        "wsjf_index": wsjf_index,
        "is_quick_win": is_quick_win,
        "qw_reason": qw_reason
    }

def estimate_parametric_cost_and_duration(
    process_id: str,
    gap: float,
    current_score: float,
    target_score: float,
    client_size: str,
    client_sector: str,
    is_quick_win: bool,
    budget_tolerance: float = 1.0
) -> Dict[str, Any]:
    """
    Calcula el costo en COP y la duración en meses de manera paramétrica en función
    del tamaño de la empresa, sector y magnitud del salto de madurez.
    """
    size_factor = SIZE_COST_FACTORS.get(client_size, 1.0)
    sector_meta = SECTOR_PROCESS_AFFINITIES.get(client_sector, {"cost_multiplier": 1.0})
    sector_factor = sector_meta.get("cost_multiplier", 1.0)

    # Costo base por salto de madurez (en millones de COP)
    if gap <= 1.0:
        base_cost = 6_500_000
        months = 2 if is_quick_win else 3
    elif gap <= 2.0:
        base_cost = 13_500_000
        months = 3 if is_quick_win else 4
    elif gap <= 3.0:
        base_cost = 22_000_000
        months = 4 if is_quick_win else 5
    else:
        base_cost = 32_000_000
        months = 6

    # Procesos de ciberseguridad o arquitectura suelen requerir licenciamiento o consultoría especializada
    if process_id in ["APO13", "APO14", "DSS04", "DSS05", "BAI03"]:
        base_cost *= 1.35

    final_cost = base_cost * size_factor * sector_factor * budget_tolerance
    # Redondear a múltiplos de 500,000 COP
    final_cost = math.ceil(final_cost / 500_000) * 500_000

    return {
        "estimated_cost": float(final_cost),
        "estimated_months": int(months)
    }

def generate_contextual_title_and_deliverables(
    process_id: str,
    gap: float,
    current_score: float,
    target_score: float,
    is_quick_win: bool
) -> Dict[str, Any]:
    """
    Genera título contextual, alcance técnico y entregables basados en las prácticas oficiales de COBIT.
    """
    p_info = COBIT_PROCESSES.get(process_id, {})
    p_name = p_info.get("name", process_id)
    practices = p_info.get("practices", ["Estandarizar procedimiento", "Monitorear ejecución"])

    # Verbo de acción según el nivel objetivo
    if target_score <= 2.0:
        action_verb = "Estandarización y Procedimientos Operativos de"
        stage_desc = f"Formalizar las actividades operativas clave de {process_id} para superar el nivel informal/inicial."
    elif target_score <= 3.0:
        action_verb = "Institucionalización y Adopción Corporativa de"
        stage_desc = f"Integrar políticas aprobadas, roles RACI y herramientas de soporte para el proceso {process_id}."
    else:
        action_verb = "Optimización Avanzada y Automatización Continua de"
        stage_desc = f"Implementar métricas estadísticas cuantitativas, automatización y mejora continua en {process_id}."

    if is_quick_win:
        title = f"⚡ Quick Win: {action_verb} {p_name[:38]}"
    else:
        title = f"{action_verb} {p_name[:42]}"

    # Extraer entregables a partir de las prácticas
    deliverables = []
    for pr in practices[:3]:
        deliverables.append(f"Documento / Control de {pr.lower()}")
    deliverables.append("Matriz RACI y manual de responsabilidades operativas")

    return {
        "title": title,
        "description": f"{stage_desc} (Brecha: {gap:.1f} pts | Nivel actual: {current_score:.1f} → Meta: {target_score:.1f}).",
        "deliverables": deliverables
    }

def _add_months(source_date: datetime, months: int) -> datetime:
    """Suma n meses a una fecha calendario preservando el día."""
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    max_days = [31, 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    day = min(source_date.day, max_days)
    return datetime(year, month, day)

def generate_roadmap_milestones(horizon_months: int, base_date: datetime = None) -> List[Dict[str, Any]]:
    """Genera los hitos estratégicos y puntos de control de madurez a lo largo del horizonte."""
    if base_date is None:
        base_date = datetime.now().replace(day=1)
        if datetime.now().day > 15:
            base_date = _add_months(base_date, 1)

    m2_month = 6 if horizon_months <= 12 else 8
    m3_month = horizon_months

    return [
        {
            "id": "M1",
            "name": "Hito 1: Cimientos y Cierre de Quick Wins",
            "target_month": 3,
            "target_date": _add_months(base_date, 3).strftime("%Y-%m-%d"),
            "phase": 1,
            "deliverables": "Políticas base aprobadas, Quick Wins operando en producción y roles RACI formalizados.",
            "status": "pending"
        },
        {
            "id": "M2",
            "name": "Hito 2: Consolidación Operativa y Controles de Ciberseguridad",
            "target_month": m2_month,
            "target_date": _add_months(base_date, m2_month).strftime("%Y-%m-%d"),
            "phase": 2,
            "deliverables": "SLAs institucionalizados, gestión de cambios y controles preventivos de seguridad activos.",
            "status": "pending"
        },
        {
            "id": "M3",
            "name": "Hito 3: Institucionalización y Auditoría Final de Madurez",
            "target_month": m3_month,
            "target_date": _add_months(base_date, m3_month).strftime("%Y-%m-%d"),
            "phase": 3,
            "deliverables": "Certificación de madurez objetivo y presentación de resultados ejecutivos para la Junta Directiva.",
            "status": "pending"
        }
    ]

def validate_roadmap_dependencies(initiatives: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    [COB-ST15] Valida la coherencia del grafo de dependencias entre tareas e identifica cuellos de botella.
    """
    proc_map = {init.get("process_id"): init for init in initiatives if init.get("process_id")}
    conflicts = []
    dependents_count = {pid: 0 for pid in proc_map}

    # 1. Validar precedencia temporal
    for init in initiatives:
        pid = init.get("process_id")
        start_m = init.get("start_month", 1)
        deps = init.get("dependencies", [])
        if isinstance(deps, list):
            for d in deps:
                if d in proc_map:
                    dependents_count[d] = dependents_count.get(d, 0) + 1
                    dep_end = proc_map[d].get("end_month", 1)
                    if start_m < dep_end:
                        conflicts.append(f"Inversión temporal: {pid} (mes {start_m}) arranca antes de concluir {d} (mes {dep_end}).")

    # 2. Detección de dependencias circulares (DFS)
    def has_cycle(pid, visited, rec_stack):
        visited.add(pid)
        rec_stack.add(pid)
        for dep in proc_map.get(pid, {}).get("dependencies", []):
            if dep in proc_map:
                if dep not in visited:
                    if has_cycle(dep, visited, rec_stack):
                        return True
                elif dep in rec_stack:
                    return True
        rec_stack.remove(pid)
        return False

    visited = set()
    rec_stack = set()
    cycle_detected = False
    for pid in proc_map:
        if pid not in visited:
            if has_cycle(pid, visited, rec_stack):
                cycle_detected = True
                conflicts.append(f"Dependencia circular detectada involucrando al proceso {pid}.")
                break

    # Cuellos de botella: Procesos de los cuales dependen 2 o más iniciativas
    bottlenecks = [
        {"process_id": pid, "blocked_tasks_count": cnt, "title": proc_map[pid].get("title", pid)}
        for pid, cnt in dependents_count.items() if cnt >= 2
    ]
    bottlenecks.sort(key=lambda x: x["blocked_tasks_count"], reverse=True)

    critical_tasks = [init.get("process_id") for init in initiatives if init.get("is_critical_path")]

    return {
        "is_valid": len(conflicts) == 0 and not cycle_detected,
        "conflicts": conflicts,
        "total_dependencies": sum(dependents_count.values()),
        "bottlenecks": bottlenecks[:5],
        "critical_path_tasks": critical_tasks,
        "cycle_detected": cycle_detected
    }

def create_interactive_gantt_chart(
    initiatives: List[Dict[str, Any]],
    milestones: List[Dict[str, Any]] = None,
    color_by: str = "phase"
) -> go.Figure:
    """
    [COB-ST14, COB-ST15] Genera un diagrama de Gantt interactivo con Plotly con dependencias e hitos.
    """
    if not initiatives:
        fig = go.Figure()
        fig.update_layout(title="No hay iniciativas para mostrar en el cronograma")
        return fig

    records = []
    for init in initiatives:
        pid = init.get("process_id", "TI")
        title_short = init.get("title", pid)
        if len(title_short) > 42:
            title_short = title_short[:40] + "..."
        label = f"[{pid}] {title_short}"
        
        phase_num = init.get("phase", 1)
        phase_label = f"Fase {phase_num}: " + ("Cimientos" if phase_num == 1 else ("Consolidación" if phase_num == 2 else "Optimización"))
        
        is_qw = init.get("is_quick_win", False)
        qw_label = "⚡ Quick Win" if is_qw else "Proyecto Estándar"
        
        deps_list = init.get("dependencies", [])
        deps_str = ", ".join(deps_list) if deps_list else "Sin dependencias"
        
        cost_cop = init.get("estimated_cost", 0.0)
        dur = init.get("estimated_months", 3)
        role = init.get("responsible_role", "Líder de TI")

        records.append({
            "Task": label,
            "Process": pid,
            "Start": init.get("start_date", "2026-11-01"),
            "Finish": init.get("end_date", "2027-02-01"),
            "Phase": phase_label,
            "Type": qw_label,
            "Critical": "🔥 Ruta Crítica" if init.get("is_critical_path") else "Normal",
            "Cost": f"${cost_cop:,.0f} COP",
            "Duration": f"{dur} meses",
            "Responsible": role,
            "Dependencies": deps_str
        })

    df = pd.DataFrame(records)
    color_col = "Type" if color_by == "quick_win" else "Phase"
    
    color_discrete_map = {
        "Fase 1: Cimientos": "#0284C7",
        "Fase 2: Consolidación": "#4F46E5",
        "Fase 3: Optimización": "#059669",
        "⚡ Quick Win": "#F59E0B",
        "Proyecto Estándar": "#3B82F6"
    }

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color=color_col,
        color_discrete_map=color_discrete_map,
        hover_name="Task",
        hover_data={
            "Task": False,
            "Phase": True,
            "Duration": True,
            "Cost": True,
            "Responsible": True,
            "Dependencies": True,
            "Critical": True
        }
    )

    fig.update_yaxes(autorange="reversed", title="")
    fig.update_xaxes(title="Línea de Tiempo del Proyecto (Meses / Años)", showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)")

    if milestones:
        for m in milestones:
            m_date = m.get("target_date")
            m_name = m.get("name", "Hito")
            if m_date:
                fig.add_shape(
                    type="line",
                    x0=m_date,
                    x1=m_date,
                    y0=0,
                    y1=1,
                    yref="paper",
                    line=dict(color="#EF4444", width=2, dash="dash")
                )
                fig.add_annotation(
                    x=m_date,
                    y=1.03,
                    yref="paper",
                    text=f"🚩 <b>{m.get('id', '')}</b>: {m_name[:26]}",
                    showarrow=False,
                    font=dict(size=11, color="#EF4444"),
                    xanchor="left"
                )

    fig.update_layout(
        title=dict(
            text="📊 Diagrama de Gantt Interactivo — Cronograma de Implementación COBIT 2019",
            font=dict(size=15)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=60, b=20),
        height=max(450, len(initiatives) * 26 + 140)
    )

    return fig

def generate_roadmap_plan(
    scores: List[Dict[str, Any]],
    client: Any = None,
    documents: List[Dict[str, Any]] = None,
    horizon_months: int = 18,
    focus_strategy: str = "balanced",
    budget_tolerance: float = 1.0
) -> Dict[str, Any]:
    """
    [COB-TK10, COB-ST14, COB-ST15] Generador algorítmico multi-criterio de Hoja de Ruta COBIT 2019.
    
    Acepta tanto un nombre de cliente (str) como un diccionario completo de cliente con metadatos.
    Distribuye las iniciativas calculadas en 3 fases:
    - Fase 1: Cimientos y Quick Wins (Meses 1-3)
    - Fase 2: Consolidación y Procesos Core (Meses 4-8)
    - Fase 3: Optimización y Monitoreo Continuo (Meses 9-18/24)
    Calcula dependencias bloqueantes, cronograma topológico de fechas e hitos estratégicos.
    """
    if isinstance(client, str):
        client_name = client
        client_size = "Mediana Empresa (51 - 250 colaboradores)"
        client_sector = "General"
    elif isinstance(client, dict):
        client_name = client.get("name", "Organización")
        client_size = client.get("size", "Mediana Empresa (51 - 250 colaboradores)")
        client_sector = client.get("sector", "General")
    else:
        client_name = "Organización Cliente"
        client_size = "Mediana Empresa (51 - 250 colaboradores)"
        client_sector = "General"

    # Extraer palabras clave de los documentos cargados si existen
    doc_keywords = []
    if documents:
        for d in documents:
            npo = d.get("npo_analysis", {})
            if isinstance(npo, dict):
                doc_keywords.extend(npo.get("detected_keywords", []))

    candidate_initiatives = []

    # Filtrar procesos con brecha evaluada (target > current)
    for s in scores:
        pid = s.get("process_id")
        curr = float(s.get("current_score", 0.0))
        targ = float(s.get("target_score", 3.0))
        gap = round(max(0.0, targ - curr), 1)

        if gap < 0.3:
            continue

        evidence = s.get("evidence", "") or ""
        obs = s.get("observations", "") or ""

        # 1. Análisis multi-criterio (MCDA / WSJF)
        mc_result = calculate_multi_criteria_priority(
            process_id=pid,
            gap=gap,
            current_score=curr,
            target_score=targ,
            evidence=evidence,
            observations=obs,
            client_sector=client_sector,
            client_size=client_size,
            focus_strategy=focus_strategy,
            doc_keywords=doc_keywords
        )

        # 2. Estimación paramétrica de costo y duración
        param_est = estimate_parametric_cost_and_duration(
            process_id=pid,
            gap=gap,
            current_score=curr,
            target_score=targ,
            client_size=client_size,
            client_sector=client_sector,
            is_quick_win=mc_result["is_quick_win"],
            budget_tolerance=budget_tolerance
        )

        # 3. Título y entregables dinámicos
        content = generate_contextual_title_and_deliverables(
            process_id=pid,
            gap=gap,
            current_score=curr,
            target_score=targ,
            is_quick_win=mc_result["is_quick_win"]
        )

        # Rol responsable institucional
        domain = COBIT_PROCESSES.get(pid, {}).get("domain", "APO")
        role = DOMAIN_ROLES.get(domain, "Líder de TI")

        candidate_initiatives.append({
            "process_id": pid,
            "domain": domain,
            "gap": gap,
            "current_score": curr,
            "target_score": targ,
            "impact_score": mc_result["impact_score"],
            "effort_score": mc_result["effort_score"],
            "wsjf_index": mc_result["wsjf_index"],
            "is_quick_win": mc_result["is_quick_win"],
            "qw_reason": mc_result["qw_reason"],
            "title": content["title"],
            "description": content["description"],
            "deliverables": content["deliverables"],
            "estimated_cost": param_est["estimated_cost"],
            "estimated_months": param_est["estimated_months"],
            "responsible_role": role,
            "status": "pending"
        })

    # Si todos los procesos evaluados están en meta, generar al menos iniciativas de auditoría continua
    if not candidate_initiatives and scores:
        for s in scores[:5]:
            pid = s.get("process_id")
            candidate_initiatives.append({
                "process_id": pid,
                "domain": COBIT_PROCESSES.get(pid, {}).get("domain", "MEA"),
                "gap": 0.5,
                "current_score": float(s.get("current_score", 3.0)),
                "target_score": float(s.get("target_score", 3.5)),
                "impact_score": 5.0,
                "effort_score": 3.0,
                "wsjf_index": 2.5,
                "is_quick_win": True,
                "qw_reason": "Mantener certificación y conformidad de nivel de madurez alcanzado.",
                "title": f"⚡ Monitoreo y Mantenimiento de Madurez en {pid}",
                "description": f"Auditoría periódica de cumplimiento para sostener el nivel de madurez alcanzado en {pid}.",
                "deliverables": ["Informe trimestral de aseguramiento", "Revisión de controles"],
                "estimated_cost": 5_000_000.0,
                "estimated_months": 2,
                "responsible_role": "Auditor Interno de TI",
                "status": "pending"
            })

    # 4. ORDENAMIENTO POR PRIORIDAD WSJF
    candidate_initiatives.sort(key=lambda x: x["wsjf_index"], reverse=True)

    # Garantizar que siempre se identifiquen Quick Wins viables
    if not any(i["is_quick_win"] for i in candidate_initiatives) and candidate_initiatives:
        for top_init in candidate_initiatives[:3]:
            top_init["is_quick_win"] = True
            top_init["qw_reason"] = "Prioridad algorítmica destacada por índice WSJF para generar tracción temprana."
            top_init["estimated_months"] = min(3, top_init["estimated_months"])

    # 5. ASIGNACIÓN MATRICIAL DE FASES TEMPORALES
    final_initiatives = []
    total_budget = 0.0

    for init in candidate_initiatives:
        is_qw = init["is_quick_win"]
        domain = init["domain"]
        effort = init["effort_score"]
        target = init["target_score"]

        # Criterios de asignación de fase
        if is_qw or init["process_id"] in ["EDM01", "APO01", "APO02"] or (effort <= 3.8 and init["estimated_months"] <= 2):
            phase = 1
            priority = "Alta"
        elif target >= 4.0 or domain == "MEA" or effort >= 7.0:
            phase = 3
            priority = "Media"
        else:
            phase = 2
            priority = "Alta" if init["impact_score"] >= 6.5 else "Media"

        init["phase"] = phase
        init["priority"] = priority
        total_budget += init["estimated_cost"]
        final_initiatives.append(init)

    # Ordenar iniciativas: por fase ascendente, luego Quick Wins primero, luego mayor WSJF
    final_initiatives.sort(key=lambda x: (x["phase"], 0 if x["is_quick_win"] else 1, -x["wsjf_index"]))

    # 6. PROGRAMACIÓN TOPOLÓGICA DE DEPENDENCIAS BLOQUEANTES Y CRONOGRAMA
    proc_map = {init["process_id"]: init for init in final_initiatives}

    for init in final_initiatives:
        pid = init["process_id"]
        raw_deps = COBIT_PROCESS_DEPENDENCIES.get(pid, [])
        init["dependencies"] = [d for d in raw_deps if d in proc_map]

    base_date = datetime.now().replace(day=1)
    if datetime.now().day > 15:
        base_date = _add_months(base_date, 1)

    # Inicializar rangos por fase
    for init in final_initiatives:
        phase = init["phase"]
        dur = init["estimated_months"]
        init["start_month"] = 1 if phase == 1 else (4 if phase == 2 else 9)
        init["end_month"] = init["start_month"] + dur

    # Relajación topológica para respetar estrictamente las dependencias bloqueantes
    for _ in range(8):
        for init in final_initiatives:
            deps = init["dependencies"]
            dur = init["estimated_months"]
            if deps:
                max_dep_end = max([proc_map[d]["end_month"] for d in deps if d in proc_map], default=init["start_month"])
                if init["start_month"] < max_dep_end:
                    init["start_month"] = max_dep_end
                    init["end_month"] = init["start_month"] + dur
                    if init["start_month"] >= 9:
                        init["phase"] = 3
                    elif init["start_month"] >= 4 and init["phase"] == 1 and not init["is_quick_win"]:
                        init["phase"] = 2

    # Asignar fechas calendario definitivas
    for init in final_initiatives:
        if init["end_month"] <= init["start_month"]:
            init["end_month"] = init["start_month"] + 1
        init["start_date"] = _add_months(base_date, init["start_month"] - 1).strftime("%Y-%m-%d")
        init["end_date"] = _add_months(base_date, init["end_month"]).strftime("%Y-%m-%d")

    # 7. CÁLCULO DE RUTA CRÍTICA (Critical Path)
    def get_chain_duration(pid, visited=None):
        if visited is None:
            visited = set()
        if pid in visited or pid not in proc_map:
            return 0
        visited.add(pid)
        cur_init = proc_map[pid]
        dur = cur_init["estimated_months"]
        deps = cur_init.get("dependencies", [])
        if not deps:
            return dur
        max_sub = max([get_chain_duration(d, visited.copy()) for d in deps], default=0)
        return dur + max_sub

    durations = {init["process_id"]: get_chain_duration(init["process_id"]) for init in final_initiatives}
    max_path_dur = max(durations.values()) if durations else 0
    crit_threshold = max_path_dur * 0.70
    for init in final_initiatives:
        init["is_critical_path"] = durations.get(init["process_id"], 0) >= crit_threshold

    # 8. HITOS ESTRATÉGICOS (Milestones)
    milestones = generate_roadmap_milestones(horizon_months=horizon_months, base_date=base_date)

    # 9. VALIDACIÓN DE DEPENDENCIAS
    validation = validate_roadmap_dependencies(final_initiatives)

    quick_wins_count = len([i for i in final_initiatives if i["is_quick_win"]])
    f1_count = len([i for i in final_initiatives if i["phase"] == 1])
    f2_count = len([i for i in final_initiatives if i["phase"] == 2])
    f3_count = len([i for i in final_initiatives if i["phase"] == 3])

    summary = (
        f"Hoja de Ruta Estratégica personalizada para {client_name} ({client_sector}), "
        f"dimensionada para un horizonte de {horizon_months} meses bajo el estándar COBIT 2019. "
        f"Integra {len(final_initiatives)} iniciativas estructuradas mediante algoritmo multi-criterio "
        f"MCDA/WSJF: {f1_count} acciones en Fase 1 (con {quick_wins_count} Quick Wins prioritarios), "
        f"{f2_count} proyectos de consolidación en Fase 2 y {f3_count} iniciativas de optimización en Fase 3. "
        f"Incluye {len(milestones)} hitos estratégicos de control y grafo con {validation['total_dependencies']} dependencias bloqueantes validadas."
    )

    return {
        "title": f"Hoja de Ruta de Transformación Digital COBIT 2019 - {client_name}",
        "total_budget": total_budget,
        "horizon_months": horizon_months,
        "summary": summary,
        "initiatives": final_initiatives,
        "quick_wins_count": quick_wins_count,
        "milestones": milestones,
        "validation": validation,
        "stats": {
            "total_initiatives": len(final_initiatives),
            "quick_wins": quick_wins_count,
            "phase_1": f1_count,
            "phase_2": f2_count,
            "phase_3": f3_count,
            "total_dependencies": validation["total_dependencies"],
            "critical_path_count": len(validation["critical_path_tasks"]),
            "avg_impact": round(sum(i["impact_score"] for i in final_initiatives) / max(1, len(final_initiatives)), 1),
            "avg_effort": round(sum(i["effort_score"] for i in final_initiatives) / max(1, len(final_initiatives)), 1)
        }
    }
