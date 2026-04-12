import streamlit as st
import base64
import json
import gspread
from google.oauth2.service_account import Credentials

# ==============================================================================
# BLOCO 1: CONFIGURAÇÕES, CONEXÃO E NAVEGAÇÃO
# ==============================================================================
st.set_page_config(page_title="Zion Tecnologia", layout="centered")

def conectar_planilha():
    try:
        b64_content = st.secrets["gcp_service_account"]["content"]
        json_info = json.loads(base64.b64decode(b64_content).decode('utf-8'))
        json_info["private_key"] = json_info["private_key"].replace("\\n", "\n")
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(json_info, scopes=scopes)
        return gspread.authorize(creds).open("Zion")
    except:
        return None

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

# ==============================================================================
# BLOCO 2: ENGINE DE ESTILO (MÁSCARA MOBILE E NITIDEZ)
# ==============================================================================
def aplicar_visual_celular(cor_fundo_interna):
    st.markdown(f"""
        <style>
        .stApp {{ background-color: #121212; }}
        
        .main .block-container {{
            max-width: 380px;
            min-height: 800px;
            background-color: {cor_fundo_interna};
            border: 10px solid #444;
            border-radius: 40px;
            padding: 40px 20px;
            margin-top: 10px;
            box-shadow: 0px 0px 25px rgba(0,0,0,0.9);
        }}

        .texto-branco {{
            color: #FFFFFF !important;
            text-align: center;
            font-family: 'Arial', sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,1);
            font-weight: bold;
        }}

        .titulo-amarelo {{
            color: #FFFF00 !important;
            text-align: center;
            font-size: 40px;
            font-weight: 900;
            text-shadow: 2px 2px 2px #000;
        }}

        div.stButton > button {{
            background-color: #FF8C00;
            color: white;
            border-radius: 12px;
            width: 100%;
            height: 60px;
            font-size: 18px;
            box-shadow: 0px 5px 0px #B26200;
            margin-bottom: 25px;
            border: none;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BLOCO 3: TELA DE LOGIN / INÍCIO (VISUAL MOBILE)
# ==============================================================================
if st.session_state['pagina'] == 'inicio':
    aplicar_visual_celular("#333333") 
    
    st.markdown('<div class="texto-branco">', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 35px;">Seja Bem Vindo</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 20px;">ao</p>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 35px;">Zion Tecnologia</h1>', unsafe_allow_html=True)
    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size: 26px; color: #FFD700 !important;">Transdourado</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    for _ in range(8): st.write("")
    
    if st.button("ACESSO"):
        st.session_state['pagina'] = 'menu'
        st.rerun()

# ==============================================================================
# BLOCO 4: TELA DE MENU PRINCIPAL (VISUAL MOBILE)
# ==============================================================================
elif st.session_state['pagina'] == 'menu':
    aplicar_visual_celular("#002366") 
    
    st.markdown('<h1 class="titulo-amarelo">MENU</h1>', unsafe_allow_html=True)
    
    if st.button("Logistica Patio / ETC"): pass
    if st.button("Classificação"): pass
    if st.button("Balança"): pass
    if st.button("Tombador"): pass
    if st.button("Tabela Ent/Said"): pass
    if st.button("Dashboard"): pass

    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("VOLTAR PARA LOGIN"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()
