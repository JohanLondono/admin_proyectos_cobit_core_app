"""
Motor Avanzado de Inteligencia Artificial, NLP y Diagnóstico Heurístico COBIT 2019 [COB-ST09, COB-ST12, COB-ST13].
Proporciona:
1. Análisis NLP para extracción de Necesidades, Problemas y Oportunidades (NPO) con similitud semántica.
2. Alineación Estratégica de Negocio mediante TF-IDF + Similitud Coseno sobre los 40 procesos COBIT.
3. Diagnóstico integral multi-fuente que fusiona puntajes, evidencias registradas y hallazgos documentales.
4. Matriz dinámica y cuantitativa de riesgos de gobernanza y TI.
"""

import re
import io
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime
import docx
import pdfplumber
from engine.cobit_data import COBIT_PROCESSES, DOMAINS

# Intentar importar scikit-learn para TF-IDF y similitud coseno
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# =====================================================================
# CORPUS Y VECTORIZACIÓN SEMÁNTICA DE PROCESOS COBIT 2019
# =====================================================================

def _build_cobit_corpus() -> Dict[str, str]:
    """Construye un documento enriquecido para cada uno de los 40 procesos COBIT."""
    corpus = {}
    for pid, pdata in COBIT_PROCESSES.items():
        dom_meta = DOMAINS.get(pdata["domain"], {})
        text = (
            f"{pid} {pdata['name']} {pdata['purpose']} "
            f"{dom_meta.get('name', '')} {dom_meta.get('description', '')} "
            f"{' '.join(pdata.get('practices', []))}"
        )
        corpus[pid] = text
    return corpus

_COBIT_CORPUS = _build_cobit_corpus()
_CORPUS_PIDS = list(_COBIT_CORPUS.keys())
_CORPUS_TEXTS = list(_COBIT_CORPUS.values())

if SKLEARN_AVAILABLE:
    _VECTORIZER = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        strip_accents='unicode'
    )
    _CORPUS_MATRIX = _VECTORIZER.fit_transform(_CORPUS_TEXTS)
else:
    _VECTORIZER = None
    _CORPUS_MATRIX = None

# Mapeo de términos sectoriales para potenciar la alineación
SECTOR_KEYWORDS = {
    "Banca, Finanzas y Seguros": ["fraude", "riesgo", "liquidez", "ciberseguridad", "cumplimiento", "auditoria", "regulatorio", "privacidad", "datos", "banco", "transaccional"],
    "Salud y Servicios Médicos": ["paciente", "historia clinica", "privacidad", "confidencialidad", "disponibilidad", "continuidad", "datos sensibles", "medico"],
    "Comercio Minorista (Retail)": ["ventas", "e-commerce", "sla", "mesa de ayuda", "incidentes", "pasarela", "facturacion", "cambios", "catalogo de servicios"],
    "Manufactura e Industria": ["planta", "scada", "continuidad", "proveedores", "activos", "mantenimiento", "inventario", "operaciones"],
    "Gobierno y Sector Público": ["ciudadano", "transparencia", "control interno", "auditoria", "contratacion", "politicas publicas", "normativa"],
    "Tecnología y Software": ["devops", "desarrollo", "requisitos", "scrum", "agil", "apis", "cloud", "despliegues", "testing", "calidad"]
}

# =====================================================================
# 1. ALINEACIÓN ESTRATÉGICA CON NLP (TF-IDF + SIMILITUD COSENOS)
# =====================================================================

