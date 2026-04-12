import streamlit as st
import gspread
import base64
import json
import os

def conectar_definitivo_mesmo():
    try:
        # 1. Pega o Base64 do Secret
        encoded_json = st.secrets["gcp_service_account"]["content"].strip()
        
        # 2. Decodifica e limpa as quebras de linha da chave
        decoded_bytes = base64.b64decode(encoded_json)
        json_data = json.loads(decoded_bytes)
        json_data["private_key"] = json_data["private_key"].replace("\\n", "\n")
        
        # 3. CRIA UM ARQUIVO DE VERDADE NO SERVIDOR
        # Isso engana a biblioteca de segurança e evita o erro PEM
        with open("temp_key.json", "w") as f:
            json.dump(json_data, f)
        
        # 4. Autentica lendo o ARQUIVO, não o dicionário
        # O gspread.service_account aceita o caminho do arquivo
        client = gspread.service_account(filename="temp_key.json")
        
        # 5. Remove o arquivo por segurança após conectar
        os.remove("temp_key.json")
        
        return client.open("Zion").worksheet("Tempo")
        
    except Exception as e:
        st.error(f"Erro persistente: {e}")
        return None

if st.button("TENTAR CONEXÃO VIA ARQUIVO"):
    sheet = conectar_definitivo_mesmo()
    if sheet:
        st.success("✅ AGORA FOI! Conectado via arquivo físico temporário.")
