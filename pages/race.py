import streamlit as st
from services.notification_service import NotificationServices
from services.request_services import RequestServices
from services.races_services import RacesServices

races_services = RacesServices(RequestServices(), NotificationServices())

all_races = races_services.get_all()

st.title("Administracion de Carreras")

left_column, right_column = st.columns(2, gap="medium")

with left_column:
    st.subheader('Añadir nueva carrera', divider=True)
    with st.form("form_race"):
        race_name = st.text_input('Nombre de la carrera', placeholder='Nombre de carrrera')
        url = st.text_input('Url', placeholder='http://')
        platform_inscriptions = st.selectbox('Plataforma', [1,2,3])
        submitted = st.form_submit_button("Añadir")

        if submitted:
            if race_name != '' and url != '':
                races_services.add({
                    "name": race_name,
                    "url": url,
                    "platform_inscriptions": int(platform_inscriptions),
                })

with right_column:
    st.subheader('Lista de carreras', divider=True)

    edited_df = st.dataframe(all_races,
        column_order=["name", "url", "processed", "platform_inscriptions"])


st.subheader("Acciones")

process_column, delete_column = st.columns(2, gap="medium")

with process_column:
    st.subheader('Processar carrera', divider=True)
    with st.form("form_process_race"):
        race_obj = st.selectbox('Nombre de la carrera', all_races, placeholder='Nombre de carrrera', format_func=lambda x: str(x['name'] ))
        submitted = st.form_submit_button("Processar")

        if submitted:
            if race_obj is not None:
                races_services.process(race_obj["id"])

with delete_column:
    st.subheader('Eliminar una carrera', divider=True)
    with st.form("form_delete_race"):
        race_obj = st.selectbox('Nombre de la carrera', all_races, placeholder='Nombre de carrrera', format_func=lambda x: str(x['name'] ))
        submitted = st.form_submit_button("Delete")

        if submitted:
            if race_obj is not None:
                races_services.delete(race_obj["id"])