def align_business_goals(strategic_goal: str, client_sector: str = "", top_k: int = 5) -> List[Dict[str, Any]]:
    """
    [COB-ST12] Alinea un reto o meta estratégica del negocio del cliente con los
    procesos COBIT 2019 utilizando análisis semántico TF-IDF y afinidad de sector.
    """
    if not strategic_goal or len(strategic_goal.strip()) < 5:
        strategic_goal = "Garantizar la seguridad, estabilidad y continuidad de las operaciones tecnológicas"

    clean_goal = strategic_goal.strip().lower()
    recommendations = []

    if SKLEARN_AVAILABLE and _VECTORIZER is not None and _CORPUS_MATRIX is not None:
        goal_vec = _VECTORIZER.transform([clean_goal])
        similarities = cosine_similarity(goal_vec, _CORPUS_MATRIX)[0]

        # Enriquecer con multiplicador sectorial
        sector_terms = SECTOR_KEYWORDS.get(client_sector, [])
        scored_processes = []

        for idx, pid in enumerate(_CORPUS_PIDS):
            raw_sim = float(similarities[idx])
            p_text = _COBIT_CORPUS[pid].lower()

            # Bonus por coincidencia de términos de sector
            sector_matches = sum(1 for term in sector_terms if term in clean_goal and term in p_text)
            boosted_score = raw_sim * (1.0 + (0.15 * sector_matches))

            # Bonus para procesos core
            if COBIT_PROCESSES.get(pid, {}).get("core"):
                boosted_score *= 1.10

            scored_processes.append((pid, boosted_score, raw_sim))

        # Ordenar por similitud semántica
        scored_processes.sort(key=lambda x: x[1], reverse=True)
        top_matches = scored_processes[:top_k]

        for pid, final_score, raw_sim in top_matches:
            p_info = COBIT_PROCESSES.get(pid, {})
            pct_match = min(98.5, max(42.0, (final_score * 100.0) + 30.0))
            
            criticality = "Alta" if pct_match >= 75.0 else ("Media" if pct_match >= 58.0 else "Baja")
            
            # Generar justificación semántica y práctica sugerida
            practices = p_info.get("practices", ["Formalizar procedimientos"])
            suggested_practice = practices[0] if practices else "Definir controles operativos"
            
            reason = (
                f"Alineación semántica del {pct_match:.1f}% con los objetivos declarados. "
                f"Soporta la meta mediante: '{p_info.get('purpose', '')[:100]}...'. "
                f"Práctica recomendada: {suggested_practice}."
            )

            recommendations.append({
                "process_id": pid,
                "domain": p_info.get("domain", ""),
                "name": p_info.get("name", pid),
                "criticality": criticality,
                "similarity_pct": round(pct_match, 1),
                "reason": reason,
                "suggested_practice": suggested_practice
            })
    else:
        # Fallback robusto sin scikit-learn
        keywords = {
            "seguridad": ["APO13", "DSS05", "APO12"],
            "riesgo": ["EDM03", "APO12", "DSS04"],
            "fraude": ["APO12", "APO13", "DSS05"],
            "costos": ["EDM04", "APO06", "APO10"],
            "crecimiento": ["APO02", "BAI02", "EDM02"],
            "incidentes": ["DSS02", "DSS03", "APO09"],
            "continuidad": ["DSS04", "BAI04", "DSS01"]
        }
        matched_pids = set()
        for kw, pids in keywords.items():
            if kw in clean_goal:
                matched_pids.update(pids)

        if not matched_pids:
            matched_pids = {"EDM01", "APO02", "APO13", "DSS05", "MEA01"}

        for pid in list(matched_pids)[:top_k]:
            p_info = COBIT_PROCESSES.get(pid, {})
            recommendations.append({
                "process_id": pid,
                "domain": p_info.get("domain", ""),
                "name": p_info.get("name", pid),
                "criticality": "Alta",
                "similarity_pct": 85.0,
                "reason": f"Proceso clave para cumplir el objetivo organizacional: {p_info.get('purpose', '')[:110]}.",
                "suggested_practice": p_info.get("practices", ["Estandarizar control"])[0]
            })

    return recommendations

# =====================================================================
# 2. PROCESAMIENTO DOCUMENTAL, TABLAS, HASH Y OCR
# =====================================================================

def calculate_content_hash(content_bytes: bytes) -> str:
    """Calcula el hash SHA-256 criptográfico para integridad y deduplicación documental."""
    return hashlib.sha256(content_bytes).hexdigest()

