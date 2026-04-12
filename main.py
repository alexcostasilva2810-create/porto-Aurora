import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import textwrap # Biblioteca para garantir os 64 caracteres por linha

def conectar_blindado():
    try:
        # 1. Pega os dados dos Secrets
        info = dict(st.secrets["gcp_service_account"])
        
        # 2. Limpa a chave de qualquer coisa (espaços, aspas, \n de texto)
        pure_key = info["private_key"]
        pure_key = pure_key.replace("-----BEGIN PRIVATE KEY-----", "")
        pure_key = pure_key.replace("-----END PRIVATE KEY-----", "")
        pure_key = pure_key.replace("\\n", "").replace("\n", "").replace(" ", "").strip()
        
        # 3. RECONSTRUÇÃO OBRIGATÓRIA (Padrão RFC 1421 - 64 caracteres por linha)
        # Isso resolve o erro InvalidByte(1624, 61) que aparece na sua tela
        linhas = textwrap.wrap(pure_key, 64)
        chave_formatada = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(linhas) + "\n-----END PRIVATE KEY-----\n"
        
        # 4. Atualiza o dicionário com a chave perfeita
        info["private_key"] = chave_formatada
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(creds)
        
        return client.open("Zion").worksheet("Tempo")
    except Exception as e:
        st.error(f"Erro de Formatação PEM: {e}")
        return None

# Botão de teste
if st.button("TESTAR CONEXÃO FINAL"):
    sheet = conectar_blindado()
    if sheet:
        st.success("✅ CONECTADO! A re-formatação automática funcionou.")
