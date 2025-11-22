import streamlit as st

st.set_page_config(page_title="Painel das Fases", page_icon="🚀")

st.title("🚀 Painel de Navegação Entre Fases")
st.write("Clique em uma fase para abrir a interface correspondente.")

# Mapeamento baseado no docker-compose informado
fases = {
    "Fase 1 - CLI (Streamlit)": "http://localhost:8501",
    "Fase 3 - App (Streamlit)": "http://localhost:8503",
    "Fase 4 - App (Streamlit)": "http://localhost:8504",
    "Fase 6 - App (Streamlit)": "http://localhost:8506",
    # DBs não possuem interface via navegador, então são ignorados
}

for nome, url in fases.items():
    if st.button(nome):
        st.markdown(f"""
            <meta http-equiv="refresh" content="0; url={url}" />
        """, unsafe_allow_html=True)