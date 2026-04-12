import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

def conectar_definitivo():
    try:
        # 1. Carrega os dados do Secret
        info = dict(st.secrets["gcp_service_account"])
        
        # 2. Limpeza da chave: remove qualquer \n em texto e garante quebras reais
        # Isso evita o erro de PEM file que apareceu nas suas telas anteriores
        info["private_key"] = info["private_key"].replace("\\n", "\n")
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # 3. Abre a planilha e aba
        return client.open("Zion").worksheet("Tempo")
        
    except Exception as e:
        st.error(f"Erro técnico: {e}")
        return None

if st.button("CONECTAR AO SISTEMA ZION"):
    # LEMBRETE: O e-mail da conta de serviço PRECISA estar como EDITOR na planilha Zion
    aba = conectar_definitivo()
    if aba:
        st.success("✅ Conectado com sucesso!")
