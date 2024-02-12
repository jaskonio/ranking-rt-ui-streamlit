import streamlit as st
import pandas as pd
from io import StringIO
from services.person_services import PersonServices
from services.notification_service import NotificationServices
from services.request_services import RequestServices

person_services = PersonServices(RequestServices(), NotificationServices())

st.title("Administracion de Participantes")

left_column, right_column = st.columns(2, gap="medium")

with left_column:
    st.subheader('Añadir nuevo Participante', divider=True)
    with st.form("form_person"):
        name = st.text_input('Nombre', placeholder='Nombre')
        last_name = st.text_input('Apellido', placeholder='Apellido')
        gender = st.multiselect('Genero', ['M','F'], placeholder="Genero", max_selections=1)
        image = st.file_uploader('Foto', type=['png', 'jpg'], accept_multiple_files=False)
        submitted = st.form_submit_button("Añadir")

        if submitted:
            if name != '' and last_name != '' and gender != []:
                person_services.add_person([{
                    "first_name": name,
                    "last_name": last_name,
                    "gender": gender[0],
                    # "photo": StringIO(image.getvalue().decode("utf-8")),
                }])

def df_on_change():
    state = st.session_state["df_editor_person"]
    for index, updates in state["edited_rows"].items():
        old_person = personsDf.iloc[index].to_dict()

        for key in updates.keys():
            old_person[key] = updates[key]

        person_services.update_person({
            "id": old_person["id"],
            "first_name": old_person["first_name"],
            "last_name": old_person["last_name"],
            "nationality": old_person["nationality"],
            "gender": old_person["gender"],
        })

with right_column:
    st.subheader('Lista de Particpantes', divider=True)

    personsDf = pd.DataFrame(person_services.get_all())

    edited_df = st.data_editor(personsDf,
        key="df_editor_person",
        column_order=["first_name", "last_name", "nationality", "gender", "photo_url"],
        column_config={
            "photo_url": st.column_config.ImageColumn(
                "Preview Image", help="Streamlit app preview screenshots",
            )
        },
        on_change=df_on_change,
        width=900,
        height=450)