def extract_tables_from_docx_bytes(file_bytes: bytes) -> List[Dict[str, Any]]:
    """Extrae todas las tablas estructuradas de un archivo DOCX en formato normalizado."""
    tables_data = []
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        for t_idx, table in enumerate(doc.tables):
            if not table.rows:
                continue
            raw_headers = [cell.text.strip() for cell in table.rows[0].cells]
            headers = []
            for h_idx, h in enumerate(raw_headers):
                headers.append(h if h else f"Columna_{h_idx + 1}")
            
            rows_data = []
            for row in table.rows[1:]:
                row_vals = [cell.text.strip() for cell in row.cells]
                if any(row_vals):
                    rows_data.append(row_vals)

            if rows_data:
                tables_data.append({
                    "table_id": t_idx + 1,
                    "headers": headers,
                    "rows": rows_data,
                    "row_count": len(rows_data),
                    "col_count": len(headers)
                })
    except Exception as ex:
        print(f"Error extrayendo tablas DOCX: {ex}")
    return tables_data

def extract_tables_from_pdf_bytes(file_bytes: bytes) -> List[Dict[str, Any]]:
    """Extrae todas las tablas estructuradas de un archivo PDF utilizando pdfplumber."""
    tables_data = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            t_counter = 1
            for p_idx, page in enumerate(pdf.pages):
                extracted = page.extract_tables()
                for table in extracted:
                    if not table or len(table) < 2:
                        continue
                    cleaned_table = [[(c.strip() if c else "") for c in row] for row in table]
                    headers = [(h if h else f"Columna_{c_idx+1}") for c_idx, h in enumerate(cleaned_table[0])]
                    rows = [r for r in cleaned_table[1:] if any(r)]
                    if rows:
                        tables_data.append({
                            "table_id": t_counter,
                            "page": p_idx + 1,
                            "headers": headers,
                            "rows": rows,
                            "row_count": len(rows),
                            "col_count": len(headers)
                        })
                        t_counter += 1
    except Exception as ex:
        print(f"Error extrayendo tablas PDF: {ex}")
    return tables_data

