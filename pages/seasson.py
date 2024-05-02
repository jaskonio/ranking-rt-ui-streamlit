import streamlit as st
st.title("Administracion de Temporadas")

left_column, right_column = st.columns(2, gap="medium")


with left_column:
    st.subheader('Añadir nueva temporada', divider=True)

    with st.form("form_add_seasson"):
        league_name = st.text_input('Nombre de la Temporada', placeholder='Nombre de la temporada')
        submitted = st.form_submit_button("Añadir")
        if submitted:
            if league_name != '':
                print("Servicio para añadir temporada")

with right_column:
    st.subheader('Eliminar Temporada', divider=True)
    with st.form("form_delete_seasson"):
        league_obj = st.selectbox('Nombre de la Temporada', data_league, placeholder='Nombre de la temporada', format_func=lambda x: str(x['name'] ))
        submitted = st.form_submit_button("Delete")

        if submitted:
            if league_obj is not None:
                print("Servicio para eliminar temporada")