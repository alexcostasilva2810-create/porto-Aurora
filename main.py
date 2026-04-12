import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import base64
import json

def conectar_zion_forca_bruta():
    try:
        # 1. Pega o Base64 e remove qualquer espaço que você possa ter colado sem querer
        encoded_json = st.secrets["gcp_service_account"]["content"].strip()
        
        # 2. Decodifica
        decoded_bytes = base64.b64decode(encoded_json)
        json_data = json.loads(decoded_bytes)
        
        # 3. LIMPEZA DA CHAVE PRIVADA (Onde o erro 1625 acontece)
        # Removemos tudo o que não for a chave pura e reconstruímos
        raw_key = json_data["private_key"]
        
        # Remove cabeçalhos, rodapés, quebras de linha e espaços
        clean_key = raw_key.replace("-----BEGIN PRIVATE KEY-----", "")
        clean_key = clean_key.replace("-----END PRIVATE KEY-----", "")
        clean_key = clean_key.replace("\\n", "").replace("\n", "").replace(" ", "").strip()
        
        # Reconstrói do zero no formato que o Google AMA (com quebras de linha reais)
        # Isso mata o erro InvalidByte de uma vez por todas
        final_key = "-----BEGIN PRIVATE KEY-----\n"
        for i in range(0, len(clean_key), 64):
            final_key += clean_key[i:i+64] + "\n"
        final_key += "-----END PRIVATE KEY-----\n"
        
        json_data["private_key"] = final_key
        
        # 4. Tenta conectar
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(json_data, scopes=scopes)
        client = gspread.authorize(creds)
        
        return client.open("Zion").worksheet("Tempo")
        
    except Exception as e:
        st.error(f"Erro na força bruta: {e}")
        return None

if st.button("TENTATIVA FINAL - FORÇA BRUTA"):
    sheet = conectar_zion_forca_bruta()
    if sheet:
        st.success("✅ FINALMENTE! Conectado e chave reconstruída com sucesso.")