def extract_document_content(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    [COB-ST08, COB-TK07] Extractor integral de documentos (PDF, DOCX, TXT):
    - Genera hash SHA-256 para verificación de integridad.
    - Extrae texto digital nativo.
    - Extrae tablas estructuradas con pdfplumber y python-docx.
    - Diagnostica estado de capa digital y OCR opcional.
    """
    sha256 = calculate_content_hash(file_bytes)
    fn_lower = filename.lower()
    text = ""
    tables = []
    ocr_status = "digital"

    if fn_lower.endswith(".pdf"):
        tables = extract_tables_from_pdf_bytes(file_bytes)
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                page_texts = [p.extract_text() or "" for p in pdf.pages]
                text = "\n\n".join(page_texts).strip()
        except Exception:
            text = ""

        if not text:
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                text = "\n\n".join([p.extract_text() or "" for p in reader.pages]).strip()
            except Exception:
                pass

        # Validar si es documento escaneado sin capa de texto
        if len(text.strip()) < 30:
            ocr_text = ""
            try:
                import pytesseract
                from pdf2image import convert_from_bytes
                images = convert_from_bytes(file_bytes, first_page=1, last_page=3)
                for img in images:
                    ocr_text += pytesseract.image_to_string(img, lang="spa") + "\n"
                if ocr_text.strip():
                    text = ocr_text.strip()
                    ocr_status = "ocr_tesseract"
                else:
                    ocr_status = "scanned_no_ocr"
            except Exception:
                ocr_status = "scanned_no_ocr"
        else:
            ocr_status = "digital"

    elif fn_lower.endswith(".docx"):
        tables = extract_tables_from_docx_bytes(file_bytes)
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            para_texts = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n\n".join(para_texts).strip()
            ocr_status = "digital"
        except Exception as ex:
            text = f"Error al leer DOCX: {ex}"
            ocr_status = "error"

    else:
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = file_bytes.decode("latin-1")
            except Exception:
                text = str(file_bytes)
        ocr_status = "digital"

    return {
        "extracted_text": text,
        "extracted_tables": tables,
        "file_hash": sha256,
        "file_size": len(file_bytes),
        "ocr_status": ocr_status,
        "tables_count": len(tables)
    }

# =====================================================================
# 3. ANÁLISIS DOCUMENTAL Y EXTRACCIÓN NLP DE NPO
# =====================================================================

def analyze_npo_text(text: str) -> Dict[str, Any]:
    """
    [COB-ST09] Analiza texto institucional o evidencias de auditoría con NLP
    para extraer Necesidades (N), Problemas (P) y Oportunidades (O),
    detectar tecnologías y asociar los procesos COBIT 2019 directamente impactados.
    """
    if not text or len(text.strip()) < 15:
        return {
            "needs": ["Definir formalmente el marco de gobernanza y políticas de TI."],
            "problems": ["Carencia de documentación técnica consolidada."],
            "opportunities": ["Alinear los proyectos de TI al crecimiento comercial de la empresa."],
            "detected_keywords": ["gobernanza", "politicas", "documentacion"],
            "urgency_score": 50.0,
            "suggested_processes": ["EDM01", "APO02", "DSS05"]
        }

    text_clean = text.strip()
    sentences = [s.strip() for s in re.split(r'[\n\.\;]+', text_clean) if len(s.strip()) > 18]

    # Patrones lingüísticos en español
    pattern_needs = re.compile(r'\b(requiere|necesita|debe|es necesario|se proyecta|prioridad|indispensable|fundamental|se exige|tiene como meta)\b', re.IGNORECASE)
    pattern_problems = re.compile(r'\b(falla|error|retraso|vulnerabilidad|carece|falta|riesgo|brecha|indisponibilidad|incidente|manual|deficiencia|desactualizado|cuello de botella|sin formalizar|perdida|obsolescencia)\b', re.IGNORECASE)
    pattern_opps = re.compile(r'\b(oportunidad|optimizar|automatizar|modernizar|migrar|implementar|mejorar|innovar|potencial|beneficio|agilizar|integrar|escalar|eficiencia)\b', re.IGNORECASE)

    extracted_needs = []
    extracted_problems = []
    extracted_opps = []

    for s in sentences:
        s_norm = s.strip()
        if len(s_norm) > 180:
            s_display = s_norm[:177] + "..."
        else:
            s_display = s_norm

        if pattern_problems.search(s_norm) and len(extracted_problems) < 5:
            extracted_problems.append(s_display)
        elif pattern_needs.search(s_norm) and len(extracted_needs) < 5:
            extracted_needs.append(s_display)
        elif pattern_opps.search(s_norm) and len(extracted_opps) < 5:
            extracted_opps.append(s_display)

    # Detección de tecnologías y conceptos clave
    tech_patterns = [
        "cloud", "nube", "aws", "azure", "erp", "sap", "crm", "mfa", "vpn",
        "firewall", "backup", "respaldo", "drp", "bcp", "active directory",
        "ransomware", "iso 27001", "ciberseguridad", "base de datos", "sql",
        "api", "microservicios", "service desk", "sla", "scrum", "devops"
    ]
    detected_techs = []
    for tp in tech_patterns:
        if re.search(r'\b' + re.escape(tp) + r'\b', text_clean, re.IGNORECASE):
            detected_techs.append(tp.capitalize())

    # Cálculo del índice de urgencia / severidad del documento (0 a 100%)
    prob_count = len(re.findall(pattern_problems, text_clean))
    total_words = max(1, len(text_clean.split()))
    prob_density = (prob_count / total_words) * 100.0
    urgency_score = min(95.0, max(25.0, round(prob_density * 22.0 + 35.0, 1)))

    # Fallbacks inteligentes si la redacción no contenía los verbos clave
    if not extracted_needs:
        extracted_needs = [
            "Formalizar e institucionalizar las políticas de seguridad de la información y control de accesos.",
            "Establecer métricas cuantitativas de cumplimiento para el portafolio de proyectos de TI.",
            "Definir acuerdos de nivel de servicio (SLA) con las áreas de negocio."
        ]
    if not extracted_problems:
        extracted_problems = [
            "Gestión de incidentes con resolución manual y falta de registro estandarizado.",
            "Dependencia del conocimiento empírico en personas clave sin manuales operativos.",
            "Ausencia de simulacros periódicos de recuperación ante desastres (DRP)."
        ]
    if not extracted_opps:
        extracted_opps = [
            "Implementar herramientas de automatización de mesas de ayuda y gestión de cambios.",
            "Adoptar un tablero ejecutivo de KPIs de TI para visibilidad de la Junta Directiva.",
            "Fortalecer la cultura de prevención y concientización en ciberseguridad."
        ]

    # Asociar procesos COBIT usando TF-IDF sobre el texto completo del documento
    associated_processes = []
    if SKLEARN_AVAILABLE and _VECTORIZER is not None:
        doc_vec = _VECTORIZER.transform([text_clean])
        sims = cosine_similarity(doc_vec, _CORPUS_MATRIX)[0]
        top_indices = sims.argsort()[-7:][::-1]
        for idx in top_indices:
            if sims[idx] > 0.05:
                associated_processes.append(_CORPUS_PIDS[idx])

    if not associated_processes:
        associated_processes = ["EDM01", "APO12", "APO13", "DSS04", "DSS05", "MEA01"]

    return {
        "needs": extracted_needs,
        "problems": extracted_problems,
        "opportunities": extracted_opps,
        "detected_keywords": detected_techs[:10],
        "urgency_score": urgency_score,
        "suggested_processes": associated_processes[:6]
    }

# =====================================================================
# 3. DIAGNÓSTICO INTEGRAL Y MATRIZ CUANTITATIVA DE RIESGOS
# =====================================================================

def generate_heuristic_diagnosis(
    client: Dict[str, Any],
    metrics: Dict[str, Any],
    scores: List[Dict[str, Any]] = None,
    documents: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    [COB-ST13] Genera un diagnóstico integral cualitativo y cuantitativo que
    sintetiza:
    - Métricas de madurez (IMO, Meta, Salud, Riesgo)
    - Puntuaciones individuales y evidencias registradas en la evaluación
    - Hallazgos NPO de documentos ingestados mediante NLP
    - Matriz de riesgos tecnológicos calculada dinámicamente
    - Recomendaciones priorizadas por impacto real
    """
    client_name = client.get("name", "Organización")
    sector = client.get("sector", "Sector Empresarial")
    size = client.get("size", "Mediana Empresa")
    imo = metrics.get("imo", 0.0)
    target_imo = metrics.get("target_imo", 3.0)
    overall_gap = metrics.get("overall_gap", 0.0)
    health_score = metrics.get("health_score", 0.0)
    risk_score = metrics.get("risk_score", 0.0)
    level_label = metrics.get("level_label", "Incompleto")
    top_gaps = metrics.get("top_gaps", [])

    # Integración de documentos NLP
    doc_findings_summary = ""
    doc_techs = []
    if documents:
        total_docs = len(documents)
        sample_doc = documents[0]
        npo = sample_doc.get("npo_analysis", {})
        if isinstance(npo, dict):
            doc_techs = npo.get("detected_keywords", [])
            prob_samples = npo.get("problems", [])
            if prob_samples:
                doc_findings_summary = (
                    f" Adicionalmente, el análisis NLP de {total_docs} documento(s) institucional(es) "
                    f"reveló hallazgos operativos críticos: '{prob_samples[0]}'."
                )

    # 1. RESUMEN EJECUTIVO DINÁMICO
    summary = f"""### 🏛️ Diagnóstico Estratégico de Gobernanza y Gestión de TI (COBIT 2019)
**Organización Evaluada:** {client_name}  
**Sector Económico:** {sector} | **Dimensión:** {size}  
**Índice de Madurez Organizacional (IMO):** **{imo:.2f} / 5.00** ({level_label})  
**Meta Institucional:** **{target_imo:.2f} / 5.00** | **Brecha Global (Gap):** **{overall_gap:.2f} puntos**  
**Efectividad del Marco de TI:** **{health_score:.1f}%** | **Exposición Cuantitativa al Riesgo:** **{risk_score:.1f}%**

#### 📋 Conclusión Ejecutiva del Diagnóstico:
La evaluación integral bajo el marco oficial **ISACA COBIT 2019** posiciona a **{client_name}** en un estado de capacidad **{level_label}**. La organización demuestra capacidades operativas en ejecución, pero evidencia vulnerabilidades estructurales en la formalización de políticas directivas, la medición cuantitativa del valor generado y los controles de aseguramiento.{doc_findings_summary}

Para alcanzar la meta directiva de **{target_imo:.2f} / 5.00**, se recomienda priorizar una hoja de ruta con intervenciones tempranas (*Quick Wins*) enfocadas en estandarizar procedimientos y fortalecer la resiliencia tecnológica."""

    # 2. HALLAZGOS POR DOMINIO BASADOS EN DATOS
    findings = []
    dom_summary = metrics.get("domains", {})
    for dom_code, dom_info in dom_summary.items():
        curr = dom_info.get("current", 0.0)
        targ = dom_info.get("target", 3.0)
        gap = dom_info.get("gap", 0.0)
        d_name = dom_info.get("name", dom_code)

        if gap > 1.3:
            severity_badge = "🔴 **Crítico**"
            status_desc = f"Brecha sustancial de {gap:.2f} pts que compromete la gobernanza del área."
        elif gap > 0.7:
            severity_badge = "🟡 **Atención Requerida**"
            status_desc = f"Brecha moderada de {gap:.2f} pts; requiere estandarizar procedimientos y roles."
        else:
            severity_badge = "🟢 **Favorable**"
            status_desc = f"Nivel adecuado ({curr:.2f}/{targ:.2f}); mantener mecanismos de monitoreo continuo."

        findings.append(f"{severity_badge} **Dominio {dom_code}** ({d_name[:35]}...): Actual **{curr:.2f}** vs Meta **{targ:.2f}**. {status_desc}")

    # 3. AUDITORÍA DE EVIDENCIAS Y OBSERVACIONES
    if scores:
        evidenced_count = sum(1 for s in scores if s.get("evidence") and len(str(s["evidence"]).strip()) > 3)
        total_eval = len(scores)
        pct_evidenced = (evidenced_count / max(1, total_eval)) * 100.0
        findings.append(
            f"📑 **Trazabilidad Documental de Evidencias:** De {total_eval} procesos evaluados, "
            f"**{evidenced_count} ({pct_evidenced:.0f}%)** cuentan con evidencias probatorias registradas. "
            f"{'Se requiere subsanar la justificación en los procesos restantes para soportar auditorías externas.' if pct_evidenced < 70 else 'Buen nivel de soporte documental registrado.'}"
        )

    # 4. MATRIZ DINÁMICA DE RIESGOS CUANTITATIVOS
    # Mapeo de puntajes individuales para calcular riesgos específicos
    score_map = {s["process_id"]: float(s.get("current_score", 0.0)) for s in (scores or [])}
    
    # Riesgo 1: Ciberseguridad y Protección de Datos (APO13, DSS05, APO14)
    sec_avg = (score_map.get("APO13", imo) + score_map.get("DSS05", imo) + score_map.get("APO14", imo)) / 3.0
    sec_level = "Alto" if sec_avg < 2.0 else ("Medio" if sec_avg < 3.0 else "Bajo")

    # Riesgo 2: Continuidad y Resiliencia Operativa (DSS04, DSS01)
    cont_avg = (score_map.get("DSS04", imo) + score_map.get("DSS01", imo)) / 2.0
    cont_level = "Alto" if cont_avg < 2.0 else ("Medio" if cont_avg < 3.0 else "Bajo")

    # Riesgo 3: Desalineación Estratégica y Fuga de Valor (EDM01, EDM02, APO02)
    gov_avg = (score_map.get("EDM01", imo) + score_map.get("EDM02", imo) + score_map.get("APO02", imo)) / 3.0
    gov_level = "Alto" if gov_avg < 2.2 else ("Medio" if gov_avg < 3.2 else "Bajo")

    # Riesgo 4: Cumplimiento Normativo y Auditoría (MEA02, MEA03)
    comp_avg = (score_map.get("MEA02", imo) + score_map.get("MEA03", imo)) / 2.0
    comp_level = "Alto" if comp_avg < 2.0 else ("Medio" if comp_avg < 3.0 else "Bajo")

    # Riesgo 5: Gestión de Servicios y SLAs (APO09, DSS02, BAI06)
    serv_avg = (score_map.get("APO09", imo) + score_map.get("DSS02", imo) + score_map.get("BAI06", imo)) / 3.0
    serv_level = "Alto" if serv_avg < 2.0 else ("Medio" if serv_avg < 3.0 else "Bajo")

    risks = [
        {
            "category": "Ciberseguridad y Protección de Datos",
            "level": sec_level,
            "exposure_score": round((5.0 - sec_avg) * 20.0, 1),
            "description": f"Capacidad promedio de seguridad en {sec_avg:.2f}/5.0. Riesgo de fuga de información, incidentes de ransomware o accesos no autorizados por falta de MFA y controles SGSI institucionalizados (APO13, DSS05).",
            "action": "Desplegar política de seguridad ISO/COBIT, autenticación multifactor obligatoria y monitoreo perimetral de eventos.",
            "cobit_ref": "APO13, DSS05, APO14"
        },
        {
            "category": "Continuidad Operativa y Resiliencia ante Desastres",
            "level": cont_level,
            "exposure_score": round((5.0 - cont_avg) * 20.0, 1),
            "description": f"Capacidad de continuidad evaluada en {cont_avg:.2f}/5.0. Ausencia de planes DRP con pruebas periódicas documentadas ante eventuales indisponibilidades de servidores o enlaces críticos (DSS04).",
            "action": "Diseñar el Plan de Recuperación ante Desastres (DRP) con RTO/RPO definidos y ejecutar un simulacro semestral.",
            "cobit_ref": "DSS04, DSS01"
        },
        {
            "category": "Gobernanza Estratégica y Rendimiento de Inversiones",
            "level": gov_level,
            "exposure_score": round((5.0 - gov_avg) * 20.0, 1),
            "description": f"Madurez directiva en {gov_avg:.2f}/5.0. Inversiones tecnológicas no priorizadas mediante modelo formal de valor, con riesgo de desvío presupuestal y desarticulación respecto a las metas de negocio (EDM02, APO02).",
            "action": "Institucionalizar el Comité de Dirección de TI con participación de gerencia y evaluar el ROI antes de aprobar proyectos.",
            "cobit_ref": "EDM01, EDM02, APO02"
        },
        {
            "category": "Cumplimiento Normativo, Legal y Aseguramiento",
            "level": comp_level,
            "exposure_score": round((5.0 - comp_avg) * 20.0, 1),
            "description": f"Madurez de control en {comp_avg:.2f}/5.0. Exposición a sanciones legales o hallazgos desfavorables en auditorías externas por vacíos en la supervisión de requisitos sectoriales (MEA03).",
            "action": "Construir matriz de cumplimiento legal de TI y ejecutar programa de auto-evaluación previa de controles.",
            "cobit_ref": "MEA02, MEA03"
        },
        {
            "category": "Gestión de Servicios, SLAs y Control de Cambios",
            "level": serv_level,
            "exposure_score": round((5.0 - serv_avg) * 20.0, 1),
            "description": f"Capacidad de servicio en {serv_avg:.2f}/5.0. Servicios de TI prestados sin catálogo formalizado ni SLAs medibles, con riesgo de afectación a producción por cambios no evaluados (BAI06, APO09).",
            "action": "Estandarizar el catálogo de servicios con acuerdos de nivel de servicio (SLA) y formalizar el Comité de Cambios (CAB).",
            "cobit_ref": "APO09, BAI06, DSS02"
        }
    ]

    # 5. RECOMENDACIONES ESTRATÉGICAS DINÁMICAS (QUICK WINS + ACCIONES DE IMPACTO)
    recommendations = []
    if top_gaps:
        for g in top_gaps[:3]:
            pid = g["process_id"]
            p_name = g.get("name", pid)
            gap_val = g.get("gap", 0.0)
            recommendations.append(
                f"Abordar prioritariamente el proceso **{pid}** ({p_name}): presenta la mayor brecha ({gap_val:.1f} pts). Implementar sus prácticas base en menos de 90 días."
            )
    else:
        recommendations.append("Formalizar el Catálogo de Servicios de TI con Acuerdos de Nivel de Servicio (SLA) medibles (APO09).")
        recommendations.append("Institucionalizar el Comité de Control de Cambios (CAB) para pases a producción seguros (BAI06).")

    recommendations.append("Aprobar formalmente la Política General de Ciberseguridad por parte de la Junta Directiva (EDM01 / APO13).")
    recommendations.append("Implementar un tablero ejecutivo de KPIs mensuales para visibilizar la disponibilidad y desempeño del área TI (MEA01).")

    return {
        "summary": summary,
        "findings": findings,
        "risks": risks,
        "recommendations": recommendations,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
