import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Validação de Chave PEM")

if "gcp_service_account" in st.secrets:
    try:
        # Tenta carregar as credenciais
        creds_dict = dict(st.secrets["gcp_service_account"])
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        
        # Se passar desta linha, o erro "Unable to load PEM file" foi resolvido!
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        st.success("✅ CONSISTÊNCIA CONFIRMADA: A chave PEM foi carregada com sucesso!")
        
    except Exception as e:
        st.error(f"O erro persiste: {e}")
        st.info("Verifique se você usou as aspas triplas nos Secrets como mostrei acima.")
else:
    st.warning("Secrets não configurados.")
