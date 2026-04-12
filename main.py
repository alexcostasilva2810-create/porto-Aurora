import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import textwrap

def conectar_com_chave_corrigida():
    # Puxa os dados dos Secrets
    info = dict(st.secrets["gcp_service_account"])
    
    # 1. Limpa a chave de qualquer espaço ou quebra de linha mal feita
    key_content = info["private_key"].replace("-----BEGIN PRIVATE KEY-----", "")
    key_content = key_content.replace("-----END PRIVATE KEY-----", "")
    key_content = key_content.replace("\\n", "").replace("\n", "").replace(" ", "").strip()
    
    # 2. Quebra o texto em linhas de exatamente 64 caracteres (conforme a documentação que você leu)
    #
    key_lines = textwrap.wrap(key_content, 64)
    formatted_key = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(key_lines) + "\n-----END PRIVATE KEY-----\n"
    
    # 3. Substitui na configuração
    info["private_key"] = formatted_key
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    return gspread.authorize(creds).open("Zion").worksheet("Tempo")

# Teste o botão
if st.button("TESTAR COM REFORMATAÇÃO"):
    try:
        sheet = conectar_com_chave_corrigida()
        st.success("✅ Conectado! A re-formatação de 64 caracteres funcionou.")
    except Exception as e:
        st.error(f"Erro: {e}")
