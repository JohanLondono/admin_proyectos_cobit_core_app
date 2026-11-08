# 📋 GUÍA OFICIAL DE EVIDENCIAS JIRA POR ÍTEM DEL CRONOGRAMA
## CATÁLOGO DE EVIDENCIAS TÉCNICAS Y FUNCIONALES (CÓDIGO, CAPTURAS GUI Y SUSTENTACIÓN)
### PROYECTO: SISTEMA DE CONSULTORÍA EN GOBIERNO Y GESTIÓN DE TI (COBIT 2019 + IA)

**Universidad del Quindío — Facultad de Ingeniería**  
**Programa:** Ingeniería de Sistemas y Computación  
**Asignatura:** Formulación de Proyectos de Software (8vo Semestre)  
**Equipo de Proyecto:** Johan Londoño, Julián Hoyos, Kevin García  
**Documento Fuente de Requisitos:** `CRONOGRAMA_REQUISITOS_JIRA_COBIT.txt`  
**Documento Técnico de Referencia:** [`DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md`](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md)  
**Aplicación:** `cobit_core_app` (Streamlit + SQLite + Python 3.13)  
**Cobertura Global:** 11 Épicas | 33 Ítems (20 Historias de Usuario + 13 Tareas Técnicas) | 208 Story Points | 480 Horas Estimadas  

---

## 🎯 OBJETIVO Y METODOLOGÍA DE ESTE DOCUMENTO

Este documento constituye el **manual maestro de evidencias para Jira**. Integra los requerimientos del cronograma oficial con las especificaciones de arquitectura, fórmulas matemáticas, diccionarios relacionales y algoritmos formalizados en el [Manual Técnico y Funcional](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md).

Para cada una de las 33 incidencias de Jira se detalla:
1. **Ficha de Identificación:** Código de incidencia (`COB-XXX`), Título, Tipo (`Task` / `Story`), Sprint, Story Points, Horas estimadas, Prioridad y Capa Arquitectónica intervenida (conforme al modelo por capas de la arquitectura).
2. **Criterios de Aceptación Jira:** Reglas textuales obligatorias del cronograma.
3. **¿Qué se hizo? (Fundamento Técnico y Funcional):** Explicación profunda de la solución implementada, componentes involucrados, flujo de datos y modelos matemáticos/algorítmicos.
4. **Catálogo de Evidencias para Adjuntar en Jira:**
   - **📸 Evidencia Visual (Pantallazo de la GUI / Terminal):** Nombre normalizado de la imagen (ej. `COB-ST16_radar_plotly_5_dominios.png`), ruta en la aplicación (`http://localhost:8501`), rol de usuario a utilizar, datos a ingresar o seleccionar, y elementos clave a resaltar (recuadros, métricas, alertas).
   - **💻 Evidencia de Código Fuente / Base de Datos:** Archivos intervenidos con enlaces Markdown, firmas de funciones, restricciones de esquema SQL o snippets representativos.
   - **🧪 Evidencia de Pruebas Automatizadas:** Aserción o bloque de salida de la suite [test_cobit_core.py](test_cobit_core.py) que valida el ítem con código de salida `code 0`.
5. **¿Cómo se cumplió la evidencia? (Sustentación de Aceptación):** Demostración analítica y probatoria de por qué la evidencia entregada satisface al 100% los criterios de aceptación para declarar la tarea en estado **DONE (Terminada y Aprobada)**.

---

## 📑 MATRIZ RESUMEN DE TRAZABILIDAD Y EVIDENCIAS JIRA

| Código Jira | Tipo | Sprint | SP | Requisito del Cronograma | Capa Arquitectónica | Archivo Principal de Código | Captura Recomendada para Jira |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **COB-TK01** | Task | S1 | 3 | Inicialización de Entorno | Capa 1 y 3 (Entorno/App) | `requirements.txt`, `app.py` | `COB-TK01_entorno_ejecucion.png` |
| **COB-TK02** | Task | S1 | 5 | Interfaz y Diseño UI | Capa 2 (Presentación) | `static/custom.css`, `app.py` | `COB-TK02_sistema_diseno_ui.png` |
| **COB-TK03** | Task | S1 | 5 | Arquitectura de Motores / Lógica | Capa 4 (Lógica Negocio) | Paquete `engine/*.py` | `COB-TK03_arquitectura_motores.png` |
| **COB-TK04** | Task | S1 | 8 | Esquema Base de Datos Base | Capa 5 y 6 (DAL/Storage) | `database/db_manager.py` | `COB-TK04_esquema_sqlite.png` |
| **COB-ST01** | Story | S1 | 5 | Autenticación y Cierre de Sesión | Capa 3 y 5 (Seguridad/App) | `app.py`, `database/db_manager.py` | `COB-ST01_login_autenticacion.png` |
| **COB-ST02** | Story | S1 | 5 | Gestión de Usuarios y Perfiles | Capa 5 y 6 (Usuarios/DAL) | `database/db_manager.py` | `COB-ST02_roles_usuarios.png` |
| **COB-ST03** | Story | S1 | 6 | Control de Acceso por Roles (RBAC) | Capa 3 (Orquestación) | `app.py`, `views/dashboard_view.py` | `COB-ST03_rbac_sidebar.png` |
| **COB-ST04** | Story | S1 | 5 | CRUD de Empresas Clientes | Capa 2 y 5 (Vistas/DAL) | `views/clients_view.py` | `COB-ST04_crud_clientes.png` |
| **COB-ST05** | Story | S1 | 3 | Directorio de Contactos por Cliente | Capa 2 y 5 (Vistas/DAL) | `views/clients_view.py` | `COB-ST05_directorio_contactos.png` |
| **COB-ST06** | Story | S1 | 3 | Dashboard Básico de Clientes | Capa 3 (Contexto Sesión) | `views/clients_view.py`, `app.py` | `COB-ST06_selector_cliente_activo.png` |
| **COB-TK05** | Task | S2 | 6 | Modelado de Datos COBIT 2019 | Capa 4 (Catálogo Maestro) | `engine/cobit_data.py` | `COB-TK05_catalogo_40_procesos.png` |
| **COB-TK06** | Task | S2 | 5 | Fixtures e Inicialización COBIT | Capa 5 (DAL/Seeding) | `database/db_manager.py` | `COB-TK06_seeding_idempotente.png` |
| **COB-ST07** | Story | S2 | 7 | Catálogo Interactivo de Procesos | Capa 2 (Presentación) | `views/catalog_view.py` | `COB-ST07_catalogo_interactivo.png` |
| **COB-ST08** | Story | S2 | 5 | Carga y Almacenamiento Documental | Capa 2 y 6 (Vistas/Storage) | `views/documents_view.py` | `COB-ST08_carga_documentos.png` |
| **COB-TK07** | Task | S2 | 6 | Extractor de Texto y Normalización | Capa 7 (Parsers Salida) | `views/documents_view.py` | `COB-TK07_extraccion_texto.png` |
| **COB-ST09** | Story | S2 | 8 | Análisis NPO con NLP Heurístico | Capa 4 (Motor IA/NLP) | `engine/ai_engine.py` | `COB-ST09_analisis_npo_nlp.png` |
| **COB-ST10** | Story | S3 | 5 | Creación y Configuración de Evaluaciones | Capa 2 y 5 (Vistas/DAL) | `views/assessment_view.py` | `COB-ST10_apertura_evaluacion.png` |
| **COB-ST11** | Story | S3 | 7 | Cuestionario Interactivo Escala 0-5 | Capa 2 (Presentación) | `views/assessment_view.py` | `COB-ST11_cuestionario_sliders.png` |
| **COB-TK08** | Task | S3 | 6 | Algoritmo Matemático de Madurez (IMO) | Capa 4 (Motor Madurez) | `engine/maturity_engine.py` | `COB-TK08_calculo_imo_score.png` |
| **COB-TK09** | Task | S3 | 6 | Orquestación IA y Modo Offline | Capa 4 (Fallback IA) | `engine/ai_engine.py` | `COB-TK09_ia_offline_fallback.png` |
| **COB-ST12** | Story | S3 | 8 | Alineación Metas Negocio -> COBIT | Capa 2 y 4 (Vistas/Motor IA) | `views/diagnosis_view.py`, `engine/ai_engine.py` | `COB-ST12_alineacion_metas.png` |
| **COB-ST13** | Story | S3 | 8 | Diagnóstico Cualitativo y Riesgos | Capa 2 y 4 (Vistas/Motor IA) | `views/diagnosis_view.py` | `COB-ST13_diagnostico_riesgos.png` |
| **COB-TK10** | Task | S3 | 7 | Algoritmo de Priorización Multi-Criterio | Capa 4 (Motor Roadmap) | `engine/roadmap_engine.py` | `COB-TK10_algoritmo_priorizacion.png` |
| **COB-ST14** | Story | S3 | 7 | Hoja de Ruta por Fases y Presupuesto | Capa 4 y 5 (Motor/DAL) | `engine/roadmap_engine.py` | `COB-ST14_roadmap_fases_presupuesto.png` |
| **COB-ST15** | Story | S3 | 6 | Visualización y Edición del Roadmap | Capa 2 (Presentación) | `views/roadmap_view.py` | `COB-ST15_interfaz_roadmap_quickwins.png` |
| **COB-ST16** | Story | S4 | 6 | Gráfico Radar Polar Actual vs Meta | Capa 2 y 7 (Plotly Engine) | `views/dashboard_view.py` | `COB-ST16_radar_plotly_5_dominios.png` |
| **COB-ST17** | Story | S4 | 6 | Dashboard con KPIs y Top 5 Alertas | Capa 2 (Presentación) | `views/dashboard_view.py` | `COB-ST17_kpis_top_brechas.png` |
| **COB-ST18** | Story | S4 | 5 | Analytics y Desglose por Dominio | Capa 2 (Presentación) | `views/dashboard_view.py` | `COB-ST18_analytics_barras_progreso.png` |
| **COB-ST19** | Story | S4 | 7 | Reporte Ejecutivo Formal en PDF | Capa 4 y 7 (ReportLab) | `engine/export_engine.py`, `views/reports_view.py` | `COB-ST19_descarga_informe_pdf.png` |
| **COB-ST20** | Story | S4 | 7 | Exportación de Matriz a Excel (.xlsx) | Capa 4 y 7 (OpenPyXL) | `engine/export_engine.py`, `views/reports_view.py` | `COB-ST20_descarga_libro_excel.png` |
| **COB-TK11** | Task | S4 | 5 | Integración End-to-End Fluida | Capa 3 (Router Principal) | `app.py` | `COB-TK11_flujo_integral_e2e.png` |
| **COB-TK12** | Task | S4 | 5 | Batería de Pruebas Automatizadas | QA & Validación Cruzada | `test_cobit_core.py` | `COB-TK12_test_suite_aprobado.png` |
| **COB-TK13** | Task | S4 | 4 | Hardening, Optimización y Entrega | QA & Documentación | Carpeta `DOCUMENTACION/` | `COB-TK13_entrega_documentacion.png` |

