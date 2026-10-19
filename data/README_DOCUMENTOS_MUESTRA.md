# 📁 DOCUMENTOS DE PRUEBA REALES PARA INGESTA Y NLP (COBIT 2019)

Esta carpeta contiene dos escenarios corporativos reales y complementarios generados en formatos oficiales (**PDF** y **Word .docx**), listos para ser procesados por el módulo **"📄 Ingesta Documental y Análisis NPO"** de la aplicación:

---

## 🏥 Escenario 1 (Formato PDF): Sector Salud y Hospitalario
- **Archivo:** `Auditoria_Ciberseguridad_y_Continuidad_Hospital_San_Rafael.pdf`
- **Versión de texto plano:** `Auditoria_Ciberseguridad_Hospital_San_Rafael.txt`
- **Entidad:** Hospital Universitario San Rafael E.S.E.
- **Perspectiva y Situación Analizada:**
  - Auditoría técnica centrada en **Ciberseguridad, Continuidad Operacional y Cumplimiento Regulatorio** (Circular 007 de Supersalud y Ley de Protección de Datos Personales).
  - Ausencia de autenticación multifactor (MFA) para médicos y personal asistencial.
  - Vulnerabilidad ante ataques de *ransomware* y secuestro de historias clínicas electrónicas.
  - Copias de seguridad (*backups*) almacenadas sin pruebas de restauración y sin centro de contingencia alterno.
  - Inexistencia de un Plan de Recuperación ante Desastres (*DRP*) para salas de cirugía y urgencias.
  - Retrasos severos en la mesa de ayuda afectando la dispensación de medicamentos.
- **Procesos COBIT 2019 que activa el motor:**
  - `APO13` (Gestionar la Seguridad)
  - `DSS05` (Servicios de Seguridad Operativa)
  - `DSS04` (Gestionar la Continuidad / DRP)
  - `DSS02` (Gestionar Incidentes de Servicio / Mesa de Ayuda)
  - `MEA03` (Conformidad con Requisitos Externos / Supersalud)

---

## 🚛 Escenario 2 (Formato Word DOCX): Sector Logística y Cadena de Suministro
- **Archivo:** `Plan_Estrategico_Gobernanza_TI_Logistica_Andina.docx`
- **Versión de texto plano:** `Plan_Gobernanza_TI_Logistica_Andina.txt`
- **Entidad:** Logística y Carga Andina S.A.S.
- **Perspectiva y Situación Analizada:**
  - Diagnóstico preliminar de **Gobernanza Corporativa de TI, Gestión de Cambios y Control de Proveedores**.
  - Inexistencia de un Comité Directivo de Gobernanza de TI formal (decisiones reactivas sin cálculo de ROI).
  - Caídas frecuentes en la plataforma de tracking satelital (GPS) por pasos a producción sin aprobación del comité CAB (*Change Advisory Board*).
  - Problemas contractuales y ausencia de Acuerdos de Nivel de Servicio (*SLAs*) con el proveedor del software de almacenes (WMS).
  - Descontrol en el inventario de activos tecnológicos y licenciamiento de software en terminales de transporte.
  - Oportunidad de transformación digital mediante analítica avanzada de telemetría y portal web B2B para clientes corporativos.
- **Procesos COBIT 2019 que activa el motor:**
  - `EDM01` (Asegurar el Marco de Gobernanza de TI)
  - `APO02` (Gestionar la Estrategia / PETI)
  - `APO09` (Gestionar los Acuerdos de Servicio / SLA)
  - `APO10` (Gestionar los Proveedores y Terceros)
  - `BAI06` (Gestionar los Cambios de TI / CAB)
  - `BAI09` (Gestionar los Activos de TI)
  - `APO14` (Gestionar los Datos de Telemetría)

---

## 🚀 ¿Cómo probarlos en la aplicación?

1. En la aplicación web Streamlit (`http://localhost:8501`), ve al menú lateral y entra en **"📄 Ingesta Documental (NLP)"**.
2. En la sección **"Subir Evidencia Documental"**, haz clic en **Browse files** (Explorar archivos).
3. Navega hasta esta carpeta:
   `cobit_core_app/data/`
4. Selecciona cualquiera de los dos archivos:
   - `Auditoria_Ciberseguridad_y_Continuidad_Hospital_San_Rafael.pdf`
   - `Plan_Estrategico_Gobernanza_TI_Logistica_Andina.docx`
5. Presiona el botón azul **"🚀 Extraer y Analizar NPO (NLP)"**.
6. Observa cómo el sistema:
   - Extrae el texto completo en milisegundos.
   - Clasifica los hallazgos en las 3 columnas: **Necesidades (N)**, **Problemas (P)** y **Oportunidades (O)**.
   - Identifica y lista los **procesos COBIT 2019 sugeridos** que deben evaluarse en la consultoría.
   - Almacena el documento en la base de datos SQLite para consulta histórica.
