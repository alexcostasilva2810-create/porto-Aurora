import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Teste de Conexão Zion")

# 1. Verifica se o segredo existe no sistema
if "gcp_service_account" in st.secrets:
    st.success("✅ O Streamlit encontrou a chave 'gcp_service_account' nos Secrets!")
    
    try:
        # 2. Tenta autenticar
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        
        # 3. Tenta abrir a planilha
        # Certifique-se que o nome da planilha é 'Zion' e a aba é 'Tempo'
        planilha = client.open("Zion").worksheet("Tempo")
        
        st.success("🔥 CONEXÃO TOTAL ESTABELECIDA! O Google Sheets respondeu.")
        st.write("Última linha lida:", planilha.get_all_values()[-1])
        
    except Exception as e:
        st.error(f"❌ Erro na autenticação ou leitura: {e}")
else:
    st.error("🚨 O Streamlit NÃO encontrou as credenciais. Verifique o painel Secrets.")
