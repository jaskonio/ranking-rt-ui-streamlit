from json import loads
import streamlit as st
import pandas as pd
from services.league_services import LeagueServices
from services.notification_service import NotificationServices
from services.request_services import RequestServices
from services.person_services import PersonServices
from services.races_services import RacesServices
from services.runner_csv_loader import RunnerCSV_Loader
from services.csv_reader import CSV_reader

league_services = LeagueServices(RequestServices(), NotificationServices())
participantes_services = PersonServices(RequestServices(), NotificationServices())
races_services = RacesServices(RequestServices(), NotificationServices())
runner_csv_loader = RunnerCSV_Loader(races_services, participantes_services, league_services, NotificationServices())

data_league = league_services.get_all()
data_all_participantes = participantes_services.get_all()
data_all_races = races_services.get_all()

st.title("Administracion de Ligas")

left_column, right_column = st.columns(2, gap="medium")

with left_column:
    st.subheader('Añadir nueva Liga', divider=True)

    with st.form("form_league"):
        league_name = st.text_input('Nombre Liga', placeholder='Nombre Liga')
        submitted = st.form_submit_button("Añadir")
        if submitted:
            if league_name != '':
                league_services.add([{"name": league_name}])

with right_column:
    st.subheader('Eliminar Liga', divider=True)
    with st.form("form_delete_race"):
        league_obj = st.selectbox('Nombre de la Liga', data_league, placeholder='Nombre de la Liga', format_func=lambda x: str(x['name'] ))
        submitted = st.form_submit_button("Delete")

        if submitted:
            if league_obj is not None:
                league_services.delete(league_obj['id'])

st.subheader('Lista de Ligas', divider=True)

st.dataframe(data_league,
    column_order=["name"],
    width=900,
    height=450)

st.subheader('Editar Liga', divider=True)

league_options = [item['name'] for item in data_league]

league_option = st.selectbox("Selecciona una Liga", league_options)
current_league = list(filter(lambda item: league_option == item["name"], data_league))[0]

participant_column, races_column = st.columns(2, gap="medium")

with participant_column:
    current_participants_league = [item['id'] for item in current_league['participants']]
    participant_not_in_current_league = list(filter(lambda item: item["id"] not in current_participants_league, data_all_participantes))
    news_participants = st.multiselect('Añadir nuevos participantes', participant_not_in_current_league, format_func=lambda x: str(x['first_name'] + " " + x["last_name"]), placeholder='Selecciona nuevos participantes')

    for news_participant in news_participants:
        current_league["participants"].append(news_participant)

    league_name = st.text_input('Nombre Liga', value=current_league["name"], placeholder='Nombre Liga')

    participants = pd.DataFrame(current_league["participants"])

    participants_edited_df = st.data_editor(participants,
        column_order=["first_name", "last_name", "dorsal"],
        width=900,
        height=450)

with races_column:
    current_races_league = [item['id'] for item in current_league['races']]
    races_not_in_current_league = list(filter(lambda item: item["id"] not in current_races_league, data_all_races))
    new_races = st.multiselect('Añadir nuevas carreras', races_not_in_current_league, format_func=lambda x: str(x['name'] ), placeholder='Selecciona nuevas carreras')

    for new_race in new_races:
        order_value = 0
        if len(current_league["races"]) != 0:
            order_value = current_league["races"][-1]['order']
        new_race["order"] = order_value
        current_league["races"].append(new_race)

    races_df = pd.DataFrame(current_league["races"])

    races_edited_df = st.data_editor(races_df,
        column_order=["name", "processed", "is_sorted", "order"],
        disabled=["raw_ranking", "ranking", "participants"])

submitted = st.button("Actualizar")
if submitted:
    if league_name != '':
        current_league["participants"] = loads(participants_edited_df.to_json(orient="records"))
        current_league["races"] = loads(races_edited_df.to_json(orient="records"))
        league_services.update(current_league)

with st.form("form_person_csv"):
    st.subheader('Subir Fichero csv', divider=True)
    uploaded_file = st.file_uploader("Selecciona un fichero", type=["csv"], accept_multiple_files=False)
    exclude_header = st.checkbox("Excluir encabezado", value=True)


    st.text("Ejemplo del contenido:")
    st.code("""DORSAL;Nombre;Apellidos;LIGA\n
    2008;NOMBRE_1;Apellido_1;eliTEAM\n
    2015;NOMBRE_2;Apellido_2;Otro Nombre de Liga\n""", language='csv')

    submitted = st.form_submit_button("Subir fichero")
    if submitted and uploaded_file is not None:
        bytes_data = uploaded_file.read()

        stringio = uploaded_file.getvalue().decode("utf-8").splitlines()
        rows = CSV_reader.convertCsvToPersonFile(data=stringio, exclude_header=exclude_header)
        runner_csv_loader.upload_file(rows)
