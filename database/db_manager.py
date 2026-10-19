"""
Gestor de Base de Datos SQLite para COBIT Core System.
Maneja conexiones, esquema relacional, migraciones automáticas y operaciones CRUD.
"""

import sqlite3
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

DB_PATH = Path(__file__).parent.parent / "cobit_core.db"

def get_connection() -> sqlite3.Connection:
    """Crea una conexión con row_factory para acceder a columnas por nombre."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def hash_password(password: str) -> str:
    """Retorna el hash SHA-256 de la contraseña."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    """Inicializa las tablas y datos semilla de la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Tabla de Usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL DEFAULT 'consultant', -- 'admin', 'consultant', 'client'
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. Tabla de Empresas Clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tax_id TEXT UNIQUE, -- NIT / RUT
            sector TEXT NOT NULL,
            size TEXT NOT NULL,
            city TEXT,
            phone TEXT,
            email TEXT,
            contact_name TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Activo',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 3. Directorio de Contactos por Cliente
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role_title TEXT,
            department TEXT,
            is_primary INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
        );
        """)

        # 4. Evaluaciones COBIT
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            code TEXT UNIQUE,
            title TEXT NOT NULL,
            assessment_type TEXT DEFAULT 'comprehensive', -- 'quick', 'comprehensive'
            status TEXT DEFAULT 'in_progress', -- 'draft', 'in_progress', 'completed'
            lead_consultant TEXT,
            target_date TEXT,
            notes TEXT,
            overall_maturity REAL DEFAULT 0.0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
        );
        """)

        # 5. Puntuaciones y Evidencias por Proceso
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER NOT NULL,
            process_id TEXT NOT NULL,
            domain TEXT NOT NULL,
            current_score REAL DEFAULT 0.0,
            target_score REAL DEFAULT 3.0,
            evidence TEXT,
            observations TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(assessment_id, process_id),
            FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
        );
        """)

        # 6. Hojas de Ruta (Roadmaps)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            total_budget REAL DEFAULT 0.0,
            horizon_months INTEGER DEFAULT 18,
            summary TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
        );
        """)

        # 7. Iniciativas de la Hoja de Ruta
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap_initiatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roadmap_id INTEGER NOT NULL,
            process_id TEXT,
            phase INTEGER DEFAULT 1, -- 1: Corto Plazo/Quick Wins, 2: Mediano Plazo, 3: Largo Plazo
            title TEXT NOT NULL,
            description TEXT,
            is_quick_win INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'Media', -- 'Alta', 'Media', 'Baja'
            estimated_months INTEGER DEFAULT 3,
            estimated_cost REAL DEFAULT 0.0,
            responsible_role TEXT,
            status TEXT DEFAULT 'pending', -- 'pending', 'in_progress', 'completed'
            FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
        );
        """)

        # 8. Documentos Ingestados y Análisis NPO
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT,
            file_size INTEGER,
            extracted_text TEXT,
            npo_analysis TEXT, -- JSON con necesidades, problemas y oportunidades
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
        );
        """)

        conn.commit()

    # Si la base de datos está recién creada, sembrar datos de inicio
    seed_initial_data()

