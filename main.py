import streamlit as st
import base64
import json
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# BLOCO 1: CONFIGURAÇÕES E ESTILIZAÇÃO (CSS)
# ==========================================
st.set_page_config(page_title="Zion Tecnologia", layout="wide", initial_sidebar_state="collapsed")

def aplicar_estilo(cor_fundo):
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {cor_fundo}; }}
        
        /* Título do Menu */
        .titulo-menu {{
            color: white; text-align: center; font-size: 55px; font-weight: bold; margin-bottom: 40px;
            text-shadow: 2px 2px 4px #000000;
        }}

        /* Botões Laranja 3D */
        div.stButton > button {{
            background-color: #FF8C00; color: white; font-weight: bold; border-radius: 12px;
            border: none; width: 100%; height: 90px; font-size: 20px;
            box-shadow: 0px 8px 0px #CC7000; transition: all 0.1s ease;
            margin-bottom: 5px;
        }}
        div.stButton > button:active {{
            box-shadow: 0px 2px 0px #CC7000; transform: translateY(6px);
        }}
        
        /* Centralização de ícones e legendas */
        .icon-box {{ text-align: center; color: white; font-size: 40px; margin-bottom: 20px; }}
        .label-icon {{ font-size: 14px; font-weight: normal; margin-top: -10px; }}

        /* Botão Voltar (Estilo Diferente) */
        .btn-voltar-container {{ display: flex; justify-content: center; margin-top: 50px; }}
        .stButton > button[kind="secondary"] {{
            background-color: #4A4A4A; box-shadow: 0px 5px 0px #222; height: 50px; width: 200px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# BLOCO 2: CONEXÃO COM BANCO DE DADOS (ZION)
# ==========================================
def conectar_zion():
    try:
        # Usa a conexão Base64 que validamos
        b64_content = st.secrets["gcp_service_account"]["content"]
        json_info = json.loads(base64.b64decode(b64_content).decode('utf-8'))
        json_info["private_key"] = json_info["private_key"].replace("\\n", "\n")
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(json_info, scopes=scopes)
        return gspread.authorize(creds).open("Zion")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

# Controle de Navegação
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

# ==========================================
# BLOCO 3: TELA INICIAL (CINZA/PRATA)
# ==========================================
if st.session_state['pagina'] == 'inicio':
    aplicar_estilo("#C0C0C0") # Cinza Prata
    
    st.markdown("""
        <div style="text-align: center; margin-top: 5%;">
            <h1 style="font-size: 60px;">Seja Bem Vindo</h1>
            <h2 style="font-size: 40px;">ao</h2>
            <h1 style="font-size: 60px;">Zion Tecnologia</h1>
            <br><br>
            <h3 style="font-size: 30px; margin-top: 50px;">Transdourado</h3>
        </div>
    """, unsafe_allow_html=True)
    
    for _ in range(8): st.write("")
    
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("ACESSO"):
            st.session_state['pagina'] = 'menu'
            st.rerun()

# ==========================================
# BLOCO 4: TELA DE MENU (AZUL ROYAL) - COMPACTO
# ==========================================
elif st.session_state['pagina'] == 'menu':
    aplicar_estilo("#002366")
    
    # Título MENU Amarelo
    st.markdown('<h1 style="color: yellow; text-align: center; font-size: 50px; font-weight: bold; margin-bottom: 30px;">MENU</h1>', unsafe_allow_html=True)
    
    # CSS para forçar o espaçamento de "3cm" (aprox. 110px) e visual compacto
    st.markdown("""
        <style>
        /* Ajusta o espaçamento entre as colunas e linhas do Streamlit */
        [data-testid="stHorizontalBlock"] {
            gap: 80px !important; /* Distância horizontal entre botões */
        }
        .stButton {
            margin-bottom: 60px !important; /* Distância vertical entre botões */
        }
        </style>
    """, unsafe_allow_html=True)

    # Organização em 3 colunas para visual compacto
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Logistica Patio / ETC"):
            st.session_state['modulo'] = "logistica"
        if st.button("Tombador"):
            st.session_state['modulo'] = "tombador"
            
    with col2:
        if st.button("Classificação"):
            st.session_state['modulo'] = "classificacao"
        if st.button("Tabela Ent/Said"):
            st.session_state['modulo'] = "tabela"
            
    with col3:
        if st.button("Balança"):
            st.session_state['modulo'] = "balanca"
        if st.button("Dashboard"):
            st.session_state['modulo'] = "dashboard"

    # --- BOTÃO VOLTAR CENTRALIZADO ---
    st.write("") 
    _, col_v, _ = st.columns([2, 1, 2])
    with col_v:
        st.markdown('<div class="btn-voltar-estilo">', unsafe_allow_html=True)
        if st.button("VOLTAR PARA LOGIN"):
            st.session_state['pagina'] = 'inicio'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
