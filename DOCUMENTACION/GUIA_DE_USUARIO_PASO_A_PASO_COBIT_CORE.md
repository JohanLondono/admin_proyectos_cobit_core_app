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

El sistema cuenta con tres tipos de usuarios listos para usar:

| Si quieres entrar como... | Usuario | Contraseña | ¿Qué podrás hacer? |
| :--- | :--- | :--- | :--- |
| **👑 Administrador** | `admin` | `admin123` | Acceso a todo el sistema y configuración general. |
| **💼 Consultor Líder** *(Recomendado)* | `consultor` | `cobit2019` | Crear clientes, realizar evaluaciones, usar la IA y generar hojas de ruta. |
| **🏢 Cliente (CIO / Gerente)** | `cliente` | `cliente2019` | Ver el dashboard, consultar resultados y descargar informes de su empresa. |

> 💡 **Consejo:** Para realizar todo el recorrido de consultoría, ingresa con el usuario **`consultor`** y la contraseña **`cobit2019`**.

---

## 🧭 CÓMO MOVERSE POR EL SISTEMA (EL MENÚ LATERAL)

A la izquierda de tu pantalla siempre tendrás una barra lateral (Sidebar) con el menú principal:

- 📊 **Dashboard Principal:** La pantalla de control con los gráficos y los puntajes globales.
- 🏢 **Gestión de Clientes:** Donde registras las empresas y a sus directivos de contacto.
- 📖 **Catálogo COBIT 2019:** Tu enciclopedia interactiva con los 40 procesos oficiales explicados.
- 📝 **Evaluación de Madurez:** El cuestionario donde calificas los procesos del 0 al 5.
- 🤖 **Diagnóstico e IA:** El asistente inteligente que analiza brechas y redacta hallazgos.
- 🗺️ **Hoja de Ruta (Roadmap):** El plan de proyectos por fases con fechas y presupuestos.
- 📄 **Ingesta Documental (NLP):** Donde subes políticas o auditorías para que la IA extraiga problemas automáticamente.
- 📥 **Reportes y Descargas:** Donde descargas el PDF y el Excel con un solo clic.
- 🚪 **Cerrar Sesión:** Para salir del sistema de forma segura.

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
Toma los datos numéricos de la evaluación y los convierte en **diagnósticos en prosa**, hallazgos cualitativos y una matriz de riesgos mediante un motor de inteligencia heurística.

#### ¿Qué puedes hacer aquí?
Tiene 3 pestañas muy poderosas:

1. **Pestaña "📑 Diagnóstico Integral":**
   - Te redacta un informe ejecutivo automático con fecha, estado del cliente, hallazgos clave por dominio y recomendaciones prioritarias. ¡Listo para copiar y pegar en un informe!
2. **Pestaña "🎯 Alineación Estratégica":**
   - Escribe en una frase lo que la empresa quiere lograr (ej. *"Queremos abrir sucursales en todo el país sin que se caiga el sistema y evitando hackeos"*).
   - Presionas **"Analizar Alineación"** y la IA te dirá con exactitud matemática cuáles procesos COBIT deben fortalecerse para que ese sueño se haga realidad, con su criticidad y justificación.
3. **Pestaña "🛡️ Matriz de Riesgos":**
   - Analiza las debilidades y te alerta sobre los peligros reales: ¿Están expuestos a ransomware? ¿Tienen riesgo de multas legales? ¿Qué acción de mitigación deben tomar ya mismo?

---

### MÓDULO 6: 🗺️ HOJA DE RUTA (ROADMAP) Y QUICK WINS

#### ¿Para qué sirve?
Un diagnóstico sin un plan de acción no sirve para nada. Este módulo toma todas las debilidades encontradas y **construye un plan de proyectos ordenado en el tiempo** para los próximos 18 meses, con presupuesto estimado en dinero y responsables sugeridos.