def seed_initial_data():
    """Siembra usuarios y cliente de ejemplo si no existen."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Usuarios predeterminados
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            users = [
                ("admin", hash_password("admin123"), "Administrador del Sistema", "admin@cobitconsulting.com", "admin"),
                ("consultor", hash_password("cobit2019"), "Ing. Johan Londoño (Consultor Líder)", "jlondono@cobitconsulting.com", "consultant"),
                ("cliente", hash_password("cliente2019"), "Dra. Carolina Ríos (CIO)", "crios@financieradelcafe.com", "client")
            ]
            cursor.executemany("""
                INSERT INTO users (username, password_hash, full_name, email, role)
                VALUES (?, ?, ?, ?, ?)
            """, users)

        # Cliente piloto de ejemplo
        cursor.execute("SELECT COUNT(*) FROM clients")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO clients (name, tax_id, sector, size, city, phone, email, contact_name, notes, status)
                VALUES (
                    'Financiera del Café S.A.',
                    '900.548.123-4',
                    'Servicios Financieros y Banca',
                    'Mediana Empresa (51 - 250 colaboradores)',
                    'Armenia, Quindío',
                    '+57 (6) 745-9000',
                    'contacto@financieradelcafe.com',
                    'Carolina Ríos Gómez',
                    'Entidad financiera regional en proceso de modernización tecnológica e implementación de COBIT 2019.',
                    'Activo'
                )
            """)
            client_id = cursor.lastrowid

            # Contactos del cliente
            cursor.execute("""
                INSERT INTO client_contacts (client_id, name, email, phone, role_title, department, is_primary)
                VALUES 
                (?, 'Carolina Ríos Gómez', 'crios@financieradelcafe.com', '+57 310 445 8899', 'Directora de Tecnología (CIO)', 'Tecnología', 1),
                (?, 'Mauricio Castaño', 'mcastano@financieradelcafe.com', '+57 312 901 2345', 'Oficial de Seguridad (CISO)', 'Ciberseguridad', 0),
                (?, 'Andrés Villa', 'avilla@financieradelcafe.com', '+57 315 678 1234', 'Auditor Interno de TI', 'Auditoría', 0)
            """, (client_id, client_id, client_id))

            # Evaluación Inicial Piloto
            eval_code = f"EVAL-CAF-{datetime.now().strftime('%Y%m')}-01"
            cursor.execute("""
                INSERT INTO assessments (client_id, code, title, assessment_type, status, lead_consultant, target_date, notes, overall_maturity)
                VALUES (?, ?, 'Diagnóstico Integral COBIT 2019 - Vigencia 2026', 'comprehensive', 'in_progress', 'Ing. Johan Londoño', '2026-11-30', 'Evaluación de los 40 procesos para el plan estratégico de TI.', 2.15)
            """, (client_id, eval_code))
            assessment_id = cursor.lastrowid

            # Calificaciones de prueba realistas para los 40 procesos
            scores_seed = [
                # EDM
                (assessment_id, "EDM01", "EDM", 2.0, 3.0, "Comité de TI se reúne trimestralmente", "Falta formalizar la política marco"),
                (assessment_id, "EDM02", "EDM", 2.0, 3.0, "Cálculo de ROI informal en proyectos", "No hay seguimiento de beneficios post-proyecto"),
                (assessment_id, "EDM03", "EDM", 1.5, 3.5, "Matriz de riesgos desactualizada", "Alta exposición en canales digitales"),
                (assessment_id, "EDM04", "EDM", 2.5, 3.0, "Presupuesto anual asignado", "Recursos humanos de TI con sobrecarga"),
                (assessment_id, "EDM05", "EDM", 2.0, 3.0, "Informes a Junta Directiva mensuales", "Interesados operativos poco consultados"),
                # APO
                (assessment_id, "APO01", "APO", 2.0, 3.5, "Organigrama de TI establecido", "Falta actualizar descripciones de cargos"),
                (assessment_id, "APO02", "APO", 2.5, 4.0, "Plan Estratégico de TI (PETI) a 2 años", "Alineado parcialmente con metas comerciales"),
                (assessment_id, "APO03", "APO", 1.5, 3.0, "Sin repositorio formal de arquitectura", "Duplicidad de herramientas"),
                (assessment_id, "APO04", "APO", 1.0, 3.0, "Iniciativas aisladas de fintech", "No existe proceso formal de innovación"),
                (assessment_id, "APO05", "APO", 2.0, 3.5, "Lista de proyectos en Excel", "Priorización reactiva por urgencia"),
                (assessment_id, "APO06", "APO", 2.5, 3.5, "Control financiero mensual de TI", "Costos de nube sin etiquetado de centros de costo"),
                (assessment_id, "APO07", "APO", 2.0, 3.0, "Evaluación de desempeño anual", "Falta plan de retención de talento"),
                (assessment_id, "APO08", "APO", 2.5, 3.5, "Buena relación con áreas de negocio", "Reuniones de coordinación quincenales"),
                (assessment_id, "APO09", "APO", 1.5, 3.5, "SLAs no formalizados internamente", "Reclamos recurrentes por lentitud de soporte"),
                (assessment_id, "APO10", "APO", 2.0, 3.0, "Contratos revisados por el área jurídica", "Sin evaluación periódica de proveedores"),
                (assessment_id, "APO11", "APO", 1.5, 3.0, "Pruebas de software sin estándar", "Falta control de calidad de código"),
                (assessment_id, "APO12", "APO", 2.0, 4.0, "Riesgos de TI integrados al riesgo operativo", "Falta cuantificación de impacto financiero"),
                (assessment_id, "APO13", "APO", 2.0, 4.5, "Firewall y antivirus corporativo", "Falta implementar SOC y MFA obligatorio"),
                (assessment_id, "APO14", "APO", 1.5, 3.5, "Bases de datos relacionales tradicionales", "Sin catálogo maestro de datos ni linaje"),
                # BAI
                (assessment_id, "BAI01", "BAI", 2.0, 3.5, "Programas de modernización en marcha", "Dependencias entre proyectos poco gestionadas"),
                (assessment_id, "BAI02", "BAI", 2.5, 3.5, "Formatos de levantamiento de requisitos", "Cambios en alcance durante desarrollo"),
                (assessment_id, "BAI03", "BAI", 2.0, 3.5, "Desarrollo in-house con Git", "Falta pruebas de seguridad automáticas"),
                (assessment_id, "BAI04", "BAI", 2.5, 3.5, "Servidores con monitoreo de CPU/RAM", "Capacidad suficiente pero sin plan a 3 años"),
                (assessment_id, "BAI05", "BAI", 1.5, 3.0, "Resistencia al cambio en nuevas apps", "Falta plan de comunicación y capacitación"),
                (assessment_id, "BAI06", "BAI", 2.5, 4.0, "Procedimiento de paso a producción", "Comité de cambios (CAB) semanal"),
                (assessment_id, "BAI07", "BAI", 2.0, 3.5, "Ambiente de UAT disponible", "Pruebas de aceptación con demoras"),
                (assessment_id, "BAI08", "BAI", 1.5, 3.0, "Documentación técnica dispersa", "Dependencia de desarrolladores sénior"),
                (assessment_id, "BAI09", "BAI", 2.0, 3.5, "Inventario de equipos físicos", "Licenciamiento de software con brechas"),
                (assessment_id, "BAI10", "BAI", 1.5, 3.0, "No cuentan con CMDB centralizada", "Dificultad para rastrear configuraciones"),
                (assessment_id, "BAI11", "BAI", 2.5, 4.0, "Uso de tableros Kanban en proyectos", "Metodología ágil en adopción gradual"),
                # DSS
                (assessment_id, "DSS01", "DSS", 2.5, 3.5, "Procedimientos de operación documentados", "Respaldos diarios en cinta y nube"),
                (assessment_id, "DSS02", "DSS", 2.5, 4.0, "Mesa de ayuda con sistema de tickets", "Tiempos de resolución superan lo deseado"),
                (assessment_id, "DSS03", "DSS", 1.5, 3.5, "No se hace análisis sistemático de causa raíz", "Incidentes recurrentes de red"),
                (assessment_id, "DSS04", "DSS", 2.0, 4.5, "Plan DRP documentado en 2024", "No se han ejecutado pruebas de simulación reales"),
                (assessment_id, "DSS05", "DSS", 2.0, 4.5, "Controles perimetrales de seguridad", "Falta implementar segmentación Zero Trust"),
                (assessment_id, "DSS06", "DSS", 2.0, 3.5, "Validaciones básicas en formularios de negocio", "Faltan bitácoras de auditoría de transacciones"),
                # MEA
                (assessment_id, "MEA01", "MEA", 2.0, 3.5, "Indicadores operativos de disponibilidad", "Falta tablero de mando integral para la gerencia"),
                (assessment_id, "MEA02", "MEA", 2.0, 3.5, "Controles revisados anualmente por auditoría", "Monitoreo continuo no automatizado"),
                (assessment_id, "MEA03", "MEA", 2.5, 4.0, "Cumplimiento normativo de Superintendencia", "Reportes regulatorios al día"),
                (assessment_id, "MEA04", "MEA", 2.0, 3.5, "Auditorías externas periódicas", "Cierre lento de hallazgos observaciones")
            ]

            cursor.executemany("""
                INSERT INTO assessment_scores (assessment_id, process_id, domain, current_score, target_score, evidence, observations)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, scores_seed)

            # Hoja de Ruta Piloto
            cursor.execute("""
                INSERT INTO roadmaps (assessment_id, client_id, title, total_budget, horizon_months, summary)
                VALUES (?, ?, 'Hoja de Ruta Estratégica COBIT 2019 (2026-2027)', 145000000, 18, 'Plan de transformación hacia un nivel de madurez 3.5 en ciberseguridad, gobernanza y servicios.')
            """, (assessment_id, client_id))
            roadmap_id = cursor.lastrowid

            # Iniciativas del Roadmap
            cursor.execute("""
                INSERT INTO roadmap_initiatives (roadmap_id, process_id, phase, title, description, is_quick_win, priority, estimated_months, estimated_cost, responsible_role, status)
                VALUES
                (?, 'DSS05', 1, 'Implementación de MFA Obligatorio y Protección Endpoint', 'Desplegar autenticación de múltiples factores en correos y VPN corporativa.', 1, 'Alta', 2, 12000000, 'Oficial de Seguridad (CISO)', 'in_progress'),
                (?, 'APO09', 1, 'Formalización de SLAs Internos y Catálogo de Servicios', 'Establecer acuerdos de nivel de servicio claros con las áreas operativas.', 1, 'Alta', 2, 8000000, 'Líder de Soporte / Service Desk', 'pending'),
                (?, 'DSS04', 1, 'Simulacro y Actualización del Plan DRP/BCP', 'Actualizar protocolos de continuidad operativa y realizar prueba de restauración.', 1, 'Alta', 3, 15000000, 'Gerente de Infraestructura', 'pending'),
                (?, 'EDM01', 2, 'Formalización del Comité Directivo de Gobernanza de TI', 'Crear el estatuto del comité con participación del Presidente y Gerencias.', 0, 'Alta', 4, 18000000, 'CIO y Asesoría Legal', 'pending'),
                (?, 'APO13', 2, 'Adopción del SGSI conforme a ISO 27001 / COBIT APO13', 'Estandarizar políticas de seguridad, gestión de incidentes y cifrado.', 0, 'Alta', 6, 45000000, 'CISO y Consultor Externo', 'pending'),
                (?, 'BAI06', 2, 'Automatización del Flujo de Gestión de Cambios (CAB)', 'Digitalizar la aprobación y registro de cambios en producción.', 0, 'Media', 4, 15000000, 'Líder DevOps / Infraestructura', 'pending'),
                (?, 'APO14', 3, 'Gobierno de Datos y Data Warehouse Institucional', 'Centralizar la información para analítica avanzada y business intelligence.', 0, 'Media', 8, 32000000, 'Arquitecto de Datos', 'pending')
            """, (roadmap_id, roadmap_id, roadmap_id, roadmap_id, roadmap_id, roadmap_id, roadmap_id))

        conn.commit()

# =====================================================================
# FUNCIONES CRUD: AUTENTICACIÓN Y USUARIOS
# =====================================================================

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Valida credenciales y retorna los datos del usuario."""
    pwd_hash = hash_password(password)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, full_name, email, role, is_active
            FROM users
            WHERE username = ? AND password_hash = ? AND is_active = 1
        """, (username, pwd_hash))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def create_user(username: str, password: str, full_name: str, email: str, role: str = 'consultant') -> int:
    """Crea un nuevo usuario."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, email, role)
            VALUES (?, ?, ?, ?, ?)
        """, (username, hash_password(password), full_name, email, role))
        conn.commit()
        return cursor.lastrowid

# =====================================================================
# FUNCIONES CRUD: CLIENTES Y CONTACTOS
# =====================================================================

def get_all_clients() -> List[Dict[str, Any]]:
    """Obtiene todas las empresas clientes ordenadas por nombre."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, tax_id, sector, size, city, phone, email, contact_name, status, created_at
            FROM clients
            ORDER BY name ASC
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_client_by_id(client_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene los detalles de un cliente específico."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def create_client(data: Dict[str, Any]) -> int:
    """Inserta una nueva empresa cliente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clients (name, tax_id, sector, size, city, phone, email, contact_name, notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("name"),
            data.get("tax_id"),
            data.get("sector"),
            data.get("size"),
            data.get("city"),
            data.get("phone"),
            data.get("email"),
            data.get("contact_name"),
            data.get("notes", ""),
            data.get("status", "Activo")
        ))
        conn.commit()
        return cursor.lastrowid

def update_client(client_id: int, data: Dict[str, Any]) -> bool:
    """Actualiza los datos de un cliente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clients
            SET name = ?, tax_id = ?, sector = ?, size = ?, city = ?,
                phone = ?, email = ?, contact_name = ?, notes = ?, status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            data.get("name"),
            data.get("tax_id"),
            data.get("sector"),
            data.get("size"),
            data.get("city"),
            data.get("phone"),
            data.get("email"),
            data.get("contact_name"),
            data.get("notes", ""),
            data.get("status", "Activo"),
            client_id
        ))
        conn.commit()
        return cursor.rowcount > 0

