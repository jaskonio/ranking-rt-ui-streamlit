import streamlit as st

class ConfigServices():

    @staticmethod
    def getBackendConfig(property_name):
        return st.secrets.backend[property_name]