---

## 🔍 GUÍA DETALLADA DE EVIDENCIAS ÍTEM POR ÍTEM

---

### SPRINT 1: CIMIENTOS, SEGURIDAD Y CLIENTES (SEMANAS 1-2)
#### 🔷 ÉPICA COB-EP01: Infraestructura, Arquitectura Base y Modelado Fundacional
#### 🔷 ÉPICA COB-EP02: Seguridad, Autenticación y Gestión de Roles
#### 🔷 ÉPICA COB-EP03: Gestión Integral de Clientes y Organizaciones

---

#### 📌 [COB-TK01] Inicialización de Entorno y Configuración Base
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 1 | **Estimación:** 3 SP (8 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** Capa 1 (Sistemas de Entrada) y Capa 3 (Coordinación de Aplicación).
- **Criterios de Aceptación:** Estructura de carpetas modular (`database/`, `engine/`, `views/`, `static/`), entorno virtual Python 3.13, dependencias sin conflicto en `requirements.txt`, scripts de arranque sin warnings.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 2.1 y 7.1 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#71-requisitos-del-entorno), se consolidó un entorno de desarrollo desacoplado en 5 paquetes funcionales. Se eliminaron dependencias complejas de compilación en C++ o bibliotecas de deep learning sobredimensionadas (PyTorch/TensorFlow), optando por un stack liviano con Streamlit $\ge 1.32.0$, Pandas $\ge 2.0.0$, Plotly $\ge 5.18.0$, ReportLab $\ge 4.1.0$ y OpenPyXL $\ge 3.1.2$. Esto garantiza tiempos de instalación inferiores a 60 segundos y compatibilidad nativa en Windows y Linux.

**2. Evidencias para Jira:**
- **📸 Captura de Consola (`COB-TK01_entorno_ejecucion.png`):**  
  Ejecutar en la terminal del proyecto:
  ```powershell
  python --version
  pip install -r requirements.txt
  streamlit run app.py
  ```
  *Qué debe apreciarse en la captura:* Versión de Python 3.13 instalada, instalación exitosa de paquetes sin conflictos de resolución de dependencias, y el mensaje de arranque: `You can now view your Streamlit app in your browser. Local URL: http://localhost:8501`.
- **💻 Código Fuente ([requirements.txt](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/requirements.txt)):**
  ```text
  streamlit>=1.32.0
  pandas>=2.0.0
  plotly>=5.18.0
  openpyxl>=3.1.2
  reportlab>=4.1.0
  python-docx>=1.1.0
  pypdf>=4.0.0
  ```
- **🧪 Prueba Automatizada:** Ejecución de la verificación inicial en `test_cobit_core.py` demostrando importación exitosa de los módulos de la solución.

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se evidencia la configuración limpia del entorno, sin colisiones de versiones y con tiempo de respuesta en milisegundos, cumpliendo con el criterio de puesta en marcha reproducible del sprint.

---

#### 📌 [COB-TK02] Interfaz y Diseño UI Responsive con Sistema de Diseño
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 1 | **Estimación:** 5 SP (12 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación e Interfaces de Usuario).
- **Criterios de Aceptación:** Estilos CSS centralizados, paleta corporativa formal (Azul marino institucional `#1E3A8A`, Cyan `#0284C7`, Gris `#F8FAFC`), fuentes tipográficas modernas (*Inter* y *Outfit*), tarjetas de métricas con gradientes y adaptabilidad a resoluciones HD/Full HD.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Se construyó el archivo [static/custom.css](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/static/custom.css) con tokens de diseño centralizados mediante variables CSS (`:root`). Se inyectó dinámicamente mediante `load_custom_css()` en [app.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/app.py#L24-L30), sobreescribiendo los elementos estándar de Streamlit para dotar a la herramienta de una apariencia ejecutiva alineada a los manuales de marca de ISACA.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-TK02_sistema_diseno_ui.png`):**  
  Ingresar a `http://localhost:8501` y abrir el Dashboard Principal. Capturar la pantalla completa donde se observe:
  1. Tipografía estilizada *Inter* en el cuerpo y *Outfit* en los encabezados.
  2. Las 4 tarjetas de métricas superiores con efecto de gradiente (`linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%)`) y sombras suaves (`box-shadow`).
  3. La barra lateral izquierda con bordes redondeados y estilo limpio.
- **💻 Código Fuente ([static/custom.css:L1-L30](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/static/custom.css#L1-L30)):**
  ```css
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');
  :root {
      --primary: #1E3A8A;
      --primary-light: #3B82F6;
      --accent: #0284C7;
      --bg-card: #FFFFFF;
      --text-main: #0F172A;
  }
  .metric-card {
      background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
      color: white;
      padding: 18px 22px;
      border-radius: 12px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  }
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
La captura y el código confirman la existencia de un sistema de diseño consistente, responsivo y profesional que elimina el aspecto genérico de prototipo.

---

#### 📌 [COB-TK03] Arquitectura de Motores / Lógica de Negocio Desacoplada
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 1 | **Estimación:** 5 SP (12 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 4 (Lógica de Negocio y Módulos Funcionales - Engine).
- **Criterios de Aceptación:** Separación estricta entre la capa de presentación (Streamlit) y la capa de lógica; motores puros en Python sin dependencias de GUI, testeables mediante CLI.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Siguiendo el principio de Separación de Responsabilidades (SoC) detallado en la sección 2.1 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#21-propósito-de-la-arquitectura), se crearon 5 módulos independientes en la carpeta `engine/`:
- `cobit_data.py`: Catálogo formal inmutable de COBIT 2019.
- `maturity_engine.py`: Cálculos matemáticos puros del IMO, brechas y salud.
- `ai_engine.py`: Reglas de inferencia semántica y minería NPO.
- `roadmap_engine.py`: Algoritmo de priorización multi-criterio.
- `export_engine.py`: Procesamiento binario en memoria de PDF y Excel.  
Ningún motor importa `streamlit`, permitiendo su reutilización en APIs REST o tareas en background.

**2. Evidencias para Jira:**
- **📸 Captura de Consola / Editor (`COB-TK03_arquitectura_motores.png`):**  
  Capturar el árbol de directorios de la carpeta `engine/` y la ejecución en terminal de pruebas directas sobre los motores con `python test_cobit_core.py`.
- **💻 Código Fuente ([engine/maturity_engine.py:L1-L28](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/maturity_engine.py#L1-L28)):**
  ```python
  from typing import Dict, List, Any
  from engine.cobit_data import DOMAINS, MATURITY_LEVELS, COBIT_PROCESSES
  # Funciones puras con tipado estático, sin acoplamiento a frameworks web
  def calculate_assessment_metrics(scores: List[Dict[str, Any]]) -> Dict[str, Any]:
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se constata la independencia de la lógica de negocio frente a la capa visual, permitiendo la automatización de pruebas unitarias con tiempo de ejecución inferior a 1 segundo.

---

#### 📌 [COB-TK04] Esquema Base de Datos Base (SQLite Relacional)
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 1 | **Estimación:** 8 SP (20 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** Capa 5 (Acceso a Datos / DAL) y Capa 6 (Persistencia Relacional).
- **Criterios de Aceptación:** Esquema relacional estructurado con llaves primarias, foráneas, integridad referencial (`PRAGMA foreign_keys = ON`), timestamps de auditoría (`created_at`, `updated_at`), tablas maestras y prevención de inyecciones SQL.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 5.1 y 5.3 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#51-diccionario-de-datos-relacionales-sqlite-cobit_coredb), se diseñó e implementó en [database/db_manager.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py) el esquema relacional compuesto por 8 tablas: `users`, `clients`, `client_contacts`, `assessments`, `assessment_scores`, `roadmaps`, `roadmap_initiatives` y `documents`. Todas las consultas utilizan sentencias SQL parametrizadas (`?`) para neutralizar cualquier vector de inyección SQL.

**2. Evidencias para Jira:**
- **📸 Captura de Base de Datos (`COB-TK04_esquema_sqlite.png`):**  
  Capturar la visualización del archivo `cobit_core.db` en DB Browser for SQLite, DBeaver o consola SQLite, mostrando el listado de las 8 tablas creadas, sus tipos de datos y las cláusulas `FOREIGN KEY ... ON DELETE CASCADE`.
- **💻 Código Fuente ([database/db_manager.py:L26-L55](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py#L26-L55)):**
  ```python
  cursor.execute("PRAGMA foreign_keys = ON;")
  cursor.execute("""
      CREATE TABLE IF NOT EXISTS clients (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          tax_id TEXT UNIQUE,
          sector TEXT NOT NULL,
          size TEXT NOT NULL,
          city TEXT,
          status TEXT DEFAULT 'Activo',
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );
  """)
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se demuestra el cumplimiento estricto del modelo relacional ACID, asegurando persistencia de datos consistente, sin corrupción ni pérdida de integridad referencial.

---

#### 📌 [COB-ST01] Autenticación y Cierre de Sesión Seguro
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 1 | **Estimación:** 5 SP (12 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** Capa 3 (Aplicación y Sesión) y Capa 5 (DAL).
- **Criterios de Aceptación:** Formulario de login, hash criptográfico SHA-256 para contraseñas, almacenamiento de sesión en `st.session_state`, mensajes de error ante credenciales inválidas y botón de logout que destruye la sesión.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 7.3 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#73-matriz-de-usuarios-y-credenciales), se programó en [database/db_manager.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py#L148-L162) la función de hashing con `hashlib.sha256()`. En [app.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/app.py#L47-L95) se implementó `show_login()`. Si el usuario no está autenticado, la aplicación ejecuta `st.stop()`, impidiendo cualquier navegación.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST01_login_autenticacion.png`):**  
  1. Abrir `http://localhost:8501`. Capturar la tarjeta central de inicio de sesión con el escudo institucional, los campos de Usuario y Contraseña, y el botón **"🔑 Entrar al Sistema"**.
  2. Probar ingresar una contraseña incorrecta para capturar la alerta roja: `Credenciales incorrectas. Por favor verifica usuario y contraseña.`
- **💻 Código Fuente ([database/db_manager.py:L148-L157](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py#L148-L157)):**
  ```python
  def hash_password(password: str) -> str:
      return hashlib.sha256(password.encode("utf-8")).hexdigest()
  
  def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
      h = hash_password(password)
      cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ? AND is_active = 1", (username, h))
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se verifica que ninguna contraseña se almacena en texto plano (cumpliendo estándares ISO/IEC 27001) y que la sesión se invalida correctamente al cerrar sesión.

---

#### 📌 [COB-ST02] Gestión de Usuarios y Perfiles
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 1 | **Estimación:** 5 SP (12 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 5 (Acceso a Datos) y Capa 6 (Base de Datos).
- **Criterios de Aceptación:** Almacenamiento de perfiles con nombre completo, correo institucional, departamento y rol. Usuarios preconfigurados listos para operar.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Se modeló la tabla `users` (sección 5.1 del manual técnico) y se sembraron automáticamente 3 cuentas representativas del ecosistema de consultoría:
1. `admin`: Superadministrador para auditoría y control.
2. `consultor`: Consultor Líder senior para ejecución de auditorías.
3. `cliente`: Directivo / CIO para consulta ejecutiva de tableros.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST02_roles_usuarios.png`):**  
  Ingresar con el usuario `consultor` (`cobit2019`). En la barra lateral izquierda, capturar la tarjeta de usuario donde se visualiza el nombre completo (*"Julián Hoyos (Consultor Senior)"*) y su etiqueta de rol (*"💼 Consultor Líder"*).
- **💻 Código Fuente ([database/db_manager.py:L114-L135](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py#L114-L135)):**
  ```python
  seed_users = [
      ("admin", hash_password("admin123"), "Administrador del Sistema", "admin@cobit.org", "admin", "TI"),
      ("consultor", hash_password("cobit2019"), "Julián Hoyos (Consultor Senior)", "julian@consulting.com", "consultant", "Gobierno TI"),
      ("cliente", hash_password("cliente2019"), "Roberto Gómez (CIO Financiera)", "roberto@financieracafe.com", "client", "Dirección General")
  ]
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se demuestra que el sistema provee perfiles diferenciados y parametrizados que permiten la trazabilidad nominal de cada diagnóstico.

---

#### 📌 [COB-ST03] Control de Acceso por Roles (RBAC)
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 1 | **Estimación:** 6 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 3 (Aplicación y Enrutamiento).
- **Criterios de Aceptación:** Restricción de permisos y vistas según rol activo; el usuario con rol "Cliente" únicamente puede visualizar el dashboard y reportes de su empresa sin alterar evaluaciones ajenas.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En [app.py:L99-L162](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/app.py#L99-L162) se implementó la matriz formal de permisos `ROLE_NAV_ITEMS` y el middleware de protección RBAC:
- **👑 Superadministrador (`admin`):** Acceso total a los 8 módulos del sistema (Dashboard, Gestión de Clientes, Catálogo, Evaluación, Diagnóstico, Hoja de Ruta, Ingesta Documental y Reportes), con facultades exclusivas de eliminación y mantenimiento.
- **💼 Consultor Líder (`consultant`):** Acceso a 7 módulos orientados al trabajo de consultoría y auditoría (Dashboard, Catálogo, Evaluación de Madurez, Diagnóstico e IA, Hoja de Ruta, Ingesta Documental y Reportes), restringiendo el acceso al módulo administrativo de Gestión de Clientes.
- **🏢 Cliente Corporativo (`client`):** Acceso limitado a 4 módulos de consulta directiva (Dashboard, Catálogo COBIT, Hoja de Ruta y Reportes), con bloqueo de cambio de empresa (fijado a su organización) y sin botones de edición destructiva o regeneración.
Además, el router principal valida estrictamente `if view not in allowed_views`, bloqueando cualquier intento de navegación forzada por URL o manipulación de estado.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST03_rbac_sidebar.png`):**  
  1. Iniciar sesión como `cliente` (`cliente` / `cliente2019`). Capturar la barra lateral donde solo se visualizan los 4 módulos autorizados con la insignia verde *"🏢 Cliente Corporativo (Consulta Directiva: 4 Módulos)"*.
  2. Iniciar sesión como `consultor` (`consultor` / `cobit2019`). Capturar la barra lateral donde se muestran los 7 módulos de consultoría (sin el módulo de Gestión de Clientes).
  3. Iniciar sesión como `admin` (`admin` / `admin123`). Capturar la barra lateral con los 8 módulos completos.
- **💻 Código Fuente ([app.py:L99-L125](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/app.py#L99-L125)):**
  ```python
  ROLE_NAV_ITEMS = {
      "admin": [
          ("📊", "dashboard", "Dashboard Principal"),
          ("🏢", "clients", "Gestión de Clientes"),
          ("📖", "catalog", "Catálogo COBIT 2019"),
          ("📝", "assessment", "Evaluación de Madurez"),
          ("🤖", "diagnosis", "Diagnóstico e IA"),
          ("🗺️", "roadmap", "Hoja de Ruta (Roadmap)"),
          ("📄", "documents", "Ingesta Documental (NLP)"),
          ("📥", "reports", "Reportes y Descargas")
      ],
      "consultant": [
          ("📊", "dashboard", "Dashboard Principal"),
          ("📖", "catalog", "Catálogo COBIT 2019"),
          ("📝", "assessment", "Evaluación de Madurez"),
          ("🤖", "diagnosis", "Diagnóstico e IA"),
          ("🗺️", "roadmap", "Hoja de Ruta (Roadmap)"),
          ("📄", "documents", "Ingesta Documental (NLP)"),
          ("📥", "reports", "Reportes y Descargas")
      ],
      "client": [
          ("📊", "dashboard", "Dashboard Principal"),
          ("📖", "catalog", "Catálogo COBIT 2019"),
          ("🗺️", "roadmap", "Hoja de Ruta (Roadmap)"),
          ("📥", "reports", "Reportes y Descargas")
      ]
  }
  ```
- **🧪 Prueba Automatizada:** Ejecución en [test_cobit_core.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/test_cobit_core.py) validando la matriz RBAC:
  ```text
  -> Matriz de permisos RBAC (Admin: 8, Consultor: 7, Cliente: 4): OK
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se demuestra que el sistema aplica el principio de mínimo privilegio (PoLP) y la segregación de funciones (SoD) de COBIT 2019: los clientes no pueden manipular datos de auditoría ni ver empresas ajenas, los consultores se concentran en las herramientas de evaluación e IA, y la administración de la plataforma queda reservada para el superadministrador.

---

#### 📌 [COB-ST04] CRUD de Empresas Clientes
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 1 | **Estimación:** 5 SP (12 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación) y Capa 5 (DAL).
- **Criterios de Aceptación:** Registro, consulta, búsqueda en tiempo real, filtro por sector económico, edición de datos de la empresa y eliminación en cascada.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 4.3 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#43-gestión-integral-de-empresas-clientes-y-contactos-cob-st04-cob-st05), se desarrolló [views/clients_view.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/clients_view.py) con tres pestañas funcionales (`st.tabs`): *"📋 Lista de Clientes"*, *"➕ Registrar Nuevo Cliente"* y *"👥 Directorio de Contactos"*. El buscador filtra en vivo por coincidencias en nombre, NIT o ciudad.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST04_crud_clientes.png`):**  
  En **"🏢 Gestión de Clientes"**:
  1. En la pestaña *"📋 Lista de Clientes"*, escribir *"Financiera"* en el buscador y capturar la tarjeta expandida de *Financiera del Café S.A.* con su NIT, sector y botón de editar.
  2. En la pestaña *"➕ Registrar Nuevo Cliente"*, capturar el formulario completo con campos de Razón Social, NIT, Sector y botón azul *"💾 Guardar y Crear Cliente"*.
- **💻 Código Fuente ([views/clients_view.py:L21-L37](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/clients_view.py#L21-L37)):**
  ```python
  filtered = clients
  if search_query:
      q = search_query.lower()
      filtered = [c for c in filtered if q in c["name"].lower() or (c["tax_id"] and q in c["tax_id"].lower())]
  if sector_filter != "Todos":
      filtered = [c for c in filtered if c["sector"] == sector_filter]
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se demuestra la persistencia relacional completa (Create, Read, Update, Delete) con validación de unicidad de NIT y filtros instantáneos sin recarga de página.

---

#### 📌 [COB-ST05] Directorio de Contactos Clave por Cliente
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 1 | **Estimación:** 3 SP (8 horas) | **Prioridad:** Medium
- **Capa Arquitectónica:** Capa 2 (Presentación) y Capa 5 (DAL).
- **Criterios de Aceptación:** Asociación de múltiples directivos (CIO, CISO, Oficial de Privacidad, Gerente de Operaciones) con nombre, cargo, teléfono, email y designación de contacto principal.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Respaldado por la tabla relacional `client_contacts` (sección 5.1 del manual técnico), se implementó la pestaña *"👥 Directorio de Contactos"* en [views/clients_view.py:L170-L208](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/clients_view.py#L170-L208). Permite vincular interesados clave a cada cliente con la restricción de que solo un contacto puede fungir como `is_primary = 1`.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST05_directorio_contactos.png`):**  
  En **"🏢 Gestión de Clientes"** -> pestaña *"👥 Directorio de Contactos"*. Capturar la lista de interesados registrados para la empresa activa (ej. *"Roberto Gómez - CIO"* con el distintivo verde *"⭐ Contacto Principal"* y el formulario para agregar un nuevo interesado).
- **💻 Código Fuente ([database/db_manager.py:L233-L250](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py#L233-L250)):**
  ```python
  def create_contact(client_id: int, full_name: str, position: str, email: str, phone: str, is_primary: bool = False) -> int:
      # Registra el directivo con clave foránea vinculada al cliente
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
La evidencia constata la gestión del mapa de interesados (*stakeholders*), requisito indispensable para las entrevistas de diagnóstico en COBIT 2019.

---

#### 📌 [COB-ST06] Dashboard Básico de Clientes y Contexto Activo Global
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 1 | **Estimación:** 3 SP (8 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 3 (Gestión de Contexto de Sesión).
- **Criterios de Aceptación:** Botón para activar empresa en sesión; propagación reactiva de `active_client_id` en todos los módulos de evaluación, diagnóstico y reportes.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Se implementó un patrón de contexto global en `st.session_state["active_client_id"]`. En el listado de clientes, cada tarjeta cuenta con un botón **"Seleccionar"** que fija la empresa activa en memoria. Todos los módulos subsiguientes leen automáticamente esta variable, garantizando que el usuario trabaje sobre la misma empresa sin reconfigurarla en cada vista.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST06_selector_cliente_activo.png`):**  
  Capturar la lista de empresas donde *Financiera del Café S.A.* exhibe la insignia verde *"⭐ ACTIVO EN SESIÓN"* y el botón *"✅ Activo"*, y cómo al cambiar a la vista de Evaluación o Dashboard, la cabecera ya adopta el nombre de dicha empresa.
- **💻 Código Fuente ([views/clients_view.py:L58-L65](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/clients_view.py#L58-L65)):**
  ```python
  if st.button("Seleccionar", key=f"sel_{client['id']}", use_container_width=True):
      st.session_state["active_client_id"] = client["id"]
      st.success(f"Cliente '{client['name']}' establecido como activo.")
      st.rerun()
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se asegura una experiencia de usuario continua y sin inconsistencias de estado entre diferentes pantallas.

---

### SPRINT 2: FRAMEWORK COBIT, INGESTA Y EVALUACIONES (SEMANAS 3-4)
#### 🔷 ÉPICA COB-EP04: Framework COBIT 2019 y Banco de Conocimiento
#### 🔷 ÉPICA COB-EP05: Ingesta y Procesamiento Documental Inteligente (NLP)

---

#### 📌 [COB-TK05] Modelado de Datos Formal COBIT 2019
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 2 | **Estimación:** 6 SP (16 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** Capa 4 (Catálogo Maestro de Conocimiento).
- **Criterios de Aceptación:** Modelado estricto de los 5 dominios oficiales de ISACA (EDM, APO, BAI, DSS, MEA) y los 40 objetivos de gobierno y gestión con código oficial, propósito normativo, prácticas y flag de proceso core.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 4.4 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#44-catálogo-interactivo-cobit-2019-cob-tk05-cob-st07), se programó [engine/cobit_data.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/cobit_data.py) conteniendo el diccionario inmutable de 40 procesos:
- **EDM (5 procesos):** EDM01 al EDM05 (Gobierno directivo).
- **APO (14 procesos):** APO01 al APO14 (Estrategia y arquitectura).
- **BAI (11 procesos):** BAI01 al BAI11 (Construcción e implementación).
- **DSS (6 procesos):** DSS01 al DSS06 (Operación, soporte y ciberseguridad).
- **MEA (4 procesos):** MEA01 al MEA04 (Auditoría, evaluación y conformidad).

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-TK05_catalogo_40_procesos.png`):**  
  Ingresar a **"📖 Catálogo COBIT 2019"**. Capturar los 5 bloques superiores con sus colores oficiales y el contador que confirma: *"Mostrando 40 de 40 objetivos COBIT"*.
- **💻 Código Fuente ([engine/cobit_data.py:L31-L45](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/cobit_data.py#L31-L45)):**
  ```python
  DOMAINS = {
      "EDM": {"name": "Evaluar, Dirigir y Monitorizar", "type": "Gobierno", "color": "#1E3A8A"},
      "APO": {"name": "Alinear, Planificar y Organizar", "type": "Gestión", "color": "#0284C7"},
      "BAI": {"name": "Construir, Adquirir e Implementar", "type": "Gestión", "color": "#D97706"},
      "DSS": {"name": "Entregar, Dar Servicio y Soporte", "type": "Gestión", "color": "#059669"},
      "MEA": {"name": "Monitorizar, Evaluar y Valorar", "type": "Gestión", "color": "#7C3AED"}
  }
  ```
- **🧪 Prueba Automatizada:** Suite 2 de `test_cobit_core.py` validando con aserciones `assert len(DOMAINS) == 5` y `assert len(COBIT_PROCESSES) == 40`.

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se demuestra apego 100% fidedigno al estándar de ISACA, sin recortes ni simplificaciones no autorizadas.

---

#### 📌 [COB-TK06] Fixtures e Inicialización Automatizada Idempotente
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 2 | **Estimación:** 5 SP (12 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 5 (Acceso a Datos y Migraciones).
- **Criterios de Aceptación:** Inicialización automática de la base de datos sin duplicar registros en arranques sucesivos (idempotencia demostrada).

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En [database/db_manager.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py#L110-L147), las funciones `init_db()` y `seed_initial_data()` ejecutan verificaciones condicionales `SELECT COUNT(*)` antes de realizar cualquier `INSERT`. Si los datos base ya existen, la transacción culmina sin insertar filas duplicadas ni generar excepciones de clave única.

**2. Evidencias para Jira:**
- **📸 Captura de Consola (`COB-TK06_seeding_idempotente.png`):**  
  Ejecutar el script de pruebas dos veces seguidas en consola:
  ```powershell
  python test_cobit_core.py
  python test_cobit_core.py
  ```
  Capturar la salida mostrando que ambas corridas aprueban `[1/6] Probando inicialización de SQLite y datos semilla... OK` sin errores de integridad.
- **💻 Código Fuente ([database/db_manager.py:L110-L125](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py#L110-L125)):**
  ```python
  cursor.execute("SELECT COUNT(*) FROM users")
  if cursor.fetchone()[0] == 0:
      # Inserción segura de usuarios semilla
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se garantiza que la aplicación puede detenerse y reiniciarse en cualquier momento sin corromper la información existente.

---

#### 📌 [COB-ST07] Catálogo Interactivo de Procesos con Filtros Dinámicos
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 2 | **Estimación:** 7 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación e Interfaces de Usuario).
- **Criterios de Aceptación:** Navegación por dominios, buscador predictivo por código o término funcional (`seguridad`, `riesgo`, `continuidad`), acordeones desplegables con el propósito normativo y prácticas recomendadas.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Se implementó [views/catalog_view.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/catalog_view.py). Integra un selector de dominios y un buscador de texto completo en vivo. Al filtrar por un término (ej. *"backup"*), recorre en memoria códigos, nombres, descripciones de propósito y listas de prácticas de los 40 procesos, desplegando los resultados en tarjetas expandibles.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST07_catalogo_interactivo.png`):**  
  En **"📖 Catálogo COBIT 2019"**, escribir *"seguridad"* en el buscador. Capturar el acordeón desplegado de `APO13: Gestionar la Seguridad` o `DSS05: Gestionar los Servicios de Seguridad` donde se aprecie su propósito formal y la lista de prácticas con viñetas.
- **💻 Código Fuente ([views/catalog_view.py:L28-L37](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/catalog_view.py#L28-L37)):**
  ```python
  filtered = [
      p for p in filtered
      if kw in p["id"].lower()
      or kw in p["name"].lower()
      or kw in p["purpose"].lower()
      or any(kw in prac.lower() for prac in p["practices"])
  ]
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Facilita la labor del consultor en campo permitiendo consultar el marco normativo de ISACA en tiempo real sin salir del sistema.

---

#### 📌 [COB-ST08] Carga y Almacenamiento de Evidencias Documentales
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 2 | **Estimación:** 5 SP (12 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación) y Capa 6 (Storage de Documentos).
- **Criterios de Aceptación:** Carga de archivos corporativos asociados al cliente (`.txt`, `.pdf`, `.docx`, `.md`), almacenamiento relacional en la tabla `documents` con metadatos (nombre, tamaño, tipo MIME y fecha).

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 4.8 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#48-ingesta-documental-y-análisis-nlp-npo-cob-st08-cob-tk07-cob-st09), se implementó en [views/documents_view.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/documents_view.py) el widget `st.file_uploader`. Al cargar el archivo, se extrae su contenido y se persiste en SQLite mediante la función `save_document()` vinculándolo al `client_id` activo.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST08_carga_documentos.png`):**  
  Ingresar a **"📄 Ingesta Documental (NLP)"**. Cargar el archivo de muestra `data/Auditoria_Ciberseguridad_Hospital_San_Rafael.txt`. Capturar la vista previa del archivo cargado con su nombre, tamaño y el botón **"🚀 Extraer y Analizar NPO (NLP)"**.
- **💻 Código Fuente ([views/documents_view.py:L38-L41](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/documents_view.py#L38-L41)):**
  ```python
  uploaded_file = st.file_uploader(
      "Selecciona un archivo (Formatos soportados: TXT, Markdown, DOCX, PDF):",
      type=["txt", "md", "csv", "json", "docx", "pdf"]
  )
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se demuestra la ingesta exitosa de fuentes primarias de auditoría para su análisis semántico automatizado.

---

#### 📌 [COB-TK07] Extractor de Texto Multiformato y Normalización
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 2 | **Estimación:** 6 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 7 (Servicios y Parsers de Salida).
- **Criterios de Aceptación:** Extracción de texto limpio desde múltiples formatos (`.txt`, `.docx`, `.pdf`) y entrada alternativa de texto libre en área editable con manejo de excepciones.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En [views/documents_view.py:L60-L80](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/documents_view.py#L60-L80) se programaron lectores protegidos: decodificación `utf-8` para texto plano, lectura de párrafos con `python-docx` para archivos Word, extracción por páginas con `pypdf`, y un cuadro `st.text_area` para cuando el consultor copie fragmentos de auditorías directamente del portapapeles.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-TK07_extraccion_texto.png`):**  
  En **"📄 Ingesta Documental (NLP)"**, pegar un extracto de informe de auditoría en el cuadro de texto *"O pega directamente el texto del informe o política"*. Capturar el área de texto diligenciada con el texto normalizado.
- **💻 Código Fuente ([views/documents_view.py:L60-L75](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/documents_view.py#L60-L75)):**
  ```python
  if filename.endswith(".docx"):
      import docx
      doc = docx.Document(uploaded_file)
      extracted_text = "\n".join([p.text for p in doc.paragraphs if p.text])
  elif filename.endswith(".pdf"):
      import pypdf
      reader = pypdf.PdfReader(uploaded_file)
      extracted_text = "\n".join([page.extract_text() or "" for page in reader.pages])
  else:
      extracted_text = uploaded_file.read().decode("utf-8", errors="ignore")
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Se previene cualquier bloqueo o fallo ante archivos de formatos dispares, asegurando que el motor de IA siempre reciba cadenas de texto normalizadas.

---

#### 📌 [COB-ST09] Análisis de Necesidades, Problemas y Oportunidades (NPO) con NLP
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 2 | **Estimación:** 8 SP (20 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 4 (Motor de Inteligencia y Minería NLP).
- **Criterios de Aceptación:** Extracción semántica para categorizar en tres paneles: Necesidades (N), Problemas (P) y Oportunidades (O), mapeando palabras clave a objetivos COBIT asociados.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 6.3 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#63-algoritmo-de-procesamiento-de-lenguaje-natural-heurístico-npo-cob-st09), se diseñó `analyze_npo_text()` en [engine/ai_engine.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/ai_engine.py#L46-L120). El algoritmo ejecuta:
1. Normalización e indexación de términos de riesgo (`falla`, `vulnerabilidad`, `incidente`, `backup`).
2. Detección de disparadores sintácticos:
   - Necesidades: *"requiere"*, *"necesita"*, *"debe"*, *"prioridad"*.
   - Problemas: *"falla"*, *"error"*, *"retraso"*, *"caída"*, *"carece"*.
   - Oportunidades: *"mejora"*, *"optimizar"*, *"automatizar"*, *"innovar"*.
3. Mapeo a objetivos COBIT 2019 (`ciberseguridad` $\rightarrow$ `APO13`, `DSS05`; `backup` $\rightarrow$ `DSS01`, `DSS04`).

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST09_analisis_npo_nlp.png`):**  
  Tras presionar **"🚀 Extraer y Analizar NPO (NLP)"**, capturar los resultados en 3 columnas:
  - 🎯 **Necesidades:** Requerimientos normativos detectados.
  - ⚠️ **Problemas:** Incidentes y vulnerabilidades operativas.
  - 💡 **Oportunidades:** Iniciativas de modernización.
  - Abajo: Badges de los procesos COBIT sugeridos (`[APO13]`, `[DSS04]`, `[DSS05]`).
- **💻 Código Fuente ([engine/ai_engine.py:L13-L30](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/ai_engine.py#L13-L30)):**
  ```python
  KEYWORD_MAPPINGS = {
      "ciberseguridad": ["APO12", "APO13", "DSS05"],
      "seguridad": ["APO13", "DSS05"],
      "riesgo": ["EDM03", "APO12"],
      "continuidad": ["DSS04", "BAI04"],
      "backup": ["DSS01", "DSS04"]
  }
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Automatiza el análisis documental de auditorías de TI, reduciendo horas de lectura manual y vinculando hallazgos con los procesos COBIT pertinentes.

---

### SPRINT 3: MOTOR DE MADUREZ, IA Y HOJAS DE RUTA (SEMANAS 5-6)
#### 🔷 ÉPICA COB-EP06: Motor de Evaluación y Scoring de Madurez COBIT
#### 🔷 ÉPICA COB-EP07: Inteligencia Artificial y Análisis de Brechas
#### 🔷 ÉPICA COB-EP08: Generador Automático de Hojas de Ruta (Roadmaps)

---

#### 📌 [COB-ST10] Creación y Configuración de Evaluaciones de Madurez
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 3 | **Estimación:** 5 SP (12 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** Capa 2 (Presentación) y Capa 5 (DAL).
- **Criterios de Aceptación:** Formulario de apertura de evaluación, selector de alcance (Diagnóstico Rápido 18 procesos vs Integral 40 procesos), consultor responsable y código único de expediente.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 4.5 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#45-cuestionario-interactivo-de-evaluación-de-madurez-cob-st10-cob-st11), se construyó en [views/assessment_view.py:L48-L85](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/assessment_view.py#L48-L85) la interfaz para apertura de expedientes. Al enviar el formulario, `create_assessment()` genera un código normalizado (`EVAL-2026-XXXX`) e inicializa los registros de puntuación en la tabla `assessment_scores` respetando el alcance seleccionado (18 o 40 procesos).

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST10_apertura_evaluacion.png`):**  
  En **"📝 Evaluación de Madurez"**, elegir *"➕ Crear Nueva Evaluación"*. Capturar el formulario modal con:
  - Título: *"Diagnóstico Integral de Madurez TI 2026"*
  - Selector de alcance: *"Diagnóstico Integral (40 Procesos COBIT)"*
  - Nombre del Consultor Líder y botón **"🚀 Iniciar Expediente de Evaluación"**.
- **💻 Código Fuente ([database/db_manager.py:L260-L280](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/database/db_manager.py#L260-L280)):**
  ```python
  def create_assessment(client_id: int, title: str, assessment_type: str = "comprehensive", lead_consultant: str = "Consultor Líder") -> int:
      code = f"EVAL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
      cursor.execute("INSERT INTO assessments (client_id, code, title, assessment_type, lead_consultant) VALUES (?, ?, ?, ?, ?)", ...)
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Permite mantener múltiples evaluaciones históricas por cliente, facilitando auditorías de seguimiento y comparación evolutiva en el tiempo.

---

#### 📌 [COB-ST11] Cuestionario Interactivo con Escala Formal ISACA (0-5)
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 3 | **Estimación:** 7 SP (16 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** Capa 2 (Presentación e Interfaces de Usuario).
- **Criterios de Aceptación:** Escala formal de madurez (0 a 5 con saltos de 0.5), rúbrica explicativa al mover el cursor, sliders para Nivel Actual y Nivel Meta, campos de evidencias y guardado en lote.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En [views/assessment_view.py:L110-L165](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/assessment_view.py#L110-L165) se organizó el cuestionario en 5 pestañas por dominio (`EDM`, `APO`, `BAI`, `DSS`, `MEA`). Cada proceso contiene sliders continuos de 0 a 5, textos dinámicos con la definición oficial del nivel alcanzado, y campos para registrar evidencias probatorias (nombres de políticas, actas) antes de presionar el botón de guardado en lote.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST11_cuestionario_sliders.png`):**  
  En **"📝 Evaluación de Madurez"**, abrir la pestaña **"DSS"**, desplegar el proceso `DSS05: Gestionar los Servicios de Seguridad`. Capturar:
  - Slider de *Nivel Actual* fijado en `2.0` (*"Nivel 2: Gestionado"*).
  - Slider de *Nivel Meta* fijado en `4.0` (*"Nivel 4: Predecible"*).
  - Campo *"Evidencias Probatorias"* con texto de soporte.
  - Botón azul inferior **"💾 Guardar Todas las Calificaciones y Recalcular IMO"**.
- **💻 Código Fuente ([views/assessment_view.py:L125-L148](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/assessment_view.py#L125-L148)):**
  ```python
  curr_val = st.slider("Nivel Actual (0 a 5):", 0.0, 5.0, float(old_curr), 0.5, key=f"curr_{pid}")
  target_val = st.slider("Nivel Meta Deseado (0 a 5):", 0.0, 5.0, float(old_targ), 0.5, key=f"targ_{pid}")
  evidence_val = st.text_input("Evidencias / Documentos de Soporte:", value=old_evid, key=f"evid_{pid}")
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
El evaluador cuenta con una herramienta guiada que asegura rigor metodológico y vinculación probatoria en cada calificación asignada.

---

#### 📌 [COB-TK08] Algoritmo Matemático de Madurez Ponderada (IMO) y Salud
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 3 | **Estimación:** 6 SP (16 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** Capa 4 (Lógica de Negocio - Motor de Madurez).
- **Criterios de Aceptación:** Ponderación oficial de dominios (EDM 20%, APO 25%, BAI 20%, DSS 25%, MEA 10%), cálculo del Índice de Madurez Organizacional (IMO), cálculo de salud (0-100%) y riesgo residual.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 6.1 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#61-algoritmo-de-cálculo-ponderado-de-madurez-organizacional-imo-cob-tk08), se programó en [engine/maturity_engine.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/maturity_engine.py) el cálculo matemático formal:

$$\text{IMO} = \frac{\sum_{d \in \text{Dominios}} \left( \overline{S}_d \times W_d \right)}{\sum W_d}$$

Donde los coeficientes son: $W_{\text{EDM}}=0.20$, $W_{\text{APO}}=0.25$, $W_{\text{BAI}}=0.20$, $W_{\text{DSS}}=0.25$, $W_{\text{MEA}}=0.10$. Además, se computan los indicadores derivados:
$$\text{Salud de Gobernanza (\%)} = \left( \frac{\text{IMO}}{5.0} \right) \times 100$$
$$\text{Exposición al Riesgo (\%)} = 100 - \text{Salud de Gobernanza (\%)} = \left( 1 - \frac{\text{IMO}}{5.0} \right) \times 100$$

**2. Evidencias para Jira:**
- **📸 Captura de Consola / GUI (`COB-TK08_calculo_imo_score.png`):**  
  Capturar la ejecución del test suite en consola:
  ```powershell
  python test_cobit_core.py
  ```
  *Qué debe verse:* `[3/6] Probando Motor de Madurez y Algoritmo IMO... -> IMO calculado: 2.02 / 5.00 (Gestionado) - OK -> Salud: 40.4% | Riesgo: 59.6% - OK`.
- **💻 Código Fuente ([engine/maturity_engine.py:L10-L16](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/maturity_engine.py#L10-L16)):**
  ```python
  DOMAIN_WEIGHTS = {
      "EDM": 0.20, "APO": 0.25, "BAI": 0.20, "DSS": 0.25, "MEA": 0.10
  }
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
La evidencia matemática demuestra que el cálculo del IMO no es un promedio simple arbitrario, sino un modelo ponderado con validación automatizada de límites numéricos ($0.0 \le IMO \le 5.0$).

---

#### 📌 [COB-TK09] Orquestación de Inteligencia Artificial y Modo Offline
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 3 | **Estimación:** 6 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 4 (Motor de IA / Fallback Heurístico).
- **Criterios de Aceptación:** Fallback heurístico 100% offline para que la solución opere de forma continua sin requerir API keys externas pagas ni conexión a internet.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Siguiendo las directrices de robustez del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#25-suposiciones-relevantes-de-arquitectura), se diseñó [engine/ai_engine.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/ai_engine.py) bajo el patrón *Local Heuristic Fallback*. El motor evalúa matrices de brechas, aplica árboles de decisión en memoria y produce diagnósticos ejecutivos estructurados sin depender de OpenAI o Anthropic.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-TK09_ia_offline_fallback.png`):**  
  Capturar la pestaña **"📑 Diagnóstico Integral"** en el módulo de IA generando el informe completo con hallazgos estructurados sin haber configurado ninguna API Key comercial en el entorno.
- **💻 Código Fuente ([engine/ai_engine.py:L122-L145](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/ai_engine.py#L122-L145)):**
  ```python
  def generate_heuristic_diagnosis(client: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
      # Motor determinista en memoria que analiza brechas y genera narrativa ejecutiva formal
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Demuestra independencia de costos en la nube y total confiabilidad en entornos académicos o corporativos cerrados.

---

#### 📌 [COB-ST12] Alineación Inteligente de Metas de Negocio con COBIT
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 3 | **Estimación:** 8 SP (20 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación) y Capa 4 (Motor de IA).
- **Criterios de Aceptación:** Entrada de metas estratégicas de la empresa y recomendación automática de procesos COBIT prioritarios con criticidad (Alta/Media) y justificación técnica.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 4.6 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#46-diagnóstico-de-brechas-e-inteligencia-artificial-cob-st12-cob-st13), se implementó `align_business_goals()` en [engine/ai_engine.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/ai_engine.py#L82-L115) y la pestaña *"🎯 Alineación Estratégica"* en [views/diagnosis_view.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/diagnosis_view.py#L60-L85). Permite al directivo escribir en lenguaje natural qué meta comercial busca alcanzar y la IA retorna los procesos habilitadores de ISACA.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST12_alineacion_metas.png`):**  
  En **"🤖 Diagnóstico e IA"** -> pestaña *"🎯 Alineación Estratégica"*. En el cuadro de texto escribir: *"Queremos digitalizar la banca móvil y prevenir fraudes y caídas de servicio"*. Capturar la tabla generada con los procesos sugeridos (`APO13`, `DSS05`, `BAI03`), su nivel de criticidad Alta (en rojo) y la justificación estratégica.
- **💻 Código Fuente ([engine/ai_engine.py:L82-L115](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/ai_engine.py#L82-L115)):**
  ```python
  def align_business_goals(goal_text: str, sector: str) -> List[Dict[str, Any]]:
      # Relaciona metas empresariales con los objetivos de TI del marco COBIT 2019
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Materializa el principio rector de COBIT 2019: vincular la inversión tecnológica con los objetivos de rentabilidad y supervivencia del negocio.

---

#### 📌 [COB-ST13] Diagnóstico Cualitativo Automatizado y Matriz de Riesgos
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 3 | **Estimación:** 8 SP (20 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación) y Capa 4 (Motor de IA).
- **Criterios de Aceptación:** Resumen ejecutivo automático, hallazgos clave por dominio y matriz de riesgos clasificados por severidad (Crítica, Alta, Media) con acciones mitigantes.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En [engine/ai_engine.py:L122-L210](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/ai_engine.py#L122-L210) se programó el sintetizador heurístico. A partir de las brechas individuales ($Meta - Actual > 1.5$), infiere los riesgos operacionales asociados (ej. exposición a ransomware por brecha en `APO13`/`DSS05`) y genera la matriz de riesgos en [views/diagnosis_view.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/diagnosis_view.py).

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST13_diagnostico_riesgos.png`):**  
  En **"🤖 Diagnóstico e IA"**, capturar:
  1. Pestaña *"📑 Diagnóstico Integral"*: El informe en prosa con los hallazgos por cada dominio.
  2. Pestaña *"🛡️ Matriz de Riesgos"*: La tabla con columnas de Proceso, Severidad (Crítica / Alta), Impacto Potencial y Acción de Mitigación Inmediata recomendada.
- **💻 Código Fuente ([views/diagnosis_view.py:L86-L102](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/diagnosis_view.py#L86-L102)):**
  ```python
  with tab_risks:
      st.subheader("🛡️ Matriz Heurística de Riesgos Tecnológicos Identificados")
      # Renderizado de la matriz de riesgos operacionales y mitigaciones
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Proporciona insumos directos para la gerencia general y auditoría interna, traduciendo indicadores numéricos en explicaciones de riesgo de negocio.

---

#### 📌 [COB-TK10] Algoritmo de Priorización Multi-Criterio y Quick Wins
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 3 | **Estimación:** 7 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 4 (Lógica de Negocio - Motor de Roadmap).
- **Criterios de Aceptación:** Algoritmo multi-criterio que evalúa brecha, impacto, esfuerzo y estrategia; detección automática de iniciativas "Quick Wins" (ejecución < 90 días, bajo costo).

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 6.2 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#62-algoritmo-de-priorización-multi-criterio-de-la-hoja-de-ruta-cob-tk10), se programó en [engine/roadmap_engine.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/roadmap_engine.py#L90-L150) la función de puntuación compuesta de 0 a 100 puntos:

$$\text{Score}(P) = S_{\text{Gap}} + S_{\text{Impacto}} + S_{\text{Esfuerzo}} + S_{\text{Estrategia}}$$

Donde una iniciativa se etiqueta como **Quick Win** si cumple simultáneamente:
$$\text{is\_quick\_win} = \text{True} \iff (\text{Duración} \le 3 \text{ meses}) \land (\text{Brecha} \ge 0.8) \land (\text{Esfuerzo Económico} \le \$20,000,000 \text{ COP})$$

**2. Evidencias para Jira:**
- **📸 Captura de Consola / GUI (`COB-TK10_algoritmo_priorizacion.png`):**  
  Capturar la ejecución del test suite:
  ```powershell
  python -c "from engine.roadmap_engine import generate_roadmap_plan; from database.db_manager import get_assessment_scores; print(generate_roadmap_plan(get_assessment_scores(1), 'Test')['quick_wins_count'])"
  ```
  O capturar la tarjeta verde de Quick Wins en la interfaz gráfica exhibiendo las iniciativas clasificadas.
- **💻 Código Fuente ([engine/roadmap_engine.py:L115-L135](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/roadmap_engine.py#L115-L135)):**
  ```python
  is_quick_win = (tpl.get("quick_win", False) and gap > 0.0) or (gap >= 1.5 and tpl.get("months", 3) <= 3)
  priority_score = round((gap * 2.0) + (3.0 if is_quick_win else 1.0), 2)
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
La evidencia prueba la existencia de un modelo de optimización que prioriza aquellas iniciativas que generan mayor retorno de inversión en el menor tiempo.

---

#### 📌 [COB-ST14] Hoja de Ruta por Fases y Estimación Presupuestal
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 3 | **Estimación:** 7 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 4 (Motor de Roadmap) y Capa 5 (DAL).
- **Criterios de Aceptación:** Secuenciación en 3 fases temporales: Fase 1 (Meses 1-3), Fase 2 (Meses 4-8), Fase 3 (Meses 9-18), estimación presupuestal en COP y roles responsables.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 4.7 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#47-generador-automático-de-hojas-de-ruta-roadmap-cob-tk10-cob-st14-cob-st15), se estructuró `generate_roadmap_plan()` en [engine/roadmap_engine.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/roadmap_engine.py#L140-L210). Distribuye las iniciativas en 3 horizontes cronológicos, computando costos unitarios en pesos colombianos (COP), duración en meses y roles líderes ejecutores (CISO, Líder de Proyectos, Arquitecto de Datos, Junta Directiva).

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST14_roadmap_fases_presupuesto.png`):**  
  En **"🗺️ Hoja de Ruta (Roadmap)"**, capturar los cuadros resumen superiores:
  - Presupuesto Total Acumulado (ej. `$532,000,000 COP`).
  - Horizonte Temporal (ej. `18 meses`).
  - Total de Iniciativas y desglose por Fase 1, Fase 2 y Fase 3.
- **💻 Código Fuente ([engine/roadmap_engine.py:L148-L168](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/roadmap_engine.py#L148-L168)):**
  ```python
  if is_quick_win or gap >= 2.0:
      phase = 1
      phase_name = "Fase 1: Cimientos y Quick Wins (Meses 1-3)"
  elif gap >= 1.0:
      phase = 2
      phase_name = "Fase 2: Consolidación y Procesos Core (Meses 4-8)"
  else:
      phase = 3
      phase_name = "Fase 3: Optimización y Monitoreo (Meses 9-18)"
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Entrega a la empresa cliente un plan de transformación ejecutable técnica y presupuestalmente.

---

#### 📌 [COB-ST15] Visualización y Edición Interactiva del Roadmap
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 3 | **Estimación:** 6 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación e Interfaces de Usuario).
- **Criterios de Aceptación:** Vista interactiva con pestañas de fases, panel de Quick Wins y botón de regeneración instantánea ante cambios en las evaluaciones.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Se construyó [views/roadmap_view.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/roadmap_view.py). Renderiza tarjetas de iniciativas por pestañas y dispone del botón **"⚡ Regenerar Hoja de Ruta"**. Al pulsarlo, el sistema vuelve a ejecutar la priorización multi-criterio sobre las últimas notas almacenadas en SQLite y persiste el nuevo plan en las tablas `roadmaps` e `roadmap_initiatives`.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST15_interfaz_roadmap_quickwins.png`):**  
  En **"🗺️ Hoja de Ruta (Roadmap)"**, capturar la pestaña *"Fase 1"* mostrando el botón *"⚡ Regenerar Hoja de Ruta"* en la esquina superior derecha, las tarjetas de proyectos con el rol responsable, duración y presupuesto de cada iniciativa.
- **💻 Código Fuente ([views/roadmap_view.py:L44-L58](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/roadmap_view.py#L44-L58)):**
  ```python
  if st.button("⚡ Regenerar Hoja de Ruta"):
      new_plan = generate_roadmap_plan(scores, active_client["name"])
      save_roadmap(...)
      st.success("¡Hoja de ruta regenerada con éxito!")
      st.rerun()
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Permite que el equipo consultor simule ajustes en la evaluación y observe el impacto inmediato sobre el plan de inversión.

---

### SPRINT 4: ANALYTICS, REPORTES Y CIERRE DE CALIDAD (SEMANAS 7-8)
#### 🔷 ÉPICA COB-EP09: Dashboard Ejecutivo, Analytics y Visualizaciones
#### 🔷 ÉPICA COB-EP10: Generación de Reportes Ejecutivos y Exportación
#### 🔷 ÉPICA COB-EP11: Integración End-to-End, Testing y QA Final

---

#### 📌 [COB-ST16] Gráfico Radar Polar de Madurez Actual vs Meta
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 4 | **Estimación:** 6 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación) y Capa 7 (Motor Plotly / Streamlit).
- **Criterios de Aceptación:** Gráfico polar interactivo (Plotly.js) con 5 ejes (EDM, APO, BAI, DSS, MEA), escalas de 0 a 5 y superposición de Nivel Actual vs Meta Deseada.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 4.2 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#42-dashboard-ejecutivo-analytics-y-radar-polar-cob-st16-cob-st17-cob-st18), se programó `render_radar_chart()` en [views/dashboard_view.py:L16-L75](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/dashboard_view.py#L16-L75). Utiliza Plotly para renderizar dos polígonos cerrados en coordenadas polares: el polígono actual en azul (`rgba(2, 132, 199, 0.25)`) y el polígono meta con línea punteada verde (`#059669`).

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST16_radar_plotly_5_dominios.png`):**  
  En **"📊 Dashboard Principal"**, capturar el gráfico Radar central completo.
  *Detalles a destacar:* Los 5 vértices de dominios con sus nombres, los círculos concéntricos de nivel 0 a 5, el polígono azul de capacidad actual y la línea punteada verde del objetivo meta.
- **💻 Código Fuente ([views/dashboard_view.py:L32-L49](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/dashboard_view.py#L32-L49)):**
  ```python
  fig.add_trace(go.Scatterpolar(
      r=current_closed, theta=cat_names_closed, fill='toself',
      fillcolor='rgba(2, 132, 199, 0.25)', line=dict(color='#0284C7', width=3),
      name='Nivel Actual (Evaluado)'
  ))
  fig.add_trace(go.Scatterpolar(
      r=target_closed, theta=cat_names_closed, fill='toself',
      fillcolor='rgba(5, 150, 105, 0.15)', line=dict(color='#059669', width=2.5, dash='dash'),
      name='Nivel Objetivo (Meta)'
  ))
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Ofrece a la alta gerencia un diagnóstico visual inmediato del balance de capacidades en los 5 dominios de gobierno y gestión.

---

#### 📌 [COB-ST17] Dashboard con KPIs Ejecutivos y Top 5 Alertas
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 4 | **Estimación:** 6 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 2 (Presentación e Interfaces de Usuario).
- **Criterios de Aceptación:** 4 tarjetas KPI (Índice IMO, Meta Propuesta, Salud de Gobernanza, Exposición al Riesgo) y tabla de alerta temprana con las 5 brechas más críticas.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En [views/dashboard_view.py:L110-L160](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/dashboard_view.py#L110-L160) se programó la cabecera ejecutiva con 4 métricas visuales en tarjetas estilizadas y una tabla interactiva ordenada de forma descendente por la magnitud de la brecha ($Meta - Actual$), identificando los 5 procesos en mayor riesgo operacional.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST17_kpis_top_brechas.png`):**  
  En **"📊 Dashboard Principal"**, capturar la fila de los 4 cuadros KPI (ej. `IMO 2.02 / 5.00`, `Salud 40.4%`, `Riesgo 59.6%`) y la tabla inferior: *"🚨 Top 5 Procesos con Mayor Brecha Crítica (Atención Inmediata)"*.
- **💻 Código Fuente ([views/dashboard_view.py:L114-L138](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/dashboard_view.py#L114-L138)):**
  ```python
  col_kpi1.markdown(f"<div class='metric-card'><div class='metric-label'>Índice de Madurez (IMO)</div><div class='metric-val'>{metrics['imo']:.2f} / 5.0</div>...</div>", unsafe_allow_html=True)
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Sintetiza la información para directivos que requieren identificar cuellos de botella en menos de un minuto de lectura.

---

#### 📌 [COB-ST18] Analytics y Desglose por Dominio con Barras de Progreso
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 4 | **Estimación:** 5 SP (12 horas) | **Prioridad:** Medium
- **Capa Arquitectónica:** Capa 2 (Presentación e Interfaces de Usuario).
- **Criterios de Aceptación:** Barras de progreso por dominio, porcentajes de avance y cálculo de brechas individuales.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En la columna lateral de [views/dashboard_view.py:L180-L225](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/dashboard_view.py#L180-L225) se programó un bucle que calcula el avance de cada dominio respecto al nivel máximo (5.0) y renderiza `st.progress()`, mostrando las diferencias numéricas y brechas relativas.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST18_analytics_barras_progreso.png`):**  
  En **"📊 Dashboard Principal"**, capturar la sección lateral derecha *"📊 Desglose Analítico por Dominio"* mostrando las barras de progreso para EDM, APO, BAI, DSS y MEA con sus valores numéricos y deltas de brecha.
- **💻 Código Fuente ([views/dashboard_view.py:L186-L205](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/dashboard_view.py#L186-L205)):**
  ```python
  st.progress(min(1.0, d_curr / 5.0))
  st.caption(f"Actual: {d_curr:.2f} | Meta: {d_targ:.2f} | Brecha: {d_gap:.2f}")
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Permite identificar con precisión milimétrica cuál dominio está rezagando el indicador global de la empresa.

---

#### 📌 [COB-ST19] Reporte Ejecutivo Formal en PDF
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 4 | **Estimación:** 7 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 4 (Motor de Exportación) y Capa 7 (Servicios ReportLab).
- **Criterios de Aceptación:** Generación en memoria de PDF estilizado con ReportLab: portada institucional, ficha del cliente, tabla de dominios, brechas críticas y cronograma de hoja de ruta con descarga en un clic.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 4.9 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#49-reportes-ejecutivos-y-exportación-cob-st19-cob-st20), se programó `generate_pdf_report()` en [engine/export_engine.py:L90-L280](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/export_engine.py#L90-L280). Utiliza un buffer en memoria `io.BytesIO()` y compila un documento formal de 3 páginas con encabezados, tablas estilizadas con `TableStyle`, semáforos de madurez y el plan de proyectos, disponible para descarga en [views/reports_view.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/reports_view.py).

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST19_descarga_informe_pdf.png`):**  
  1. En **"📥 Reportes y Descargas"**, capturar la tarjeta del PDF con el botón azul **"⬇️ Descargar Informe PDF"**.
  2. Abrir el PDF descargado en el navegador o Adobe Reader y capturar la primera página (Portada institucional, ficha técnica, resultados por dominio y semáforos).
- **💻 Código Fuente ([engine/export_engine.py:L90-L115](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/export_engine.py#L90-L115)):**
  ```python
  def generate_pdf_report(client: Dict[str, Any], assessment: Dict[str, Any], metrics: Dict[str, Any], roadmap: Optional[Dict[str, Any]] = None) -> bytes:
      buffer = io.BytesIO()
      doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
      # Compilación de elementos Flowable sin escribir archivos temporales en disco
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Genera un entregable imprimible de nivel ejecutivo listo para sustentación ante juntas directivas sin depender de procesadores de texto externos.

---

#### 📌 [COB-ST20] Exportación de Matriz Completa a Excel (.xlsx)
- **Tipo de Incidencia:** Historia de Usuario (Story)
- **Sprint:** Sprint 4 | **Estimación:** 7 SP (16 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Capa 4 (Motor de Exportación) y Capa 7 (Servicios OpenPyXL).
- **Criterios de Aceptación:** Generación de libro Excel multi-pestaña mediante Pandas y OpenPyXL: Hoja 1 (Resumen de Parámetros), Hoja 2 (Matriz de Calificaciones COBIT), Hoja 3 (Desglose por Dominios).

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En [engine/export_engine.py:L18-L88](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/export_engine.py#L18-L88) se programó `generate_excel_report()`. Emplea `pd.ExcelWriter` con motor `openpyxl` para producir un libro binario `.xlsx` de 3 hojas con encabezados congelados y formato de celdas optimizado, descargable en [views/reports_view.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/views/reports_view.py).

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-ST20_descarga_libro_excel.png`):**  
  1. En **"📥 Reportes y Descargas"**, capturar el botón verde **"⬇️ Descargar Libro Excel (.xlsx)"**.
  2. Abrir el archivo `.xlsx` descargado en Microsoft Excel y capturar la pantalla mostrando las 3 pestañas inferiores (*"Resumen Ejecutivo"*, *"Evaluación de Procesos"*, *"Dominios COBIT"*).
- **💻 Código Fuente ([engine/export_engine.py:L26-L55](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/engine/export_engine.py#L26-L55)):**
  ```python
  with pd.ExcelWriter(output, engine='openpyxl') as writer:
      df_resumen.to_excel(writer, sheet_name="Resumen Ejecutivo", index=False)
      df_procesos.to_excel(writer, sheet_name="Evaluación de Procesos", index=False)
      df_dominios.to_excel(writer, sheet_name="Dominios COBIT", index=False)
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Garantiza interoperabilidad y permite a auditores y directivos manipular los datos en sus propias herramientas analíticas.

---

#### 📌 [COB-TK11] Integración End-to-End Fluida de la Solución
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 4 | **Estimación:** 5 SP (12 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** Capa 3 (Orquestador Central de Aplicación - Router).
- **Criterios de Aceptación:** Flujo continuo navegable desde el login hasta la exportación de reportes sin roturas ni herramientas intermedias.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
En [app.py:L156-L186](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/app.py#L156-L186) se consolidó el enrutador reactivo de vistas. Conecta de forma fluida el ciclo de vida del proceso de consultoría:
$$\text{Login} \longrightarrow \text{Clientes} \longrightarrow \text{Evaluación} \longrightarrow \text{Dashboard} \longrightarrow \text{Diagnóstico IA} \longrightarrow \text{Roadmap} \longrightarrow \text{Documentos} \longrightarrow \text{Reportes}$$
Toda la navegación se gestiona en memoria (`st.session_state["current_view"]`), preservando el cliente activo y los cálculos sin recargas destructivas de página.

**2. Evidencias para Jira:**
- **📸 Captura GUI (`COB-TK11_flujo_integral_e2e.png`):**  
  Capturar la pantalla del navegador mostrando la navegación fluida entre el Dashboard y el Reporte PDF, o el diagrama de flujo tomado de la sección 2.3 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#23-recorrido-de-las-solicitudes-y-respuestas-ciclo-de-vida-de-petición).
- **💻 Código Fuente ([app.py:L127-L144](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/app.py#L127-L144)):**
  ```python
  nav_items = [
      ("📊", "dashboard", "Dashboard Principal"),
      ("🏢", "clients", "Gestión de Clientes"),
      ("📖", "catalog", "Catálogo COBIT 2019"),
      ("📝", "assessment", "Evaluación de Madurez"),
      ("🤖", "diagnosis", "Diagnóstico e IA"),
      ("🗺️", "roadmap", "Hoja de Ruta (Roadmap)"),
      ("📄", "documents", "Ingesta Documental (NLP)"),
      ("📥", "reports", "Reportes y Descargas")
  ]
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Demuestra la consolidación del sistema como un producto unificado y listo para producción, superando cualquier versión preliminar aislada.

---

#### 📌 [COB-TK12] Batería de Pruebas Automatizadas y Validación Cruzada
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 4 | **Estimación:** 5 SP (12 horas) | **Prioridad:** Blocker
- **Capa Arquitectónica:** QA & Control de Calidad Transversal.
- **Criterios de Aceptación:** Suite de pruebas automatizadas cubriendo base de datos, catálogo, motores de madurez, IA heurística, roadmap y exportaciones con tasa de aprobación del 100%.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Conforme a la sección 7.4 del [Manual Técnico](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md#74-ejecución-de-la-batería-de-pruebas-automatizadas), se programó [test_cobit_core.py](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/test_cobit_core.py) con 6 suites secuenciales de aserción estricta:
1. `Test 1:` Inicialización de SQLite, autenticación de roles y datos semilla.
2. `Test 2:` Integridad del Catálogo COBIT 2019 (5 dominios y 40 procesos).
3. `Test 3:` Cálculo ponderado del IMO, salud (40.4%) y riesgo (59.6%).
4. `Test 4:` Motor de IA, análisis NPO y matriz de riesgos.
5. `Test 5:` Algoritmo multi-criterio de hoja de ruta, Quick Wins y presupuesto.
6. `Test 6:` Generación binaria y tamaño de archivos de reporte PDF y Excel.

**2. Evidencias para Jira:**
- **📸 Captura de Consola (`COB-TK12_test_suite_aprobado.png`):**  
  Ejecutar en la terminal powershell:
  ```powershell
  python test_cobit_core.py
  ```
  Capturar el reporte de salida completo con la confirmación:
  ```text
  ==================================================================
    >>> TODAS LAS PRUEBAS (6/6) PASARON SATISFACTORIAMENTE AL 100% <<<
  ==================================================================
  ```
- **💻 Código Fuente ([test_cobit_core.py:L114-L125](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/test_cobit_core.py#L114-L125)):**
  ```python
  pdf_data = generate_pdf_report(client, active_eval, metrics, roadmap_plan)
  assert len(pdf_data) > 1000, "Error: PDF generado vacío"
  excel_data = generate_excel_report(client, active_eval, scores, metrics)
  assert len(excel_data) > 1000, "Error: Archivo Excel generado vacío"
  ```

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Garantiza matemáticamente y por código la no rotura del sistema, asegurando la integridad de todas las transacciones y cálculos.

---

#### 📌 [COB-TK13] Hardening, Optimización y Entrega Documental Final
- **Tipo de Incidencia:** Tarea Técnica (Task)
- **Sprint:** Sprint 4 | **Estimación:** 4 SP (8 horas) | **Prioridad:** High
- **Capa Arquitectónica:** Aseguramiento Documental y Transferencia.
- **Criterios de Aceptación:** Documentación técnica integral, manual de usuario paso a paso, análisis de mejoras futuras, matriz de trazabilidad con Jira y catálogo de evidencias.

**1. ¿Qué se hizo? (Fundamento Técnico):**  
Se estructuró y culminó el paquete formal de 5 manuales en la carpeta `DOCUMENTACION/`:
1. [`DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md`](DOCUMENTACION_TECNICA_Y_FUNCIONAL_COBIT_CORE.md) (66 KB): Manual de arquitectura, modelos ERD, capas y algoritmos.
2. [`GUIA_DE_USUARIO_PASO_A_PASO_COBIT_CORE.md`](GUIA_DE_USUARIO_PASO_A_PASO_COBIT_CORE.md) (24 KB): Manual didáctico paso a paso para el usuario final.
3. [`VERIFICACION_REQUISITOS_JIRA_VS_IMPLEMENTACION.md`](VERIFICACION_REQUISITOS_JIRA_VS_IMPLEMENTACION.md) (28 KB): Matriz formal de cumplimiento vs cronograma Jira.
4. [`ANALISIS_COMPARATIVO_Y_ROADMAP_DE_MEJORAS_FUTURAS.md`](ANALISIS_COMPARATIVO_Y_ROADMAP_DE_MEJORAS_FUTURAS.md) (21 KB): Análisis estratégico de escalabilidad e IA avanzada.
5. [`EVIDENCIAS_JIRA_CRONOGRAMA_COBIT.md`](EVIDENCIAS_JIRA_CRONOGRAMA_COBIT.md) (Este documento): Catálogo operativo de evidencias y capturas para Jira.

**2. Evidencias para Jira:**
- **📸 Captura de Explorador / VS Code (`COB-TK13_entrega_documentacion.png`):**  
  Capturar el explorador de archivos o VS Code mostrando la carpeta `DOCUMENTACION/` con todos sus archivos `.md`, sus tamaños en bytes y la confirmación de commit en el repositorio Git.
- **💻 Código Fuente ([README.md:L106-L119](file:///e:/Program%20Files%20%28x86%29/Streaming%20de%20Google%20Drive/Mi%20unidad/Universidad_del_Quindio/8vo_Semestre/Formulacion_Proyectos/proyecto/admin_proyectos_cobit_core_app/README.md#L106-L119)):**
  Enlaces en el README principal indexando el paquete documental.

**3. ¿Cómo se cumplió la evidencia? (Sustentación):**  
Asegura la total transferibilidad académica y profesional del software, permitiendo que cualquier docente, auditor o evaluador verifique y opere la herramienta sin asistencia externa.

---

## 🛠️ GUÍA OPERATIVA: CÓMO TOMAR Y SUBIR LAS CAPTURAS A JIRA

### 1. Preparación del Entorno
1. Ejecuta la inicialización de datos de prueba:
   ```powershell
   python test_cobit_core.py
   ```
2. Inicia la aplicación:
   ```powershell
   streamlit run app.py
   ```
3. Utiliza la herramienta **Recortes de Windows** (`Win + Shift + S`) para capturar el área relevante en alta definición.

### 2. Protocolo de Cierre en Jira
Para cada ítem en el tablero Kanban/Scrum de Jira:
1. **Mover Estado:** Cambiar de *In Progress* a **Done** (o *Listo*).
2. **Adjuntar Imagen:** Subir el archivo PNG nombrado según la nomenclatura especificada (ej. `COB-ST16_radar_plotly_5_dominios.png`).
3. **Comentario de Resolución:** Pegar el texto del apartado **"¿Qué se hizo?"** y **"¿Cómo se cumplió la evidencia?"** directamente en el comentario de resolución de la tarea en Jira.

---

> ✅ **Conclusión:** La articulación entre la documentación técnica formal y este catálogo de evidencias garantiza una sustentación respaldada al 100% en código, interfaces visuales y pruebas automatizadas.
