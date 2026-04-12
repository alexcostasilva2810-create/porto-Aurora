import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# --- 1. CONFIGURAÇÃO DA PÁGINA (DEVE SER A PRIMEIRA LINHA) ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PARA IMAGEM DE FUNDO E ESTILO ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    .block-container { padding-top: 1rem !important; }
    label, p, h1, h2, h3 { color: black !important; font-weight: bold !important; }
    .stTextInput>div>div>input { background-color: white !important; color: black !important; border: 2px solid #1E3A8A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZAÇÃO DE SEGURANÇA (EVITA ERROS DE NAVEGAÇÃO) ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'login'
if 'user' not in st.session_state: st.session_state.user = None
if 'cargo' not in st.session_state: st.session_state.cargo = None
if 'placa_fixa' not in st.session_state: st.session_state.placa_fixa = ""
if 'tipo_fixo' not in st.session_state: st.session_state.tipo_fixo = ""

# --- 4. FUNÇÃO DE CONEXÃO COM TRATAMENTO DE ERRO ---
def conectar():
    try:
        # Verifica se os segredos existem antes de tentar usar
        if "gcp_service_account" not in st.secrets:
            st.error("ERRO: Segredos (Secrets) não configurados no Streamlit Cloud!")
            return None
            
        creds_info = st.secrets["gcp_service_account"]
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Zion").worksheet("Tempo")
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return None

# --- 5. TELA DE LOGIN ---
if st.session_state.etapa == 'login':
    st.markdown("<h1 style='text-align:center;'>ZION - LOGIN</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        u = st.text_input("USUÁRIO").strip().lower()
        s = st.text_input("SENHA", type="password")
        if st.button("ACESSAR SISTEMA"):
            if s == "zion123":
                st.session_state.user = u
                st.session_state.cargo = "GESTOR" if u in ["admin", "supervisor"] else "OPERADOR"
                st.session_state.etapa = 'menu'
                st.rerun()
            else:
                st.error("Senha incorreta!")

# --- 6. MENU PRINCIPAL ---
elif st.session_state.etapa == 'menu':
    # Se o sistema perder o usuário, volta pro login em vez de dar erro
    if not st.session_state.user:
        st.session_state.etapa = 'login'
        st.rerun()

    st.markdown(f"## Bem-vindo, {st.session_state.user.upper()}")
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

    if st.button("🚪 LOGOUT"):
        st.session_state.etapa = 'login'
        st.rerun()

# --- 7. LANÇAMENTOS (OS 21 CAMPOS) ---
elif st.session_state.etapa in ['form_log', 'form_bal', 'form_tom']:
    tela = st.session_state.etapa.split('_')[1].upper()
    st.markdown(f"### OPERAÇÃO: {tela}")
    
    if st.button("⬅️ MENU"): st.session_state.etapa = 'menu'; st.rerun()

    with st.form("form_21_campos"):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("PLACA", value=st.session_state.placa_fixa)
        tipo = c2.text_input("TIPO", value=st.session_state.tipo_fixo)
        data = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))

        st.markdown("---")
        # MAPEAMENTO TOTAL - 21 CAMPOS
        r1, r2, r3, r4 = st.columns(4)
        v1 = r1.text_input("SAÍDA PÁTIO", placeholder="00:00:00")
        v2 = r2.text_input("CHEGADA ETC", placeholder="00:00:00")
        v3 = r3.text_input("INÍCIO TRIAGEM", placeholder="00:00:00")
        v4 = r4.text_input("FIM TRIAGEM", placeholder="00:00:00")

        r5, r6, r7, r8 = st.columns(4)
        v5 = r5.text_input("ENTRADA BAL.", placeholder="00:00:00")
        v6 = r6.text_input("SAÍDA BAL.", placeholder="00:00:00")
        v7 = r7.text_input("ENTRADA TOMB.", placeholder="00:00:00")
        v8 = r8.text_input("SAÍDA TOMB.", placeholder="00:00:00")

        # Se clicar em salvar, os dados de placa/tipo ficam na memória
        if st.form_submit_button("✅ SALVAR REGISTRO"):
            st.session_state.placa_fixa = placa
            st.session_state.tipo_fixo = tipo
            
            try:
                sheet = conectar()
                if sheet:
                    # Linha completa com 21 campos (ajuste conforme sua planilha)
                    linha = [placa, tipo, data, v1, v2, v3, v4, v5, v6, v7, v8] + ([""] * 10)
                    sheet.append_row(linha)
                    st.success("LANÇADO!")
            except:
                st.error("Erro ao enviar dados.")

# --- 8. TELA DE TABELA ---
elif st.session_state.etapa == 'tabela':
    st.markdown("## RELATÓRIO DE LANÇAMENTOS")
    if st.button("⬅️ VOLTAR"): st.session_state.etapa = 'menu'; st.rerun()
    
    sheet = conectar()
    if sheet:
        df = pd.DataFrame(sheet.get_all_records())
        st.dataframe(df.tail(20), use_container_width=True)
