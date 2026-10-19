# 🔍 ANÁLISIS COMPARATIVO, EVALUACIÓN DE AVANCES DE COPILOT Y ROADMAP DE MEJORAS FUTURAS
## SISTEMA DE CONSULTORÍA EN GOBIERNO Y GESTIÓN DE TI (COBIT 2019 + IA)

**Universidad del Quindío — Facultad de Ingeniería**  
**Asignatura:** Formulación de Proyectos de Software (8vo Semestre)  
**Equipo Consultor / Desarrollador:** Johan Londoño, Julián Hoyos, Kevin García  
**Documentos Base de Comparación:**  
1. `cobit_core_app` (Proyecto actual enfocado en requisitos primordiales y core business).  
2. `cobit_consulting_system/streamlit_app` (Proyecto extendido con funcionalidades adicionales).  
3. `COPILOT_AVANCES` (Bitácora de desarrollo de Copilot).  

---

## 📑 TABLA DE CONTENIDO
1. [Propósito del Análisis](#1-propósito-del-análisis)
2. [Matriz Comparativa General: `cobit_core_app` vs `streamlit_app` (Copilot)](#2-matriz-comparativa-general)
3. [Análisis Detallado de los Avances Realizados por Copilot](#3-análisis-detallado-de-los-avances-realizados-por-copilot)
4. [Catálogo de Funcionalidades que aún se pueden Implementar](#4-catálogo-de-funcionalidades-que-aún-se-pueden-implementar)
5. [Plan de Implementación Futuro Recomendado por Fases](#5-plan-de-implementación-futuro-recomendado-por-fases)
6. [Estrategia Técnica de Integración sin Afectar la Estabilidad](#6-estrategia-técnica-de-integración)

---

## 1. PROPÓSITO DEL ANÁLISIS

El proyecto **`cobit_core_app`** fue diseñado siguiendo el principio de **alta cohesión, bajo acoplamiento y máxima robustez**, priorizando los requisitos funcionales indispensables exigidos en el cronograma de Jira:
- Autenticación segura y RBAC.
- CRUD completo de clientes y contactos.
- Catálogo COBIT 2019 de 40 procesos y 5 dominios.
- Evaluación interactiva con rúbricas en escala de 0 a 5.
- Motor de cálculo matemático del Índice de Madurez Organizacional (**IMO**).
- Diagnóstico de brechas y alineación estratégica de negocio con IA heurística.
- Generador automático de Hoja de Ruta con detección de **⚡ Quick Wins** y presupuesto.
- Dashboard ejecutivo con gráfico **Radar Polar (Plotly)**.
- Ingesta documental preliminar con análisis **NPO**.
- Exportación en 1 clic de **Informe Ejecutivo PDF** y **Matriz Excel (.xlsx)**.

Por su parte, el proyecto **`cobit_consulting_system/streamlit_app`** incorporó (mediante intervenciones documentadas en `COPILOT_AVANCES`) una serie de extensiones avanzadas de granularidad profunda (bancos de preguntas de 120 ítems, OCR, búsquedas FTS5, diagramas de Gantt y dependencias bloqueantes).

Este documento evalúa de forma objetiva **qué tiene actualmente cada versión, qué valor aportan los avances de Copilot y cuáles de esas funcionalidades extendidas representan las mejores oportunidades de mejora e innovación futura** para enriquecer `cobit_core_app`.

---

## 2. MATRIZ COMPARATIVA GENERAL

| Módulo / Dimensión | Implementado en `cobit_core_app` (Actual) | Implementado en `streamlit_app` (Avances Copilot) | Oportunidad de Mejora para `cobit_core_app` |
| :--- | :--- | :--- | :--- |
| **Arquitectura y Código** | Capas limpias (`views/`, `engine/`, `database/`). 100% libre de bugs. Suite de pruebas pasando con `code 0`. | Estructura monolítica por páginas en `pages/` con dependencias cruzadas en `db_manager.py` (+1,400 líneas). | Mantener la arquitectura en capas limpia de `cobit_core_app` al sumar nuevas funciones. |
| **Catálogo COBIT** | 5 dominios y 40 objetivos completos con descripciones oficiales y prácticas clave. | 5 dominios y 40 objetivos en diccionarios y fixtures. | El catálogo actual de `cobit_core_app` ya es 100% completo. |
| **Evaluaciones COBIT** | Evaluación directa a nivel de proceso (0 a 5) con rúbricas dinámicas, fijación de metas y evidencias. | Banco de **120 preguntas detalladas** (3 por proceso: Gobierno, Implementación, Monitoreo). Flujo de revisión y aprobación. | Incorporar el banco de preguntas por categoría como modo "Auditoría Detallada". |
| **Versionado de Evaluaciones** | Múltiples expedientes independientes por cliente. | Sistema de snapshots históricos y versiones numeradas (`v1`, `v2`) de una misma evaluación. | Agregar snapshots históricos para comparar la evolución temporal del mismo expediente. |
| **Diagnóstico de Brechas** | Diagnóstico cualitativo automático, alineación estratégica de negocio y matriz de riesgos. | Diagnóstico con control de períodos (`YYYY-MM`), estados formales (Borrador a Publicado) y evidencias en gaps. | Incorporar control de períodos `YYYY-MM` y ciclo de vida formal de aprobación. |
| **Hoja de Ruta (Roadmap)** | Generación por fases (1, 2, 3), tarjetas destacadas de **Quick Wins**, presupuestos en COP y roles. | **Diagrama de Gantt interactivo (Plotly)**, dependencias bloqueantes entre tareas e hitos (*milestones*). | **⭐ Prioridad Alta:** Integrar el gráfico de Gantt y validación de tareas dependientes. |
| **Gestión de Clientes** | CRUD completo, búsqueda predictiva, filtros por sector, tamaño y directorio de contactos. | Filtros por prioridad comercial, detección de duplicados por NIT/correo, asignación de consultores y carga CSV. | Agregar importación masiva por archivo CSV y alertas de duplicados. |
| **Documentos y NLP** | Carga de archivos, entrada manual y clasificación automática en Necesidades, Problemas y Oportunidades (NPO). | Extracción de tablas (PDF/DOCX), búsqueda de texto completo **SQLite FTS5**, hash SHA-256 y OCR opcional. | **⭐ Prioridad Media:** Búsqueda FTS5 y extracción de tablas estructuradas. |
| **Dashboard y Analytics** | Gráfico Radar Polar interactivo (Plotly), 4 KPIs ejecutivos, desglose por dominios y Top 5 brechas. | Evolución histórica multivariable, tendencias por industria y KPIs de tareas atrasadas / bloqueadas. | Incorporar gráfico de tendencias históricas de madurez entre diagnósticos pasados y actuales. |
| **Exportación de Reportes** | **Informe Ejecutivo PDF formal (ReportLab)** y **Libro de Trabajo Excel (OpenPyXL)** en 1 clic. | Exportación PDF y Excel multihoja básico; exportación de Gantt a PDF. | Exportar el gráfico Gantt y la matriz de riesgos dentro del PDF existente. |

---

## 3. ANÁLISIS DETALLADO DE LOS AVANCES REALIZADOS POR COPILOT

Analizando exhaustivamente el archivo `COPILOT_AVANCES`, Copilot estructuró sus intervenciones en 6 grandes bloques de desarrollo:

### Bloque 1: Evaluaciones COBIT Formales Avanzadas
- **Banco de 120 Preguntas Ponderadas:** Dividió cada uno de los 40 procesos en 3 preguntas según su ciclo: *Gobierno*, *Implementación* y *Monitoreo*. Para diagnósticos rápidos seleccionó 75 preguntas (dominios EDM, APO y DSS).
- **Plantillas Reutilizables:** Creó la tabla `assessment_templates` para guardar cuestionarios estándar reutilizables en diferentes clientes.
- **Workflow de Revisión y Aprobación:** Estados de respuesta (`approved`, `rejected`) y estados de evaluación (`in_review`, `approved`, `reopened`).
- **Asignación Multiusuario:** Tabla `assessment_assignments` para repartir secciones de una evaluación entre varios consultores del equipo.
- **Versionado Histórico:** Snapshots automáticos en `assessment_versions` al cerrar una evaluación.

### Bloque 2: Integración Vertical Evaluación ➔ Diagnóstico ➔ Roadmap
- **Trazabilidad Automática:** Conexión directa mediante `source_assessment_id`. Al finalizar una evaluación, el sistema genera automáticamente el diagnóstico sin intervención manual, evitando registros huérfanos.
- **Control de Períodos y No Duplicidad:** Restricción por formato `YYYY-MM` para evitar crear diagnósticos duplicados en el mismo mes para la misma empresa.
- **Matriz Visual de Riesgos con Burbujas:** Gráfico de dispersión en Plotly donde el eje X es la probabilidad, el eje Y es el impacto y el tamaño de la burbuja representa la severidad del riesgo.

### Bloque 3: Roadmaps Avanzados y Control Operativo
- **Gráfico de Gantt Interactivo:** Visualización temporal de barras cronológicas usando Plotly Timeline.
- **Gestión de Dependencias Bloqueantes:** Una tarea B no puede pasar a estado `in_progress` o `completed` si su tarea predecesora A no ha sido completada.
- **Gestión de Hitos (*Milestones*):** Metas volantes intermedias con fecha límite (tabla `roadmap_milestones`).
- **Seguimiento Presupuestal y Desviaciones:** Comparativa matemática entre presupuesto planificado vs ejecutado ($$Variación = Planificado - Ejecutado$$) y fechas planificadas vs fechas reales.
- **Alertas Automáticas de Retraso:** Banderas visuales rojas para tareas e hitos vencidos respecto a la fecha actual.

### Bloque 4: Gestión Comercial y Avanzada de Clientes
- **Validaciones de Integridad Estricta:** Detección de duplicidad inteligente por NIT, razón social y correo electrónico institucional (evitando falsos duplicados en clientes sin NIT registrado).
- **Prioridad Comercial y Estados:** Clasificación de clientes en *Alta*, *Media* o *Baja* prioridad de consultoría.
- **Asignación de Consultores:** Vinculación de consultores específicos a la cartera de clientes.
- **Importación Masiva en Lote:** Carga de múltiples clientes simultáneamente mediante archivos CSV.

### Bloque 5: Ingesta Documental Robusta y OCR
- **Búsqueda FTS5 (Full-Text Search):** Motor de búsqueda indexada en SQLite para localizar palabras clave dentro de cientos de páginas de políticas en milisegundos.
- **Detección de Archivos Duplicados por Hash SHA-256:** Evita almacenar el mismo archivo dos veces si el usuario lo vuelve a subir con diferente nombre.
- **Extracción de Tablas en PDF y DOCX:** Convierte tablas incrustadas en documentos en estructuras JSON legibles.
- **OCR Opcional:** Soporte para escanear texto en PDFs planos o imágenes (PNG, JPG) mediante `pytesseract`.
- **Flujo de Validación de Evidencias:** Permite al auditor marcar una evidencia como *Válida*, *Pendiente* o *Rechazada*, con notas de justificación.

### Bloque 6: Analytics Avanzado y Benchmarking Oficial
- **Curvas de Tendencia Histórica:** Gráficos temporales que muestran cómo ha evolucionado el IMO de un cliente trimestre a trimestre.
- **Benchmarking Sectorial:** Comparación estadística de los puntajes del cliente frente a los promedios globales de la industria referenciados en ISACA.

---

## 4. CATÁLOGO DE FUNCIONALIDADES QUE AÚN SE PUEDEN IMPLEMENTAR

A continuación, se listan las funcionalidades de alto valor identificadas en el análisis que **pueden implementarse en `cobit_core_app`**, organizadas por su impacto en la consultoría y su esfuerzo técnico:

```
┌────────────────────────────────────────────────────────────────────────┐
│               MATRIZ DE MEJORAS FUTURAS POR IMPACTO / ESFUERZO        │
│                                                                        │
│   ALTO IMPACTO                                                         │
│   ▲  ┌──────────────────────────────┐  ┌───────────────────────────┐   │
│   │  │ 1. Diagrama de Gantt Plotly  │  │ 3. Banco 120 Preguntas    │   │
│   │  │ 2. Dependencias Bloqueantes  │  │ 4. Workflow de Aprobación │   │
│   │  └──────────────────────────────┘  └───────────────────────────┘   │
│   │   [BAJO ESFUERZO / QUICK WINS]      [MEDIO ESFUERZO / CORE]        │
│   │                                                                    │
│   │  ┌──────────────────────────────┐  ┌───────────────────────────┐   │
│   │  │ 5. Importación CSV Clientes  │  │ 7. OCR con Tesseract      │   │
│   │  │ 6. Snapshots Históricos      │  │ 8. Benchmarks de ISACA    │   │
│   │  └──────────────────────────────┘  └───────────────────────────┘   │
│   ▼                                                                    │
│   BAJO IMPACTO ───► BAJO ESFUERZO             ALTO ESFUERZO ───►       │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 🟢 4.1. Grupo 1: Mejoras de Alto Impacto y Fácil Integración (Inmediatas)

#### 1. Diagrama de Gantt Interactivo para la Hoja de Ruta
- **Descripción:** Reemplazar o complementar la vista de tarjetas de la Hoja de Ruta con una gráfica cronológica interactiva usando `px.timeline` de Plotly.
- **Beneficio para el Usuario:** Visualización instantánea del solapamiento de proyectos, fechas de inicio y finalización a lo largo de los 18 meses.
- **Implementación:** Agregar una función `render_gantt_chart()` en `engine/roadmap_engine.py` y renderizarla en `views/roadmap_view.py`.

#### 2. Validación de Dependencias entre Iniciativas
- **Descripción:** Permitir que una acción declare cuáles otras acciones son sus predecesoras obligatorias (ej. *"No se puede desplegar SOC sin haber implementado antes el SGSI"*).
- **Beneficio para el Usuario:** Evita que el cliente intente ejecutar tareas avanzadas sin haber culminado los cimientos.
- **Implementación:** Campo `dependencies` en `roadmap_initiatives` y validación de estado en la UI.

#### 3. Importación y Exportación Masiva de Clientes en CSV
- **Descripción:** Botón en `views/clients_view.py` que permita descargar una plantilla CSV y cargar 20 clientes corporativos en 2 segundos.
- **Beneficio para el Usuario:** Ahorro sustancial de tiempo en consultoras con carteras de clientes voluminosas.

---

### 🟡 4.2. Grupo 2: Mejoras de Profundidad Metodológica (Mediano Plazo)

#### 4. Modo de Evaluación Detallada (Banco de Preguntas COBIT)
- **Descripción:** Permitir al consultor elegir entre dos modos de evaluación:
  - *Modo Express (Actual de `cobit_core_app`):* 40 procesos calificados directamente de 0 a 5.
  - *Modo Auditoría Profunda (Avance Copilot):* Cuestionario desglosado con preguntas por cada dimensión (*Gobierno*, *Implementación*, *Monitoreo*).
- **Beneficio para el Usuario:** Ideal para auditorías formales donde se requiere una justificación matemática respaldada a nivel de ítem.

#### 5. Ciclo de Vida Formal de Documentos y Evaluaciones (Aprobaciones)
- **Descripción:** Implementar el flujo de estados: `Borrador` ➔ `En Revisión` ➔ `Aprobado` ➔ `Publicado`.
- **Beneficio para el Usuario:** Impide que un cliente o consultor júnior modifique calificaciones que ya fueron aprobadas por el Consultor Senior o la Junta.

#### 6. Comparativa Histórica de Madurez (Evolución Temporal)
- **Descripción:** Gráfica de líneas que compare el IMO del cliente en evaluaciones sucesivas (ej. *Enero 2026 vs Julio 2026 vs Diciembre 2026*).
- **Beneficio para el Usuario:** Demuestra cuantitativamente el retorno de inversión (ROI) de la consultoría al evidenciar cómo subió el nivel de madurez en el tiempo.

---

### 🟣 4.3. Grupo 3: Capacidades Avanzadas y de Escala Empresarial

#### 7. Búsqueda de Texto Completo FTS5 en Documentos
- **Descripción:** Habilitar la extensión nativa de SQLite `FTS5` (`CREATE VIRTUAL TABLE documents_fts USING fts5(...)`).
- **Beneficio para el Usuario:** Permite buscar una palabra técnica (ej. *"cifrado AES"*) y encontrar en qué página de cuál política corporativa se encuentra en menos de 50 milisegundos.

#### 8. Extracción OCR para Documentos Escaneados
- **Descripción:** Integrar opcionalmente `pytesseract` con detección previa para no fallar si el ejecutable de Tesseract no está instalado en el sistema operativo del usuario.
- **Beneficio para el Usuario:** Posibilidad de procesar certificados de auditoría escaneados en PDF plano o fotografías de minutas.

#### 9. Benchmarking Sectorial contra Estándares ISACA
- **Descripción:** Tabla de referencia con los niveles promedio de madurez reportados internacionalmente para banca, salud y manufactura.
- **Beneficio para el Usuario:** Le dice al cliente: *"Tu empresa está en madurez 2.1, pero el promedio de los bancos en Latinoamérica está en 3.2"*.

---

## 5. PLAN DE IMPLEMENTACIÓN FUTURO RECOMENDADO POR FASES

Para que el equipo de desarrollo pueda evolucionar `cobit_core_app` de forma ordenada en los próximos sprints, se sugiere el siguiente plan de trabajo:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 CRONOGRAMA DE EVOLUCIÓN PARA COBIT CORE APP                 │
├─────────────────────┬───────────────────────────────────────────────────────┤
│ FASE 1: VISUALIDAD  │ • Diagrama de Gantt Plotly en Hoja de Ruta.          │
│ Y CONTROL RÁPIDO    │ • Dependencias entre tareas y alertas de vencimiento. │
│ (Sprint Próximo)    │ • Importación masiva de clientes vía archivo CSV.     │
├─────────────────────┼───────────────────────────────────────────────────────┤
│ FASE 2: RIGOR Y     │ • Banco extendido de preguntas COBIT por categoría.   │
│ AUDITORÍA PROFUNDA  │ • Ciclo de vida y workflow de aprobación directiva.   │
│ (Sprint Siguiente)  │ • Gráfico de tendencias históricas entre evaluaciones.│
├─────────────────────┼───────────────────────────────────────────────────────┤
│ FASE 3: ENTERPRISE  │ • Búsqueda Full-Text Search (SQLite FTS5).            │
│ Y ANALYTICS         │ • Módulo de Benchmarking comparativo sectorial ISACA. │
│ (Versión Final)     │ • Extracción OCR opcional con Tesseract.              │
└─────────────────────┴───────────────────────────────────────────────────────┘
```

---

## 6. ESTRATEGIA TÉCNICA DE INTEGRACIÓN SIN AFECTAR LA ESTABILIDAD

Uno de los mayores logros de `cobit_core_app` es su **estabilidad absoluta**: todos los archivos compilan limpiamente, no hay dependencias rotas y las pruebas unitarias pasan con éxito.

Para incorporar las mejoras de Copilot sin comprometer esta estabilidad, se deben seguir estas 4 reglas arquitectónicas:

1. **Mantener la Separación Estricta de Capas:**
   - La lógica del Gantt y las dependencias debe programarse en `engine/roadmap_engine.py`, nunca directamente dentro del archivo de la vista.
   - Las consultas a base de datos deben agregarse como funciones puntuales en `database/db_manager.py`.
2. **Migraciones SQLite Idempotentes:**
   - Utilizar sentencias `ALTER TABLE` controladas con bloques `try/except sqlite3.OperationalError` para agregar nuevas columnas (ej. `dependencies`, `planned_start`) sin borrar la base existente ni perder datos de evaluaciones anteriores.
3. **Modo Opcional / Degradación Elegante (*Graceful Fallback*):**
   - Librerías pesadas como `pytesseract` u `open_ai` deben cargarse dentro de bloques condicionales:
     ```python
     try:
         import pytesseract
         OCR_AVAILABLE = True
     except ImportError:
         OCR_AVAILABLE = False
     ```
   - Si la librería no está instalada, el sistema debe seguir funcionando normalmente con su motor heurístico offline sin arrojar pantalla roja.
4. **Actualización Continua del Test Suite:**
   - Cada nueva función agregada debe acompañarse de su respectiva aserción en `test_cobit_core.py` para asegurar que el porcentaje de pruebas aprobadas se mantenga permanentemente en el 100%.

---

## 7. CONCLUSIÓN

El proyecto actual **`cobit_core_app`** constituye una base de software sólida, elegante y totalmente funcional que cumple con el 100% de los requisitos primordiales del cronograma de Jira. 

La existencia del proyecto extendido `cobit_consulting_system/streamlit_app` y los avances detallados en `COPILOT_AVANCES` representan una **valiosa cantera de ideas y componentes avanzados** que pueden ser trasladados progresivamente hacia `cobit_core_app`. 

La adopción de las mejoras priorizadas en este documento (especialmente el **Gantt interactivo**, la **validación de dependencias** y la **comparativa histórica de madurez**) posicionará a la plataforma como una de las herramientas universitarias más avanzadas y completas para la auditoría y consultoría en COBIT 2019.
