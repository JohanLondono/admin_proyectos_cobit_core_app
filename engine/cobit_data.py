"""
Catálogo de Referencia COBIT 2019 y Escalas de Madurez.
Contiene los 5 dominios, los 40 procesos oficiales con propósitos y prácticas,
escalas de capacidad/madurez (0 a 5) y ponderaciones sectoriales.
"""

from typing import Dict, List, Any

# Dominios oficiales COBIT 2019
DOMAINS = {
    "EDM": {
        "name": "Evaluar, Dirigir y Monitorizar (EDM)",
        "english": "Evaluate, Direct and Monitor",
        "type": "Gobierno",
        "color": "#1E3A8A", # Deep Blue
        "description": "Responsabilidad del Directorio / Junta Directiva. Evalúa necesidades, dirige prioridades y monitoriza el cumplimiento y desempeño."
    },
    "APO": {
        "name": "Alinear, Planificar y Organizar (APO)",
        "english": "Align, Plan and Organise",
        "type": "Gestión",
        "color": "#0284C7", # Sky Blue
        "description": "Identifica cómo la TI puede contribuir de la mejor manera al logro de los objetivos del negocio."
    },
    "BAI": {
        "name": "Construir, Adquirir e Implementar (BAI)",
        "english": "Build, Acquire and Implement",
        "type": "Gestión",
        "color": "#059669", # Emerald Green
        "description": "Transforma los requisitos en soluciones concretas de TI y las implementa en los procesos de negocio."
    },
    "DSS": {
        "name": "Entregar, Dar Servicio y Soporte (DSS)",
        "english": "Deliver, Service and Support",
        "type": "Gestión",
        "color": "#D97706", # Amber
        "description": "Asegura la entrega efectiva y eficiente de los servicios de TI requeridos, incluida la seguridad y continuidad."
    },
    "MEA": {
        "name": "Monitorizar, Evaluar y Valorar (MEA)",
        "english": "Monitor, Evaluate and Assess",
        "type": "Gestión",
        "color": "#7C3AED", # Purple
        "description": "Supervisa todos los procesos para asegurar que la dirección establecida se siga y se mantenga la conformidad."
    }
}

