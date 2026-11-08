# 📘 GUÍA DE USUARIO PASO A PASO: SISTEMA COBIT 2019 + IA
## MANUAL PRÁCTICO Y DIDÁCTICO PARA CONSULTORÍA EN GOBIERNO DE TI

**Universidad del Quindío — Facultad de Ingeniería**  
**Proyecto:** Sistema de Consultoría en Gobierno y Gestión de TI (COBIT 2019 + IA)  
**Dirigido a:** Evaluadores, Consultores, Estudiantes, Directivos de TI y Usuarios Nuevos  

---

## 🌟 BIENVENIDO AL SISTEMA

### ¿Qué es este sistema y para qué sirve?
Imagina que una empresa es como un automóvil. Para que el auto funcione bien y no sufra accidentes, necesita un motor potente, frenos en buen estado, dirección precisa y reglas claras para quien lo conduce. 

En las organizaciones, la **Tecnología de la Información (TI)** (servidores, redes, software, bases de datos, seguridad) es ese motor. **COBIT 2019** es el estándar internacional más prestigioso del mundo (creado por ISACA) que funciona como el **manual de inspección técnica vehicular**: define 40 puntos de control clave para asegurar que la tecnología realmente le ayude a la empresa a ganar dinero, proteger su información y evitar fallos catastróficos.

**Este sistema informático automatiza todo ese trabajo:**
1. Te permite registrar a la empresa que vas a evaluar.
2. Te entrega un cuestionario interactivo para calificar cómo está la empresa de **0 a 5**.
3. Calcula automáticamente qué tan madura está la empresa mediante un indicador matemático llamado **IMO** (Índice de Madurez Organizacional).
4. Te dibuja una gráfica de **Radar** para ver en qué áreas está fuerte y en cuáles está débil.
5. Utiliza **Inteligencia Artificial** para detectar riesgos, brechas (*gaps*) y priorizar soluciones.
6. Te genera una **Hoja de Ruta (Roadmap)** que dice qué proyectos hacer primero (**Quick Wins**) y cuánto presupuesto se requiere.
7. Te permite descargar con **un solo clic** un informe formal en **PDF** y un libro completo en **Excel** listo para entregarle al gerente o a la junta directiva.

---

## 🚦 PASO 0: CÓMO INGRESAR AL SISTEMA

### 1. Iniciar la aplicación
Abre tu terminal en la carpeta del proyecto y escribe:
```bash
streamlit run app.py
```
Se abrirá de inmediato una pestaña en tu navegador web en la dirección: `http://localhost:8501`.

### 2. Pantalla de Inicio de Sesión
Verás una tarjeta azul oscura con el título **COBIT 2019 Core Consulting**. 

El sistema cuenta con tres tipos de perfiles con **Control de Acceso Basado en Roles (RBAC)** estricto:

| Rol | Usuario | Contraseña | Módulos Visibles en Menú | Permisos y Limitaciones |
| :--- | :--- | :--- | :--- | :--- |
| **👑 Administrador** | `admin` | `admin123` | **8 módulos** (Todos) | Acceso total al sistema, configuración global y eliminación de empresas. |
| **💼 Consultor Líder** *(Recomendado)* | `consultor` | `cobit2019` | **7 módulos** (Dashboard, Catálogo, Evaluación, Diagnóstico, Roadmap, Ingesta, Reportes) | Ejecuta evaluaciones, diagnósticos de IA, genera hojas de ruta y exporta informes técnicos. La gestión administrativa de clientes no se muestra en su menú. |
| **🏢 Cliente (CIO / Gerente)** | `cliente` | `cliente2019` | **4 módulos** (Dashboard, Catálogo, Hoja de Ruta, Reportes) | Vista ejecutiva de consulta. El selector de empresa queda bloqueado a su organización (*Acceso Directivo Autorizado*), y los botones de regeneración de planes quedan ocultos. |

> 💡 **Consejo:** Para realizar todo el recorrido de consultoría técnica completa, ingresa con el usuario **`consultor`** y la contraseña **`cobit2019`**. Para labores de administración o eliminación, ingresa como **`admin`**.

---

## 🧭 CÓMO MOVERSE POR EL SISTEMA (EL MENÚ LATERAL Y RBAC)

A la izquierda de tu pantalla siempre tendrás una barra lateral (Sidebar). El sistema adapta dinámicamente las secciones mostradas según el rol autenticado:

