# 🏛️ MANUAL TÉCNICO, ARQUITECTURA Y ESPECIFICACIÓN FUNCIONAL
## SISTEMA DE CONSULTORÍA EN GOBIERNO Y GESTIÓN DE TI (COBIT 2019 + IA) — CORE APP

**Universidad del Quindío — Facultad de Ingeniería**  
**Programa:** Ingeniería de Sistemas y Computación  
**Asignatura:** Formulación de Proyectos de Software (8vo Semestre)  
**Equipo Consultor / Desarrollador:** Johan Londoño, Julián Hoyos, Kevin García  
**Marco de Referencia:** COBIT 2019 (ISACA) & Cronograma Jira (`CRONOGRAMA_REQUISITOS_JIRA_COBIT.txt`)

---

## 📑 TABLA DE CONTENIDO
1. [Resumen Ejecutivo y Propósito del Sistema](#1-resumen-ejecutivo-y-propósito-del-sistema)
2. [Arquitectura del Sistema y Flujo de Comunicación](#2-arquitectura-del-sistema-y-flujo-de-comunicación)
   - 2.1. [Propósito de la Arquitectura](#21-propósito-de-la-arquitectura)
   - 2.2. [Diagrama General de Arquitectura por Capas y Módulos](#22-diagrama-general-de-arquitectura-por-capas-y-módulos)
   - 2.3. [Recorrido de las Solicitudes y Respuestas](#23-recorrido-de-las-solicitudes-y-respuestas-ciclo-de-vida-de-petición)
   - 2.4. [Leyenda de Conexiones, Tipos de Línea y Código de Colores](#24-leyenda-de-conexiones-tipos-de-línea-y-código-de-colores)
   - 2.5. [Suposiciones Relevantes de Arquitectura](#25-suposiciones-relevantes-de-arquitectura)
   - 2.6. [Componentes Estructurales Preexistentes](#26-componentes-estructurales-preexistentes)
3. [Flujo de Datos y Comunicación entre Módulos](#3-flujo-de-datos-y-comunicación-entre-módulos)
4. [Catálogo Detallado de Funcionalidades (Lo que puede hacer el Usuario)](#4-catálogo-detallado-de-funcionalidades-lo-que-puede-hacer-el-usuario)
5. [Modelos y Tipos de Datos del Sistema](#5-modelos-y-tipos-de-datos-del-sistema)
   - 5.1. [Diccionario de Datos Relacionales (SQLite)](#51-diccionario-de-datos-relacionales-sqlite-cobit_coredb)
   - 5.2. [Estructuras de Datos en Memoria](#52-estructuras-de-datos-en-memoria-python-engine)
   - 5.3. [Modelo de datos de la base de datos](#53-modelo-de-datos-de-la-base-de-datos)
6. [Motores de Cálculo y Algoritmos Matemáticos](#6-motores-de-cálculo-y-algoritmos-matemáticos)
7. [Guía de Ejecución, Roles y Pruebas Automatizadas](#7-guía-de-ejecución-roles-y-pruebas-automatizadas)

---

## 1. RESUMEN EJECUTIVO Y PROPÓSITO DEL SISTEMA

El **COBIT Core Consulting System** es una plataforma web y analítica diseñada para automatizar el ciclo integral de consultoría en Gobierno y Gestión de Tecnologías de Información basándose en las directrices oficiales de **COBIT 2019 (ISACA)**.

El sistema resuelve la problemática tradicional de las evaluaciones de madurez de TI: procesos manuales en hojas de cálculo propensas a errores, ausencia de trazabilidad probatoria, dificultad para traducir debilidades operativas en valor de negocio y demoras excesivas en la formulación de hojas de ruta de transformación digital.

### Objetivos Primordiales Cumplidos:
- **Centralización Corporativa:** Gestión estructurada de clientes empresariales clasificados por sector económico y tamaño.
- **Rigor Metodológico COBIT 2019:** Integración de los 5 dominios oficiales (**EDM, APO, BAI, DSS, MEA**) y los 40 objetivos de gobierno y gestión.
- **Medición Cuantitativa Estandarizada:** Evaluación en escala de capacidad 0 a 5 con cálculo automatizado del **Índice de Madurez Organizacional (IMO)**.
- **Inteligencia Analítica y NLP:** Diagnóstico heurístico de brechas (*Gaps*), extracción de Necesidades, Problemas y Oportunidades (**NPO**) desde documentos y alineación estratégica de metas del negocio a TI.
- **Planificación Estratégica:** Generación automática de hojas de ruta secuenciadas en 3 fases temporales con priorización de **Quick Wins** e inversión estimada.
- **Entregables Ejecutivos de Alto Impacto:** Tableros visuales con gráficos Radar Plotly y exportación directa de informes en **PDF formal** y hojas de cálculo **Excel (.xlsx)**.

---

## 2. ARQUITECTURA DEL SISTEMA Y FLUJO DE COMUNICACIÓN

> [!NOTE]
> **Alcance y Precisión Arquitectónica:** Conforme a las directrices metodológicas de diseño por capas y tras contrastar los procesos y funcionalidades del sistema, esta sección formaliza la **Arquitectura Lógica Modular por Capas** del **COBIT Core Consulting System (COBIT 2019 + IA)**. Se modelan los 3 perfiles de usuario, las 8 vistas de presentación, el orquestador reactivo de aplicación, los 5 motores de lógica de negocio, la capa de acceso a datos (DAL), la persistencia relacional SQLite y los servicios externos de generación documental y visualización.

### 2.1. Propósito de la Arquitectura
El propósito primordial de esta arquitectura es desacoplar las responsabilidades funcionales y técnicas del sistema en una estructura por capas estricta y modular. Esto garantiza:
1. **Separación de Responsabilidades (SoC):** La interfaz de usuario (`views/`) desconoce los detalles de persistencia SQL, interactuando únicamente a través del orquestador central (`app.py`) y los motores de cálculo (`engine/`).
2. **Determinismo y Testabilidad:** Toda la lógica matemática (cálculo de IMO [COB-TK08], priorización de hojas de ruta [COB-TK10], diagnóstico de brechas y minería NPO) reside en funciones puras e independientes de Streamlit, permitiendo la ejecución de suites de prueba automatizadas sin levantar la interfaz gráfica.
3. **Seguridad y Control de Acceso:** La coordinación de peticiones aplica control de acceso basado en roles (**RBAC**) y protección criptográfica (hashing SHA-256), mientras que la capa de persistencia asegura transacciones ACID y protección contra inyección SQL mediante consultas parametrizadas.
4. **Integración Desacoplada de Servicios:** Los generadores de documentos (PDF ejecutivo con ReportLab y hojas de cálculo con OpenPyXL) operan como servicios utilitarios que producen flujos de bytes en memoria (`io.BytesIO`), evitando escrituras temporales en disco y optimizando el rendimiento.

---

### 2.2. Diagrama General de Arquitectura por Capas y Módulos

El siguiente diagrama en sintaxis **Mermaid (`flowchart TB`)** ilustra la organización por capas, los componentes modulares y el flujo bidireccional de comunicación entre actores, interfaz, controladores, lógica de negocio, persistencia y servicios externos:

```mermaid
flowchart TB
    %% ==========================================
    %% CAPA 1: USUARIOS Y SISTEMAS DE ENTRADA
    %% ==========================================
    subgraph CAPA1["Capa 1: Usuarios y Sistemas de Entrada"]
        U_ADMIN["👑 Superadministrador<br/>(Admin: Configuración y Auditoría)"]
        U_CONS["💼 Consultor Líder<br/>(Evaluador: Operación y Análisis)"]
        U_CLI["🏢 Cliente Corporativo<br/>(Directivo / CIO: Consulta y KPIs)"]
        DISPOSITIVOS["💻 Dispositivos de Acceso<br/>(Navegador Web Desktop / Portátil / Tablet)"]
    end

    %% ==========================================
    %% CAPA 2: PRESENTACIÓN E INTERFACES DE USUARIO
    %% ==========================================
    subgraph CAPA2["Capa 2: Presentación e Interfaces de Usuario (Views)"]
        V_DASH["📊 Dashboard y Radar Polar<br/>(views/dashboard_view.py)"]
        V_CLI["🏢 Gestión de Clientes y Contactos<br/>(views/clients_view.py)"]
        V_CAT["📚 Catálogo COBIT 2019 (40 Proc)<br/>(views/catalog_view.py)"]
        V_ASS["📝 Cuestionario de Madurez 0-5<br/>(views/assessment_view.py)"]
        V_DIAG["🤖 Diagnóstico y Asistente IA<br/>(views/diagnosis_view.py)"]
        V_ROAD["🗺️ Hoja de Ruta Estratégica<br/>(views/roadmap_view.py)"]
        V_DOCS["📄 Ingesta Documental NLP<br/>(views/documents_view.py)"]
        V_REP["📥 Centro de Reportes Formales<br/>(views/reports_view.py)"]
    end

    %% ==========================================
    %% CAPA 3: APLICACIÓN Y COORDINACIÓN
    %% ==========================================
    subgraph CAPA3["Capa 3: Aplicación y Coordinación de Solicitudes"]
        ROUTER["⚙️ Orquestador Central de Aplicación (app.py)<br/>• Enrutamiento dinámico de vistas y ciclo de vida<br/>• Control de acceso RBAC y autenticación SHA-256<br/>• Gestión de contexto de sesión reactivo (st.session_state)<br/>• Sanitización y validación formal de entradas"]
    end

    %% ==========================================
    %% CAPA 4: LÓGICA DE NEGOCIO Y MÓDULOS FUNCIONALES
    %% ==========================================
    subgraph CAPA4["Capa 4: Lógica de Negocio y Módulos Funcionales (Engine)"]
        M_MAT["📐 Motor de Madurez y Gobernanza<br/>(maturity_engine.py)<br/>Algoritmo IMO [TK08], salud y riesgo"]
        M_AI["🧠 Motor de Inteligencia y NLP<br/>(ai_engine.py)<br/>Detección de brechas y minería NPO"]
        M_ROAD["📈 Motor de Hoja de Ruta Estratégica<br/>(roadmap_engine.py)<br/>Priorización [TK10], Quick Wins y fases"]
        M_DATA["🏛️ Catálogo Maestro COBIT 2019<br/>(cobit_data.py)<br/>40 objetivos oficiales y 5 dominios"]
        M_EXP["📦 Motor de Entregables y Exportación<br/>(export_engine.py)<br/>Formateo y estructura ejecutiva"]
    end

    %% ==========================================
    %% CAPA 5: ACCESO A DATOS Y PERSISTENCIA (DAL)
    %% ==========================================
    subgraph CAPA5["Capa 5: Acceso a Datos y Persistencia (DAL)"]
        DAL_MGR["🔌 Capa de Persistencia (db_manager.py)<br/>• Pool y transacciones SQLite seguras con contextmanager<br/>• Integridad referencial activa (PRAGMA foreign_keys = ON)<br/>• Consultas SQL parametrizadas contra inyección SQL<br/>• Inicialización DDL y sembrado de datos idempotente"]
    end

    %% ==========================================
    %% CAPA 6: BASE DE DATOS RELACIONAL
    %% ==========================================
    subgraph CAPA6["Capa 6: Base de Datos Relacional (Storage)"]
        DB_SQL[("💾 Base de Datos SQLite (cobit_core.db)<br/>• users: Credenciales, nombres y roles<br/>• clients & client_contacts: Empresas y actores<br/>• assessments & assessment_scores: Evaluaciones e IMO<br/>• roadmaps & roadmap_initiatives: Planes de acción<br/>• documents: Metadatos y evidencias NLP")]
    end

    %% ==========================================
    %% CAPA 7: SERVICIOS E INTEGRACIONES DE SALIDA
    %% ==========================================
    subgraph CAPA7["Capa 7: Servicios e Integraciones de Salida"]
        EXT_PDF["📄 Motor PDF (ReportLab)<br/>Compilación formal de reportes ejecutivos"]
        EXT_XLS["📊 Motor Excel (OpenPyXL / Pandas)<br/>Generación de matrices de madurez .xlsx"]
        EXT_PLOT["📈 Motor Plotly.js / Streamlit<br/>Renderizado interactivo de gráficos radar polar"]
        EXT_PARSE["📑 Parsers PyPDF / Python-Docx<br/>Extracción de texto para minería NLP"]
        EXT_AI["🌐 Motor IA / NLP Externo (Opcional)<br/>Servicio de modelos LLM vía API segura"]
    end

    %% ==========================================
    %% CONEXIONES Y FLUJOS ENTRE CAPAS
    %% ==========================================
    %% Capa 1 -> Capa 2
    U_ADMIN -->|"Sesión administrativa (RBAC)"| DISPOSITIVOS
    U_CONS -->|"Sesión consultor / evaluador"| DISPOSITIVOS
    U_CLI -->|"Sesión cliente corporativo"| DISPOSITIVOS
    DISPOSITIVOS -->|"Renderiza / Interactúa"| V_DASH
    DISPOSITIVOS -->|"Renderiza / Interactúa"| V_CLI
    DISPOSITIVOS -->|"Renderiza / Interactúa"| V_ASS
    DISPOSITIVOS -->|"Renderiza / Interactúa"| V_DIAG
    DISPOSITIVOS -->|"Renderiza / Interactúa"| V_ROAD
    DISPOSITIVOS -->|"Renderiza / Interactúa"| V_DOCS
    DISPOSITIVOS -->|"Renderiza / Interactúa"| V_REP
    DISPOSITIVOS -->|"Renderiza / Interactúa"| V_CAT

    %% Capa 2 -> Capa 3
    V_DASH -->|"Solicitud de KPIs"| ROUTER
    V_CLI -->|"CRUD clientes"| ROUTER
    V_CAT -->|"Consulta procesos"| ROUTER
    V_ASS -->|"Guarda calificaciones"| ROUTER
    V_DIAG -->|"Solicita análisis IA"| ROUTER
    V_ROAD -->|"Solicita generar plan"| ROUTER
    V_DOCS -->|"Carga actas/auditorías"| ROUTER
    V_REP -->|"Solicita reporte"| ROUTER

    %% Capa 3 -> Capa 4
    ROUTER -->|"1. Despacha cálculo IMO y salud"| M_MAT
    ROUTER -->|"2. Despacha análisis semántico y NPO"| M_AI
    ROUTER -->|"3. Despacha algoritmo priorización"| M_ROAD
    ROUTER -->|"4. Consulta catálogo 40 procesos"| M_DATA
    ROUTER -->|"5. Solicita compilación de informe"| M_EXP

    %% Capa 4 -> Capa 5
    M_MAT -->|"Consulta / Actualiza puntajes"| DAL_MGR
    M_ROAD -->|"Registra planes e iniciativas"| DAL_MGR
    M_AI -->|"Consulta textos y evidencias"| DAL_MGR
    ROUTER -->|"CRUD usuarios, clientes y empresas"| DAL_MGR

    %% Capa 5 -> Capa 6
    DAL_MGR -->|"Ejecución SQL (INSERT / UPDATE / SELECT)"| DB_SQL
    DB_SQL -.->|"Retorno de tuplas y registros"| DAL_MGR

    %% Retorno de DAL a Capa 4 y Capa 3
    DAL_MGR -.->|"Devuelve entidades y registros persistidos"| ROUTER

    %% Capa 4 -> Capa 7 (Servicios de Salida)
    M_EXP -->|"Compila informe binario en memoria"| EXT_PDF
    M_EXP -->|"Genera matriz analítica tabular"| EXT_XLS
    ROUTER -->|"Alimenta coordenadas polares"| EXT_PLOT
    M_AI -->|"Extrae texto crudo estructurado"| EXT_PARSE
    M_AI -.->|"Consumo seguro opcional vía API"| EXT_AI

    %% Retornos hacia Capa 2 y Usuario
    ROUTER -.->|"Actualiza st.session_state y re-renderiza"| V_DASH
    ROUTER -.->|"Retorna buffer de descarga (BytesIO)"| V_REP
    V_DASH -.->|"Presenta KPIs y radar en pantalla"| DISPOSITIVOS
    V_REP -.->|"Entrega archivo formal descargable"| DISPOSITIVOS

    %% ==========================================
    %% ESTILOS VISUALES POR CAPAS
    %% ==========================================
    classDef c1 fill:#E1F5FE,stroke:#0288D1,stroke-width:2px,color:#01579B;
    classDef c2 fill:#EDE7F6,stroke:#5E35B1,stroke-width:2px,color:#311B92;
    classDef c3 fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20;
    classDef c4 fill:#FFF8E1,stroke:#F57C00,stroke-width:2px,color:#E65100;
    classDef c5 fill:#FCE4EC,stroke:#C2185B,stroke-width:2px,color:#880E4F;
    classDef c6 fill:#E0F2F1,stroke:#00796B,stroke-width:2px,color:#004D40;
    classDef c7 fill:#ECEFF1,stroke:#455A64,stroke-width:2px,color:#263238;

    class U_ADMIN,U_CONS,U_CLI,DISPOSITIVOS c1;
    class V_DASH,V_CLI,V_CAT,V_ASS,V_DIAG,V_ROAD,V_DOCS,V_REP c2;
    class ROUTER c3;
    class M_MAT,M_AI,M_ROAD,M_DATA,M_EXP c4;
    class DAL_MGR c5;
    class DB_SQL c6;
    class EXT_PDF,EXT_XLS,EXT_PLOT,EXT_PARSE,EXT_AI c7;
```

---

### 2.3. Recorrido de las Solicitudes y Respuestas (Ciclo de Vida de Petición)

Para garantizar la comprensión integral de la dinámica operativa del sistema, a continuación se describen los cuatro flujos más representativos de solicitud y respuesta:

#### Flujo 1: Evaluación de Madurez y Recálculo del IMO en Tiempo Real
1. **Petición del Usuario:** El Consultor Líder ajusta el control deslizante (*slider*) de madurez del proceso `EDM01` de nivel 2 a nivel 4 e ingresa el hallazgo de auditoría en `views/assessment_view.py`. Al presionar el botón *"💾 Guardar Calificaciones y Recalcular"*, la vista emite un evento al coordinador.
2. **Coordinación y Validación:** El Orquestador Central (`app.py`) verifica que el usuario posea el rol `consultant` o `admin`, sanitiza los puntajes recibidos y actualiza el diccionario contextual en memoria.
3. **Procesamiento de Negocio:** `app.py` delega el cálculo matemático a `maturity_engine.py:calculate_assessment_metrics()`, el cual ejecuta el algoritmo del Índice de Madurez Organizacional (**IMO**), computando el promedio ponderado por dominios (**EDM, APO, BAI, DSS, MEA**), el porcentaje de Salud de Gobernanza y el índice de Exposición al Riesgo de TI.
4. **Persistencia Transaccional:** `app.py` invoca la capa de persistencia `database/db_manager.py:save_all_assessment_scores()`, la cual abre una transacción ACID, ejecuta `UPDATE` parametrizados sobre la tabla `assessment_scores` y actualiza el campo `overall_score` en la tabla `assessments`.
5. **Retorno y Re-renderizado:** La base de datos confirma la transacción; `app.py` actualiza las métricas en `st.session_state` y redirige el flujo hacia la interfaz, donde `views/dashboard_view.py` recibe los nuevos valores e invoca a `Plotly.js` para redibujar el polígono polar radar y actualizar los KPIs de forma instantánea.

#### Flujo 2: Ingesta Documental y Minería Heurística de NPO (NLP)
1. **Carga del Archivo:** En `views/documents_view.py`, el usuario sube un archivo de informe de auditoría (`.pdf` o `.docx`).
2. **Extracción y Normalización:** La vista transfiere el flujo binario a `ai_engine.py`, el cual utiliza los parsers documentales (`pypdf` o `python-docx`) para extraer el texto plano sin estructurar y eliminar ruido textual.
3. **Minería de Texto:** El motor aplica análisis heurístico con expresiones regulares y diccionarios de patrones para clasificar los hallazgos en la matriz **NPO (Necesidades, Problemas, Oportunidades)** y mapearlos contra los 40 objetivos COBIT 2019.
4. **Almacenamiento de Evidencias:** `db_manager.py:save_document()` registra el archivo en la tabla `documents` vinculándolo con el `client_id` y `assessment_id` activo.
5. **Presentación de Resultados:** La interfaz muestra la tabla de hallazgos NPO extraídos, resaltando las alertas críticas para consideración del consultor.

#### Flujo 3: Generación Algorítmica de la Hoja de Ruta (Roadmap)
1. **Solicitud de Generación:** El consultor ingresa a `views/roadmap_view.py` y activa la formulación del plan de transformación.
2. **Procesamiento Multi-criterio:** `roadmap_engine.py:generate_roadmap_plan()` consulta las brechas activas de madurez ($Gap = Meta - Actual$) y aplica la fórmula de priorización multi-criterio [COB-TK10]:
   $$\text{Score} = (\text{Brecha} \times 0.40) + (\text{Impacto} \times 0.35) + (\text{Riesgo} \times 0.25)$$
3. **Clasificación y Presupuesto:** El motor segrega las iniciativas con esfuerzo bajo y alto impacto como **Quick Wins**, asigna costos base de consultoría e inversión tecnológica, y distribuye las actividades en 3 fases temporales (0-6 meses, 6-12 meses, 12-24 meses).
4. **Persistencia Estructurada:** La capa DAL (`save_roadmap()`) guarda el encabezado en `roadmaps` y cada iniciativa en `roadmap_initiatives`.
5. **Renderizado Visual:** La vista presenta las tarjetas visuales por fase, los presupuestos estimados y los gráficos de distribución de iniciativas.

#### Flujo 4: Compilación y Descarga de Entregables Ejecutivos (PDF / Excel)
1. **Petición de Exportación:** En `views/reports_view.py`, el usuario presiona *"Descargar Informe Ejecutivo Formal (PDF)"*.
2. **Recolección de Información:** `app.py` recupera de `db_manager.py` los datos completos de la empresa cliente, la evaluación de madurez, las calificaciones de los 40 procesos y la hoja de ruta generada.
3. **Compilación Documental:** `export_engine.py:generate_pdf_report()` activa la librería `ReportLab`, generando programáticamente la portada institucional, las tablas estilizadas de madurez y el cronograma del roadmap dentro de un búfer de memoria (`io.BytesIO`).
4. **Entrega de Archivo:** El búfer binario es devuelto a Streamlit, el cual provee el botón de descarga nativo del navegador, permitiendo al usuario guardar el archivo localmente sin persistencia residual en el servidor.

---

### 2.4. Leyenda de Conexiones, Tipos de Línea y Código de Colores

Para facilitar la interpretación inequívoca del diagrama de arquitectura, se detalla la semántica de la simbología empleada:

| Elemento Visual | Sintaxis Mermaid | Significado Arquitectónico |
| :--- | :--- | :--- |
| **Flecha Sólida (`-->`)** | `A -->\|Etiqueta\| B` | **Flujo Síncrono Directo / Comando:** Representa una invocación directa, envío de eventos, operaciones de escritura SQL o peticiones dirigidas al controlador. |
| **Flecha Punteada (`-.->`)** | `A -.->\|Etiqueta\| B` | **Flujo de Retorno / Renderizado:** Representa la entrega de datos procesados, retorno de registros relacionales, actualización del estado en memoria o entrega de archivos descargables. |
| **Nodos Rectangulares (`[...]`)** | `ID["Texto"]` | Componentes de software, controladores, vistas o módulos de lógica de negocio. |
| **Nodos Cilíndricos (`[(...)]`)** | `ID[("Texto")]` | Componentes de persistencia física y almacenamiento en base de datos relacional. |

#### Código de Colores por Capas:
- 🔵 **Azul Claro (`#E1F5FE` / `#0288D1`):** *Capa 1 — Usuarios y Sistemas de Entrada.* Representa los actores humanos y los dispositivos de cliente.
- 🟣 **Púrpura Suave (`#EDE7F6` / `#5E35B1`):** *Capa 2 — Presentación (Views).* Identifica las interfaces y pantallas especializadas del sistema.
- 🟢 **Verde Esmeralda (`#E8F5E9` / `#2E7D32`):** *Capa 3 — Aplicación y Coordinación.* Destaca el orquestador central (`app.py`), responsable de la seguridad y el enrutamiento.
- 🟠 **Ámbar / Naranja (`#FFF8E1` / `#F57C00`):** *Capa 4 — Lógica de Negocio y Motores (Engine).* Identifica los algoritmos matemáticos puros y los catálogos metodológicos.
- 🔴 **Rosa / Magenta (`#FCE4EC` / `#C2185B`):** *Capa 5 — Acceso a Datos (DAL).* Destaca el módulo de persistencia y abstracción SQL.
- 🟢 **Verde Azulado / Teal (`#E0F2F1` / `#00796B`):** *Capa 6 — Base de Datos Relacional.* Representa el almacenamiento en disco SQLite 3.
- ⚫ **Gris Pizarra (`#ECEFF1` / `#455A64`):** *Capa 7 — Servicios e Integraciones de Salida.* Representa motores externos y bibliotecas de formato.

---

### 2.5. Suposiciones Relevantes de Arquitectura

1. **Propuesta Lógica vs. Ejecución Física:** La arquitectura propuesta organiza lógicamente el sistema en siete capas bien diferenciadas. En el despliegue físico actual, la aplicación se ejecuta como un servicio monolítico modular en Python 3.10+, donde las capas residen en el mismo entorno de ejecución pero mantienen fronteras de código estrictamente desacopladas mediante módulos de software.
2. **Gestión de Estado en Memoria (Stateful UI):** Dado el modelo reactivo de Streamlit, la coordinación de solicitudes apoya la continuidad del usuario en `st.session_state`, garantizando que variables como la empresa cliente activa (`active_client_id`) y la evaluación en curso (`active_assessment_id`) no requieran ser reconsultadas en cada ciclo de vida visual.
3. **Persistencia Local Relacional:** El sistema utiliza SQLite 3 (`cobit_core.db`) como motor de base de datos relacional embebido, garantizando cero configuración y portabilidad absoluta. La integridad referencial se fuerza explícitamente en cada conexión mediante `PRAGMA foreign_keys = ON`.
4. **Desacoplamiento Estricto de Motores:** La capa de lógica de negocio (`engine/`) no tiene dependencias cruzadas con la capa de presentación (`views/` ni `streamlit`). Esto permite que los motores puedan reutilizarse en interfaces de línea de comandos (CLI), APIs REST futuras o suites de integración continua.
5. **Operaciones de Exportación Efímeras:** Los motores de generación documental (ReportLab y OpenPyXL) trabajan exclusivamente con flujos de bytes en memoria (`io.BytesIO`), garantizando que los archivos generados no consuman espacio en disco ni expongan información corporativa confidencial en directorios temporales del servidor.
6. **IA Híbrida (Heurística Local + Proveedor Opcional):** El procesamiento de lenguaje natural (NLP) opera de manera autónoma y determinística utilizando heurística local de expresiones regulares y taxonomía COBIT, con la arquitectura preparada para delegar inferencias complejas a modelos LLM externos (OpenAI o Google Gemini) mediante interfaces abstractas y seguras.

---

### 2.6. Componentes Estructurales Preexistentes

La aplicación adopta una arquitectura modular desacoplada en tres capas fundamentales (**Layered Architecture**), asegurando separación estricta de responsabilidades, alta mantenibilidad y portabilidad:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   CAPA 1: PRESENTACIÓN E INTERFAZ (VIEWS)              │
│  app.py (Router & Session State) | custom.css (Design System Moderno)  │
│  ┌───────────────┬────────────────┬────────────────┬────────────────┐  │
│  │ Dashboard View│  Clients View  │  Catalog View  │ Assessment View│  │
│  ├───────────────┼────────────────┼────────────────┼────────────────┤  │
│  │ Diagnosis View│  Roadmap View  │ Documents View │  Reports View  │  │
│  └───────────────┴────────────────┴────────────────┴────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Invoca servicios y pasa estado
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               CAPA 2: LÓGICA DE NEGOCIO Y MOTORES (ENGINE)             │
│  ┌───────────────────────┬───────────────────────┬──────────────────┐  │
│  │ cobit_data.py         │ maturity_engine.py    │ ai_engine.py     │  │
│  │ (40 procesos COBIT)   │ (Algoritmo IMO [TK08])│ (NLP NPO & Gaps) │  │
│  ├───────────────────────┴───────────────────────┴──────────────────┤  │
│  │ roadmap_engine.py ([COB-TK10] Multi-criterio & Quick Wins)       │  │
│  │ export_engine.py ([COB-ST19/ST20] ReportLab PDF & OpenPyXL Excel)│  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Lee y persiste entidades
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               CAPA 3: PERSISTENCIA Y DATOS (DATABASE)                  │
│  db_manager.py (Conexiones, Migraciones DDL, Consultas Parametrizadas) │
│  cobit_core.db (SQLite 3 Relacional con llaves foráneas e integridad)  │
└────────────────────────────────────────────────────────────────────────┘
```

### Componentes de la Estructura:
1. **`app.py` (Orquestador Central):**
   - Configura el entorno Streamlit (`wide mode`, favicon, metadatos).
   - Inyecta el sistema de diseño visual unificado (`static/custom.css`).
   - Gobierna el ciclo de vida de la sesión (`st.session_state`) y el control de acceso por roles (**RBAC**).
   - Enruta hacia la vista seleccionada sin recargas destructivas de estado.
2. **`views/` (Vistas de Usuario):** Módulos desacoplados que renderizan formularios, tablas interactivas, sliders de puntuación y gráficos. Cada vista es una función pura que interactúa con la lógica de negocio.
3. **`engine/` (Motores de Cálculo y Lógica Pura):** Contiene las funciones determinísticas y matemáticas independientes del framework de interfaz gráfica. Esto permite probar el 100% de la lógica sin levantar la UI.
4. **`database/` (Capa de Acceso a Datos):** Encapsula las transacciones SQLite, control de integridad referencial (`PRAGMA foreign_keys = ON`), hashing de credenciales (SHA-256) y sembrado automático de datos iniciales (*idempotent seeding*).

---

## 3. FLUJO DE DATOS Y COMUNICACIÓN ENTRE MÓDULOS

### 3.1. Gestión del Estado de Sesión (`st.session_state`)
Streamlit ejecuta el script de arriba a abajo ante cada interacción del usuario. Para garantizar coherencia y persistencia sin perder selecciones, el sistema utiliza variables de contexto globales:

- `st.session_state["authenticated"]` (Booleano): Bandera de inicio de sesión seguro.
- `st.session_state["user"]` (Diccionario): Datos del usuario autenticado (`id`, `username`, `full_name`, `role`).
- `st.session_state["current_view"]` (String): Identificador de la vista activa (`dashboard`, `clients`, `assessment`, etc.).
- `st.session_state["active_client_id"]` (Entero): ID de la empresa seleccionada como contexto de trabajo.
- `st.session_state["active_assessment_id"]` (Entero): ID de la evaluación activa que alimenta los tableros y cálculos.

### 3.2. Diagrama de Secuencia: Flujo Integral de Evaluación y Generación de Entregables

```mermaid
sequenceDiagram
    autonumber
    actor Consultor as Consultor / Usuario
    participant UI as Vista (views/)
    participant State as st.session_state
    participant Engine as Motores (engine/)
    participant DB as SQLite (database/)

    Consultor->>UI: Selecciona Empresa Cliente y Evaluación
    UI->>State: Actualiza active_client_id y active_assessment_id
    UI->>DB: get_assessment_scores(assessment_id)
    DB-->>UI: Retorna registros de 40 procesos
    UI->>Engine: calculate_assessment_metrics(scores)
    Engine-->>UI: Retorna métricas {imo, dominios, brechas, salud, riesgo}
    UI-->>Consultor: Renderiza Dashboard y Radar Plotly en tiempo real

    Consultor->>UI: Modifica calificaciones 0-5 y agrega evidencias
    Consultor->>UI: Clic en "Guardar Calificaciones"
    UI->>Engine: Recalcula IMO con nuevos puntajes
    UI->>DB: save_all_assessment_scores(assessment_id, scores, nuevo_imo)
    DB-->>UI: Confirmación de actualización en base de datos

    Consultor->>UI: Navega a "Hoja de Ruta (Roadmap)"
    UI->>Engine: generate_roadmap_plan(scores, client_name)
    Note over Engine: Aplica algoritmo multi-criterio [COB-TK10]<br/>detecta Quick Wins y distribuye en 3 fases
    Engine-->>UI: Plan generado con presupuesto e iniciativas
    UI->>DB: save_roadmap(assessment_id, client_id, plan)

    Consultor->>UI: Solicita Descarga de Informe PDF
    UI->>Engine: generate_pdf_report(client, eval, metrics, roadmap)
    Note over Engine: ReportLab compila tablas, estilos y portadas
    Engine-->>UI: Retorna buffer de bytes (application/pdf)
    UI-->>Consultor: Descarga instantánea del archivo PDF
```

---

## 4. CATÁLOGO DETALLADO DE FUNCIONALIDADES (LO QUE PUEDE HACER EL USUARIO)

### 4.1. Módulo de Autenticación y Control de Acceso por Roles (RBAC) [COB-ST01, COB-ST03]
- **Inicio de Sesión Seguro:** Interfaz protegida contra credenciales erróneas mediante hash SHA-256.
- **Acceso según Perfiles:**
  - **👑 Administrador (`admin`):** Gestión completa de la plataforma, mantenimiento y visualización total.
  - **💼 Consultor Líder (`consultant`):** Registro de clientes, configuración de cuestionarios, ejecución de evaluaciones, ejecución de diagnósticos de IA y generación de hojas de ruta.
  - **🏢 Cliente Corporativo (`client`):** Lectura directiva, monitoreo de indicadores del dashboard y descarga de informes de su respectiva empresa.
- **Credenciales Demo Integradas:** Ayuda visual con tarjetas de acceso rápido para demostraciones académicas inmediatas.
- **Cierre de Sesión:** Destruye el estado de sesión y retorna a la pantalla de validación.

---

### 4.2. Dashboard Ejecutivo con Radar COBIT 2019 [COB-ST16, COB-ST17]
- **Selector de Contexto:** Menú desplegable para alternar entre diferentes empresas clientes y sus respectivas evaluaciones vigentes.
- **Tarjetas de Indicadores Clave (KPIs):**
  - **Índice de Madurez Organizacional (IMO):** Calificación ponderada de 0.00 a 5.00 con su respectivo nivel verbal oficial (Incompleto, Inicial, Gestionado, Establecido, Predecible u Optimizado).
  - **Meta Propuesta y Brecha Global:** Objetivo corporativo (ej. 3.50/5.00) y distancia numérica por cerrar.
  - **Salud de Gobernanza (%):** Nivel porcentual de efectividad y alineación de las prácticas de gobierno de TI.
  - **Exposición al Riesgo de TI (%):** Brecha de vulnerabilidad no mitigada calculada de forma complementaria al IMO.
- **Gráfico Radar Polar Interactivo (Plotly):**
  - Polígono de 5 ejes correspondiente a los 5 dominios COBIT (**EDM, APO, BAI, DSS, MEA**).
  - Dos capas superpuestas: **Nivel Actual Evaluado** (azul traslúcido) vs **Nivel Deseado / Meta** (verde punteado).
  - Escala fija de 0 a 5 con etiquetas legibles y *tooltips* interactivos al pasar el cursor.
- **Barras de Desempeño por Dominio:** Barras de progreso porcentuales por área de gobierno y gestión con desglose de la brecha.
- **Tabla de Alerta Temprana (Top 5 Brechas Críticas):** Destaca de forma automática los 5 procesos que presentan la mayor diferencia entre el nivel actual y el requerido.
- **Accesos Directos de Navegación:** Botones rápidos hacia el Cuestionario, Diagnóstico de IA, Hoja de Ruta y Reportes.

---

### 4.3. Gestión Integral de Empresas Clientes y Contactos [COB-ST04, COB-ST05]
- **Pestaña 1: Listado y Filtros Avanzados:**
  - Buscador predictivo en tiempo real por Razón Social, NIT o Ciudad de sede.
  - Filtro desplegable por sector industrial (Banca, Salud, Tecnología, Manufactura, Retail, etc.).
  - Acordeones informativos por empresa destacando la empresa **ACTIVA EN SESIÓN**.
  - Operaciones en un clic: Establecer como cliente activo, editar datos y eliminar cliente con eliminación en cascada.
- **Pestaña 2: Registro de Nueva Organización:**
  - Formulario validado para registrar Razón Social, NIT/RUT, Sector Económico, Tamaño Corporativo (Micro a Multinacional), Sede, Teléfonos, Correo institucional y Contacto Principal.
  - Asignación inmediata como empresa activa al guardar.
- **Pestaña 3: Directorio de Interesados y Contactos Clave:**
  - Asociación de múltiples interesados por empresa (CIO, CISO, Auditor Interno, Gerente de Operaciones).
  - Registro de nombres, correo, teléfono, cargo, área y designación del **Contacto Principal**.

---

### 4.4. Catálogo Interactivo COBIT 2019 [COB-TK05, COB-ST07]
- **Explorador Oficial de ISACA:** Presenta los 5 dominios y los 40 procesos del estándar en español.
- **Filtrado por Dominio:** Selector para aislar los procesos de gobierno (EDM) o de gestión (APO, BAI, DSS, MEA).
- **Buscador Universal en Vivo:** Búsqueda por coincidencia de código (ej. `DSS05`, `APO13`), término funcional (`ciberseguridad`, `riesgo`, `continuidad`, `datos`) o prácticas.
- **Tarjetas Resumen de Dominio:** Cajas de color con contadores dinámicos de procesos por cada área.
- **Ficha Técnica Expandible por Proceso:**
  - Código y nombre oficial.
  - Indicador de **Proceso Core / Esencial**.
  - Propósito formal del objetivo según COBIT 2019.
  - Prácticas clave recomendadas para auditar en campo.

---

### 4.5. Cuestionario Interactivo de Evaluación de Madurez [COB-ST10, COB-ST11]
- **Creación de Expedientes de Evaluación:**
  - Posibilidad de crear múltiples evaluaciones por cliente para seguimiento temporal de avances.
  - **Alcance Flexible:** Selección entre **Diagnóstico Integral** (los 40 procesos) o **Diagnóstico Rápido / Quick Assessment** (18 procesos críticos seleccionados).
  - Asignación del Consultor Líder responsable y fecha objetivo de culminación.
- **Pestañas por Dominio:** Organización por pestañas (**EDM, APO, BAI, DSS, MEA**) que evita la fatiga visual del consultor.
- **Calificación en Escala Oficial 0 a 5:**
  - *Sliders* interactivos con saltos decimales de 0.5.
  - **Rúbrica Dinámica:** Al deslizar el valor, el sistema muestra en pantalla la definición de la escala:
    - `0`: Incompleto
    - `1`: Inicial
    - `2`: Gestionado
    - `3`: Establecido / Definido
    - `4`: Predecible / Cuantitativamente Gestionado
    - `5`: Optimizado
- **Fijación de Meta Específica por Proceso:** Permite que un proceso tenga meta 4.0 y otro 3.0 según la criticidad del negocio.
- **Bitácora de Evidencias Probatorias y Observaciones:** Campos de texto por cada proceso para adjuntar nombres de políticas, actas de comité, fechas de auditoría y planes inmediatos.
- **Guardado en Lote y Recálculo en Vivo:** Botón principal que consolida todas las calificaciones en SQLite y recalcula instantáneamente el IMO.

---

### 4.6. Diagnóstico de Brechas e Inteligencia Artificial [COB-ST12, COB-ST13]
- **Pestaña 1: Diagnóstico Integral Heurístico:**
  - Genera automáticamente un Resumen Ejecutivo estructurado con fecha, nivel de salud y conclusiones formales.
  - Hallazgos clave automáticos clasificados por dominio según la magnitud de la brecha.
  - Lista de recomendaciones de acción inmediata sugeridas para el comité de TI.
- **Pestaña 2: Asistente de Alineación Estratégica Negocio -> TI:**
  - Permite al consultor escribir en lenguaje natural una meta comercial (ej. *"Expandir canales digitales reduciendo fraudes bancarios y tiempos de respuesta"*).
  - El motor semántico analiza las intenciones y extrae los procesos COBIT 2019 que soportan directamente dicha meta (ej. `APO13`, `DSS05`, `BAI02`, `EDM02`), indicando su nivel de criticidad y la justificación técnica.
- **Pestaña 3: Matriz de Riesgos Tecnológicos:**
  - Mapeo automatizado de riesgos operacionales clasificados en categorías: *Ciberseguridad y Resiliencia*, *Alineación Estratégica*, *Continuidad Operativa*.
  - Clasificación de severidad (*Alto*, *Medio*, *Bajo*) en función del IMO actual y acciones mitigantes asociadas a procesos COBIT.

---

### 4.7. Generador Automático de Hojas de Ruta (Roadmap) [COB-TK10, COB-ST14, COB-ST15]
- **Generación Algorítmica Multi-Criterio:** Evalúa todas las brechas detectadas y genera un plan estructurado con presupuestos en pesos colombianos (COP), horizontes de tiempo y roles responsables.
- **Sección Destacada de Quick Wins:**
  - Destaca de forma prioritaria aquellas iniciativas de alto impacto con tiempo de implementación inferior a 90 días (< 3 meses) y bajo esfuerzo económico (ej. despliegue de MFA, formalización de catálogo de servicios, automatización del comité de cambios).
- **Desglose en 3 Fases Temporales:**
  - **Fase 1: Cimientos y Quick Wins (Meses 1-3):** Victorias tempranas y aseguramiento de políticas básicas.
  - **Fase 2: Consolidación y Procesos Core (Meses 4-8):** Implementación de SGSI, metodologías de proyectos y DRP.
  - **Fase 3: Optimización y Monitoreo Continuo (Meses 9-18):** Gobierno de datos, tableros BI e innovación.
- **Botón de Regeneración:** Permite actualizar la hoja de ruta cuando se modifican las calificaciones en el cuestionario.

---

### 4.8. Ingesta Documental y Análisis NLP (NPO) [COB-ST08, COB-TK07, COB-ST09]
- **Carga de Archivos de Evidencia:** Acepta documentos en formatos de texto (`.txt`, `.md`, `.json`, `.csv`, `.docx`, `.pdf`).
- **Entrada Manual de Texto:** Permite pegar directamente extractos de auditorías internas, políticas o minutas de comités.
- **Extracción NLP de Necesidades, Problemas y Oportunidades (NPO):**
  - Analiza la semántica textual buscando patrones lingüísticos de requerimientos, deficiencias y mejoras potenciales.
  - Clasifica los hallazgos en tres paneles diferenciados:
    - 🎯 **Necesidades (N):** Requisitos obligatorios no satisfechos.
    - ⚠️ **Problemas (P):** Fallas, desvíos operativos, retrasos o vulnerabilidades.
    - 💡 **Oportunidades (O):** Iniciativas de modernización y optimización.
- **Mapeo a Procesos COBIT 2019:** Vincula las palabras clave detectadas con los códigos oficiales correspondientes.
- **Historial Documental:** Repositorio histórico para consultar documentos cargados previamente por cliente.

---

### 4.9. Reportes Ejecutivos y Exportación [COB-ST19, COB-ST20]
- **Informe Ejecutivo en PDF (Descarga con 1 Clic):**
  - Generado en memoria usando el motor **ReportLab**.
  - Incluye: Portada corporativa formal, ficha técnica del cliente, tabla resumen de los 5 dominios con semáforos, tabla de las 5 brechas críticas y cronograma de iniciativas del roadmap con costos.
  - Cumple con estándares de presentación para juntas directivas y comités de auditoría.
- **Libro de Trabajo en Excel (.xlsx):**
  - Generado con **Pandas** y **OpenPyXL**.
  - Consta de 3 hojas de cálculo formateadas:
    1. *Resumen Ejecutivo:* Parámetros organizacionales, IMO, metas y métricas globales.
    2. *Calificaciones COBIT:* Matriz completa de procesos, dominios, nivel actual, meta, brecha y texto de evidencias.
    3. *Resumen por Dominio:* Promedios agrupados y cantidad de procesos evaluados.
- **Vista Previa en Pantalla:** Permite revisar los datos antes de proceder con la descarga.

---

## 5. MODELOS Y TIPOS DE DATOS DEL SISTEMA

El sistema maneja dos niveles de datos: **Persistencia Relacional SQLite** (en disco) y **Estructuras de Memoria Operativa** (en Python durante la ejecución).

### 5.1. Diccionario de Datos Relacionales (SQLite: `cobit_core.db`)

#### 1. Tabla `users` (Usuarios y Control de Acceso)
| Columna | Tipo de Dato SQLite | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | PRIMARY KEY AUTOINCREMENT | Identificador único del usuario. |
| `username` | `TEXT` | NOT NULL, UNIQUE | Nombre de usuario para autenticación (ej. `admin`, `consultor`). |
| `password_hash` | `TEXT` | NOT NULL | Resumen criptográfico SHA-256 de la contraseña (64 caracteres hexadecimales). |
| `full_name` | `TEXT` | NOT NULL | Nombre y apellidos del usuario / consultor. |
| `email` | `TEXT` | NULL | Correo electrónico de contacto. |
| `role` | `TEXT` | NOT NULL, DEFAULT 'consultant' | Rol del sistema: `'admin'`, `'consultant'`, `'client'`. |
| `is_active` | `INTEGER` | DEFAULT 1 | Estado de habilitación (1 = Activo, 0 = Inactivo). |
| `created_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo ISO-8601 de creación. |

#### 2. Tabla `clients` (Empresas Clientes)
| Columna | Tipo de Dato SQLite | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | PRIMARY KEY AUTOINCREMENT | ID interno de la organización. |
| `name` | `TEXT` | NOT NULL | Razón social formal de la empresa (ej. `Financiera del Café S.A.`). |
| `tax_id` | `TEXT` | UNIQUE | Identificación tributaria (NIT / RUT, ej. `900.548.123-4`). |
| `sector` | `TEXT` | NOT NULL | Sector económico (ej. `Servicios Financieros y Banca`). |
| `size` | `TEXT` | NOT NULL | Tamaño corporativo (ej. `Mediana Empresa (51 - 250 colaboradores)`). |
| `city` | `TEXT` | NULL | Ciudad de domicilio principal. |
| `phone` | `TEXT` | NULL | Teléfono institucional de contacto. |
| `email` | `TEXT` | NULL | Correo corporativo general. |
| `contact_name` | `TEXT` | NULL | Nombre del contacto principal ejecutivo. |
| `notes` | `TEXT` | NULL | Observaciones de contexto o antecedentes de consultoría. |
| `status` | `TEXT` | DEFAULT 'Activo' | Estado del cliente (`'Activo'`, `'Suspendido'`). |
| `created_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Fecha de registro. |
| `updated_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Fecha de última modificación. |

#### 3. Tabla `client_contacts` (Directorio de Contactos)
| Columna | Tipo de Dato SQLite | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | PRIMARY KEY AUTOINCREMENT | Identificador del contacto. |
| `client_id` | `INTEGER` | NOT NULL, FK -> `clients(id)` | Llave foránea hacia la empresa asociada (eliminación en cascada). |
| `name` | `TEXT` | NOT NULL | Nombre del directivo o profesional. |
| `email` | `TEXT` | NULL | Correo laboral directo. |
| `phone` | `TEXT` | NULL | Teléfono o móvil directo. |
| `role_title` | `TEXT` | NULL | Cargo formal (ej. `CIO`, `CISO`, `Auditor Interno TI`). |
| `department` | `TEXT` | NULL | Área organizacional (ej. `Ciberseguridad`, `Tecnología`). |
| `is_primary` | `INTEGER` | DEFAULT 0 | Booleano (1 si es el contacto principal, 0 en caso contrario). |
| `created_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Fecha de registro. |

#### 4. Tabla `assessments` (Expedientes de Evaluación COBIT)
| Columna | Tipo de Dato SQLite | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | PRIMARY KEY AUTOINCREMENT | Identificador del expediente. |
| `client_id` | `INTEGER` | NOT NULL, FK -> `clients(id)` | Empresa objeto de la evaluación. |
| `code` | `TEXT` | UNIQUE | Código normalizado (ej. `EVAL-001-20261019`). |
| `title` | `TEXT` | NOT NULL | Título del proyecto de evaluación. |
| `assessment_type` | `TEXT` | DEFAULT 'comprehensive' | Alcance: `'comprehensive'` (40 procesos) o `'quick'` (18 procesos). |
| `status` | `TEXT` | DEFAULT 'in_progress' | Estado: `'draft'`, `'in_progress'`, `'completed'`. |
| `lead_consultant` | `TEXT` | NULL | Nombre del auditor o consultor líder. |
| `target_date` | `TEXT` | NULL | Fecha programada de culminación (formato `YYYY-MM-DD`). |
| `notes` | `TEXT` | NULL | Alcance y notas preliminares. |
| `overall_maturity`| `REAL` | DEFAULT 0.0 | Valor decimal del IMO calculado (rango 0.00 a 5.00). |
| `created_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Fecha de inicio del expediente. |
| `updated_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Fecha de última actualización. |

#### 5. Tabla `assessment_scores` (Calificaciones y Evidencias por Proceso)
| Columna | Tipo de Dato SQLite | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | PRIMARY KEY AUTOINCREMENT | Identificador del registro de puntuación. |
| `assessment_id` | `INTEGER` | NOT NULL, FK -> `assessments(id)`| Evaluación a la que pertenece. |
| `process_id` | `TEXT` | NOT NULL | Código oficial del proceso (ej. `EDM01`, `APO13`, `DSS05`). |
| `domain` | `TEXT` | NOT NULL | Código del dominio (`EDM`, `APO`, `BAI`, `DSS`, `MEA`). |
| `current_score` | `REAL` | DEFAULT 0.0 | Nivel de madurez actual evaluado (0.0 a 5.0 con saltos de 0.5). |
| `target_score` | `REAL` | DEFAULT 3.0 | Nivel objetivo deseado por la empresa (1.0 a 5.0). |
| `evidence` | `TEXT` | NULL | Justificación documental, nombres de archivos, actas o hallazgos. |
| `observations` | `TEXT` | NULL | Recomendaciones específicas y plan de acción para el proceso. |
| `updated_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Fecha del último guardado de este proceso. |
| *Constraint* | `UNIQUE` | `(assessment_id, process_id)` | Impide duplicidad de calificaciones para un mismo proceso. |

#### 6. Tabla `roadmaps` (Hojas de Ruta Estratégicas)
| Columna | Tipo de Dato SQLite | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | PRIMARY KEY AUTOINCREMENT | ID único del roadmap. |
| `assessment_id` | `INTEGER` | NOT NULL, FK -> `assessments(id)`| Diagnóstico de origen que fundamenta la hoja de ruta. |
| `client_id` | `INTEGER` | NOT NULL, FK -> `clients(id)` | Empresa beneficiaria. |
| `title` | `TEXT` | NOT NULL | Título de la propuesta de transformación. |
| `total_budget` | `REAL` | DEFAULT 0.0 | Presupuesto total estimado acumulado en pesos colombianos (COP). |
| `horizon_months`| `INTEGER` | DEFAULT 18 | Duración total proyectada en meses (ej. 18 meses). |
| `summary` | `TEXT` | NULL | Síntesis ejecutiva del plan de mejora. |
| `created_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Fecha de generación. |

#### 7. Tabla `roadmap_initiatives` (Proyectos e Iniciativas Específicas)
| Columna | Tipo de Dato SQLite | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | PRIMARY KEY AUTOINCREMENT | ID de la iniciativa. |
| `roadmap_id` | `INTEGER` | NOT NULL, FK -> `roadmaps(id)` | Hoja de ruta a la que pertenece. |
| `process_id` | `TEXT` | NULL | Proceso COBIT que mitiga (ej. `APO13`, `DSS05`). |
| `phase` | `INTEGER` | DEFAULT 1 | Fase de ejecución: `1` (Corto Plazo), `2` (Mediano), `3` (Largo). |
| `title` | `TEXT` | NOT NULL | Nombre descriptivo del proyecto o iniciativa. |
| `description` | `TEXT` | NULL | Detalle de actividades y entregables esperados. |
| `is_quick_win` | `INTEGER` | DEFAULT 0 | Booleano (1 si es victoria temprana < 90 días, 0 si no). |
| `priority` | `TEXT` | DEFAULT 'Media' | Prioridad: `'Alta'`, `'Media'`, `'Baja'`. |
| `estimated_months`| `INTEGER` | DEFAULT 3 | Duración estimada en meses. |
| `estimated_cost` | `REAL` | DEFAULT 0.0 | Presupuesto estimado en COP (ej. $16,000,000). |
| `responsible_role`| `TEXT` | NULL | Rol ejecutor sugerido (ej. `Oficial de Seguridad (CISO)`). |
| `status` | `TEXT` | DEFAULT 'pending' | Estado: `'pending'`, `'in_progress'`, `'completed'`. |

#### 8. Tabla `documents` (Evidencias e Ingesta Documental)
| Columna | Tipo de Dato SQLite | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | PRIMARY KEY AUTOINCREMENT | ID del documento almacenado. |
| `client_id` | `INTEGER` | NOT NULL, FK -> `clients(id)` | Empresa dueña de la evidencia. |
| `filename` | `TEXT` | NOT NULL | Nombre original del archivo (ej. `Plan_PETI_2026.docx`). |
| `file_type` | `TEXT` | NULL | Tipo MIME o extensión (`application/pdf`, `text/plain`). |
| `file_size` | `INTEGER` | NULL | Tamaño en bytes. |
| `extracted_text`| `TEXT` | NULL | Texto plano extraído para indexación y análisis. |
| `npo_analysis` | `TEXT` | NULL | Cadena JSON estructurada con listas de `needs`, `problems`, `opportunities` y palabras clave detectadas. |
| `created_at` | `TEXT` | DEFAULT CURRENT_TIMESTAMP | Fecha y hora de carga. |

---

### 5.2. Estructuras de Datos en Memoria (Python Engine)

#### Objeto `metrics` (Retornado por `calculate_assessment_metrics`)
```python
{
    "imo": 2.15,                           # Float: Índice global ponderado (0.00 a 5.00)
    "target_imo": 3.40,                    # Float: Meta promedio ponderada
    "overall_gap": 1.25,                   # Float: Brecha global restante
    "level_label": "Gestionado",           # String: Categoría verbal oficial COBIT 2019
    "level_description": "...",            # String: Descripción detallada del nivel
    "health_score": 43.0,                  # Float: Porcentaje de salud (0.0% a 100.0%)
    "risk_score": 57.0,                    # Float: Porcentaje de riesgo no mitigado (0.0% a 100.0%)
    "domains": {                           # Dict: Resumen por cada uno de los 5 dominios
        "EDM": {"name": "...", "current": 2.20, "target": 3.00, "gap": 0.80, "count": 5},
        "APO": {"name": "...", "current": 1.95, "target": 3.50, "gap": 1.55, "count": 14},
        "BAI": {"name": "...", "current": 2.10, "target": 3.40, "gap": 1.30, "count": 11},
        "DSS": {"name": "...", "current": 2.30, "target": 3.60, "gap": 1.30, "count": 6},
        "MEA": {"name": "...", "current": 2.25, "target": 3.50, "gap": 1.25, "count": 4}
    },
    "top_gaps": [                          # List[Dict]: Top 5 procesos con mayor brecha
        {"process_id": "APO13", "name": "...", "gap": 2.5, "current_score": 2.0, "target_score": 4.5},
        ...
    ],
    "all_scored_processes": [...],         # List[Dict]: Lista con los 40 procesos evaluados
    "processes_count": 40                  # Int: Total de procesos calificados
}
```

---

### 5.3. Modelo de datos de la base de datos

#### 1. Descripción del Propósito del Modelo
El modelo entidad-relación (ERD) formaliza la persistencia relacional implementada en la base de datos SQLite del sistema (`cobit_core.db`). Su propósito principal es estructurar y relacionar de forma consistente las organizaciones clientes, su directorio de interesados, las evaluaciones de madurez basadas en COBIT 2019, la evidencia documental procesada mediante NLP, y los planes estratégicos de transformación digital expresados en hojas de ruta (roadmaps) con iniciativas por fases y estimaciones presupuestales.

#### 2. Diagrama Entidad-Relación (Código Mermaid)

```mermaid
erDiagram
    USUARIO {
        int id PK
        string username
        string password_hash
        string full_name
        string email
        string role
        boolean is_active
        datetime created_at
    }

    CLIENTE {
        int id PK
        string name
        string tax_id
        string sector
        string size
        string city
        string phone
        string email
        string contact_name
        string notes
        string status
        datetime created_at
        datetime updated_at
    }

    CONTACTO_CLIENTE {
        int id PK
        int client_id FK
        string name
        string email
        string phone
        string role_title
        string department
        boolean is_primary
        datetime created_at
    }

    EVALUACION {
        int id PK
        int client_id FK
        string code
        string title
        string assessment_type
        string status
        string lead_consultant
        datetime target_date
        string notes
        float overall_maturity
        datetime created_at
        datetime updated_at
    }

    CALIFICACION_PROCESO {
        int id PK
        int assessment_id FK
        string process_id
        string domain
        float current_score
        float target_score
        string evidence
        string observations
        datetime updated_at
    }

    HOJA_RUTA {
        int id PK
        int assessment_id FK
        int client_id FK
        string title
        float total_budget
        int horizon_months
        string summary
        datetime created_at
    }

    INICIATIVA_ROADMAP {
        int id PK
        int roadmap_id FK
        string process_id
        int phase
        string title
        string description
        boolean is_quick_win
        string priority
        int estimated_months
        float estimated_cost
        string responsible_role
        string status
    }

    DOCUMENTO {
        int id PK
        int client_id FK
        string filename
        string file_type
        int file_size
        string extracted_text
        string npo_analysis
        datetime created_at
    }

    CLIENTE ||--o{ CONTACTO_CLIENTE : "posee"
    CLIENTE ||--o{ EVALUACION : "recibe"
    CLIENTE ||--o{ HOJA_RUTA : "beneficia"
    CLIENTE ||--o{ DOCUMENTO : "adjunta"
    EVALUACION ||--|{ CALIFICACION_PROCESO : "desglosa"
    EVALUACION ||--o| HOJA_RUTA : "fundamenta"
    HOJA_RUTA ||--|{ INICIATIVA_ROADMAP : "contiene"
    USUARIO ||--o{ EVALUACION : "gestiona"
```

#### 3. Leyenda de Simbología y Cardinalidades Utilizadas
El diagrama emplea la notación estándar de "Pata de Gallo" (*Crow's Foot notation*) implementada nativamente en Mermaid `erDiagram`:

- `||--o{` (**Uno a Cero o Muchos**): Una instancia de la entidad padre se relaciona opcionalmente con múltiples registros de la entidad dependiente.
  - `CLIENTE` posee de 0 a muchos `CONTACTO_CLIENTE`.
  - `CLIENTE` recibe de 0 a muchas `EVALUACION`.
  - `CLIENTE` adjunta de 0 a muchos `DOCUMENTO`.
  - `CLIENTE` se beneficia de 0 a muchas `HOJA_RUTA`.
  - `USUARIO` gestiona de 0 a muchas `EVALUACION`.
- `||--|{` (**Uno a Uno o Muchos Obligatorio**): Una instancia de la entidad padre debe contener forzosamente al menos un registro secundario.
  - `EVALUACION` se desglosa obligatoriamente en al menos una (y hasta 40) `CALIFICACION_PROCESO`.
  - `HOJA_RUTA` contiene obligatoriamente una o múltiples `INICIATIVA_ROADMAP`.
- `||--o|` (**Uno a Cero o Uno**): Relación de opcionalidad unitaria.
  - `EVALUACION` fundamenta de 0 a 1 `HOJA_RUTA` (la hoja de ruta se genera una vez consolidado el diagnóstico).
- `PK` (**Primary Key**): Identificador único autoincremental de la entidad.
- `FK` (**Foreign Key**): Clave foránea que referencia la clave primaria de la tabla contenedora con restricción de eliminación en cascada (`ON DELETE CASCADE`).

#### 4. Suposiciones Relevantes del Modelo
1. **Catálogo Estándar COBIT 2019:** Los 40 procesos del marco internacional residen como catálogo estático e inmutable en el motor (`cobit_data.py`). En consecuencia, la entidad `CALIFICACION_PROCESO` almacena el código estandarizado `process_id` (ej. `EDM01`, `APO13`, `DSS05`) y el `domain` (`EDM`, `APO`, `BAI`, `DSS`, `MEA`) como identificadores referenciales lógicos, evitando tablas de catálogo redundantes en la base local.
2. **Relación entre Usuarios y Evaluaciones:** En la tabla física `assessments`, el consultor responsable se registra textualmente en el campo `lead_consultant` para agilizar la portabilidad de reportes directivos. En el modelo entidad-relación, dicha asociación se formaliza como `USUARIO ||--o{ EVALUACION : gestiona` para representar la auditoría y responsabilidad del consultor que inicia y suscribe la evaluación.
3. **Persistencia del Análisis NLP Documental:** La entidad `DOCUMENTO` preserva el análisis de Necesidades, Problemas y Oportunidades (NPO) en formato serializado JSON dentro del campo `npo_analysis`. Esto permite guardar estructuras arbóreas de hallazgos y términos clave detectados sin requerir múltiples tablas asociativas complejas.
4. **Ciclo de Vida de la Hoja de Ruta:** Una `HOJA_RUTA` mantiene doble referencia foránea: hacia `EVALUACION` (diagnóstico origen que justifica el plan) y hacia `CLIENTE` (empresa beneficiaria), garantizando consultas directas y consistencia histórica.

---

## 6. MOTORES DE CÁLCULO Y ALGORITMOS MATEMÁTICOS

### 6.1. Algoritmo de Cálculo Ponderado de Madurez Organizacional (IMO) [COB-TK08]
El Índice de Madurez Organizacional (**IMO**) consolida la capacidad de la entidad ponderando los 5 dominios de acuerdo con su criticidad estructural dentro del ciclo de gobierno y gestión:

$$\text{IMO} = \frac{\sum_{d \in \text{Dominios}} \left( \overline{S}_d \times W_d \right)}{\sum_{d \in \text{Dominios}} W_d}$$

Donde:
- $\overline{S}_d = \frac{1}{N_d} \sum_{i=1}^{N_d} s_{d,i}$ es la media aritmética de las calificaciones de los procesos evaluados en el dominio $d$.
- $W_d$ son los coeficientes de ponderación definidos en `DOMAIN_WEIGHTS`:
  - **$W_{\text{EDM}} = 0.20$** (Gobierno directivo y orientación de recursos).
  - **$W_{\text{APO}} = 0.25$** (Gestión estratégica y arquitectura).
  - **$W_{\text{BAI}} = 0.20$** (Construcción y gestión de proyectos y cambios).
  - **$W_{\text{DSS}} = 0.25$** (Continuidad operacional, mesa de ayuda y ciberseguridad).
  - **$W_{\text{MEA}} = 0.10$** (Monitoreo de desempeño y cumplimiento legal).
- $\sum W_d = 1.00$.

#### Escala Verbal Oficial:
- $0.00 \le \text{IMO} < 0.50 \longrightarrow$ **Incompleto**
- $0.50 \le \text{IMO} < 1.50 \longrightarrow$ **Inicial**
- $1.50 \le \text{IMO} < 2.50 \longrightarrow$ **Gestionado**
- $2.50 \le \text{IMO} < 3.50 \longrightarrow$ **Establecido / Definido**
- $3.50 \le \text{IMO} < 4.50 \longrightarrow$ **Predecible / Cuantitativamente Gestionado**
- $4.50 \le \text{IMO} \le 5.00 \longrightarrow$ **Optimizado**

#### Indicadores Complementarios de Gobernanza:
$$\text{Salud de Gobernanza (\%)} = \left( \frac{\text{IMO}}{5.0} \right) \times 100$$

$$\text{Exposición al Riesgo (\%)} = 100 - \text{Salud de Gobernanza (\%)} = \left( 1 - \frac{\text{IMO}}{5.0} \right) \times 100$$

---

### 6.2. Algoritmo de Priorización Multi-Criterio de la Hoja de Ruta [COB-TK10]
Para ordenar las iniciativas y asignar su fase de ejecución (Fase 1, 2 o 3), el motor evalúa una función de puntuación compuesta de 0 a 100 puntos:

$$\text{Score}(P) = S_{\text{Gap}} + S_{\text{Impacto}} + S_{\text{Esfuerzo}} + S_{\text{Estrategia}}$$

1. **Magnitud de la Brecha ($S_{\text{Gap}} \in [0, 40]$):** Proporcional a la distancia entre el estado actual y deseado ($\text{Meta} - \text{Actual}$).
2. **Impacto en Dependencias COBIT ($S_{\text{Impacto}} \in [0, 30]$):** Procesos que habilitan a otros (ej. seguridad `APO13` y operaciones `DSS01` tienen mayor peso que procesos periféricos).
3. **Facilidad / Esfuerzo de Implementación ($S_{\text{Esfuerzo}} \in [0, 20]$):** Tiempos de entrega menores a 3 meses otorgan el puntaje máximo de agilidad.
4. **Valor Estratégico para el Negocio ($S_{\text{Estrategia}} \in [0, 10]$):** Procesos directamente alineados con los objetivos declarados por la empresa.

#### Identificación Automática de Quick Wins:
Una iniciativa es clasificada como **Quick Win** si cumple simultáneamente:
$$\text{is\_quick\_win} = \text{True} \iff (\text{Duración} \le 3 \text{ meses}) \land (\text{Brecha} \ge 0.8) \land (\text{Esfuerzo Económico} \le \$20,000,000 \text{ COP})$$

---

### 6.3. Algoritmo de Procesamiento de Lenguaje Natural Heurístico (NPO) [COB-ST09]
El motor de extracción documental procesa el texto en 3 fases:
1. **Normalización e Indexación de Términos:** Convierte a minúsculas, remueve signos ortográficos y evalúa expresiones regulares para mapear contra un diccionario de más de 30 conceptos clave de TI (`ciberseguridad`, `sla`, `drp`, `auditoría`, `backups`, etc.).
2. **Segmentación y Análisis Sintáctico de Oraciones:** Divide el texto en proposiciones lógicas y evalúa disparadores contextuales:
   - Disparador de Necesidad: `"requiere"`, `"necesita"`, `"debe"`, `"es necesario"`, `"prioridad"`.
   - Disparador de Problema: `"falla"`, `"error"`, `"retraso"`, `"vulnerabilidad"`, `"carece"`, `"riesgo"`.
   - Disparador de Oportunidad: `"mejora"`, `"optimizar"`, `"automatizar"`, `"innovar"`, `"potencial"`.
3. **Mapeo a Objetivos COBIT:** Cada término identificado activa los procesos de ISACA correspondientes (ej. `vulnerabilidad` $\longrightarrow$ `APO13`, `DSS05`).

---

## 7. GUÍA DE EJECUCIÓN, ROLES Y PRUEBAS AUTOMATIZADAS

### 7.1. Requisitos del Entorno
- **Sistema Operativo:** Windows 10/11, Linux o macOS.
- **Python:** Versión 3.10, 3.11, 3.12 o 3.13.
- **Librerías Requeridas:** Documentadas en `requirements.txt`:
  ```txt
  streamlit>=1.30.0
  plotly>=5.18.0
  pandas>=2.0.0
  reportlab>=4.0.0
  openpyxl>=3.1.0
  pydantic>=2.0.0
  ```

### 7.2. Puesta en Marcha (Paso a Paso)
1. Abrir terminal en la carpeta del proyecto:
   ```powershell
   cd "e:\Program Files (x86)\Streaming de Google Drive\Mi unidad\Universidad_del_Quindio\8vo_Semestre\Formulacion_Proyectos\proyecto\cobit_core_app"
   ```
2. Instalar dependencias si no se ha hecho previamente:
   ```powershell
   pip install -r requirements.txt
   ```
3. Ejecutar el servidor de la aplicación web:
   ```powershell
   streamlit run app.py
   ```
4. El navegador web se abrirá automáticamente en:
   `http://localhost:8501`

### 7.3. Matriz de Usuarios y Credenciales
El sistema cuenta con 3 usuarios sembrados automáticamente en SQLite listos para pruebas:

| Perfil | Nombre Completo | Usuario | Contraseña | Permisos y Propósito |
| :--- | :--- | :--- | :--- | :--- |
| **Superadministrador** | Administrador del Sistema | `admin` | `admin123` | Control total del sistema y gestión de configuración. |
| **Consultor Líder** | Ing. Johan Londoño | `consultor` | `cobit2019` | Evaluación de empresas, carga de evidencias, diagnóstico y hojas de ruta. |
| **Cliente CIO** | Dra. Carolina Ríos | `cliente` | `cliente2019` | Visualización ejecutiva del dashboard, estado de madurez y descarga de informes. |

*Nota: La base de datos incluye una empresa de prueba completamente cargada (**Financiera del Café S.A.**) con 40 procesos calificados, hoja de ruta calculada y contactos para poder probar los gráficos y reportes sin requerir entrada previa de datos.*

---

### 7.4. Ejecución de la Batería de Pruebas Automatizadas
Para verificar la integridad de todos los motores, cálculos matemáticos, base de datos y exportadores sin necesidad de abrir el navegador:

```powershell
python test_cobit_core.py
```

#### Salida del Test Suite (6/6 Suites Aprobadas al 100%):
```text
==================================================================
   INICIANDO PRUEBAS AUTOMATIZADAS DE COBIT CORE CONSULTING APP   
==================================================================

[1/6] Probando inicialización de SQLite y datos semilla...
  -> Autenticación de admin: OK
  -> Autenticación de consultor: OK
  -> Cliente semilla encontrado: Financiera del Café S.A. (NIT: 900.548.123-4) - OK

[2/6] Probando Catálogo COBIT 2019...
  -> 5 Dominios y 40 Procesos oficiales validados: OK

[3/6] Probando Motor de Madurez y Algoritmo IMO [COB-TK08]...
  -> IMO calculado: 2.02 / 5.00 (Gestionado) - OK
  -> Salud de Gobernanza: 40.4% | Riesgo: 59.6% - OK

[4/6] Probando Motor de IA y Alineación Estratégica [COB-ST09, COB-ST12, COB-ST13]...
  -> Alineación generada: 3 procesos recomendados - OK
  -> Análisis NPO: 1 necesidades, 3 problemas - OK
  -> Diagnóstico cualitativo y matriz de riesgos generada: OK

[5/6] Probando Generador de Hoja de Ruta [COB-TK10, COB-ST14]...
  -> Roadmap generado: 40 iniciativas (16 Quick Wins) - OK
  -> Presupuesto Total: $532,000,000 COP - OK

[6/6] Probando Exportación de Reportes [COB-ST19, COB-ST20]...
  -> Informe Ejecutivo en PDF generado (4387 bytes): OK
  -> Libro de Evaluación Excel generado (10442 bytes): OK

==================================================================
  >>> TODAS LAS PRUEBAS (6/6) PASARON SATISFACTORIAMENTE AL 100% <<<
==================================================================
```

---

## 8. CONCLUSIÓN
El **COBIT Core Consulting System** proporciona una solución informática completa, rigurosa y visualmente atractiva que materializa los objetivos de la materia de Formulación de Proyectos de Software y cumple cabalmente con cada tarea e historia de usuario programada en Jira, sirviendo como una herramienta real de auditoría y consultoría estratégica de TI.
