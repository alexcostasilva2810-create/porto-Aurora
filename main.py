import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

def conectar_zion_real():
    try:
        # Puxa o dicionário formatado do TOML
        cred_dict = dict(st.secrets["gcp_service_account"])
        
        # Corrige as quebras de linha para o formato PEM que o Google aceita
        cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
        
        escopos = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Autenticação
        creds = Credentials.from_service_account_info(cred_dict, scopes=escopos)
        client = gspread.authorize(creds)
        
        # Tenta abrir a planilha (Certifique-se que compartilhou com o e-mail zion-operador...)
        return client.open("Zion").worksheet("Tempo")
        
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return None

if st.button("CONECTAR AGORA"):
    planilha = conectar_zion_real()
    if planilha:
        st.success("✅ SISTEMA ZION ONLINE. Finalmente conectado.")