### Tarjeta de Perfil en la Barra Lateral
En la parte superior del menú siempre se muestra la tarjeta de identidad con:
- Nombre y apellido del usuario activo.
- Badge con el nombre del Rol (`ADMINISTRADOR`, `CONSULTOR`, `CLIENTE`).
- Botón rojo **"Cerrar Sesión"**.

### Matriz de Módulos según Perfil
- 📊 **Dashboard Principal:** Disponible para **Admin**, **Consultor** y **Cliente**. (Para Cliente está fijado a su propia compañía).
- 🏢 **Gestión de Clientes:** Exclusivo para **Admin**. (Permite altas, bajas y directorio corporativo).
- 📖 **Catálogo COBIT 2019:** Disponible para **Admin**, **Consultor** y **Cliente**.
- 📝 **Evaluación de Madurez:** Disponible para **Admin** y **Consultor**.
- 🤖 **Diagnóstico e IA:** Disponible para **Admin** y **Consultor**.
- 🗺️ **Hoja de Ruta (Roadmap):** Disponible para **Admin**, **Consultor** y **Cliente** (Clientes en modo lectura).
- 📄 **Ingesta Documental (NLP):** Disponible para **Admin** y **Consultor**.
- 📥 **Reportes y Descargas:** Disponible para **Admin**, **Consultor** y **Cliente**.

---

## 📖 GUÍA MÓDULO POR MÓDULO

---

### MÓDULO 1: 🏢 GESTIÓN DE CLIENTES Y CONTACTOS

#### ¿Para qué sirve?
Es la libreta corporativa del sistema. Antes de evaluar una empresa, necesitas tenerla registrada con sus datos básicos (nombre, NIT, sector, ciudad y las personas de contacto como el CIO o el Oficial de Seguridad).

#### ¿Qué puedes hacer aquí?
Este módulo tiene 3 pestañas en la parte superior:

1. **Pestaña "📋 Lista de Clientes":**
   - Puedes buscar cualquier empresa escribiendo su nombre, su NIT o su ciudad en la barra de búsqueda.
   - Puedes filtrar por sector (ej. *Servicios Financieros y Banca*, *Salud*, *Tecnología*).
   - Al hacer clic en una empresa, verás toda su ficha técnica.
   - **Botón "Seleccionar":** Sirve para establecer esa empresa como la **empresa activa en la que estás trabajando hoy**. Todo lo que hagas en los otros módulos afectará a esta empresa seleccionada.
   - **Botones "Editar Datos" y "Eliminar":** Para corregir información o dar de baja a una empresa.

2. **Pestaña "➕ Registrar Nuevo Cliente":**
   - Aquí inscribes a una nueva empresa llenando el formulario: Razón Social, NIT, Sector, Tamaño de empresa (Micro, Pequeña, Mediana, Grande o Multinacional), Ciudad, Teléfono y Correo.
   - Haces clic en **"💾 Guardar y Crear Cliente"** y listo: el sistema la registra y la deja seleccionada automáticamente.

3. **Pestaña "👥 Directorio de Contactos":**
   - Seleccionas la empresa y puedes agregar a las personas clave con las que te vas a comunicar (ej. *"Ing. Carolina Ríos - Directora de TI"*, *"Mauricio Castaño - Oficial de Ciberseguridad"*).
   - Puedes marcar a uno de ellos como el **Contacto Principal**.

---

### MÓDULO 2: 📖 CATÁLOGO INTERACTIVO COBIT 2019

#### ¿Para qué sirve?
Es tu guía de consulta oficial. Te explica con palabras claras los **5 dominios** y los **40 objetivos** que componen el estándar COBIT 2019, para que nunca tengas dudas de qué significa cada código.

#### ¿Cómo entender los 5 Dominios?
COBIT divide el mundo de la tecnología en 5 grandes bloques:
- **EDM (Evaluar, Dirigir y Monitorizar):** Es el área de los **dueños y la junta directiva**. Define hacia dónde va la empresa y cuánto riesgo está dispuesta a tolerar (5 procesos).
- **APO (Alinear, Planificar y Organizar):** Es la **estrategia de TI**. Planifica presupuestos, personal, arquitectura, seguridad y relaciones con el negocio (14 procesos).
- **BAI (Construir, Adquirir e Implementar):** Es la **fábrica de soluciones**. Desarrollo de software, compra de tecnología, gestión de cambios y proyectos (11 procesos).
- **DSS (Entregar, Dar Servicio y Soporte):** Es el **día a día operativo**. La mesa de ayuda, solución de incidentes, copias de seguridad (backups), continuidad y ciberseguridad (6 procesos).
- **MEA (Monitorizar, Evaluar y Valorar):** Es el área de **auditoría y control**. Revisa si los controles funcionan y si la empresa cumple las leyes del país (4 procesos).