# 40 Procesos Oficiales de COBIT 2019
COBIT_PROCESSES = {
    # Dominio EDM (5 procesos)
    "EDM01": {
        "domain": "EDM",
        "name": "Asegurar el Establecimiento y Mantenimiento del Marco de Gobernanza",
        "purpose": "Proporcionar un enfoque coherente e integrado alineado con la misión corporativa.",
        "practices": ["Evaluar el sistema de gobernanza", "Dirigir el sistema de gobernanza", "Monitorizar el sistema de gobernanza"],
        "core": True
    },
    "EDM02": {
        "domain": "EDM",
        "name": "Asegurar la Entrega de Beneficios",
        "purpose": "Garantizar el valor óptimo de las iniciativas de TI habilitadas para el negocio.",
        "practices": ["Evaluar la optimización del valor", "Dirigir la optimización del valor", "Monitorizar la optimización del valor"],
        "core": True
    },
    "EDM03": {
        "domain": "EDM",
        "name": "Asegurar la Optimización del Riesgo",
        "purpose": "Asegurar que el apetito y la tolerancia al riesgo empresarial sean entendidos y gestionados.",
        "practices": ["Evaluar la gestión del riesgo", "Dirigir la gestión del riesgo", "Monitorizar la gestión del riesgo"],
        "core": True
    },
    "EDM04": {
        "domain": "EDM",
        "name": "Asegurar la Optimización de Recursos",
        "purpose": "Garantizar que los recursos humanos, financieros y tecnológicos sean adecuados y suficientes.",
        "practices": ["Evaluar la gestión de recursos", "Dirigir la gestión de recursos", "Monitorizar la gestión de recursos"],
        "core": False
    },
    "EDM05": {
        "domain": "EDM",
        "name": "Asegurar el Compromiso de las Partes Interesadas",
        "purpose": "Garantizar que la comunicación con los stakeholders sea transparente y oportuna.",
        "practices": ["Evaluar requisitos de las partes interesadas", "Dirigir la comunicación", "Monitorizar el compromiso"],
        "core": False
    },

    # Dominio APO (14 procesos)
    "APO01": {
        "domain": "APO",
        "name": "Gestionar el Marco de Gestión de I&T",
        "purpose": "Diseñar e implementar una estructura organizativa y operativa clara para TI.",
        "practices": ["Diseñar la estructura de gestión", "Definir roles y responsabilidades", "Mantener políticas y procedimientos"],
        "core": True
    },
    "APO02": {
        "domain": "APO",
        "name": "Gestionar la Estrategia",
        "purpose": "Alinear los planes de TI con la dirección estratégica general del negocio.",
        "practices": ["Comprender el contexto empresarial", "Evaluar capacidades actuales", "Definir el plan estratégico de TI"],
        "core": True
    },
    "APO03": {
        "domain": "APO",
        "name": "Gestionar la Arquitectura Empresarial",
        "purpose": "Establecer una arquitectura que vincule componentes de negocio, datos, aplicaciones y tecnología.",
        "practices": ["Desarrollar la visión de arquitectura", "Definir arquitecturas de referencia", "Gestionar transiciones arquitectónicas"],
        "core": False
    },
    "APO04": {
        "domain": "APO",
        "name": "Gestionar la Innovación",
        "purpose": "Identificar oportunidades tecnológicas emergentes que generen ventaja competitiva.",
        "practices": ["Crear un entorno para la innovación", "Evaluar tecnologías emergentes", "Fomentar iniciativas piloto"],
        "core": False
    },
    "APO05": {
        "domain": "APO",
        "name": "Gestionar el Portafolio",
        "purpose": "Optimizar el rendimiento del portafolio global de programas, proyectos y servicios de TI.",
        "practices": ["Definir criterios de inversión", "Evaluar y priorizar programas", "Monitorear el rendimiento del portafolio"],
        "core": False
    },
    "APO06": {
        "domain": "APO",
        "name": "Gestionar el Presupuesto y los Costos",
        "purpose": "Garantizar una gestión financiera transparente, predecible y eficiente de TI.",
        "practices": ["Elaborar presupuestos anuales", "Monitorear costos y desvíos", "Gestionar asignación de costos y ROI"],
        "core": False
    },
    "APO07": {
        "domain": "APO",
        "name": "Gestionar los Recursos Humanos",
        "purpose": "Desarrollar y retener el talento tecnológico necesario para los objetivos institucionales.",
        "practices": ["Planificar necesidades de personal", "Evaluar competencias de TI", "Capacitar y gestionar planes de carrera"],
        "core": False
    },
    "APO08": {
        "domain": "APO",
        "name": "Gestionar las Relaciones",
        "purpose": "Construir relaciones de confianza y colaboración entre TI y las áreas de negocio.",
        "practices": ["Entender expectativas de las áreas usuarias", "Gestionar satisfacción del cliente interno", "Coordinar comités de enlace"],
        "core": False
    },
    "APO09": {
        "domain": "APO",
        "name": "Gestionar los Acuerdos de Servicio (SLA)",
        "purpose": "Formalizar y monitorear acuerdos de nivel de servicio acordes a las necesidades operativas.",
        "practices": ["Catalogar servicios de TI", "Negociar y acordar SLAs", "Revisar y reportar cumplimiento de SLAs"],
        "core": True
    },
    "APO10": {
        "domain": "APO",
        "name": "Gestionar los Proveedores",
        "purpose": "Minimizar riesgos y asegurar la calidad en la contratación de terceros y proveedores tecnológicos.",
        "practices": ["Evaluar y seleccionar proveedores", "Gestionar contratos de TI", "Supervisar desempeño de proveedores"],
        "core": False
    },
    "APO11": {
        "domain": "APO",
        "name": "Gestionar la Calidad",
        "purpose": "Asegurar que las soluciones y servicios cumplan sistemáticamente con los estándares definidos.",
        "practices": ["Establecer un sistema de gestión de calidad", "Enfocar la calidad en el cliente", "Monitorear y auditar la calidad"],
        "core": False
    },
    "APO12": {
        "domain": "APO",
        "name": "Gestionar el Riesgo",
        "purpose": "Identificar, evaluar y mitigar de manera continua los riesgos operacionales y de ciberseguridad.",
        "practices": ["Recopilar datos de eventos de riesgo", "Analizar impacto y probabilidad", "Ejecutar planes de respuesta a riesgos"],
        "core": True
    },
    "APO13": {
        "domain": "APO",
        "name": "Gestionar la Seguridad",
        "purpose": "Establecer y mantener un sistema de gestión de seguridad de la información (SGSI).",
        "practices": ["Definir el marco de seguridad", "Gestionar la política de seguridad", "Monitorear el estado de seguridad"],
        "core": True
    },
    "APO14": {
        "domain": "APO",
        "name": "Gestionar los Datos",
        "purpose": "Garantizar la calidad, integridad, gobernanza y disponibilidad de los activos de datos.",
        "practices": ["Definir estrategia de gobierno de datos", "Asegurar integridad y linaje de datos", "Gestionar el ciclo de vida de los datos"],
        "core": False
    },

    # Dominio BAI (11 procesos)
    "BAI01": {
        "domain": "BAI",
        "name": "Gestionar los Programas",
        "purpose": "Gestionar iniciativas agrupadas de cambio para asegurar el logro de resultados de negocio.",
        "practices": ["Iniciar programas de inversión", "Monitorear ejecución de programas", "Gestionar cierre de programas"],
        "core": False
    },
    "BAI02": {
        "domain": "BAI",
        "name": "Gestionar la Definición de Requisitos",
        "purpose": "Asegurar que los requisitos de negocio y funcionales sean claros, completos y trazables.",
        "practices": ["Levantar necesidades de usuarios", "Especificar requisitos funcionales y de seguridad", "Validar y aprobar especificaciones"],
        "core": True
    },
    "BAI03": {
        "domain": "BAI",
        "name": "Gestionar la Identificación y Construcción de Soluciones",
        "purpose": "Diseñar, construir o adquirir componentes de software acordes a los requisitos aprobados.",
        "practices": ["Diseñar arquitectura de solución", "Desarrollar y probar componentes", "Asegurar controles de seguridad por diseño"],
        "core": False
    },
    "BAI04": {
        "domain": "BAI",
        "name": "Gestionar la Disponibilidad y la Capacidad",
        "purpose": "Garantizar que la infraestructura y sistemas satisfagan la demanda actual y futura de procesamiento.",
        "practices": ["Evaluar capacidad y uso actual", "Planificar ampliaciones de capacidad", "Monitorear disponibilidad de servicios"],
        "core": False
    },
    "BAI05": {
        "domain": "BAI",
        "name": "Gestionar el Cambio Organizacional",
        "purpose": "Facilitar la adopción cultural y operativa de nuevas herramientas tecnológicas en el personal.",
        "practices": ["Diseñar plan de gestión del cambio", "Gestionar la comunicación del cambio", "Monitorear adopción y capacitación"],
        "core": False
    },
    "BAI06": {
        "domain": "BAI",
        "name": "Gestionar los Cambios de TI",
        "purpose": "Minimizar el impacto negativo y los fallos derivados de modificaciones en sistemas e infraestructura.",
        "practices": ["Evaluar y clasificar cambios", "Aprobar solicitudes en Comité CAB", "Ejecutar y revisar post-implementación"],
        "core": True
    },
    "BAI07": {
        "domain": "BAI",
        "name": "Gestionar la Aceptación del Cambio y la Transición",
        "purpose": "Asegurar que los nuevos sistemas sean probados exhaustivamente antes de pasar a producción.",
        "practices": ["Definir plan de pruebas y aceptación", "Ejecutar pruebas de estrés y seguridad", "Planificar la puesta en producción"],
        "core": False
    },
    "BAI08": {
        "domain": "BAI",
        "name": "Gestionar el Conocimiento",
        "purpose": "Mantener actualizada y accesible la base de conocimientos técnicos y operacionales de TI.",
        "practices": ["Cultivar transferencia de conocimiento", "Documentar lecciones aprendidas", "Mantener repositorio de documentación técnica"],
        "core": False
    },
    "BAI09": {
        "domain": "BAI",
        "name": "Gestionar los Activos",
        "purpose": "Mantener un inventario confiable y optimizar el uso y licencias de hardware y software.",
        "practices": ["Identificar y registrar activos", "Monitorear ciclo de vida de activos", "Asegurar cumplimiento de licencias"],
        "core": False
    },
    "BAI10": {
        "domain": "BAI",
        "name": "Gestionar la Configuración",
        "purpose": "Mantener la integridad y relaciones de los elementos de configuración (CMDB).",
        "practices": ["Establecer repositorio CMDB", "Actualizar elementos de configuración", "Auditar consistencia de la configuración"],
        "core": False
    },
    "BAI11": {
        "domain": "BAI",
        "name": "Gestionar los Proyectos",
        "purpose": "Entregar proyectos tecnológicos a tiempo, dentro del presupuesto y con la calidad requerida.",
        "practices": ["Definir plan de proyecto y entregables", "Gestionar cronograma y costos", "Monitorear riesgos y cierre de proyectos"],
        "core": True
    },

    # Dominio DSS (6 procesos)
    "DSS01": {
        "domain": "DSS",
        "name": "Gestionar las Operaciones",
        "purpose": "Ejecutar las operaciones rutinarias de TI de manera segura, estable y conforme a procedimientos.",
        "practices": ["Ejecutar procedimientos operativos", "Monitorear infraestructura de TI", "Gestionar respaldos y mantenimiento preventivo"],
        "core": True
    },
    "DSS02": {
        "domain": "DSS",
        "name": "Gestionar las Solicitudes y los Incidentes de Servicio",
        "purpose": "Restaurar los servicios normales de TI con la mayor rapidez posible ante interrupciones.",
        "practices": ["Registrar y clasificar incidentes", "Investigar y diagnosticar causas", "Resolver incidentes y escalar solicitudes"],
        "core": True
    },
    "DSS03": {
        "domain": "DSS",
        "name": "Gestionar los Problemas",
        "purpose": "Identificar y mitigar las causas raíz de incidentes recurrentes para evitar su repetición.",
        "practices": ["Identificar y clasificar problemas", "Investigar y encontrar causa raíz", "Crear soluciones conocidas y errores temporales"],
        "core": False
    },
    "DSS04": {
        "domain": "DSS",
        "name": "Gestionar la Continuidad",
        "purpose": "Asegurar que las operaciones críticas puedan continuar o recuperarse rápidamente ante desastres.",
        "practices": ["Desarrollar plan de continuidad (BCP/DRP)", "Probar planes de recuperación", "Monitorear capacidades de contingencia"],
        "core": True
    },
    "DSS05": {
        "domain": "DSS",
        "name": "Gestionar los Servicios de Seguridad",
        "purpose": "Proteger la confidencialidad, integridad y disponibilidad de la información frente a ciberamenazas.",
        "practices": ["Gestionar identidades y accesos", "Proteger redes y endpoints", "Monitorear eventos de seguridad e intrusiones"],
        "core": True
    },
    "DSS06": {
        "domain": "DSS",
        "name": "Gestionar los Controles de los Procesos de Negocio",
        "purpose": "Mantener la efectividad de los controles automatizados embebidos en las aplicaciones del negocio.",
        "practices": ["Alinear controles de negocio con TI", "Gestionar accesos a transacciones críticas", "Asegurar trazabilidad y no repudio"],
        "core": False
    },

    # Dominio MEA (4 procesos)
    "MEA01": {
        "domain": "MEA",
        "name": "Gestionar el Monitoreo del Desempeño y la Conformidad",
        "purpose": "Evaluar regularmente la efectividad y logro de los objetivos trazados para I&T.",
        "practices": ["Establecer marco de monitoreo y KPIs", "Recopilar métricas de desempeño", "Reportar avances a la alta dirección"],
        "core": True
    },
    "MEA02": {
        "domain": "MEA",
        "name": "Gestionar el Sistema de Control Interno",
        "purpose": "Garantizar que los controles internos sean adecuados, eficaces y cumplan con las directrices.",
        "practices": ["Monitorear la eficacia de los controles", "Ejecutar auto-evaluaciones de control", "Identificar deficiencias y corregir"],
        "core": True
    },
    "MEA03": {
        "domain": "MEA",
        "name": "Gestionar la Conformidad con los Requisitos Externos",
        "purpose": "Garantizar que la organización cumpla con leyes, regulaciones y estándares de la industria aplicables.",
        "practices": ["Identificar leyes y normativas aplicables", "Evaluar nivel de cumplimiento normativo", "Asegurar mitigación de brechas regulatorias"],
        "core": True
    },
    "MEA04": {
        "domain": "MEA",
        "name": "Gestionar el Aseguramiento",
        "purpose": "Proporcionar a los directivos certeza independiente sobre la efectividad de la gobernanza de TI.",
        "practices": ["Planificar auditorías de aseguramiento", "Ejecutar revisiones independientes", "Hacer seguimiento a hallazgos de auditoría"],
        "core": False
    }
}

