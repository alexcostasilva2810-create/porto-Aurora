import streamlit as st
import base64
import json
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Zion Tecnologia", layout="wide", initial_sidebar_state="collapsed")

# Inicializa o estado da página se não existir
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'login'

# --- ESTILIZAÇÃO CSS (AZUL ROYAL E BOTÕES 3D LARANJA) ---
st.markdown(
    """
    <style>
    /* Fundo Azul Royal */
    .stApp {
        background-color: #002366;
    }

    /* Título Centralizado */
    .titulo-menu {
        color: white;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        margin-bottom: 50px;
    }

    /* Estilo dos Botões Laranja 3D */
    div.stButton > button {
        background-color: #FF8C00;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 20px;
        width: 100%;
        height: 100px;
        font-size: 18px;
        box-shadow: 0px 9px 0px #CC7000; /* Efeito 3D (Sombra inferior) */
        transition: all 0.1s ease;
    }

    /* Efeito ao clicar (Botão abaixa) */
    div.stButton > button:active {
        box-shadow: 0px 2px 0px #CC7000;
        transform: translateY(7px);
    }
    
    /* Botão de Voltar específico */
    .btn-voltar button {
        background-color: #4A4A4A !important;
        height: 50px !important;
        box-shadow: 0px 5px 0px #222 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- FUNÇÃO DE CONEXÃO (A QUE FUNCIONOU!) ---
def conectar_zion():
    try:
        b64_content = st.secrets["gcp_service_account"]["content"]
        json_info = json.loads(base64.b64decode(b64_content).decode('utf-8'))
        json_info["private_key"] = json_info["private_key"].replace("\\n", "\n")
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(json_info, scopes=scopes)
        return gspread.authorize(creds).open("Zion")
    except:
        return None

# --- TELA 1: LOGIN / BOAS-VINDAS ---
if st.session_state['pagina'] == 'login':
    st.markdown('<div style="text-align: center; margin-top: 5%; color: white;">'
                '<h1 style="font-size: 60px;">Seja Bem Vindo</h1>'
                '<h2 style="font-size: 40px;">ao</h2>'
                '<h1 style="font-size: 60px;">Zion Tecnologia</h1>'
                '<br><br>'
                '<h3 style="font-size: 30px; margin-top: 50px;">Transdourado</h3>'
                '</div>', unsafe_allow_html=True)
    
    for _ in range(10): st.write("")
    
    col1, _ = st.columns([1, 4])
    with col1:
        if st.button("ACESSO"):
            st.session_state['pagina'] = 'menu'
            st.rerun()

# --- TELA 2: MENU PRINCIPAL ---
elif st.session_state['pagina'] == 'menu':
    st.markdown('<h1 class="titulo-menu">MENU</h1>', unsafe_allow_html=True)
    
    # Grid de Botões (3 colunas para organizar)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("Logistica Patio / ETC")
        st.button("Tombador")
        
    with col2:
        st.button("Classificação")
        st.button("Tabela Ent/Said")
        
    with col3:
        st.button("Balança")
        st.button("Dashboard")

    # Botão de Voltar para Login (Canto inferior)
    st.write("---")
    col_voltar, _ = st.columns([1, 5])
    with col_voltar:
        st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
        if st.button("VOLTAR PARA LOGIN"):
            st.session_state['pagina'] = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