#### ¿Qué puedes hacer aquí?
- **Buscar cualquier tema:** Si escribes *"seguridad"*, *"datos"*, *"riesgo"* o *"backup"*, el buscador te mostrará al instante cuáles procesos aplican.
- **Abrir las fichas:** Al hacer clic en un proceso (ej. `APO13: Gestionar la Seguridad`), verás su propósito oficial y una lista de **prácticas recomendadas** para saber qué pedirle al cliente durante la consultoría.

---

### MÓDULO 3: 📝 EVALUACIÓN DE MADUREZ COBIT

#### ¿Para qué sirve?
Es el **corazón del sistema**. Aquí es donde el consultor se sienta con el cliente y califica cómo está la empresa en cada proceso de tecnología.

#### ¿Cómo funciona la Escala de 0 a 5?
El sistema utiliza la escala internacional de madurez de ISACA:

| Nivel | Nombre | ¿Qué significa en la práctica? |
| :---: | :--- | :--- |
| **0** | **Incompleto** | El proceso no existe o es un caos total; se trabaja de forma reactiva apagando incendios. |
| **1** | **Inicial** | Se logran cosas pero de forma intuitiva; depende de que una persona sepa cómo hacerlo. Si esa persona se va, nadie sabe qué hacer. |
| **2** | **Gestionado** | El área de TI ya planifica y documenta a nivel de su departamento, pero cada quien lo hace a su estilo. |
| **3** | **Establecido** | Todo el proceso está formalizado y estandarizado con manuales y políticas aprobadas para toda la empresa. |
| **4** | **Predecible** | El proceso se mide con indicadores numéricos (KPIs) y gráficos de control estadístico. |
| **5** | **Optimizado** | La empresa mejora continuamente, usa inteligencia artificial, automatizaciones y se anticipa al futuro. |

#### ¿Qué puedes hacer aquí?
1. **Crear o elegir una evaluación:**
   - Puedes abrir una evaluación anterior o hacer clic en **"➕ Crear Nueva Evaluación"**.
   - Puedes escoger entre:
     - **Diagnóstico Integral:** Evalúa los 40 procesos completos.
     - **Diagnóstico Rápido (Quick Assessment):** Evalúa los 18 procesos más críticos para diagnósticos exprés.
2. **Calificar con Sliders interactivos:**
   - Eliges la pestaña del dominio que vas a calificar (ej. `DSS`).
   - Abres un proceso (ej. `DSS05: Gestionar los Servicios de Seguridad`).
   - Mueves el control deslizante del **Nivel Actual** (ej. de 1.0 a 2.5). Al moverlo, la pantalla te explica exactamente qué significa ese número.
   - Ajustas el **Nivel Meta** que la empresa sueña alcanzar (ej. 4.0).
3. **Escribir las Evidencias:**
   - En el campo *"Evidencias Probatorias"*, anotas qué documentos o hechos sustentan esa nota (ej. *"Tienen firewall pero no tienen autenticación de dos factores ni copias de seguridad probadas"*).
4. **Guardar:**
   - Al final de la página haces clic en el botón azul **"💾 Guardar Todas las Calificaciones y Recalcular IMO"**. El sistema actualiza todo al segundo.

---

### MÓDULO 4: 📊 DASHBOARD PRINCIPAL Y RADAR DE MADUREZ

#### ¿Para qué sirve?
Es el centro de control visual. Aquí no tienes que leer cientos de números: el sistema convierte las calificaciones en gráficos elegantes y métricas ejecutivas para que cualquier directivo entienda el estado de la empresa en 10 segundos.

#### ¿Qué elementos ves en pantalla?
1. **Los 4 Cuadros de Mando (KPI Cards):**
   - **Índice de Madurez (IMO):** Es la nota global ponderada de la empresa (ej. `2.02 / 5.0 - Nivel Gestionado`).
   - **Meta Propuesta:** Hacia dónde debe llegar la empresa (ej. `3.40 / 5.0`) y cuánto le falta (Brecha).
   - **Salud de Gobernanza:** Un porcentaje del 0 al 100% que dice qué tan sana está la gestión de tecnología.
   - **Exposición al Riesgo:** Muestra el porcentaje de peligro tecnológico al que está expuesta la organización.
