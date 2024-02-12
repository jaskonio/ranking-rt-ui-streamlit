from json import loads
import streamlit as st
import pandas as pd
from services.league_services import LeagueServices
from services.notification_service import NotificationServices
from services.request_services import RequestServices
from services.person_services import PersonServices
from services.races_services import RacesServices

league_services = LeagueServices(RequestServices(), NotificationServices())
participantes_services = PersonServices(RequestServices(), NotificationServices())
races_services = RacesServices(RequestServices(), NotificationServices())

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

def df_on_change():
    state = st.session_state["df_editor_league"]
    for index, updates in state["edited_rows"].items():
        old_person = leagues_df.iloc[index].to_dict()

        for key in updates.keys():
            old_person[key] = updates[key]

        league_services.update({
            "id": old_person["id"],
            "name": old_person["name"],
            "races": old_person["races"],
            "ranking": old_person["ranking"],
            "participants": old_person["participants"],
        })

with right_column:
    st.subheader('Lista de Ligas', divider=True)

    leagues_df = pd.DataFrame(data_league)

    edited_df = st.data_editor(leagues_df,
        key="df_editor_league",
        column_order=["name"],
        on_change=df_on_change,
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

    races = pd.DataFrame(current_league["races"])
    ranking = pd.DataFrame(current_league["ranking"])
    participants = pd.DataFrame(current_league["participants"])

    edited_df = st.data_editor(participants,
        key="df_editor_participants",
        column_order=["first_name", "last_name", "dorsal"],
        width=900,
        height=450)

with races_column:
    current_races_league = [item['id'] for item in current_league['races']]
    races_not_in_current_league = list(filter(lambda item: item["id"] not in current_races_league, data_all_races))
    news_participants = st.multiselect('Añadir nuevas carreras', races_not_in_current_league, format_func=lambda x: str(x['name'] ), placeholder='Selecciona nuevas carreras')

submitted = st.button("Actualizar")
if submitted:
    if league_name != '':
        current_league["participants"] = loads(edited_df.to_json(orient="records"))
        st.write(current_league["participants"])
        # league_services.add([{"name": league_name}])