def delete_client(client_id: int) -> bool:
    """Elimina un cliente y sus registros asociados."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_contacts_by_client(client_id: int) -> List[Dict[str, Any]]:
    """Retorna los contactos asociados a un cliente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM client_contacts WHERE client_id = ? ORDER BY is_primary DESC, name ASC
        """, (client_id,))
        return [dict(row) for row in cursor.fetchall()]

def create_contact(client_id: int, data: Dict[str, Any]) -> int:
    """Registra un nuevo contacto para un cliente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO client_contacts (client_id, name, email, phone, role_title, department, is_primary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            client_id,
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("role_title"),
            data.get("department"),
            1 if data.get("is_primary") else 0
        ))
        conn.commit()
        return cursor.lastrowid

def delete_contact(contact_id: int) -> bool:
    """Elimina un contacto."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM client_contacts WHERE id = ?", (contact_id,))
        conn.commit()
        return cursor.rowcount > 0

# =====================================================================
# FUNCIONES CRUD: EVALUACIONES Y CALIFICACIONES
# =====================================================================

def get_assessments_by_client(client_id: int) -> List[Dict[str, Any]]:
    """Retorna todas las evaluaciones de un cliente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM assessments WHERE client_id = ? ORDER BY created_at DESC
        """, (client_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_assessment_by_id(assessment_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene una evaluación por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def create_assessment(client_id: int, title: str, assessment_type: str, lead_consultant: str, target_date: str = "", notes: str = "") -> int:
    """Crea una nueva evaluación e inicializa los registros de puntuación para los procesos."""
    from engine.cobit_data import get_all_processes_list, QUICK_ASSESSMENT_PROCESSES

    code = f"EVAL-{client_id:03d}-{datetime.now().strftime('%Y%m%d%H%M')}"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO assessments (client_id, code, title, assessment_type, status, lead_consultant, target_date, notes)
            VALUES (?, ?, ?, ?, 'in_progress', ?, ?, ?)
        """, (client_id, code, title, assessment_type, lead_consultant, target_date, notes))
        assessment_id = cursor.lastrowid

        # Determinar procesos a evaluar
        all_procs = get_all_processes_list()
        if assessment_type == 'quick':
            procs_to_add = [p for p in all_procs if p["id"] in QUICK_ASSESSMENT_PROCESSES]
        else:
            procs_to_add = all_procs

        # Sembrar registros de score inicial en 0 o valor base
        score_rows = [
            (assessment_id, p["id"], p["domain"], 1.0, 3.0, "", "")
            for p in procs_to_add
        ]
        cursor.executemany("""
            INSERT INTO assessment_scores (assessment_id, process_id, domain, current_score, target_score, evidence, observations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, score_rows)

        conn.commit()
        return assessment_id

def get_assessment_scores(assessment_id: int) -> List[Dict[str, Any]]:
    """Retorna las puntuaciones registradas para una evaluación."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM assessment_scores WHERE assessment_id = ? ORDER BY process_id ASC
        """, (assessment_id,))
        return [dict(row) for row in cursor.fetchall()]

def update_assessment_score(assessment_id: int, process_id: str, current_score: float, target_score: float, evidence: str = "", observations: str = ""):
    """Actualiza la calificación y evidencia de un proceso específico."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE assessment_scores
            SET current_score = ?, target_score = ?, evidence = ?, observations = ?, updated_at = CURRENT_TIMESTAMP
            WHERE assessment_id = ? AND process_id = ?
        """, (current_score, target_score, evidence, observations, assessment_id, process_id))
        conn.commit()

def save_all_assessment_scores(assessment_id: int, scores_data: List[Dict[str, Any]], overall_maturity: float = 0.0):
    """Guarda en lote los puntajes y actualiza el IMO global de la evaluación."""
    with get_connection() as conn:
        cursor = conn.cursor()
        for item in scores_data:
            cursor.execute("""
                UPDATE assessment_scores
                SET current_score = ?, target_score = ?, evidence = ?, observations = ?, updated_at = CURRENT_TIMESTAMP
                WHERE assessment_id = ? AND process_id = ?
            """, (
                item.get("current_score", 0.0),
                item.get("target_score", 3.0),
                item.get("evidence", ""),
                item.get("observations", ""),
                assessment_id,
                item.get("process_id")
            ))
        cursor.execute("""
            UPDATE assessments
            SET overall_maturity = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (overall_maturity, assessment_id))
        conn.commit()

