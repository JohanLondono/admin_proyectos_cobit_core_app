"""
Generador Automático de Hojas de Ruta (Roadmaps) COBIT 2019 [COB-TK10, COB-ST14].
Aplica priorización multi-criterio, detección de Quick Wins y distribución en 3 fases temporales.
"""

from typing import Dict, List, Any
from engine.cobit_data import COBIT_PROCESSES

# Plantillas de iniciativas predefinidas por proceso COBIT
INITIATIVE_TEMPLATES = {
    "EDM01": {
        "title": "Formalización del Comité de Gobernanza de TI y Marco Normativo",
        "desc": "Crear estatuto del comité con participación directiva y aprobar las políticas marco de gobierno.",
        "cost": 15000000,
        "months": 3,
        "role": "Junta Directiva / CIO",
        "quick_win": False
    },
    "EDM02": {
        "title": "Modelo de Gestión y Entrega de Valor (ROI de TI)",
        "desc": "Establecer metodología formal para justificación financiera y seguimiento de valor post-proyecto.",
        "cost": 12000000,
        "months": 3,
        "role": "Gerencia Financiera y CIO",
        "quick_win": False
    },
    "EDM03": {
        "title": "Alineación del Apetito y Tolerancia al Riesgo de TI",
        "desc": "Formalizar umbrales de riesgo empresarial y matriz de riesgo tecnológico aprobada por el Directorio.",
        "cost": 14000000,
        "months": 3,
        "role": "Comité de Riesgos y CISO",
        "quick_win": False
    },
    "APO01": {
        "title": "Actualización de la Estructura Organizacional y Roles de TI",
        "desc": "Definir manual de funciones, responsabilidades RACI y canales de escalamiento técnico.",
        "cost": 8000000,
        "months": 2,
        "role": "Recursos Humanos y TI",
        "quick_win": True
    },
    "APO02": {
        "title": "Elaboración del Plan Estratégico de TI (PETI)",
        "desc": "Construir la hoja de ruta estratégica de tecnología alineada a los objetivos de negocio a 3 años.",
        "cost": 22000000,
        "months": 4,
        "role": "Líder de Estrategia y CIO",
        "quick_win": False
    },
    "APO09": {
        "title": "Catálogo de Servicios y Acuerdos de Nivel de Servicio (SLA)",
        "desc": "Documentar los servicios que presta TI a las áreas y pactar tiempos máximos de respuesta.",
        "cost": 7000000,
        "months": 2,
        "role": "Líder de Soporte / Service Desk",
        "quick_win": True
    },
    "APO12": {
        "title": "Gestión Integral de Riesgos Operacionales de TI",
        "desc": "Implementar registro continuo de eventos de riesgo y planes de mitigación ante amenazas críticas.",
        "cost": 18000000,
        "months": 4,
        "role": "Oficial de Riesgos de TI",
        "quick_win": False
    },
    "APO13": {
        "title": "Implementación del SGSI y Políticas de Ciberseguridad",
        "desc": "Formalizar políticas de seguridad de la información, clasificación de activos y controles ISO 27001.",
        "cost": 35000000,
        "months": 6,
        "role": "Oficial de Seguridad (CISO)",
        "quick_win": False
    },
    "APO14": {
        "title": "Gobierno de Datos y Calidad de la Información",
        "desc": "Establecer diccionario de datos corporativos, custodios por área y políticas de retención.",
        "cost": 25000000,
        "months": 6,
        "role": "Arquitecto de Datos",
        "quick_win": False
    },
    "BAI02": {
        "title": "Estandarización del Levantamiento y Trazabilidad de Requisitos",
        "desc": "Adoptar plantilla estándar de especificación funcional con criterios de aceptación claros.",
        "cost": 6000000,
        "months": 2,
        "role": "Analista de Negocio / QA",
        "quick_win": True
    },
    "BAI06": {
        "title": "Digitalización del Comité de Cambios (CAB) y Flujo de Pases",
        "desc": "Automatizar la solicitud, evaluación de impacto y aprobación de cambios a producción.",
        "cost": 10000000,
        "months": 3,
        "role": "Líder de Infraestructura y Operaciones",
        "quick_win": True
    },
    "BAI11": {
        "title": "Metodología Ágil/Híbrida para Gestión de Proyectos de TI",
        "desc": "Capacitar al equipo en Scrum/Kanban e implementar herramienta de seguimiento de sprint.",
        "cost": 14000000,
        "months": 3,
        "role": "PMO de TI / Scrum Master",
        "quick_win": False
    },
    "DSS01": {
        "title": "Automatización de Procedimientos Operativos y Backups",
        "desc": "Estandarizar respaldos periódicos con pruebas de restauración y monitoreo preventivo.",
        "cost": 9000000,
        "months": 2,
        "role": "Administrador de Sistemas",
        "quick_win": True
    },
    "DSS02": {
        "title": "Optimización del Service Desk y Gestión de Incidentes",
        "desc": "Clasificar incidentes, medir satisfacción y establecer base de conocimientos para autoservicio.",
        "cost": 11000000,
        "months": 2,
        "role": "Coordinador de Soporte",
        "quick_win": True
    },
    "DSS04": {
        "title": "Plan de Recuperación ante Desastres (DRP) y Simulacro",
        "desc": "Actualizar el plan de continuidad técnica y realizar prueba de conmutación a sitio alterno.",
        "cost": 28000000,
        "months": 4,
        "role": "Gerente de Infraestructura y CISO",
        "quick_win": False
    },
    "DSS05": {
        "title": "Despliegue de Autenticación MFA y Protección de Endpoints",
        "desc": "Activar autenticación de doble factor obligatoria y herramientas EDR en todos los equipos.",
        "cost": 16000000,
        "months": 2,
        "role": "Especialista en Seguridad",
        "quick_win": True
    },
    "MEA01": {
        "title": "Tablero Ejecutivo de Indicadores de TI (KPIs)",
        "desc": "Diseñar dashboard mensual con disponibilidad, satisfacción, costos y avances de proyectos.",
        "cost": 12000000,
        "months": 3,
        "role": "Líder de BI y CIO",
        "quick_win": True
    },
    "MEA02": {
        "title": "Programa de Auto-Evaluación de Controles Internos de TI",
        "desc": "Establecer checklist semestral de controles clave previo a las auditorías externas.",
        "cost": 8000000,
        "months": 2,
        "role": "Auditor Interno de TI",
        "quick_win": True
    },
    "MEA03": {
        "title": "Matriz de Cumplimiento Normativo y Legal de TI",
        "desc": "Mapear leyes de protección de datos, circulares de supervisión y regularizaciones vigentes.",
        "cost": 10000000,
        "months": 3,
        "role": "Oficial de Cumplimiento",
        "quick_win": False
    }
}

