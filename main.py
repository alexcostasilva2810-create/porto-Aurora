import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# CONFIGURAÇÃO DE TELA
st.set_page_config(page_title="Zion", layout="wide")

# CSS COMPACTO - RESOLVE O CORTE DOS TÍTULOS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover;
    }
    .block-container { padding-top: 1rem !important; }
    label { color: black !important; font-weight: bold !important; font-size: 0.9rem !important; }
    h1, h2, h3 { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DO ESTADO
if 'logado' not in st.session_state: st.session_state.logado = False

# CONEXÃO COM TESTE DE ERRO
def conectar():
    try:
        # Se os secrets não estiverem no painel, ele avisa aqui em vez de explodir
        if "gcp_service_account" not in st.secrets:
            st.warning("⚠️ Configure os 'Secrets' no painel do Streamlit Cloud!")
            return None
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], 
               scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        return gspread.authorize(creds).open("Zion").worksheet("Tempo")
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return None

# TELA DE LOGIN
if not st.session_state.logado:
    st.title("ZION LOGIN")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if s == "zion123":
            st.session_state.logado = True
            st.rerun()
else:
    # SISTEMA COMPACTO
    t1, t2 = st.tabs(["LANÇAMENTOS", "TABELA"])
    
    with t1:
        with st.form("form_zion"):
            c1, c2, c3 = st.columns(3)
            p = c1.text_input("PLACA")
            t = c2.text_input("TIPO")
            d = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))
            
            st.write("---")
            # CAMPOS COMPACTOS (4 POR LINHA)
            cols = st.columns(4)
            v1 = cols[0].text_input("SAÍDA PÁTIO")
            v2 = cols[1].text_input("CHEGADA ETC")
            v3 = cols[2].text_input("ENTRADA CLASS")
            v4 = cols[3].text_input("SAÍDA CLASS")
            
            if st.form_submit_button("SALVAR"):
                sheet = conectar()
                if sheet:
                    # Envia exatamente 21 colunas
                    linha = [p, t, d, v1, v2, v3, v4] + ([""] * 14)
                    sheet.append_row(linha)
                    st.success("Salvo!")

    with t2:
        if st.button("Atualizar Tabela"):
            sheet = conectar()
            if sheet:
                df = pd.DataFrame(sheet.get_all_records())
                st.dataframe(df.tail(10))