2. **El Gráfico de Radar Polar:**
   - Es una telaraña de 5 puntas (una por cada dominio: EDM, APO, BAI, DSS, MEA).
   - El área azul representa **dónde está la empresa hoy**.
   - La línea verde punteada representa **la meta a la que debe llegar**.
   - Con solo mirar qué punta del radar está más hundida, sabes inmediatamente cuál área está en crisis.
3. **Barras de Progreso por Dominio:** Indican cuánto ha avanzado cada dominio respecto al nivel 5.
4. **Tabla de Alertas: Top 5 Brechas Críticas:** Te lista los 5 procesos más atrasados y urgentes que requieren proyectos de mejora de inmediato.

---

### MÓDULO 5: 🤖 DIAGNÓSTICO INTELIGENTE E IA

#### ¿Para qué sirve?
Toma los datos de la evaluación y los convierte en **diagnósticos ejecutivos en prosa**, hallazgos cualitativos fundamentados y una **matriz cuantitativa de riesgos** mediante un motor de inteligencia artificial semántica (TF-IDF), procesamiento de lenguaje natural (NLP) y análisis multi-fuente.

#### ¿Qué puedes hacer aquí?
Dispone de 3 pestañas avanzadas e intuitivas:

1. **Pestaña "📑 Diagnóstico Integral Multi-Fuente":**
   - Te redacta un informe ejecutivo automático y formal adaptado a la empresa (sector, tamaño, madurez IMO, salud y riesgo).
   - **Inteligencia Documental Activa:** Si cargaste documentos o informes en el Módulo de Ingesta, la IA los lee automáticamente y los cita dentro del diagnóstico.
   - **Auditoría de Evidencias:** Muestra el porcentaje exacto de procesos que cuentan con evidencias probatorias registradas (útil para auditorías externas).
   - **Hallazgos Clave por Dominio:** Clasifica cada uno de los 5 dominios COBIT con semáforos de criticidad (🔴 Crítico, 🟡 Atención Requerida, 🟢 Favorable).
   - **Recomendaciones Dinámicas:** Sugerencias inmediatas generadas a partir de las brechas más graves del cliente.

2. **Pestaña "🎯 Alineación Estratégica con IA / NLP":**
   - Puedes seleccionar un **reto frecuente del menú desplegable** (ej. *"Expandir canales digitales reduciendo fraudes bancarios y caídas de servicio"*, *"Garantizar continuidad ante ransomware"*, *"Cumplir normatividad de protección de datos"*) o **escribir tu propia meta en lenguaje natural libre**.
   - Presionas **"🚀 Analizar Alineación Semántica"**.
   - El motor de Machine Learning (`scikit-learn` con TF-IDF + Similitud Coseno) compara tu frase contra los 40 objetivos COBIT 2019 y te entrega una tabla con:
     - **Código y Nombre del Proceso COBIT**.
     - **Afinidad Semántica Porcentual (0% a 100%)**: Qué tan alineado está matemáticamente con tu objetivo.
     - **Nivel de Criticidad (Alta, Media, Baja)**.
     - **Justificación Semántica y Práctica Clave de ISACA** que debe aplicarse para lograr la meta.

3. **Pestaña "🛡️ Matriz de Riesgos Tecnológicos y Gobernanza":**
   - Evalúa matemáticamente la exposición de la empresa en 5 ejes esenciales:
     1. *Ciberseguridad y Protección de Datos* (`APO13`, `DSS05`, `APO14`).
     2. *Continuidad Operativa y Resiliencia ante Desastres* (`DSS04`, `DSS01`).
     3. *Gobernanza Estratégica y Rendimiento de Inversiones* (`EDM01`, `EDM02`, `APO02`).
     4. *Cumplimiento Normativo, Legal y Aseguramiento* (`MEA02`, `MEA03`).
     5. *Gestión de Servicios, SLAs y Control de Cambios* (`APO09`, `BAI06`, `DSS02`).
   - Cada eje te muestra el nivel de riesgo (**Crítico**, **Alto**, **Medio** o **Bajo**), el porcentaje de exposición calculado, la causa raíz derivada de las notas reales del cliente y la acción de mitigación recomendada.

---

### MÓDULO 6: 🗺️ HOJA DE RUTA (ROADMAP), GANTT Y QUICK WINS

