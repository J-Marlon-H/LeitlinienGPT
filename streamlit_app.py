import streamlit as st
from sidebar import sidebar
from cbfs import cbfs

### Streamlite

st.set_page_config(page_title="LeitlinienGPT", page_icon="🚑", layout="wide") # 📖
st.header("👨🏽‍⚕️LeitlinienGPT👩🏻‍⚕️")

sidebar()
print("YYY")

MODEL_LIST = ["Alle AMWF Leitlinien", "Nur aktuell gültige Leitlinien"]
model: str = st.selectbox("Datenbank", options=MODEL_LIST)  # type: ignore
print(model)

@st.cache_resource # Mutation and concurrency issues: https://docs.streamlit.io/library/advanced-features/caching#mutation-and-concurrency-issues
def Load_Langchain():
    return cbfs()

cb = Load_Langchain()

history_cleared = st.button('Clear Chat History')
if history_cleared:
    cb.clr_history()

with st.form('my_form'):
    text = st.text_area('Stelle eine Frage an die Leitlinien:', '')

    with st.spinner("Die Suche beginnt... dies kann einen Moment dauern⏳"):

        submitted = st.form_submit_button('Submit')
        if submitted:
            answer_col, sources_col = st.columns(2)
            result = cb.convchain(text) # generate_response(text)
            print("result[chat_history]:",result["chat_history"])
            for i in result:
                print(i)

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
                    st.markdown("---")

# Ist eine Anamnese auch genannt als Test in den Dokumenten?