import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import base64
import json

def conectar_zion_final():
    try:
        # Pega a string única dos Secrets
        b64_content = st.secrets["gcp_service_account"]["content"]
        
        # Converte de volta para JSON
        json_info = json.loads(base64.b64decode(b64_content).decode('utf-8'))
        
        # Corrige as quebras de linha que o JSON as vezes bagunça
        json_info["private_key"] = json_info["private_key"].replace("\\n", "\n")
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(json_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        return client.open("Zion").worksheet("Tempo")
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

if st.button("CONECTAR AGORA"):
    planilha = conectar_zion_final()
    if planilha:
        st.success("✅ FINALMENTE CONECTADO!")