# Niveles oficiales de Madurez / Capacidad COBIT 2019 (0 a 5)
MATURITY_LEVELS = {
    0: {
        "label": "Incompleto",
        "short_desc": "El proceso no está implementado o no logra su propósito.",
        "description": "Carencia casi total de prácticas o resultados reconocibles. El trabajo se realiza de manera ad-hoc y reactiva sin lineamientos."
    },
    1: {
        "label": "Inicial",
        "short_desc": "El proceso alcanza su propósito de forma intuitiva.",
        "description": "Se logra el propósito del proceso mediante actividades intuitivas y desordenadas. Depende del heroísmo de personas clave sin repetibilidad."
    },
    2: {
        "label": "Gestionado",
        "short_desc": "El proceso se planifica y ejecuta a nivel departamental.",
        "description": "Las prácticas están planificadas, monitorizadas y ajustadas a nivel de área. Existen entregables identificables pero no uniformes para toda la empresa."
    },
    3: {
        "label": "Establecido",
        "short_desc": "El proceso está formalizado y estandarizado en toda la entidad.",
        "description": "El proceso se ejecuta utilizando lineamientos formalmente definidos y documentados a nivel institucional. Permite consistencia organizacional."
    },
    4: {
        "label": "Predecible",
        "short_desc": "El proceso se mide cuantitativamente y se controla.",
        "description": "El proceso se opera dentro de límites definidos usando métricas cuantitativas, KPIs y control estadístico de desviaciones."
    },
    5: {
        "label": "Optimizado",
        "short_desc": "El proceso se mejora continuamente mediante innovación.",
        "description": "Enfoque sistemático en la mejora continua, adopción proactiva de mejores prácticas de la industria y tecnologías emergentes con análisis predictivo."
    }
}

