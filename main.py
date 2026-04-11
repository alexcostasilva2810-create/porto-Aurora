import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# --- CONEXÃO GOOGLE SHEETS ---
def conectar_planilha():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds_info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Zion").worksheet("Tempo")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    .main-title { color: white; text-align: center; font-family: 'Arial Black'; font-size: 45px; text-shadow: 2px 2px 4px #000; margin-bottom: 30px; }
    .card-login { background: rgba(255, 255, 255, 0.9); padding: 30px; border-radius: 15px; color: black; border-top: 8px solid #4169E1; }
    .stButton>button { width: 100%; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CONTROLE DE NAVEGAÇÃO (ESTADOS) ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'apresentacao'
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

# --- MÁSCARA JS PARA HORA (FIX PARA NÃO SUMIR) ---
components.html("""
    <script>
    const mask = (e) => {
        let v = e.target.value.replace(/\D/g,'');
        if (v.length > 6) v = v.slice(0,6);
        if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
        else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
        e.target.value = v;
    }
    setInterval(() => {
        window.parent.document.querySelectorAll('input[placeholder="00:00:00"]').forEach(i => {
            if(!i.dataset.m) { 
                i.addEventListener('input', mask); i.dataset.m = '1';
                i.onblur = () => { i.dispatchEvent(new Event('change', { bubbles: true })); };
            }
        });
    }, 500);
    </script>
    """, height=0)

# --- 1. TELA DE APRESENTAÇÃO ---
if st.session_state.etapa == 'apresentacao':
    st.markdown("<h1 class='main-title'>ZION PORTUÁRIO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:white; text-align:center; font-size:20px;'>Gestão de Fluxo e Logística de Grãos</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 INICIAR OPERAÇÃO"):
            st.session_state.etapa = 'login'
            st.rerun()

# --- 2. TELA DE LOGIN ---
elif st.session_state.etapa == 'login':
    st.markdown("<h1 class='main-title'>SISTEMA DE ACESSO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        with st.container():
            st.markdown("<div class='card-login'>", unsafe_allow_html=True)
            usuario = st.text_input("USUÁRIO")
            senha = st.text_input("SENHA", type="password")
            perfil_selecionado = st.selectbox("ESTAÇÃO", ["LOGÍSTICA", "BALANÇA", "TOMBADOR", "SUPERVISOR"])
            
            if st.button("EFETUAR LOGIN"):
                # Aqui você pode colocar suas senhas reais
                if usuario == "admin" and senha == "zion123":
                    st.session_state.autenticado = True
                    st.session_state.perfil = perfil_selecionado
                    st.session_state.etapa = 'menu'
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos!")
            st.markdown("</div>", unsafe_allow_html=True)

# --- 3. MENU PRINCIPAL ---
elif st.session_state.etapa == 'menu':
    st.markdown(f"<h1 class='main-title'>BEM-VINDO: {st.session_state.perfil}</h1>", unsafe_allow_html=True)
    
    colA, colB, colC = st.columns(3)
    
    # Só mostra o que o perfil tem acesso
    if st.session_state.perfil in ["LOGÍSTICA", "SUPERVISOR"]:
        with colA:
            if st.button("🚚 ABRIR LOGÍSTICA"): st.session_state.etapa = 'estacao_log'; st.rerun()
            
    if st.session_state.perfil in ["BALANÇA", "SUPERVISOR"]:
        with colB:
            if st.button("⚖️ ABRIR BALANÇA"): st.session_state.etapa = 'estacao_bal'; st.rerun()
            
    if st.session_state.perfil in ["TOMBADOR", "SUPERVISOR"]:
        with colC:
            if st.button("🏗️ ABRIR TOMBADOR"): st.session_state.etapa = 'estacao_tom'; st.rerun()

    if st.sidebar.button("🚪 LOGOUT"):
        st.session_state.etapa = 'apresentacao'
        st.session_state.autenticado = False
        st.rerun()

# --- 4. ESTAÇÕES (EXEMPLO: LOGÍSTICA) ---
elif st.session_state.etapa == 'estacao_log':
    st.markdown("<h1 class='main-title'>ESTAÇÃO LOGÍSTICA</h1>", unsafe_allow_html=True)
    
    # BOTÃO DE RETORNO QUE VOCÊ PEDIU
    if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
        st.session_state.etapa = 'menu'
        st.rerun()

    with st.form("form_log", clear_on_submit=True):
        st.markdown("<div style='background:white; padding:20px; border-radius:10px;'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("PLACA")
        cam = c2.text_input("CAMINHÃO")
        data = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))
        
        st.write("---")
        h1, h2, h3 = st.columns(3)
        s_patio = h1.text_input("Saída Pátio", placeholder="00:00:00")
        c_etc = h2.text_input("Chegada ETC", placeholder="00:00:00")
        e_class = h3.text_input("Entrada Classific", placeholder="00:00:00")
        
        if st.form_submit_button("💾 SALVAR DADOS NA PLANILHA"):
            try:
                sheet = conectar_planilha()
                # Salva na ordem da sua planilha Zion
                sheet.append_row([placa, cam, data, s_patio, c_etc, "", e_class])
                st.success("✅ Sucesso! Dados sincronizados com o AppSheet.")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
