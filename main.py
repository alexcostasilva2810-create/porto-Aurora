import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA E INTERFACE ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.4), rgba(255,255,255,0.4)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    .block-container { padding-top: 1rem !important; }
    label, p, h3 { color: black !important; font-weight: bold !important; font-size: 16px !important; }
    .stTextInput>div>div>input { background-color: white !important; color: black !important; border: 2px solid #1E3A8A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE MEMÓRIA (PERSISTÊNCIA) ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'login'
if 'dados_fixos' not in st.session_state:
    st.session_state.dados_fixos = {"placa": "", "tipo": "", "data": datetime.now().strftime("%d/%m/%Y")}

# --- CONEXÃO PLANILHA ---
def salvar_dados(lista_valores):
    try:
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        client = gspread.authorize(creds)
        sheet = client.open("Zion").worksheet("Tempo")
        sheet.append_row(lista_valores)
        return True
    except Exception as e:
        st.error(f"Erro na Planilha: {e}")
        return False

# --- NAVEGAÇÃO ---
def ir_para(tela):
    st.session_state.etapa = tela
    st.rerun()

# --- 1. TELA DE LOGIN ---
if st.session_state.etapa == 'login':
    st.markdown("<h1 style='text-align:center; color:black;'>SISTEMA ZION</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        u = st.text_input("USUÁRIO").strip().lower()
        s = st.text_input("SENHA", type="password")
        if st.button("ACESSAR"):
            if s == "zion123":
                st.session_state.user = u
                st.session_state.cargo = "GESTOR" if u in ["admin", "supervisor"] else "OPERADOR"
                ir_para('menu')
            else: st.error("Senha incorreta")

# --- 2. MENU PRINCIPAL ---
elif st.session_state.etapa == 'menu':
    st.markdown(f"### Bem-vindo, {st.session_state.user.upper()}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.session_state.cargo == "GESTOR":
            if st.button("🚛 LOGÍSTICA"): ir_para('logistica')
    with col2:
        if st.button("⚖️ BALANÇA"): ir_para('balanca')
    with col3:
        if st.button("🏗️ TOMBADOR"): ir_para('tombador')
    with col4:
        if st.button("📊 VER TABELA"): ir_para('tabela')
    
    if st.button("🚪 SAIR"): ir_para('login')

# --- 3. TELAS DE LANÇAMENTO (EXEMPLO LOGÍSTICA COM TODOS OS CAMPOS) ---
elif st.session_state.etapa in ['logistica', 'balanca', 'tombador']:
    perfil = st.session_state.etapa.upper()
    st.markdown(f"## ESTAÇÃO: {perfil}")
    
    col_nav1, col_nav2 = st.columns([1, 5])
    if col_nav1.button("⬅️ VOLTAR"): ir_para('menu')
    if col_nav2.button("🧹 LIMPAR PLACA/TIPO"): 
        st.session_state.dados_fixos = {"placa": "", "tipo": "", "data": datetime.now().strftime("%d/%m/%Y")}
        st.rerun()

    with st.form("form_operacional"):
        # Dados que replicam entre as telas
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("PLACA", value=st.session_state.dados_fixos["placa"])
        tipo = c2.text_input("TIPO CAMINHÃO", value=st.session_state.dados_fixos["tipo"])
        data = c3.text_input("DATA", value=st.session_state.dados_fixos["data"])

        st.markdown("---")
        # Campos Específicos (Totalizando os 21 campos da operação)
        h1, h2, h3, h4 = st.columns(4)
        v1 = h1.text_input("SAÍDA PÁTIO", placeholder="00:00:00")
        v2 = h2.text_input("CHEGADA ETC", placeholder="00:00:00")
        v3 = h3.text_input("INÍCIO TRIAGEM", placeholder="00:00:00")
        v4 = h4.text_input("FIM TRIAGEM", placeholder="00:00:00")

        # ... (Aqui entram os demais campos até completar 21 conforme sua planilha)

        if st.form_submit_button("✅ CONFIRMAR REGISTRO"):
            # Salva na memória para a próxima tela
            st.session_state.dados_fixos = {"placa": placa, "tipo": tipo, "data": data}
            # Envia para Google Sheets
            if salvar_dados([placa, tipo, data, v1, v2, v3, v4]):
                st.success("Dados salvos e replicados!")

# --- 4. TELA DA TABELA (PEDIDO DO USUÁRIO) ---
elif st.session_state.etapa == 'tabela':
    st.markdown("## 📊 REGISTROS RECENTES")
    if st.button("⬅️ VOLTAR AO MENU"): ir_para('menu')
    try:
        # Puxa os dados da planilha para conferência
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        df = pd.DataFrame(gspread.authorize(creds).open("Zion").worksheet("Tempo").get_all_records())
        st.dataframe(df.tail(20), use_container_width=True)
    except:
        st.warning("Sem dados para exibir no momento.")
