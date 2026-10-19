"""
Ingesta y Procesamiento Documental con NLP / Heurística [COB-ST08, COB-TK07, COB-ST09].
Carga documentos institucionales y extrae automáticamente Necesidades, Problemas y Oportunidades (NPO).
"""

import streamlit as st
import pandas as pd
from database.db_manager import (
    get_all_clients, save_document, get_documents_by_client, get_document_by_id
)
from engine.ai_engine import analyze_npo_text
from engine.cobit_data import COBIT_PROCESSES

def show_documents():
    st.title("📄 Ingesta Documental y Análisis NPO")
    st.markdown("Procesa evidencias documentales (Planes de TI, Auditorías, Políticas) para alimentar el diagnóstico.")

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

    tab_upload, tab_history = st.tabs(["📤 Cargar y Analizar Documento", "📚 Repositorio de Documentos"])

    # TAB 1: CARGA Y PROCESAMIENTO
    with tab_upload:
        st.subheader("Subir Evidencia Documental")
        uploaded_file = st.file_uploader(
            "Selecciona un archivo (Formatos soportados: TXT, Markdown, DOCX, PDF):",
            type=["txt", "md", "csv", "json", "docx", "pdf"]
        )

        st.markdown("**O pega directamente el texto del informe o política:**")
        manual_text = st.text_area(
            "Texto del Documento de Auditoría o Política:",
            height=140,
            placeholder="Pegar extracto del Plan Estratégico de TI, informe de riesgos, auditoría interna..."
        )

        if st.button("🚀 Extraer y Analizar NPO (NLP)", type="primary"):
            extracted_text = ""
            filename = "Texto Manual"
            file_type = "text/plain"
            file_size = 0

            if uploaded_file is not None:
                filename = uploaded_file.name
                file_type = uploaded_file.type
                file_size = uploaded_file.size
                try:
                    if filename.lower().endswith(".pdf"):
                        import io
                        import pypdf
                        reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
                        extracted_text = "\n".join([page.extract_text() or "" for page in reader.pages]).strip()
                    elif filename.lower().endswith(".docx"):
                        import io
                        import docx
                        doc_obj = docx.Document(io.BytesIO(uploaded_file.read()))
                        extracted_text = "\n".join([p.text for p in doc_obj.paragraphs if p.text.strip()]).strip()
                    else:
                        extracted_text = uploaded_file.read().decode("utf-8", errors="ignore")
                except Exception as ex:
                    extracted_text = f"Error al extraer texto de {filename}: {str(ex)}"

            if manual_text.strip():
                extracted_text = (extracted_text + "\n\n" + manual_text).strip()
                if filename == "Texto Manual":
                    file_size = len(extracted_text.encode('utf-8'))

            if not extracted_text:
                st.error("Por favor sube un archivo o escribe texto en el campo superior.")
            else:
                with st.spinner("Ejecutando extracción de lenguaje natural y detección NPO..."):
                    npo_result = analyze_npo_text(extracted_text)
                    doc_id = save_document(
                        client_id=active_client["id"],
                        filename=filename,
                        file_type=file_type,
                        file_size=file_size,
                        extracted_text=extracted_text,
                        npo_analysis=npo_result
                    )

                st.success(f"✅ ¡Documento '{filename}' procesado y archivado exitosamente!")

                # Renderizar resultados NPO
                st.markdown("### 📊 Resultados del Análisis NPO (Necesidades, Problemas, Oportunidades)")
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

    # TAB 2: HISTORIAL DE DOCUMENTOS
    with tab_history:
        st.subheader("📚 Documentos Guardados para este Cliente")
        docs = get_documents_by_client(active_client["id"])
        if not docs:
            st.info("No se han cargado documentos para esta organización.")
        else:
            for d in docs:
                with st.expander(f"📄 {d['filename']} — Subido el {d.get('created_at', '')[:16]}"):
                    st.markdown(f"**Tipo:** `{d.get('file_type', 'N/A')}` | **Tamaño:** `{d.get('file_size', 0)} bytes`")
                    npo = d.get("npo_analysis")
                    if npo and isinstance(npo, dict):
                        st.markdown("**Necesidades detectadas:**")
                        for n in npo.get("needs", []):
                            st.markdown(f"- {n}")
                        st.markdown("**Problemas detectados:**")
                        for p in npo.get("problems", []):
                            st.markdown(f"- {p}")
                        st.markdown("**Oportunidades:**")
                        for o in npo.get("opportunities", []):
                            st.markdown(f"- {o}")
