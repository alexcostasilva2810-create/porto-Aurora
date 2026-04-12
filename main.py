import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# 1. SETUP INICIAL
st.set_page_config(page_title="Zion", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS COMPACTO (SEM CORTES)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), 
             url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
             background-size: cover; background-attachment: fixed; }
    .block-container { padding: 0.5rem 1rem !important; }
    label { color: black !important; font-weight: bold !important; font-size: 0.8rem !important; }
    .stTextInput input { height: 35px !important; }
    h3 { margin-top: -10px !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. MEMÓRIA DO SISTEMA
if 'logado' not in st.session_state: st.session_state.logado = False
if 'placa' not in st.session_state: st.session_state.placa = ""

# 4. CONEXÃO SEGURA
def conectar():
    try:
        if "gcp_service_account" not in st.secrets: return None
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], 
               scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        return gspread.authorize(creds).open("Zion").worksheet("Tempo")
    except: return None

# --- TELAS ---
if not st.session_state.logado:
    st.markdown("## 🔐 ACESSO ZION")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("ENTRAR"):
        if s == "zion123":
            st.session_state.logado = True
            st.rerun()
else:
    tab1, tab2 = st.tabs(["📝 REGISTRO", "📊 TABELA"])
    
    with tab1:
        with st.form("form_final"):
            c1, c2, c3 = st.columns(3)
            p = c1.text_input("PLACA", value=st.session_state.placa)
            t = c2.text_input("TIPO")
            d = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))
            
            st.write("### ⏱️ LANÇAMENTOS")
            l1, l2, l3, l4 = st.columns(4)
            v1 = l1.text_input("SAÍDA PÁTIO")
            v2 = l2.text_input("CHEGADA ETC")
            v3 = l3.text_input("ENTRADA CLASS")
            v4 = l4.text_input("SAÍDA CLASS")

            if st.form_submit_button("✅ SALVAR NO GOOGLE"):
                st.session_state.placa = p # Salva para o próximo
                sheet = conectar()
                if sheet:
                    # Envia 21 colunas exatas
                    sheet.append_row([p, t, d, v1, v2, v3, v4] + ([""] * 14))
                    st.success("Dados enviados!")
                else: st.error("Erro nos Secrets ou Planilha!")

    with tab2:
        if st.button("🔄 ATUALIZAR"):
            sheet = conectar()
            if sheet:
                df = pd.DataFrame(sheet.get_all_records())
                st.table(df.tail(10))
