import streamlit as st
from sidebar import sidebar
from cbfs import cbfs

### Streamlite

st.set_page_config(page_title="LeitlinienGPT", page_icon="🚑", layout="wide") # 📖
st.header("👨🏽‍⚕️LeitlinienGPT👩🏻‍⚕️")

sidebar()

if 'cb' not in st.session_state:
    st.session_state.cb = cbfs()

def DB():
    st.session_state.cb.load_model(st.session_state.model)

def clr_hist():
    st.session_state.cb.clr_history()

MODEL_LIST = ["Alle AMWF Leitlinien", "Nur aktuell gültige Leitlinien"]
st.selectbox("Datenbank", options=MODEL_LIST, key="model",
             on_change = DB)  

st.session_state.cb.load_model_test = st.session_state.cb.load_model(st.session_state.model)

history_cleared = st.button('Clear Chat History',on_click = clr_hist)

with st.form('my_form'):
    text = st.text_area('Stelle eine Frage an die Leitlinien:', '')

    with st.spinner("Die Suche beginnt... dies kann einen Moment dauern⏳"):

        submitted = st.form_submit_button('Submit')
        if submitted:
            answer_col, sources_col = st.columns(2)
            result = st.session_state.cb.convchain(text) # generate_response(text)

            with answer_col:
                st.markdown("#### Antwort")
                st.markdown(result["answer"])

            with sources_col:
                st.markdown("#### Quellen")
                for source in result["source_documents"]:
                    st.markdown(source.page_content)
                    parts = source.metadata["source"].split('/')
                    parts[-1] = parts[-1].replace('.pdf', '')
                    st.markdown(f"[{parts[1]} - {parts[-1]}]")
                    st.markdown(f"Seite: {source.metadata['page']}")
                    st.markdown(f"{source.metadata['Gültigkeit']}")
                    st.markdown("---")