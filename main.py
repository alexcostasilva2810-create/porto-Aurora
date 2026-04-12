import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Zion Portuário", layout="wide")

def conectar_google():
    try:
        # Puxa o dicionário dos secrets
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # LIMPEZA CRÍTICA: Corrige as quebras de linha da chave privada
        # Isso remove o erro de "Invalid Byte"
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # Abre a planilha 'Zion' na aba 'Tempo' (ajuste o nome se for outro)
        return client.open("Zion").worksheet("Tempo")
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return None

# --- TELA DE TESTE ---
st.title("SISTEMA ZION - STATUS")

if st.button("TESTAR CONEXÃO AGORA"):
    sheet = conectar_google()
    if sheet:
        st.success("✅ CONEXÃO ESTABELECIDA! O Google aceitou a chave.")
        # Mostra as últimas 5 linhas da planilha para provar que está lendo
        dados = pd.DataFrame(sheet.get_all_records())
        st.write("Dados atuais na planilha:")
        st.dataframe(dados.tail(5))