# Sectores industriales predefinidos
SECTORS = [
    "Servicios Financieros y Banca",
    "Salud y Farmacéutica",
    "Tecnología y Software",
    "Manufactura e Industria",
    "Comercio Minorista (Retail)",
    "Gobierno y Sector Público",
    "Educación e Investigación",
    "Telecomunicaciones",
    "Energía y Servicios Públicos",
    "Consultoría y Servicios Profesionales",
    "Otro Sector"
]

# Tamaños de Organización
COMPANY_SIZES = [
    "Microempresa (1 - 10 colaboradores)",
    "Pequeña Empresa (11 - 50 colaboradores)",
    "Mediana Empresa (51 - 250 colaboradores)",
    "Gran Empresa (251 - 1000 colaboradores)",
    "Corporación Multinacional (+1000 colaboradores)"
]

# Procesos esenciales sugeridos para Evaluación Rápida (12 procesos clave)
QUICK_ASSESSMENT_PROCESSES = [
    "EDM01", "EDM02", "EDM03",
    "APO01", "APO02", "APO09", "APO12", "APO13",
    "BAI02", "BAI06", "BAI11",
    "DSS01", "DSS02", "DSS04", "DSS05",
    "MEA01", "MEA02", "MEA03"
]

def get_all_processes_list() -> List[Dict[str, Any]]:
    """Retorna la lista ordenada de los 40 procesos con su metadata."""
    items = []
    for pid, pdata in COBIT_PROCESSES.items():
        items.append({
            "id": pid,
            "domain": pdata["domain"],
            "name": pdata["name"],
            "purpose": pdata["purpose"],
            "practices": pdata["practices"],
            "core": pdata.get("core", False)
        })
    return items

def get_processes_by_domain(domain_code: str) -> List[Dict[str, Any]]:
    """Filtra procesos por dominio."""
    return [p for p in get_all_processes_list() if p["domain"] == domain_code]
