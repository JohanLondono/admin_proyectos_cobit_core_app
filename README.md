# 🏛️ COBIT Core Consulting System (COBIT 2019 + IA)

**Universidad del Quindío — 8vo Semestre | Formulación de Proyectos**  
**Equipo:** Johan Londoño, Julián Hoyos, Kevin García  
**Marco Metodológico:** Alineado estrictamente al Cronograma de Requisitos en Jira (`CRONOGRAMA_REQUISITOS_JIRA_COBIT.txt`).

---

## 🎯 Propósito del Proyecto
Sistema integral y modular construido en **Python** con **Streamlit** y persistencia en **SQLite**, enfocado exclusivamente en las funciones y requisitos primordiales para la consultoría formal en gobierno y gestión de tecnologías de información bajo el marco internacional **COBIT 2019 (ISACA)**.

---

## 🚀 Inicio Rápido (Quickstart)

### 1. Requisitos Previos
Tener instalado Python 3.10 o superior.

### 2. Instalación de Dependencias
Abre una terminal en la carpeta del proyecto y ejecuta:
```bash
pip install -r requirements.txt
```

### 3. Ejecución de la Aplicación
Inicia el servidor local de Streamlit:
```bash
streamlit run app.py
```
La aplicación abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 🔑 Credenciales de Acceso Preconfiguradas

La base de datos SQLite se inicializa de forma automática con datos semilla y tres roles diferenciados (RBAC):

| Rol | Usuario | Contraseña | Descripción |
| :--- | :--- | :--- | :--- |
| **👑 Administrador** | `admin` | `admin123` | Control total del sistema, configuración y usuarios. |
| **💼 Consultor Líder** | `consultor` | `cobit2019` | Gestión de empresas, evaluaciones, diagnósticos y hojas de ruta. |
| **🏢 Cliente Corporativo** | `cliente` | `cliente2019` | Acceso a tableros ejecutivos, reportes e informes de su organización. |

---

## 📦 Estructura de la Aplicación

```text
cobit_core_app/
├── app.py                      # Router principal, control de sesiones y navegación
├── requirements.txt            # Dependencias del proyecto (Streamlit, Plotly, Pandas, ReportLab, OpenPyXL)
├── README.md                   # Esta documentación
├── test_cobit_core.py          # Batería de pruebas automatizadas (6/6 suites)
├── cobit_core.db               # Base de datos relacional SQLite (auto-migrada)
│
├── database/
│   ├── __init__.py
│   └── db_manager.py           # Gestor SQLite, tablas, migraciones y operaciones CRUD
│
├── engine/
│   ├── __init__.py
│   ├── cobit_data.py           # Catálogo oficial: 5 dominios y 40 procesos con rúbricas de madurez
│   ├── maturity_engine.py      # Algoritmo de Madurez Ponderada e IMO Global [COB-TK08]
│   ├── ai_engine.py            # Motor de IA: análisis NPO, alineación estratégica y riesgos [COB-ST09, COB-ST12]
│   ├── roadmap_engine.py       # Algoritmo multi-criterio de hoja de ruta y Quick Wins [COB-TK10, COB-ST14]
│   └── export_engine.py        # Generador de informes PDF y libros Excel [COB-ST19, COB-ST20]
│
├── views/
│   ├── __init__.py
│   ├── dashboard_view.py       # Dashboard con gráfico Radar Plotly y KPIs ejecutivos
│   ├── clients_view.py         # CRUD de empresas clientes y directorio de contactos
│   ├── catalog_view.py         # Explorador interactivo con buscador y filtros por dominio
│   ├── assessment_view.py      # Cuestionario interactivo de capacidad 0-5 con evidencias
│   ├── diagnosis_view.py       # Diagnóstico cualitativo, alineación estratégica y matriz de riesgos
│   ├── roadmap_view.py         # Hoja de ruta por fases (Corto, Mediano, Largo Plazo) y Quick Wins
│   ├── documents_view.py       # Ingesta documental y extracción de términos NPO
│   └── reports_view.py         # Descargas directas en formato PDF y Excel (.xlsx)
│
└── static/
    └── custom.css              # Estilos visuales modernos, tipografía Inter/Outfit y tarjetas
```

---

## 📋 Mapeo con el Cronograma de Jira

| Épica / Requisito Jira | Implementación en COBIT Core | Estado |
| :--- | :--- | :---: |
| **[COB-TK01, TK04]** Arquitectura Base y Esquema SQLite | `database/db_manager.py` con auto-inicialización y datos semilla. | ✅ **100%** |
| **[COB-ST01, ST03]** Autenticación y Roles (RBAC) | `app.py` con pantalla de login y sesiones seguras por rol. | ✅ **100%** |
| **[COB-ST04, ST05]** CRUD de Clientes y Contactos | `views/clients_view.py` con directorios de CIO, CISO, etc. | ✅ **100%** |
| **[COB-TK05, ST07]** Catálogo COBIT 2019 (40 Procesos) | `engine/cobit_data.py` y `views/catalog_view.py` con buscador en vivo. | ✅ **100%** |
| **[COB-ST08, ST09]** Ingesta Documental y Análisis NPO | `views/documents_view.py` con extracción de Necesidades, Problemas y Oportunidades. | ✅ **100%** |
| **[COB-ST10, ST11]** Cuestionario de Madurez (Escala 0-5) | `views/assessment_view.py` con selector rápido/integral y evidencias. | ✅ **100%** |
| **[COB-TK08]** Algoritmo Matemático de Madurez (IMO) | `engine/maturity_engine.py` con pesos por dominio e intervalos. | ✅ **100%** |
| **[COB-ST12, ST13]** Alineación con IA y Matriz de Riesgos | `views/diagnosis_view.py` con sugerencias de procesos y mitigaciones. | ✅ **100%** |
| **[COB-TK10, ST14]** Hoja de Ruta en 3 Fases y Quick Wins | `views/roadmap_view.py` con algoritmo multi-criterio y presupuesto. | ✅ **100%** |
| **[COB-ST16, ST17]** Dashboard Radar Plotly y KPIs | `views/dashboard_view.py` con radar interactivo Actual vs Meta. | ✅ **100%** |
| **[COB-ST19, ST20]** Exportación de Informes PDF y Excel | `views/reports_view.py` con ReportLab y OpenPyXL en 1 clic. | ✅ **100%** |

---

## 🧪 Ejecución de Pruebas
Para verificar la integridad del sistema en cualquier momento:
```bash
python test_cobit_core.py
```
Resultado: **6/6 pruebas aprobadas satisfactoriamente al 100%**.