#### ¿Para qué sirve?
Un diagnóstico sin un plan de acción no sirve para nada. Este módulo toma todas las debilidades encontradas y **calcula matemáticamente un plan de proyectos ordenado en el tiempo** mediante análisis multi-criterio (MCDA / WSJF), estimación paramétrica de presupuesto, modelado de dependencias bloqueantes, hitos estratégicos y un **Diagrama de Gantt interactivo**.

#### ¿Cómo se organiza el plan?
El sistema divide las iniciativas en 3 etapas secuenciadas por dependencias:
- **Fase 1: Cimientos y Quick Wins (Meses 1 al 3):** Acciones de alto impacto y bajo esfuerzo que se pueden solucionar en menos de 90 días con poco dinero (ej. activar autenticación multifactor, formalizar el comité de cambios, publicar el catálogo de servicios).
- **Fase 2: Consolidación y Procesos Core (Meses 4 al 8):** Proyectos estructurales como el Plan de Continuidad ante Desastres (DRP), el Sistema de Gestión de Seguridad (SGSI) o metodologías ágiles de proyectos.
- **Fase 3: Optimización y Monitoreo Continuo (Meses 9 al 18/24):** Iniciativas avanzadas para alcanzar niveles 4 y 5 de COBIT (métricas cuantitativas, gobierno de datos y auditoría continua).

#### ¿Qué puedes hacer aquí?
1. **Configurar el Algoritmo (Roadmap Engine):**
   - En el panel desplegable **"⚙️ Motor Algorítmico Multi-Criterio"**, puedes calibrar:
     - **Estrategia de Optimización:** Elige entre *Equilibrado (Holístico COBIT)*, *Priorizar Quick Wins (< 90 Días)*, *Enfocado en Ciberseguridad y Continuidad* o *Enfocado en Gobierno Directivo*.
     - **Horizonte Temporal:** Escoge entre 12, 18 o 24 meses de ejecución.
     - **Tolerancia de Inversión:** Ajusta con el slider si la empresa tiene más o menos holgura presupuestal (0.7x a 1.4x).
   - Presionas **"⚡ Calcular y Guardar Hoja de Ruta"** y el algoritmo multi-criterio recalculará todo el plan, fechas y dependencias en tiempo real.
2. **Consultar los Indicadores de Inversión:**
   - Ver el **Presupuesto Total Estimado** en pesos colombianos (COP), calculado paramétricamente según el tamaño empresarial y sector.
   - Ver el **Total de Iniciativas** y la cantidad de **Quick Wins** identificados.
3. **Revisar las Tarjetas de ⚡ QUICK WINS:**
   - Cada tarjeta destaca el título contextual, la justificación matemática (`qw_reason`), el rol responsable, el costo estimado y el plazo en meses.
4. **Interactuar con el Diagrama de Gantt (Plotly):**
   - Cronograma visual interactivo con zoom, paneo y tooltips informativos.
   - Alterna la coloración entre **Fases Temporales** y **Tipología (Quick Wins vs Estándar)**.
   - Muestra líneas verticales rojas que demarcan los **Hitos Estratégicos (Milestones)**.
5. **Revisar los 🚩 Hitos Estratégicos (Milestones):**
   - Puntos de control formales: **Hito 1** (Mes 3: Cimientos y Quick Wins), **Hito 2** (Mes 6/8: Consolidación y Seguridad) e **Hito 3** (Mes 18: Auditoría y Madurez Objetivo).
6. **Auditoría de Dependencias Bloqueantes y Ruta Crítica:**
   - Valida que ninguna tarea inicie antes de la culminación de sus procesos prerrequisito (0 inconsistencias).
   - Identifica procesos cuello de botella (ej. `APO01`, `EDM01`) y marca con **🔥 Ruta Crítica** las tareas de supervisión obligatoria.
7. **Explorar el Detalle Técnico por Fase:**
   - En los acordeones de Fase 1, 2 y 3 verás el alcance, las dependencias bloqueantes, las fechas exactas (`YYYY-MM-DD`), la duración y el presupuesto.

---

### MÓDULO 7: 📄 INGESTA DOCUMENTAL, TABLAS Y BÚSQUEDA FTS5 (NLP)

#### ¿Para qué sirve?
A los consultores de TI siempre les entregan documentos densos (manuales de políticas, informes de auditoría, planes estratégicos). Este módulo procesa esos archivos extrayendo **tablas estructuradas (PDF/DOCX)**, validando su **integridad con SHA-256**, permitiendo **búsqueda de texto completo con SQLite FTS5** y **extrayendo automáticamente Necesidades, Problemas y Oportunidades (NPO)** con NLP.

