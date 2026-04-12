import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

def iniciar_sistema_zion():
    try:
        # Carrega as configurações dos Secrets
        credenciais_dict = dict(st.secrets["gcp_service_account"])
        
        # Garante que as quebras de linha da chave privada sejam interpretadas corretamente
        credenciais_dict["private_key"] = credenciais_dict["private_key"].replace("\\n", "\n")
        
        # Define os escopos necessários
        escopos = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Cria as credenciais e autoriza o cliente
        creds = Credentials.from_service_account_info(credenciais_dict, scopes=escopos)
        client = gspread.authorize(creds)
        
        # Tenta abrir a planilha e a aba
        return client.open("Zion").worksheet("Tempo")
        
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return None

# Interface
if st.button("CONECTAR AO SISTEMA ZION"):
    aba_tempo = iniciar_sistema_zion()
    if aba_tempo:
        st.success("✅ Conexão estabelecida! O sistema já pode ler e gravar dados.")
