import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import base64
import json

def conectar_zion_definitivo():
    try:
        # Lê a string Base64 dos Secrets
        encoded_json = st.secrets["gcp_service_account"]["content"]
        
        # Decodifica para texto (JSON)
        decoded_bytes = base64.b64decode(encoded_json)
        service_account_info = json.loads(decoded_bytes)
        
        # Corrige as quebras de linha da chave (onde dava o erro de byte 61)
        service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
        
        # Autentica
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Abre a planilha "Zion" e a aba "Tempo"
        return client.open("Zion").worksheet("Tempo")
    except Exception as e:
        st.error(f"Erro na conexão definitiva: {e}")
        return None

# Teste o botão
if st.button("TESTAR CONEXÃO AGORA"):
    sheet = conectar_zion_definitivo()
    if sheet:
        st.success("✅ AGORA FOI! O sistema está conectado à planilha.")
