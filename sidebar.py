import streamlit as st
from faq import faq

def sidebar():
    with st.sidebar:
        st.markdown(
            "## Tipps zur Benutzung\n"
            "1. Stelle eine Frage an die [AWMF Leitlinien](https://register.awmf.org/de/leitlinien/aktuelle-leitlinien).\n"  
            "2. Stelle Rückfragen und nutze LeitlinienGPT als Suchmaschine.\n"  
            "3. Verifiziere die Antwort anhand der genannten Quellen.\n"
            "4. Setze die chat history zurück für ein neues Thema!\n"
        )

        st.markdown("---")
        st.markdown("# Über die App")
        st.markdown(
            "👨🏽‍⚕️LeitlinienGPT👩🏻‍⚕️ ist eine Suchmaschine für die AWMF Leitlinien. \n"
            "Die Antworten sind einfach verständlich und nennen die relevanten Leitlinien als Quelle. "
        )
        st.markdown("Die Website ist immer offen für neue Anregungen. \n")
        st.markdown("Gebt mir gerne feedback unter marlon.hamm@outlook.de! \n")
        st.markdown("Für Interessierte kann der Code auf [GitHub](https://github.com/J-Marlon-H/LeitlinienGPT) eingesehen werden. ")
        
        st.markdown("Made by [Marlon Hamm](https://www.linkedin.com/in/m-hamm/) & [Paolo Oppelt](https://www.linkedin.com/in/paolo-oppelt/) 😃")

        st.markdown("---")

        faq()