# =====================================================================
# FUNCIONES CRUD: HOJA DE RUTA (ROADMAP)
# =====================================================================

def get_roadmap_by_assessment(assessment_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene la hoja de ruta asociada a una evaluación."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM roadmaps WHERE assessment_id = ? ORDER BY id DESC LIMIT 1", (assessment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_roadmap_initiatives(roadmap_id: int) -> List[Dict[str, Any]]:
    """Retorna las iniciativas ordenadas por fase y prioridad."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM roadmap_initiatives 
            WHERE roadmap_id = ? 
            ORDER BY phase ASC, is_quick_win DESC, priority ASC
        """, (roadmap_id,))
        return [dict(row) for row in cursor.fetchall()]

def save_roadmap(assessment_id: int, client_id: int, title: str, total_budget: float, horizon_months: int, summary: str, initiatives: List[Dict[str, Any]]) -> int:
    """Crea o reemplaza la hoja de ruta e inserta sus iniciativas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Verificar si ya existe
        cursor.execute("SELECT id FROM roadmaps WHERE assessment_id = ?", (assessment_id,))
        existing = cursor.fetchone()
        if existing:
            roadmap_id = existing[0]
            cursor.execute("""
                UPDATE roadmaps 
                SET title = ?, total_budget = ?, horizon_months = ?, summary = ?
                WHERE id = ?
            """, (title, total_budget, horizon_months, summary, roadmap_id))
            cursor.execute("DELETE FROM roadmap_initiatives WHERE roadmap_id = ?", (roadmap_id,))
        else:
            cursor.execute("""
                INSERT INTO roadmaps (assessment_id, client_id, title, total_budget, horizon_months, summary)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (assessment_id, client_id, title, total_budget, horizon_months, summary))
            roadmap_id = cursor.lastrowid

        for init in initiatives:
            cursor.execute("""
                INSERT INTO roadmap_initiatives (
                    roadmap_id, process_id, phase, title, description,
                    is_quick_win, priority, estimated_months, estimated_cost,
                    responsible_role, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                roadmap_id,
                init.get("process_id"),
                init.get("phase", 1),
                init.get("title", ""),
                init.get("description", ""),
                1 if init.get("is_quick_win") else 0,
                init.get("priority", "Media"),
                init.get("estimated_months", 3),
                init.get("estimated_cost", 0.0),
                init.get("responsible_role", "Líder de TI"),
                init.get("status", "pending")
            ))

        conn.commit()
        return roadmap_id

# =====================================================================
# FUNCIONES CRUD: DOCUMENTOS E INGESTA
# =====================================================================

def save_document(client_id: int, filename: str, file_type: str, file_size: int, extracted_text: str, npo_analysis: Dict[str, Any]) -> int:
    """Guarda un documento y su análisis NPO."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO documents (client_id, filename, file_type, file_size, extracted_text, npo_analysis)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            client_id,
            filename,
            file_type,
            file_size,
            extracted_text,
            json.dumps(npo_analysis, ensure_ascii=False)
        ))
        conn.commit()
        return cursor.lastrowid

def get_documents_by_client(client_id: int) -> List[Dict[str, Any]]:
    """Retorna los documentos cargados para un cliente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, filename, file_type, file_size, npo_analysis, created_at
            FROM documents
            WHERE client_id = ?
            ORDER BY created_at DESC
        """, (client_id,))
        results = []
        for row in cursor.fetchall():
            item = dict(row)
            if item.get("npo_analysis"):
                try:
                    item["npo_analysis"] = json.loads(item["npo_analysis"])
                except Exception:
                    pass
            results.append(item)
        return results

def get_document_by_id(doc_id: int) -> Optional[Dict[str, Any]]:
    """Retorna el documento con su texto completo extraído."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        if row:
            item = dict(row)
            if item.get("npo_analysis"):
                try:
                    item["npo_analysis"] = json.loads(item["npo_analysis"])
                except Exception:
                    pass
            return item
        return None
