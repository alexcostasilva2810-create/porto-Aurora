import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# CSS: Imagem de Fundo (grãos.jpg), Legendas Pretas e Remoção de Espaços
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    .block-container { padding-top: 0rem !important; }
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    label, p, h3 { color: black !important; font-weight: bold !important; font-size: 16px !important; }
    .stTextInput>div>div>input { background-color: white !important; color: black !important; border: 2px solid #1E3A8A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO (PREVINE ERROS DE NAVEGAÇÃO) ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'login'
if 'cargo' not in st.session_state: st.session_state.cargo = None
if 'user' not in st.session_state: st.session_state.user = None
if 'placa_fixa' not in st.session_state: st.session_state.placa_fixa = ""
if 'tipo_fixo' not in st.session_state: st.session_state.tipo_fixo = ""

# --- CONEXÃO COM GOOGLE SHEETS ---
def conectar():
    creds_info = st.secrets["gcp_service_account"]
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    return gspread.authorize(creds).open("Zion").worksheet("Tempo")

# --- TELA 1: LOGIN ---
if st.session_state.etapa == 'login':
    st.markdown("<h1 style='text-align:center; color:black;'>ZION OPERACIONAL</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("USUÁRIO").strip().lower()
        s = st.text_input("SENHA", type="password")
        if st.button("ENTRAR"):
            if s == "zion123":
                st.session_state.user = u
                st.session_state.cargo = "GESTOR" if u in ["admin", "supervisor"] else "OPERADOR"
                st.session_state.etapa = 'menu'
                st.rerun()
            else: st.error("Senha inválida")

# --- TELA 2: MENU ---
elif st.session_state.etapa == 'menu':
    st.markdown(f"<h2 style='text-align:center; color:black;'>Olá, {st.session_state.user.upper()}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.session_state.cargo == "GESTOR":
            if st.button("🚛 LOGÍSTICA"): st.session_state.etapa = 'form_log'; st.rerun()
    with col2:
        if st.button("⚖️ BALANÇA"): st.session_state.etapa = 'form_bal'; st.rerun()
    with col3:
        if st.button("🏗️ TOMBADOR"): st.session_state.etapa = 'form_tom'; st.rerun()
    with col4:
        if st.button("📊 VER TABELA"): st.session_state.etapa = 'tabela'; st.rerun()
    
    if st.sidebar.button("🚪 LOGOUT"): 
        st.session_state.etapa = 'login'
        st.rerun()

# --- TELA 3: FORMULÁRIOS (MAPEAMENTO 21 CAMPOS) ---
elif st.session_state.etapa in ['form_log', 'form_bal', 'form_tom']:
    perfil = st.session_state.etapa.split('_')[1].upper()
    st.markdown(f"### ESTAÇÃO {perfil}")
    
    if st.button("⬅️ VOLTAR AO MENU"): st.session_state.etapa = 'menu'; st.rerun()

    with st.form("registro_operacional"):
        # Dados que replicam entre as telas
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("PLACA", value=st.session_state.placa_fixa)
        tipo = c2.text_input("TIPO CAMINHÃO", value=st.session_state.tipo_fixo)
        data = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))

        st.markdown("---")
        # MAPEAMENTO TOTAL - 21 CAMPOS (Divididos por Colunas da Planilha)
        h1, h2, h3, h4 = st.columns(4)
        v1 = h1.text_input("SAÍDA PÁTIO", placeholder="00:00:00")
        v2 = h2.text_input("CHEGADA ETC", placeholder="00:00:00")
        v3 = h3.text_input("ENTRADA CLASSIF", placeholder="00:00:00")
        v4 = h4.text_input("SAÍDA CLASSIF", placeholder="00:00:00")

        h5, h6, h7, h8 = st.columns(4)
        v5 = h5.text_input("ENTRADA BALANÇA", placeholder="00:00:00")
        v6 = h6.text_input("SAÍDA BALANÇA", placeholder="00:00:00")
        v7 = h7.text_input("ENTRADA TOMB", placeholder="00:00:00")
        v8 = h8.text_input("SAÍDA TOMB", placeholder="00:00:00")

        # ... (Preencher o restante dos campos vazios para completar os 21 na lista final)

        if st.form_submit_button("✅ SALVAR REGISTRO"):
            st.session_state.placa_fixa = placa
            st.session_state.tipo_fixo = tipo
            try:
                # Criando a lista de 21 campos para a planilha
                linha = [placa, tipo, data, v1, v2, v3, v4, v5, v6, v7, v8] + [""] * 10
                conectar().append_row(linha)
                st.success("Sincronizado com Google Sheets!")
            except Exception as e: st.error(f"Erro: {e}")

# --- TELA 4: TABELA ---
elif st.session_state.etapa == 'tabela':
    st.markdown("### 📊 RELATÓRIO DE LANÇAMENTOS")
    if st.button("⬅️ VOLTAR"): st.session_state.etapa = 'menu'; st.rerun()
    try:
        df = pd.DataFrame(conectar().get_all_records())
        st.dataframe(df.tail(15), use_container_width=True)
    except Exception as e: st.error("Erro ao carregar dados.")
