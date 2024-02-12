import streamlit as st

class NotificationServices():

    def show_info(self, msg):
        st.toast(msg, icon="✅")

    def show_warnning(self, msg):
        st.toast(msg, icon="🚨")

    def show_error(self, msg):
        st.toast(msg, icon="🔥")
