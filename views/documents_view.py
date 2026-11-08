"""
Ingesta y Procesamiento Documental con NLP / Heurística [COB-ST08, COB-TK07, COB-ST09].
Carga documentos institucionales, extrae tablas estructuradas (PDF/DOCX),
valida integridad y duplicados mediante SHA-256, gestiona OCR opcional
y ofrece búsqueda indexada de texto completo mediante SQLite FTS5 con BM25.
"""

import streamlit as st
import pandas as pd
from database.db_manager import (
    get_all_clients, save_document, get_documents_by_client,
    get_document_by_id, get_document_by_hash, search_documents_fts
)
from engine.ai_engine import (
    analyze_npo_text, extract_document_content, calculate_content_hash
)
from engine.cobit_data import COBIT_PROCESSES

def show_documents():
    st.title("📄 Ingesta Documental, Tablas y NLP")
    st.markdown("Procesa evidencias documentales con extracción de tablas estructuradas, integridad SHA-256 y búsqueda FTS5.")

    clients = get_all_clients()
    if not clients:
        st.warning("No hay clientes registrados.")
        return

    client_ids = [c["id"] for c in clients]
    client_names = [f"{c['name']} ({c['sector']})" for c in clients]
    curr_c_idx = 0
    if st.session_state.get("active_client_id") in client_ids:
        curr_c_idx = client_ids.index(st.session_state["active_client_id"])

    selected_c_idx = st.selectbox("Empresa para Ingesta Documental:", range(len(clients)), format_func=lambda i: client_names[i], index=curr_c_idx, key="doc_client_picker")
    active_client = clients[selected_c_idx]
    st.session_state["active_client_id"] = active_client["id"]

    tab_upload, tab_search, tab_history = st.tabs([
        "📤 Cargar y Analizar Documento",
        "🔍 Búsqueda FTS5 de Texto Completo",
        "📚 Repositorio de Documentos"
    ])

    # =====================================================================
    # TAB 1: CARGA Y PROCESAMIENTO CON TABLAS Y SHA-256
    # =====================================================================
    with tab_upload:
        st.subheader("Subir Evidencia Documental (PDF, DOCX, TXT)")
        st.caption("Soporta extracción nativa de tablas estructuradas, verificación criptográfica SHA-256 y OCR:")
        
        uploaded_file = st.file_uploader(
            "Selecciona un archivo:",
            type=["txt", "md", "csv", "json", "docx", "pdf"]
        )

        st.markdown("**O pega directamente el texto del informe o política:**")
        manual_text = st.text_area(
            "Texto del Documento de Auditoría o Política:",
            height=130,
            placeholder="Pegar extracto del Plan Estratégico de TI, informe de riesgos, auditoría interna..."
        )

        if st.button("🚀 Extraer Tablas y Analizar NPO (NLP)", type="primary"):
            extracted_text = ""
            filename = "Texto Manual"
            file_type = "text/plain"
            file_size = 0
            file_hash = ""
            extracted_tables = []
            ocr_status = "digital"

            if uploaded_file is not None:
                filename = uploaded_file.name
                file_type = uploaded_file.type or "application/octet-stream"
                file_bytes = uploaded_file.read()
                file_size = len(file_bytes)

                with st.spinner("Procesando documento, extrayendo tablas y calculando hash SHA-256..."):
                    doc_meta = extract_document_content(file_bytes, filename)
                    extracted_text = doc_meta["extracted_text"]
                    extracted_tables = doc_meta["extracted_tables"]
                    file_hash = doc_meta["file_hash"]
                    ocr_status = doc_meta["ocr_status"]

            if manual_text.strip():
                if extracted_text:
                    extracted_text = (extracted_text + "\n\n" + manual_text).strip()
                else:
                    extracted_text = manual_text.strip()
                    file_size = len(extracted_text.encode('utf-8'))
                    file_hash = calculate_content_hash(extracted_text.encode('utf-8'))

            if not extracted_text:
                st.error("Por favor sube un archivo o escribe texto en el campo superior.")
            else:
                # Comprobar si ya existe un documento idéntico mediante SHA-256
                existing_doc = get_document_by_hash(active_client["id"], file_hash) if file_hash else None
                if existing_doc:
                    st.warning(f"⚠️ **Documento duplicado detectado:** Ya existe un archivo registrado con el mismo hash SHA-256 (`{file_hash[:16]}...`). Se guardará como nueva versión.")

                with st.spinner("Ejecutando extracción de lenguaje natural y clasificación NPO..."):
                    npo_result = analyze_npo_text(extracted_text)
                    doc_id = save_document(
                        client_id=active_client["id"],
                        filename=filename,
                        file_type=file_type,
                        file_size=file_size,
                        extracted_text=extracted_text,
                        npo_analysis=npo_result,
                        file_hash=file_hash,
                        extracted_tables=extracted_tables,
                        ocr_status=ocr_status
                    )

                st.success(f"✅ ¡Documento '{filename}' procesado, indexado en FTS5 y archivado exitosamente!")

                # Renderizar métricas e integridad
                st.markdown("---")
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                with col_m1:
                    st.metric("Índice de Urgencia NPO", f"{npo_result.get('urgency_score', 50.0):.1f}%")
                with col_m2:
                    st.metric("Tablas Extraídas", f"{len(extracted_tables)} tablas")
                with col_m3:
                    ocr_label = "Digital Nativa" if ocr_status == "digital" else ("OCR Tesseract" if ocr_status == "ocr_tesseract" else "Sin OCR")
                    st.metric("Capa de Texto", ocr_label)
                with col_m4:
                    st.metric("Procesos Mapeados", f"{len(npo_result.get('suggested_processes', []))} procesos")

                if file_hash:
                    st.caption(f"🛡️ **Firma de Integridad (SHA-256):** `{file_hash}`")

                # =============================================================
                # VISUALIZACIÓN DE TABLAS ESTRUCTURADAS EXTRAÍDAS
                # =============================================================
                if extracted_tables:
                    st.markdown("### 📊 Tablas Estructuradas Extraídas del Documento")
                    st.caption("Estructuras tabulares identificadas y parseadas automáticamente (PDF/DOCX):")
                    for t in extracted_tables:
                        t_title = f"Tabla #{t.get('table_id')}"
                        if t.get("page"):
                            t_title += f" (Página {t['page']})"
                        t_title += f" — {t.get('row_count', 0)} filas x {t.get('col_count', 0)} columnas"
                        
                        with st.expander(f"📑 {t_title}", expanded=True):
                            try:
                                df_table = pd.DataFrame(t.get("rows", []), columns=t.get("headers", []))
                                st.dataframe(df_table, use_container_width=True, hide_index=True)
                            except Exception as ex:
                                st.write("Datos de la tabla:", t.get("rows"))

                # Renderizar resultados NPO
                st.markdown("### 🎯 Resultados del Análisis NPO (Necesidades, Problemas, Oportunidades)")
                if npo_result.get("detected_keywords"):
                    st.markdown("**Conceptos y tecnologías detectadas:** " + " ".join([f"`{k}`" for k in npo_result["detected_keywords"]]))

                c_n, c_p, c_o = st.columns(3)
                with c_n:
                    st.markdown("#### 🎯 Necesidades (N)")
                    for n in npo_result.get("needs", []):
                        st.info(f"• {n}")
                with c_p:
                    st.markdown("#### ⚠️ Problemas (P)")
                    for p in npo_result.get("problems", []):
                        st.error(f"• {p}")
                with c_o:
                    st.markdown("#### 💡 Oportunidades (O)")
                    for o in npo_result.get("opportunities", []):
                        st.success(f"• {o}")

                st.markdown("---")
                st.markdown("#### 🔗 Procesos COBIT 2019 Asociados al Texto:")
                suggested_procs = npo_result.get("suggested_processes", [])
                p_items = []
                for sp in suggested_procs:
                    p_info = COBIT_PROCESSES.get(sp, {})
                    p_items.append({
                        "Código": sp,
                        "Nombre del Proceso": p_info.get("name", sp),
                        "Dominio": p_info.get("domain", "")
                    })
                st.dataframe(pd.DataFrame(p_items), use_container_width=True, hide_index=True)

    # =====================================================================
    # TAB 2: BÚSQUEDA DE TEXTO COMPLETO SQLITE FTS5
    # =====================================================================
    with tab_search:
        st.subheader("🔍 Motor de Búsqueda FTS5 de Texto Completo")
        st.caption("Búsqueda indexada ultra rápida con relevancia BM25 y resaltado contextual de fragmentos (snippets):")

        search_query = st.text_input(
            "Buscar en los documentos del cliente:",
            placeholder="Ej: ciberseguridad, backup, ransomware, continuidad, auditoría, activos...",
            key="fts5_search_query"
        )

        if search_query.strip():
            results = search_documents_fts(active_client["id"], search_query)
            if not results:
                st.info(f"No se encontraron coincidencias para '{search_query}'. Prueba con otros términos o sinónimos.")
            else:
                st.markdown(f"**Se encontraron {len(results)} documentos coincidentes con el término:**")
                for r in results:
                    rank_score = r.get("rank_score", 0.0)
                    with st.expander(f"📄 {r['filename']} — Relevancia BM25: {abs(rank_score):.2f}", expanded=True):
                        st.markdown(f"**Coincidencia Contextual:**", unsafe_allow_html=True)
                        st.markdown(f"> ...{r.get('snippet', '')}...", unsafe_allow_html=True)
                        st.caption(f"Tipo: `{r.get('file_type', 'N/A')}` | Tamaño: `{r.get('file_size', 0)} bytes` | Fecha: `{r.get('created_at', '')[:16]}`")
                        
                        full_doc = get_document_by_id(r["document_id"])
                        if full_doc and full_doc.get("extracted_tables"):
                            st.caption(f"📊 Este documento contiene **{len(full_doc['extracted_tables'])}** tablas estructuradas extraídas.")

    # =====================================================================
    # TAB 3: HISTORIAL Y REPOSITORIO DE DOCUMENTOS
    # =====================================================================
    with tab_history:
        st.subheader("📚 Repositorio de Documentos Guardados")
        docs = get_documents_by_client(active_client["id"])
        if not docs:
            st.info("No se han cargado documentos para esta organización.")
        else:
            for d in docs:
                t_count = len(d.get("extracted_tables", []))
                t_badge = f" | 📊 {t_count} tablas" if t_count > 0 else ""
                with st.expander(f"📄 {d['filename']} — Subido el {d.get('created_at', '')[:16]}{t_badge}"):
                    c_info1, c_info2 = st.columns([2, 1])
                    with c_info1:
                        st.markdown(f"**Tipo:** `{d.get('file_type', 'N/A')}` | **Tamaño:** `{d.get('file_size', 0)} bytes`")
                        if d.get("file_hash"):
                            st.caption(f"🛡️ **Hash SHA-256:** `{d['file_hash']}`")
                        st.caption(f"🔤 **Capa de Texto:** `{d.get('ocr_status', 'digital')}`")
                    with c_info2:
                        if t_count > 0:
                            st.info(f"Contiene {t_count} tablas estructuradas")

                    # Mostrar tablas archivadas si existen
                    if d.get("extracted_tables"):
                        st.markdown("##### 📑 Tablas Extraídas:")
                        for t in d["extracted_tables"]:
                            try:
                                df_t = pd.DataFrame(t.get("rows", []), columns=t.get("headers", []))
                                st.dataframe(df_t, use_container_width=True, hide_index=True)
                            except Exception:
                                pass

                    npo = d.get("npo_analysis")
                    if npo and isinstance(npo, dict):
                        if npo.get("urgency_score"):
                            st.caption(f"⚡ **Índice de Urgencia / Severidad:** {npo.get('urgency_score'):.1f}%")
                        if npo.get("detected_keywords"):
                            st.caption("🔍 **Tecnologías detectadas:** " + " ".join([f"`{k}`" for k in npo["detected_keywords"]]))
                        st.markdown("**Necesidades detectadas:**")
                        for n in npo.get("needs", []):
                            st.markdown(f"- {n}")
                        st.markdown("**Problemas detectados:**")
                        for p in npo.get("problems", []):
                            st.markdown(f"- {p}")
                        st.markdown("**Oportunidades:**")
                        for o in npo.get("opportunities", []):
                            st.markdown(f"- {o}")
