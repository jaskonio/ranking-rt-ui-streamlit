import streamlit as st
from services.all_services import race_info_service

all_races = race_info_service.get_all()

st.title("Administracion de Carreras")

left_column, right_column = st.columns(2, gap="medium")

with left_column:
    st.subheader('Añadir nueva carrera', divider=True)
    with st.form("form_race"):
        race_name = st.text_input('Nombre de la carrera', placeholder='Nombre de carrrera')
        url = st.text_input('Url', placeholder='http://')
        platform_inscriptions = st.selectbox('Plataforma', ["SPORTMANIACS_LATEST"])
        submitted = st.form_submit_button("Añadir")

        if submitted:
            if race_name != '' and url != '':
                race_info_service.add({
                    "name": race_name,
                    "url": url,
                    "platform": platform_inscriptions
                })

with right_column:
    st.subheader('Lista de carreras', divider=True)

    edited_df = st.dataframe(all_races,
        column_order=["name", "url", "processed", "platform", "processed"])


st.subheader("Acciones")

process_column, delete_column = st.columns(2, gap="medium")

with process_column:
    st.subheader('Processar carrera', divider=True)
    with st.form("form_process_race"):
        race_obj = st.selectbox('Nombre de la carrera', all_races, placeholder='Nombre de carrrera', format_func=lambda x: str(x['name'] ))
        submitted = st.form_submit_button("Processar")

        if submitted:
            if race_obj is not None:
                race_info_service.process_by_id(race_obj["id"])

with delete_column:
    st.subheader('Eliminar una carrera', divider=True)
    with st.form("form_delete_race"):
        race_obj = st.selectbox('Nombre de la carrera', all_races, placeholder='Nombre de carrrera', format_func=lambda x: str(x['name'] ))
        submitted = st.form_submit_button("Delete")

        if submitted:
            if race_obj is not None:
                race_info_service.delete(race_obj["id"])