#### ¿Qué puedes hacer aquí?
1. **Subir archivos con Extracción de Tablas y Verificación SHA-256 (Pestaña 1):**
   - Puedes subir archivos `.pdf`, `.docx`, `.txt`, `.md`, `.json`, `.csv`.
   - El sistema calcula su **firma criptográfica SHA-256** para prevenir duplicados y garantizar la inmutabilidad de la evidencia.
   - Extrae automáticamente las **tablas estructuradas** incrustadas en el PDF o Word y las muestra en pantalla como tablas interactivas con filas y columnas limpias.
   - Ejecuta NLP para clasificar los hallazgos en:
     - 🎯 **Necesidades (N):** Lo que la empresa debe hacer obligatoriamente.
     - ⚠️ **Problemas (P):** Fallas, caídas de servicio, retrasos o vulnerabilidades.
     - 💡 **Oportunidades (O):** Ideas de modernización y optimización.
   - Muestra el **Índice de Urgencia / Severidad (0% a 100%)**, conceptos tecnológicos y procesos COBIT 2019 mapeados.
2. **Motor de Búsqueda FTS5 de Texto Completo (Pestaña 2):**
   - Escribe cualquier palabra clave (ej. *ciberseguridad*, *backup*, *ransomware*, *continuidad*, *DRP*).
   - El motor **SQLite FTS5 con algoritmo BM25** busca en milisegundos en todos los documentos del cliente y te presenta los fragmentos coincidentes (**snippets**) con las palabras resaltadas en color amarillo/azul.
3. **Repositorio Histórico de Documentos (Pestaña 3):**
   - Consulta el inventario de documentos cargados para la empresa, con su firma SHA-256, diagnóstico de capa de texto (Digital / OCR) y un visor para consultar las tablas estructuradas archivadas.

---

### MÓDULO 8: 📥 REPORTES EJECUTIVOS Y EXPORTACIÓN

#### ¿Para qué sirve?
Es el módulo final de entrega. Cuando termines tu consultoría, aquí generas los documentos formales que se le entregan a la junta directiva y a los auditores.

#### ¿Qué puedes descargar?
1. **📄 Informe Ejecutivo en PDF (Botón azul "⬇️ Descargar Informe PDF"):**
   - Genera un documento PDF formal y estilizado con la portada institucional de la consultoría.
   - Contiene: Ficha de la empresa, resultados de los 5 dominios con semáforos de estado, tabla detallada de las 5 brechas más críticas con sus evidencias, y el cronograma de proyectos de la hoja de ruta con sus presupuestos.
2. **📊 Matriz Completa en Excel (.xlsx) (Botón "⬇️ Descargar Libro Excel"):**
   - Genera una hoja de cálculo profesional con 3 pestañas:
     - *Pestaña 1:* Resumen de parámetros e indicadores de gobernanza.
     - *Pestaña 2:* La tabla completa con los procesos evaluados, sus notas actuales, metas, brechas y textos de evidencia.
     - *Pestaña 3:* El resumen estadístico por dominios.

---

## 🚀 TUTORIAL PASO A PASO: TU PRIMERA CONSULTORÍA DESDE CERO

Sigue esta guía paso a paso para realizar una consultoría completa de principio a fin:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FLUJO DE CONSULTORÍA COBIT 2019                       │
│                                                                             │
│  [1. Iniciar Sesión] ──> [2. Crear Cliente] ──> [3. Crear Evaluación]       │
│           │                                              │                  │
│           ▼                                              ▼                  │
│  [4. Calificar 0-5]  ──> [5. Ver Dashboard] ──> [6. Diagnóstico IA]        │
│           │                                              │                  │
│           ▼                                              ▼                  │
│  [7. Crear Roadmap]  ──> [8. Ingesta NLP]   ──> [9. Descargar PDF y Excel]  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Paso 1: Ingresa al sistema
1. Abre tu navegador en `http://localhost:8501`.
2. Escribe usuario `consultor` y contraseña `cobit2019`. Haz clic en **"🔑 Entrar al Sistema"**.

