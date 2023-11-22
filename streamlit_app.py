# A Python file that is likely the main file for a Streamlit web application. 
# Running this file with Streamlit would start a web server and serve the application defined within.
# Streamlit is probably for its front-end interface

import streamlit as st
from sidebar import sidebar
from cbfs import cbfs

### Streamlite

# sets the page title, icon, and layout configuration for the web app. 
st.set_page_config(page_title="LeitlinienGPT", page_icon="🚑", layout="wide") # 📖
st.header("👨🏽‍⚕️LeitlinienGPT👩🏻‍⚕️")

sidebar()
print("YYY")

# user can choose between all and selected Leitlinien
MODEL_LIST = ["Alle AMWF Leitlinien", "Nur aktuell gültige Leitlinien"]
model: str = st.selectbox("Datenbank", options=MODEL_LIST)  # type: ignore
print(model)

# Caching is used to store the output of expensive computations so that future calls 
# with the same input are much faster.
@st.cache_resource # Mutation and concurrency issues: https://docs.streamlit.io/library/advanced-features/caching#mutation-and-concurrency-issues
def Load_Langchain():
    return cbfs()

cb = Load_Langchain()

history_cleared = st.button('Clear Chat History')
if history_cleared:
    cb.clr_history()

# text area where users can input their questions
with st.form('my_form'):
    text = st.text_area('Stelle eine Frage an die Leitlinien:', '')

# When the user submits the form, a spinner is shown to indicate that the app is processing the input.
    with st.spinner("Die Suche beginnt... dies kann einen Moment dauern⏳"):

        submitted = st.form_submit_button('Submit')
        if submitted:
            # The response from cb.convchain(text) is used to display the answer and the sources in
            # two separate columns created with st.columns(2).
            answer_col, sources_col = st.columns(2)
            result = cb.convchain(text) # generate_response(text)
            print("result[chat_history]:",result["chat_history"])
            for i in result:
                print(i)

# This context manager is specifying that the following block of code will be displayed in the answer_col column
            with answer_col:
                st.markdown("#### Antwort")
                st.markdown(result["answer"])

# displaying the sources
            with sources_col:
                st.markdown("#### Quellen")
                for source in result["source_documents"]:
                    st.markdown(source.page_content)
                    # Splits the source URL by the slash character to create a list of parts.
                    parts = source.metadata["source"].split('/')
                    # Removes the .pdf extension from the last part of the URL.
                    parts[-1] = parts[-1].replace('.pdf', '')
                    # Creates a markdown link with the formatted text, presumably the name of the document or source.
                    st.markdown(f"[{parts[1]} - {parts[-1]}]")
                    # Displays the page number of the source document.
                    st.markdown(f"Seite: {source.metadata['page']}")
                    # Inserts a horizontal rule for visual separation between different sources.
                    st.markdown("---")

# Ist eine Anamnese auch genannt als Test in den Dokumenten?