#### ¿Cómo se organiza el plan?
El sistema divide los proyectos en 3 etapas:
- **Fase 1: Cimientos y Quick Wins (Meses 1 al 3):** Cosas urgentes y rápidas que se pueden solucionar en menos de 90 días con poco dinero (ej. activar autenticación multifactor, publicar el manual de copias de seguridad).
- **Fase 2: Consolidación y Procesos Core (Meses 4 al 8):** Proyectos más grandes como armar el Plan de Continuidad ante Desastres (DRP) o el Sistema de Gestión de Seguridad (SGSI).
- **Fase 3: Optimización y Monitoreo (Meses 9 al 18):** Iniciativas avanzadas como analítica de datos, gobierno de datos y mejora continua.

#### ¿Qué puedes hacer aquí?
- Ver el **Presupuesto Total Estimado** en pesos colombianos (COP).
- Revisar la tarjeta verde destacada de **⚡ QUICK WINS** (victorias tempranas que le dan resultados inmediatos al cliente para ganar su confianza).
- Consultar iniciativa por iniciativa quién es el rol responsable (ej. *CISO*, *Gerente de TI*, *Líder de Proyectos*), cuántos meses dura y cuánto costará.
- Si cambiaste notas en la evaluación, haces clic en **"⚡ Regenerar Hoja de Ruta"** y el algoritmo recalcula todo el plan al instante.

---

### MÓDULO 7: 📄 INGESTA DOCUMENTAL Y ANÁLISIS NPO (NLP)

#### ¿Para qué sirve?
A los consultores de TI siempre les entregan documentos densos de 100 páginas (manuales de políticas, informes de auditoría anteriores, planes estratégicos). Este módulo analiza esos textos y **extrae automáticamente las Necesidades, Problemas y Oportunidades (NPO)** sin que tengas que leer página por página.

#### ¿Qué puedes hacer aquí?
1. **Subir un archivo o pegar texto:**
   - Puedes subir archivos `.txt`, `.docx`, `.pdf`, `.md`, o simplemente copiar y pegar un fragmento del informe de auditoría del cliente en el cuadro de texto.
2. **Procesar con NLP (Procesamiento de Lenguaje Natural):**
   - Haces clic en **"🚀 Extraer y Analizar NPO"**.
   - En segundos, el sistema clasifica la información en 3 columnas:
     - 🎯 **Necesidades (N):** Lo que la empresa debe hacer obligatoriamente.
     - ⚠️ **Problemas (P):** Fallas, caídas de servicio o riesgos detectados en el texto.
     - 💡 **Oportunidades (O):** Ideas de modernización y automatización.
   - Además, te dice qué procesos de COBIT 2019 están relacionados con lo que dice ese documento.

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

### Paso 5: Consulta el Diagnóstico de la IA
1. En el menú, haz clic en **"🤖 Diagnóstico e IA"**.
2. Lee el informe que la IA redactó de forma automática.
3. Pasa a la pestaña **"Alineación Estratégica"**, escribe un reto del cliente (ej. *"Queremos digitalizar los pagos para reducir errores en cajas"*) y presiona **"Analizar Alineación"**. Verás qué procesos apoyan esa meta.
4. Pasa a la pestaña **"Matriz de Riesgos"** para ver qué riesgos tecnológicos tiene abiertos la empresa.

### Paso 6: Genera la Hoja de Ruta (Roadmap)
1. En el menú, haz clic en **"🗺️ Hoja de Ruta (Roadmap)"**.
2. Si es la primera vez, presiona **"🚀 Generar Hoja de Ruta Ahora"**.
3. Revisa la tarjeta de **⚡ Quick Wins**: esos son los proyectos que debes proponerle al cliente que inicie este mismo mes.
4. Explora las pestañas de **Fase 1, Fase 2 y Fase 3** para ver el cronograma a 18 meses y el presupuesto total sugerido.

### Paso 7: Descarga los Entregables Finales
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
