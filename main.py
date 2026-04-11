import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# 🔑 CONFIGURAÇÃO TOTAL
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: IMAGEM DE FUNDO (A CERTA) E ESTILO DOS CAMPOS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
        url("https://raw.githubusercontent.com/sua-url-da-imagem/image_04fe05.jpg"); /* Use o link direto da sua imagem aqui */
        background-size: cover;
        background-attachment: fixed;
    }
    .title-zion { color: #4169E1; font-family: 'Arial Black'; font-size: 30px; text-align: center; background: rgba(255,255,255,0.9); padding: 15px; border-radius: 12px; margin-bottom: 25px; border-bottom: 5px solid #4169E1; }
    .menu-card { background: rgba(255,255,255,0.95); padding: 25px; border-radius: 15px; border-left: 10px solid #4169E1; text-align: center; font-size: 20px; transition: 0.3s; }
    div[data-testid="stTextInput"] { width: 150px !important; }
    input { height: 2.2rem !important; font-weight: bold !important; font-size: 15px !important; }
    .section-HR { border-bottom: 3px solid #4169E1; margin: 20px 0; color: #4169E1; font-weight: bold; font-size: 16px; width: 750px; }
    </style>
    """, unsafe_allow_html=True)

# --- MÁSCARA DE HORA BLINDADA (NÃO SOME MAIS) ---
components.html("""
    <script>
    function formatTime(v) {
        v = v.replace(/\D/g,'');
        if (v.length > 6) v = v.slice(0,6);
        if (v.length > 4) return v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
        if (v.length > 2) return v.replace(/(\d{2})(\d{2})/, "$1:$2");
        return v;
    }
    
    const applyMask = () => {
        const inputs = window.parent.document.querySelectorAll('input[placeholder="00:00:00"]');
        inputs.forEach(input => {
            if (!input.dataset.locked) {
                input.dataset.locked = "true";
                input.addEventListener('keydown', (e) => {
                    // Previne o refresh do Streamlit enquanto digita
                    e.stopPropagation();
                });
                input.addEventListener('input', (e) => {
                    e.target.value = formatTime(e.target.value);
                });
                input.addEventListener('change', (e) => {
                    // Só envia pro Streamlit quando sai do campo ou dá Enter
                    window.parent.postMessage({type: 'streamlit:setComponentValue', value: e.target.value}, '*');
                });
            }
        });
    }
    setInterval(applyMask, 500);
    </script>
    """, height=0)

# --- SISTEMA DE NAVEGAÇÃO ---
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'form_data' not in st.session_state: st.session_state.form_data = {}

def change_page(target):
    st.session_state.page = target
    st.rerun()

# --- TELA 1: LOGIN (FUNDO PORTUÁRIO) ---
if st.session_state.page == 'login':
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<br><br><div class='title-zion'>ZION PORTUÁRIO - LOGIN</div>", unsafe_allow_html=True)
        with st.container():
            st.text_input("USUÁRIO", key="user")
            st.text_input("SENHA", type="password", key="pass")
            if st.button("ACESSAR OPERAÇÃO", use_container_width=True):
                change_page('menu')

# --- TELA 2: MENU DE ESTAÇÕES ---
elif st.session_state.page == 'menu':
    st.markdown("<div class='title-zion'>PAINEL DE JANELAS OPERACIONAIS</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("<div class='menu-card'>🚛<br>LOGÍSTICA</div>", unsafe_allow_html=True)
        if st.button("Abrir Janela 1", key="m1"): change_page('logistica')
    with c2:
        st.markdown("<div class='menu-card'>⚖️<br>BALANÇA</div>", unsafe_allow_html=True)
        if st.button("Abrir Janela 2", key="m2"): change_page('balanca')
    with c3:
        st.markdown("<div class='menu-card'>🏗️<br>TOMBADOR</div>", unsafe_allow_html=True)
        if st.button("Abrir Janela 3", key="m3"): change_page('tombador')
    with c4:
        st.markdown("<div class='menu-card'>🏁<br>FECHAMENTO</div>", unsafe_allow_html=True)
        if st.button("Abrir Janela 4", key="m4"): change_page('fechamento')

# --- TELA 3: ESTAÇÃO LOGÍSTICA ---
elif st.session_state.page == 'logistica':
    st.markdown("<div class='title-zion'>JANELA: LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
    if st.button("⬅️ VOLTAR AO MENU"): change_page('menu')
    
    colA, colB, colC = st.columns(3)
    placa = colA.text_input("PLACA", key="p_placa")
    caminhao = colB.text_input("CAMINHÃO", key="p_cam")
    data = colC.date_input("DATA", format="DD/MM/YYYY")
    
    st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    spat = c1.text_input("Saída Pátio", placeholder="00:00:00", key="h_spat")
    cetc = c2.text_input("Chegada ETC", placeholder="00:00:00", key="h_cetc")
    ttvi = c3.text_input("TT Viagem", placeholder="00:00:00", key="h_ttvi")
    ecla = c4.text_input("Ent. Class", placeholder="00:00:00", key="h_ecla")
    
    if st.button("💾 SALVAR REGISTRO DE LOGÍSTICA"):
        st.success("Dados enviados para a Balança!")
