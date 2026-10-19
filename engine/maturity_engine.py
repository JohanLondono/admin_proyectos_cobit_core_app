"""
Motor de Cálculo de Madurez Organizacional e IMO - COBIT 2019 [COB-TK08].
Calcula promedios por dominio, IMO global ponderado, brechas y estado de salud.
"""

from typing import Dict, List, Any
from engine.cobit_data import DOMAINS, MATURITY_LEVELS, COBIT_PROCESSES

# Ponderación oficial de los 5 dominios para el Índice de Madurez Organizacional (IMO)
DOMAIN_WEIGHTS = {
    "EDM": 0.20, # Evaluar, Dirigir y Monitorizar (Gobierno)
    "APO": 0.25, # Alinear, Planificar y Organizar (Gestión Estratégica)
    "BAI": 0.20, # Construir, Adquirir e Implementar (Transformación)
    "DSS": 0.25, # Entregar, Dar Servicio y Soporte (Operaciones y Seguridad)
    "MEA": 0.10  # Monitorizar, Evaluar y Valorar (Aseguramiento y Control)
}

def calculate_assessment_metrics(scores: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Toma una lista de registros de puntaje y calcula:
    - Promedio por dominio (Actual y Meta)
    - Brechas (Gaps) por proceso y dominio
    - IMO Global ponderado
    - Nivel verbal de madurez
    - Top 5 procesos críticos
    - Indicadores de salud de gobernanza y riesgo
    """
    if not scores:
        return {
            "imo": 0.0,
            "target_imo": 3.0,
            "overall_gap": 0.0,
            "level_label": "No evaluado",
            "health_score": 0.0,
            "risk_score": 100.0,
            "domains": {},
            "top_gaps": [],
            "processes_count": 0
        }

    # Agrupar puntuaciones por dominio
    domain_data = {d: {"current": [], "target": [], "gaps": []} for d in DOMAINS.keys()}
    all_process_gaps = []

    for s in scores:
        dom = s["domain"]
        curr = float(s.get("current_score", 0.0))
        targ = float(s.get("target_score", 3.0))
        gap = round(max(0.0, targ - curr), 2)
        pid = s["process_id"]
        pname = COBIT_PROCESSES.get(pid, {}).get("name", pid)

        if dom in domain_data:
            domain_data[dom]["current"].append(curr)
            domain_data[dom]["target"].append(targ)
            domain_data[dom]["gaps"].append(gap)

        all_process_gaps.append({
            "process_id": pid,
            "name": pname,
            "domain": dom,
            "current_score": curr,
            "target_score": targ,
            "gap": gap,
            "evidence": s.get("evidence", ""),
            "observations": s.get("observations", "")
        })

    # Resumen por dominio
    domain_summary = {}
    weighted_current_sum = 0.0
    weighted_target_sum = 0.0
    total_active_weight = 0.0

    for dom, values in domain_data.items():
        weight = DOMAIN_WEIGHTS.get(dom, 0.20)
        curr_list = values["current"]
        targ_list = values["target"]

        if curr_list:
            avg_curr = sum(curr_list) / len(curr_list)
            avg_targ = sum(targ_list) / len(targ_list)
            avg_gap = avg_targ - avg_curr
            weighted_current_sum += avg_curr * weight
            weighted_target_sum += avg_targ * weight
            total_active_weight += weight

            domain_summary[dom] = {
                "name": DOMAINS[dom]["name"],
                "color": DOMAINS[dom]["color"],
                "current": round(avg_curr, 2),
                "target": round(avg_targ, 2),
                "gap": round(avg_gap, 2),
                "count": len(curr_list)
            }
        else:
            domain_summary[dom] = {
                "name": DOMAINS[dom]["name"],
                "color": DOMAINS[dom]["color"],
                "current": 0.0,
                "target": 3.0,
                "gap": 3.0,
                "count": 0
            }

    # Normalizar IMO ponderado
    if total_active_weight > 0:
        imo = round(weighted_current_sum / total_active_weight, 2)
        target_imo = round(weighted_target_sum / total_active_weight, 2)
    else:
        imo = 0.0
        target_imo = 3.0

    overall_gap = round(max(0.0, target_imo - imo), 2)

    # Determinar categoría verbal de madurez
    level_int = int(min(5, max(0, imo)))
    level_label = MATURITY_LEVELS.get(level_int, {}).get("label", "Incompleto")
    level_desc = MATURITY_LEVELS.get(level_int, {}).get("description", "")

    # Salud y Riesgo
    health_score = round(min(100.0, (imo / 5.0) * 100.0), 1)
    risk_score = round(max(0.0, (1.0 - (imo / 5.0)) * 100.0), 1)

    # Top 5 procesos con mayor brecha (gap)
    all_process_gaps.sort(key=lambda x: (x["gap"], 5.0 - x["current_score"]), reverse=True)
    top_gaps = all_process_gaps[:5]

    return {
        "imo": imo,
        "target_imo": target_imo,
        "overall_gap": overall_gap,
        "level_label": level_label,
        "level_description": level_desc,
        "health_score": health_score,
        "risk_score": risk_score,
        "domains": domain_summary,
        "top_gaps": top_gaps,
        "all_scored_processes": all_process_gaps,
        "processes_count": len(scores)
    }
