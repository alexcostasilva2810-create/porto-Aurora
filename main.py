import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Validação Zion - Ajuste Final")

def limpar_e_conectar():
    # Puxa o que estiver nos Secrets
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # Limpeza manual da chave para evitar o erro InvalidByte
    # Isso remove aspas extras que o Streamlit às vezes coloca sozinho
    raw_key = creds_dict["private_key"]
    clean_key = raw_key.strip().replace("\\n", "\n")
    
    # Se a chave vier com aspas no início/fim, a gente corta fora
    if clean_key.startswith('"') and clean_key.endswith('"'):
        clean_key = clean_key[1:-1]
        
    creds_dict["private_key"] = clean_key
    
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    return gspread.authorize(creds).open("Zion").worksheet("Tempo")

try:
    if "gcp_service_account" in st.secrets:
        sheet = limpar_e_conectar()
        st.success("✅ AGORA FOI! Conexão estabelecida sem erros de chave.")
        st.write("Aba conectada:", sheet.title)
    else:
        st.error("Secrets não configurados no painel.")
except Exception as e:
    st.error(f"Erro detectado: {e}")
    st.info("Se o erro 'InvalidByte' continuar, verifique se no painel Secrets a chave começa exatamente com -----BEGIN PRIVATE KEY-----")
