"""
Batería de pruebas automatizadas para COBIT Core Consulting System.
Valida inicialización de BD, cálculos de madurez, algoritmos de IA, roadmap y exportaciones.
"""

import sys
from pathlib import Path

# Agregar directorio del proyecto al path
APP_DIR = Path(__file__).parent
sys.path.insert(0, str(APP_DIR))

def test_system():
    print("==================================================================")
    print("   INICIANDO PRUEBAS AUTOMATIZADAS DE COBIT CORE CONSULTING APP   ")
    print("==================================================================")

    # 1. Test Base de Datos
    print("\n[1/6] Probando inicialización de SQLite y datos semilla...")
    from database.db_manager import (
        init_db, authenticate_user, get_all_clients, get_client_by_id,
        get_assessments_by_client, get_assessment_scores, get_roadmap_by_assessment,
        get_roadmap_initiatives
    )
    init_db()

    # Validar autenticación
    admin = authenticate_user("admin", "admin123")
    assert admin is not None, "Error: Usuario admin no autenticado"
    assert admin["role"] == "admin", "Error: Rol de admin incorrecto"
    print("  -> Autenticación de admin: OK")

    consultant = authenticate_user("consultor", "cobit2019")
    assert consultant is not None, "Error: Usuario consultor no autenticado"
    print("  -> Autenticación de consultor: OK")

    # Validar clientes
    clients = get_all_clients()
    assert len(clients) >= 1, "Error: No se encontraron clientes"
    
    # Buscar el cliente que tiene evaluaciones para el test
    client = None
    assessments = []
    for c in clients:
        assocs = get_assessments_by_client(c["id"])
        if assocs:
            client = c
            assessments = assocs
            break
    if not client:
        client = clients[0]
        create_assessment(client["id"], "Evaluación Test", "comprehensive", "Consultor Test")
        assessments = get_assessments_by_client(client["id"])

    print(f"  -> Cliente de prueba: {client['name']} (NIT: {client['tax_id']}) - OK")

    # 2. Test Catálogo COBIT
    print("\n[2/6] Probando Catálogo COBIT 2019...")
    from engine.cobit_data import DOMAINS, COBIT_PROCESSES, get_all_processes_list
    assert len(DOMAINS) == 5, f"Error: Se esperaban 5 dominios, hay {len(DOMAINS)}"
    assert len(COBIT_PROCESSES) == 40, f"Error: Se esperaban 40 procesos, hay {len(COBIT_PROCESSES)}"
    all_procs = get_all_processes_list()
    assert len(all_procs) == 40, "Error: La función get_all_processes_list() no retornó 40 procesos"
    print("  -> 5 Dominios y 40 Procesos oficiales validados: OK")

    # 3. Test Motor de Madurez e IMO
    print("\n[3/6] Probando Motor de Madurez y Algoritmo IMO [COB-TK08]...")
    from engine.maturity_engine import calculate_assessment_metrics
    active_eval = assessments[0]
    scores = get_assessment_scores(active_eval["id"])
    assert len(scores) >= 18, f"Error: Se esperaban al menos 18 calificaciones, hay {len(scores)}"

    metrics = calculate_assessment_metrics(scores)
    assert 0.0 <= metrics["imo"] <= 5.0, f"Error: IMO fuera de rango: {metrics['imo']}"
    assert metrics["health_score"] >= 0.0, "Error: Health score inválido"
    assert len(metrics["domains"]) == 5, "Error: No se calcularon los 5 dominios"
    assert len(metrics["top_gaps"]) <= 5, "Error: Top gaps excede 5"
    print(f"  -> IMO calculado: {metrics['imo']:.2f} / 5.00 ({metrics['level_label']}) - OK")
    print(f"  -> Salud de Gobernanza: {metrics['health_score']:.1f}% | Riesgo: {metrics['risk_score']:.1f}% - OK")

    # 4. Test Motor de IA y Alineación Estratégica
    print("\n[4/6] Probando Motor de IA y Alineación Estratégica [COB-ST09, COB-ST12, COB-ST13]...")
    from engine.ai_engine import align_business_goals, analyze_npo_text, generate_heuristic_diagnosis

    alignment = align_business_goals("Aumentar ciberseguridad y evitar caídas en banca", "Servicios Financieros")
    assert len(alignment) >= 1, "Error: No se generó alineación estratégica"
    print(f"  -> Alineación generada: {len(alignment)} procesos recomendados - OK")

    sample_doc = "La empresa requiere formalizar la seguridad y los backups diarios debido a constantes fallas operativas y falta de controles en la nube."
    npo = analyze_npo_text(sample_doc)
    assert len(npo["needs"]) >= 1, "Error: No se detectaron necesidades"
    assert len(npo["problems"]) >= 1, "Error: No se detectaron problemas"
    print(f"  -> Análisis NPO: {len(npo['needs'])} necesidades, {len(npo['problems'])} problemas - OK")

    diag = generate_heuristic_diagnosis(client, metrics)
    assert "summary" in diag, "Error: Diagnóstico sin resumen"
    assert len(diag["risks"]) >= 1, "Error: No se generaron riesgos"
    print("  -> Diagnóstico cualitativo y matriz de riesgos generada: OK")

    # 5. Test Generador de Hoja de Ruta (Roadmap)
    print("\n[5/6] Probando Generador de Hoja de Ruta [COB-TK10, COB-ST14]...")
    from engine.roadmap_engine import generate_roadmap_plan
    roadmap_plan = generate_roadmap_plan(scores, client["name"])
    assert roadmap_plan["total_budget"] > 0, "Error: Presupuesto total inválido"
    assert len(roadmap_plan["initiatives"]) >= 3, "Error: Muy pocas iniciativas generadas"
    assert roadmap_plan["quick_wins_count"] >= 1, "Error: No se identificaron Quick Wins"
    print(f"  -> Roadmap generado: {len(roadmap_plan['initiatives'])} iniciativas ({roadmap_plan['quick_wins_count']} Quick Wins) - OK")
    print(f"  -> Presupuesto Total: ${roadmap_plan['total_budget']:,.0f} COP - OK")

    # 6. Test Exportación de Reportes PDF y Excel
    print("\n[6/6] Probando Exportación de Reportes [COB-ST19, COB-ST20]...")
    from engine.export_engine import generate_pdf_report, generate_excel_report

    pdf_data = generate_pdf_report(client, active_eval, metrics, roadmap_plan)
    assert len(pdf_data) > 1000, "Error: PDF generado vacío o demasiado pequeño"
    print(f"  -> Informe Ejecutivo en PDF generado ({len(pdf_data)} bytes): OK")

    excel_data = generate_excel_report(client, active_eval, scores, metrics)
    assert len(excel_data) > 1000, "Error: Archivo Excel generado vacío o demasiado pequeño"
    print(f"  -> Libro de Evaluación Excel generado ({len(excel_data)} bytes): OK")

    print("\n==================================================================")
    print("  >>> TODAS LAS PRUEBAS (6/6) PASARON SATISFACTORIAMENTE AL 100% <<<")
    print("==================================================================")

if __name__ == "__main__":
    test_system()
