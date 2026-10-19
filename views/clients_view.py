"""
Gestión Integral de Empresas Clientes y Contactos [COB-ST04, COB-ST05].
Permite crear, listar, editar empresas y administrar su directorio de interesados.
"""

import streamlit as st
import pandas as pd
from database.db_manager import (
    get_all_clients, get_client_by_id, create_client, update_client, delete_client,
    get_contacts_by_client, create_contact, delete_contact
)
from engine.cobit_data import SECTORS, COMPANY_SIZES

def show_clients():
    st.title("🏢 Gestión de Clientes y Organizaciones")
    st.markdown("Administra las entidades sobre las cuales se realiza la consultoría y evaluación COBIT 2019.")

    tab_list, tab_new, tab_contacts = st.tabs(["📋 Lista de Clientes", "➕ Registrar Nuevo Cliente", "👥 Directorio de Contactos"])

    # TAB 1: LISTADO Y FILTRO DE CLIENTES
    with tab_list:
        clients = get_all_clients()
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            search_query = st.text_input("🔍 Buscar por Nombre, NIT o Ciudad:", placeholder="Ej. Financiera, 900...")
        with col_s2:
            sector_filter = st.selectbox("Filtrar por Sector:", ["Todos"] + SECTORS)

        # Filtrar clientes
        filtered = clients
        if search_query:
            q = search_query.lower()
            filtered = [c for c in filtered if q in c["name"].lower() or (c["tax_id"] and q in c["tax_id"].lower()) or (c["city"] and q in c["city"].lower())]
        if sector_filter != "Todos":
            filtered = [c for c in filtered if c["sector"] == sector_filter]

        st.caption(f"Mostrando {len(filtered)} empresas registradas.")

        if not filtered:
            st.info("No se encontraron empresas con los criterios de búsqueda.")
        else:
            for client in filtered:
                is_active = (st.session_state.get("active_client_id") == client["id"])
                border_color = "#1E3A8A" if is_active else "#E2E8F0"
                badge_active = "⭐ ACTIVO EN SESIÓN" if is_active else ""

                with st.expander(f"🏢 {client['name']} — {client['sector']} {badge_active}", expanded=is_active):
                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        st.markdown(f"**NIT / Identificación:** {client['tax_id'] or 'No especificado'}")
                        st.markdown(f"**Tamaño:** {client['size']}")
                        st.markdown(f"**Ciudad / Sede:** {client['city'] or 'No registrada'}")
                    with c2:
                        st.markdown(f"**Contacto Principal:** {client['contact_name'] or 'Sin asignar'}")
                        st.markdown(f"**Correo Electrónico:** {client['email'] or 'N/A'}")
                        st.markdown(f"**Teléfono:** {client['phone'] or 'N/A'}")
                    with c3:
                        if not is_active:
                            if st.button("Seleccionar", key=f"sel_{client['id']}", use_container_width=True):
                                st.session_state["active_client_id"] = client["id"]
                                st.success(f"Cliente '{client['name']}' establecido como activo.")
                                st.rerun()
                        else:
                            st.success("✅ Activo")

                    if client.get("notes"):
                        st.info(f"**Notas:** {client['notes']}")

                    # Botón para editar
                    col_btn1, col_btn2 = st.columns([1, 1])
                    with col_btn1:
                        if st.button("✏️ Editar Datos", key=f"edit_btn_{client['id']}"):
                            st.session_state[f"editing_client_{client['id']}"] = True

                    with col_btn2:
                        if st.button("🗑️ Eliminar Cliente", key=f"del_btn_{client['id']}"):
                            delete_client(client["id"])
                            st.warning(f"Empresa '{client['name']}' eliminada.")
                            st.rerun()

                    # Formulario de Edición condicional
                    if st.session_state.get(f"editing_client_{client['id']}"):
                        st.markdown("#### Editar Información Corporativa")
                        with st.form(f"form_edit_{client['id']}"):
                            e_name = st.text_input("Razón Social:", value=client["name"])
                            e_tax = st.text_input("NIT / RUT:", value=client.get("tax_id", "") or "")
                            e_sec = st.selectbox("Sector:", SECTORS, index=SECTORS.index(client["sector"]) if client["sector"] in SECTORS else 0)
                            e_size = st.selectbox("Tamaño:", COMPANY_SIZES, index=COMPANY_SIZES.index(client["size"]) if client["size"] in COMPANY_SIZES else 0)
                            e_city = st.text_input("Ciudad:", value=client.get("city", "") or "")
                            e_phone = st.text_input("Teléfono:", value=client.get("phone", "") or "")
                            e_email = st.text_input("Correo Electrónico:", value=client.get("email", "") or "")
                            e_contact = st.text_input("Contacto Principal:", value=client.get("contact_name", "") or "")
                            e_notes = st.text_area("Observaciones:", value=client.get("notes", "") or "")

                            if st.form_submit_button("Guardar Cambios"):
                                update_client(client["id"], {
                                    "name": e_name, "tax_id": e_tax, "sector": e_sec, "size": e_size,
                                    "city": e_city, "phone": e_phone, "email": e_email,
                                    "contact_name": e_contact, "notes": e_notes, "status": client.get("status", "Activo")
                                })
                                st.session_state[f"editing_client_{client['id']}"] = False
                                st.success("Cliente actualizado exitosamente.")
                                st.rerun()

    # TAB 2: REGISTRO DE NUEVO CLIENTE
    with tab_new:
        st.subheader("Registrar Nueva Organización Cliente")
        with st.form("new_client_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                name = st.text_input("Razón Social de la Empresa *", placeholder="Ej. Soluciones Logísticas del Eje S.A.S.")
                tax_id = st.text_input("NIT / Identificación Fiscal *", placeholder="Ej. 901.234.567-8")
                sector = st.selectbox("Sector Económico *", SECTORS)
                size = st.selectbox("Tamaño de Organización *", COMPANY_SIZES)
            with col_f2:
                city = st.text_input("Ciudad y Sede Principal", placeholder="Ej. Pereira, Risaralda")
                phone = st.text_input("Teléfono Corporativo", placeholder="Ej. +57 (6) 333-0000")
                email = st.text_input("Correo Electrónico Institucional", placeholder="Ej. gerencia@empresa.com")
                contact_name = st.text_input("Nombre del Contacto Directivo", placeholder="Ej. Ing. Carlos Mendoza (Gerente TI)")

            notes = st.text_area("Contexto Inicial y Objetivos de la Consultoría", placeholder="Describa brevemente la situación actual, dolores o motivos de la evaluación COBIT...")

            submitted = st.form_submit_button("💾 Guardar y Crear Cliente")
            if submitted:
                if not name.strip() or not tax_id.strip():
                    st.error("Por favor completa los campos obligatorios (Razón Social y NIT).")
                else:
                    new_id = create_client({
                        "name": name.strip(),
                        "tax_id": tax_id.strip(),
                        "sector": sector,
                        "size": size,
                        "city": city.strip(),
                        "phone": phone.strip(),
                        "email": email.strip(),
                        "contact_name": contact_name.strip(),
                        "notes": notes.strip(),
                        "status": "Activo"
                    })
                    st.session_state["active_client_id"] = new_id
                    st.success(f"¡Empresa '{name}' registrada con éxito y establecida como activa!")
                    st.rerun()

    # TAB 3: CONTACTOS CLAVE
    with tab_contacts:
        st.subheader("👥 Directorio de Interesados y Contactos Clave")
        clients = get_all_clients()
        if not clients:
            st.info("Primero registra un cliente para asociarle contactos.")
            return

        c_names = {c["id"]: c["name"] for c in clients}
        active_c_id = st.session_state.get("active_client_id", clients[0]["id"])
        selected_client_for_contact = st.selectbox(
            "Selecciona la Empresa para ver/agregar contactos:",
            options=list(c_names.keys()),
            format_func=lambda cid: c_names[cid],
            index=list(c_names.keys()).index(active_c_id) if active_c_id in c_names else 0
        )

        contacts = get_contacts_by_client(selected_client_for_contact)
        if contacts:
            st.markdown(f"**Contactos registrados ({len(contacts)}):**")
            for ct in contacts:
                with st.container():
                    c_col1, c_col2, c_col3 = st.columns([3, 3, 1])
                    with c_col1:
                        st.markdown(f"👤 **{ct['name']}** {'*(Contacto Principal)*' if ct['is_primary'] else ''}")
                        st.caption(f"{ct.get('role_title', 'Cargo no definido')} — {ct.get('department', 'Área TI')}")
                    with c_col2:
                        st.markdown(f"📧 {ct.get('email', 'N/A')}")
                        st.caption(f"📞 {ct.get('phone', 'N/A')}")
                    with c_col3:
                        if st.button("Eliminar", key=f"del_ct_{ct['id']}"):
                            delete_contact(ct["id"])
                            st.rerun()
                    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
        else:
            st.info("No hay contactos adicionales para este cliente.")

        # Formulario para agregar contacto
        st.markdown("#### ➕ Agregar Persona de Contacto")
        with st.form("new_contact_form"):
            c_name = st.text_input("Nombre y Apellidos *", placeholder="Ej. Lic. Fernando Rojas")
            col_ct1, col_ct2 = st.columns(2)
            with col_ct1:
                c_role = st.text_input("Cargo", placeholder="Ej. Oficial de Seguridad (CISO) o Gerente TI")
                c_email = st.text_input("Correo Electrónico", placeholder="Ej. frojas@empresa.com")
            with col_ct2:
                c_dept = st.text_input("Área o Departamento", placeholder="Ej. Seguridad de la Información")
                c_phone = st.text_input("Teléfono / Móvil", placeholder="Ej. +57 311 000 0000")
            c_primary = st.checkbox("Marcar como Contacto Principal")

            if st.form_submit_button("Guardar Contacto"):
                if not c_name.strip():
                    st.error("El nombre del contacto es obligatorio.")
                else:
                    create_contact(selected_client_for_contact, {
                        "name": c_name.strip(),
                        "role_title": c_role.strip(),
                        "email": c_email.strip(),
                        "department": c_dept.strip(),
                        "phone": c_phone.strip(),
                        "is_primary": c_primary
                    })
                    st.success(f"Contacto '{c_name}' agregado correctamente.")
                    st.rerun()
