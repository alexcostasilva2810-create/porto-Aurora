import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Teste de Conexão Zion")

# Verifica se o dicionário gcp_service_account existe
if "gcp_service_account" in st.secrets:
    st.info("🔎 Chave encontrada. Tentando conectar...")
    
    try:
        # Puxa os dados como um dicionário Python comum (evita o erro de JSONDecode)
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # Tenta abrir a planilha
        planilha = client.open("Zion").worksheet("Tempo")
        
        st.success("🔥 CONEXÃO ESTABELECIDA COM SUCESSO!")
        st.write("Conectado à aba:", planilha.title)
        
    except Exception as e:
        st.error(f"❌ Erro ao processar as chaves: {e}")
        st.write("Dica: Verifique se a 'private_key' nos Secrets está entre aspas e com os \\n")
else:
    st.error("🚨 O Streamlit não encontrou [gcp_service_account] nos Secrets.")
    st.write("Verifique se você salvou o texto no painel Settings > Secrets.")