### Paso 2: Registra o selecciona a tu cliente
1. En el menú de la izquierda, haz clic en **"🏢 Gestión de Clientes"**.
2. Si vas a practicar con la empresa de ejemplo (*Financiera del Café S.A.*), ya está lista en la lista; asegúrate de que tenga el botón verde de "Activo".
3. Si vas a registrar una empresa real, ve a la pestaña **"➕ Registrar Nuevo Cliente"**, llena su nombre, NIT y sector, y presiona **"Guardar"**.

### Paso 3: Realiza la Evaluación de Madurez
1. En el menú, haz clic en **"📝 Evaluación de Madurez"**.
2. Verifica que el cliente sea el correcto.
3. Si quieres crear una evaluación nueva, elige **"➕ Crear Nueva Evaluación"**, escribe un título y selecciona si quieres evaluar los 40 procesos o solo los 18 procesos core. Presiona **"Iniciar Expediente"**.
4. Haz clic en las pestañas (`EDM`, `APO`, `BAI`, `DSS`, `MEA`).
5. Abre cada proceso y mueve el slider para asignarle su nota actual (de 0 a 5) y la nota meta que quiere alcanzar.
6. Escribe una línea breve en *"Evidencias"* (ej. *"Cuentan con manual de procedimientos pero no se actualiza desde hace 2 años"*).
7. Cuando termines, baja hasta el final de la página y presiona el botón azul **"💾 Guardar Todas las Calificaciones y Recalcular IMO"**.

### Paso 4: Revisa el Dashboard Ejecutivo
1. En el menú, haz clic en **"📊 Dashboard Principal"**.
2. Observa el valor del **IMO** (ej. `2.15 / 5.0`).
3. Mira la gráfica de **Radar**: fíjate en qué dominio el área azul está más alejada de la línea verde (ahí está el mayor problema del cliente).
4. Revisa la tabla del **Top 5 de Brechas Críticas** para saber qué procesos necesitan intervención urgente.

### Paso 5: Consulta el Diagnóstico Inteligente de la IA
1. En el menú lateral, haz clic en **"🤖 Diagnóstico e IA"**.
2. En la pestaña **"📑 Diagnóstico Integral"**, revisa el resumen ejecutivo automático, el porcentaje de evidencias trazables y los hallazgos por dominio.
3. Pasa a la pestaña **"🎯 Alineación Estratégica con IA / NLP"**:
   - Selecciona un reto preconfigurado del menú desplegable o escribe una meta en el campo de texto (ej. *"Queremos digitalizar los pagos para reducir errores en cajas y evitar fraudes"*).
   - Presiona **"🚀 Analizar Alineación Semántica"**.
   - Observa la afinidad semántica porcentual, la criticidad y la práctica de COBIT 2019 que viabiliza el objetivo.
4. Pasa a la pestaña **"🛡️ Matriz de Riesgos"** para consultar los niveles de exposición calculados en ciberseguridad, continuidad, gobernanza, cumplimiento y servicios.

### Paso 6: Genera la Hoja de Ruta Algorítmica, Gantt y Dependencias
1. En el menú, haz clic en **"🗺️ Hoja de Ruta (Roadmap)"**.
2. Despliega el panel **"⚙️ Motor Algorítmico Multi-Criterio"**:
   - Escoge la estrategia de optimización deseada (*Equilibrado*, *Priorizar Quick Wins*, *Ciberseguridad y Continuidad* o *Gobierno Directivo*).
   - Selecciona el horizonte de tiempo (12, 18 o 24 meses).
   - Ajusta la holgura de inversión con el slider.
3. Presiona **"⚡ Calcular y Guardar Hoja de Ruta"**.
4. Revisa la sección destacada de **⚡ Quick Wins Prioritarios**: el algoritmo te explicará la justificación matemática de por qué iniciarlos en los primeros 90 días.
5. Examina el **Diagrama de Gantt interactivo**: haz zoom, coloca el cursor sobre las barras para ver los costos y las dependencias, y revisa las líneas rojas de los **3 Hitos Estratégicos (Milestones)**.
6. Consulta la **Auditoría de Dependencias Bloqueantes**: corrobora que no existan dependencias circulares y ubica las tareas prioritarias en la **🔥 Ruta Crítica**.
7. Explora las pestañas de **Fase 1, Fase 2 y Fase 3** para examinar los proyectos detallados con sus fechas calendario, alcances técnicos, roles responsables y presupuestos paramétricos en COP.