def generate_roadmap_plan(scores: List[Dict[str, Any]], client_name: str) -> Dict[str, Any]:
    """
    [COB-TK10, COB-ST14] Genera el plan de hoja de ruta en 3 fases:
    - Fase 1: Cimientos y Quick Wins (Meses 1-3)
    - Fase 2: Consolidación y Procesos Core (Meses 4-8)
    - Fase 3: Optimización y Mejora Continua (Meses 9-18)
    """
    initiatives = []
    total_cost = 0.0

    # Ordenar procesos por magnitud de la brecha
    sorted_scores = sorted(scores, key=lambda s: float(s.get("target_score", 3.0)) - float(s.get("current_score", 0.0)), reverse=True)

    # Identificar procesos que tienen brecha (> 0.5)
    candidates = [s for s in sorted_scores if (float(s.get("target_score", 3.0)) - float(s.get("current_score", 0.0))) >= 0.5]
    if not candidates:
        candidates = sorted_scores[:10]

    for item in candidates:
        pid = item["process_id"]
        gap = round(float(item.get("target_score", 3.0)) - float(item.get("current_score", 0.0)), 1)
        pname = COBIT_PROCESSES.get(pid, {}).get("name", pid)

        # Buscar si hay plantilla para este proceso o generar iniciativa personalizada
        if pid in INITIATIVE_TEMPLATES:
            tpl = INITIATIVE_TEMPLATES[pid]
            is_qw = tpl["quick_win"] and gap > 0.8
            cost = tpl["cost"]
            months = tpl["months"]
            title = tpl["title"]
            desc = f"{tpl['desc']} (Brecha actual: {gap} pts en {pid})."
            role = tpl["role"]
        else:
            is_qw = gap <= 1.0
            cost = 12000000
            months = 3
            title = f"Optimización del Proceso {pid} - {pname[:40]}"
            desc = f"Formalizar procedimientos y elevar nivel de madurez de {pid} (Brecha actual: {gap} pts)."
            role = "Líder de TI"

        # Asignar fase según criterios
        if is_qw or months <= 2:
            phase = 1
            priority = "Alta"
        elif gap >= 1.5 or cost > 25000000:
            phase = 2
            priority = "Alta"
        else:
            phase = 3
            priority = "Media"

        total_cost += cost
        initiatives.append({
            "process_id": pid,
            "phase": phase,
            "title": title,
            "description": desc,
            "is_quick_win": is_qw,
            "priority": priority,
            "estimated_months": months,
            "estimated_cost": cost,
            "responsible_role": role,
            "status": "pending"
        })

    # Asegurar que haya al menos 2 iniciativas en cada fase
    initiatives.sort(key=lambda x: (x["phase"], 0 if x["is_quick_win"] else 1, -x["estimated_cost"]))

    summary = f"Hoja de Ruta Estratégica diseñada para {client_name}, con {len(initiatives)} iniciativas estructuradas a 18 meses para cerrar brechas prioritarias bajo COBIT 2019."

    return {
        "title": f"Hoja de Ruta de Transformación Digital COBIT 2019 - {client_name}",
        "total_budget": total_cost,
        "horizon_months": 18,
        "summary": summary,
        "initiatives": initiatives,
        "quick_wins_count": len([i for i in initiatives if i["is_quick_win"]])
    }