### Paso 7: Ingesta Documental, Tablas y Búsqueda FTS5
1. En el menú, haz clic en **"📄 Ingesta Documental"**.
2. En la pestaña **"📤 Cargar y Analizar Documento"**, sube un archivo PDF o Word institucional (o pega texto).
3. Presiona **"🚀 Extraer Tablas y Analizar NPO"**.
4. Visualiza las **tablas estructuradas** extraídas automáticamente del documento y el hash criptográfico **SHA-256** generado para garantizar su autenticidad.
5. Ve a la pestaña **"🔍 Búsqueda FTS5 de Texto Completo"** y escribe cualquier término (ej. *ciberseguridad*, *riesgo*, *backup*) para ver búsquedas instantáneas con resaltado de fragmentos (*snippets*).

### Paso 8: Descarga los Entregables Finales
1. En el menú, haz clic en **"📥 Reportes y Descargas"**.
2. Haz clic en el botón azul **"⬇️ Descargar Informe PDF"**. Se guardará en tu computador un archivo PDF formal listo para imprimir o enviar por correo.
3. Haz clic en el botón verde **"⬇️ Descargar Libro Excel (.xlsx)"** para tener todas las tablas y notas en hojas de cálculo.

---

## 📚 GLOSARIO DE TÉRMINOS SENCILLOS

Para que hables como todo un consultor experto sin enredarte con tecnicismos:

- **COBIT 2019:** Marco de referencia internacional que dice cómo gobernar y gestionar la tecnología en una empresa.
- **Dominio:** Cada una de las 5 grandes familias de procesos en COBIT (EDM, APO, BAI, DSS, MEA).
- **Proceso / Objetivo:** Una actividad específica de TI (ej. `APO13` es Seguridad, `DSS04` es Continuidad, `BAI06` son Cambios de software). Hay 40 en total.
- **Nivel de Capacidad / Madurez (0 a 5):** La nota que saca un proceso, desde 0 (inexistente) hasta 5 (óptimo con mejora continua).
- **IMO (Índice de Madurez Organizacional):** El promedio ponderado de toda la empresa en escala de 0 a 5. Es la calificación final de la empresa.
- **Brecha (*Gap*):** La resta matemática entre lo que la empresa quiere sacar (Meta) y lo que tiene hoy (Actual). Si la meta es 4.0 y hoy tiene 1.5, la brecha es de 2.5 puntos.
- **Quick Win (Victoria Temprana):** Un proyecto de mejora que genera mucho impacto positivo, cuesta poco dinero y se puede terminar en menos de 90 días.
- **SLA (Acuerdo de Nivel de Servicio):** El contrato interno donde TI promete en cuántas horas o minutos solucionará una falla.
- **DRP (Plan de Recuperación ante Desastres):** El plan de emergencia que dice qué hacer si se quema el servidor, se cae internet o se inunda la oficina.
- **SGSI:** Sistema de Gestión de Seguridad de la Información (las políticas y controles que impiden que los hackers roben los datos).
- **NPO:** Necesidades, Problemas y Oportunidades extraídas de un texto documental.

---

## ❓ PREGUNTAS FRECUENTES (FAQ)

### 1. ¿Qué pasa si cierro la aplicación? ¿Se pierden mis datos?
**No, nunca.** Todo lo que guardas queda almacenado de forma permanente en la base de datos relacional SQLite (`cobit_core.db`). Cuando vuelvas a iniciar la aplicación, todo tu trabajo seguirá exactamente donde lo dejaste.

### 2. ¿Puedo evaluar a varias empresas a la vez?
**Sí.** Puedes registrar tantas empresas como desees en el módulo de *Gestión de Clientes*. Solo recuerda seleccionar con cuál quieres trabajar antes de ir a calificar o ver el dashboard.

### 3. ¿Tengo que calificar obligatoriamente los 40 procesos?
No necesariamente. Si tienes poco tiempo o la empresa es pequeña, puedes crear un **Diagnóstico Rápido (Quick Assessment)**, el cual selecciona automáticamente los 18 procesos primordiales de COBIT 2019.

### 4. ¿La aplicación requiere internet para funcionar?
**No.** La aplicación corre 100% de manera local en tu computador. El motor de diagnóstico, las fórmulas matemáticas, los gráficos, el PDF y el Excel se generan directamente en tu máquina sin costo de conexión ni consumo de APIs de pago.

### 5. ¿Cómo sé si mi sistema está funcionando sin errores?
Puedes abrir tu terminal y ejecutar:
```bash
python test_cobit_core.py
```
El sistema ejecutará automáticamente una prueba de 6 módulos y te confirmará en segundos que todo el sistema está operativo al 100%.
