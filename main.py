import streamlit as st
import base64
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ==============================================================================
# BLOCO 1: CONFIGURAÇÕES, CONEXÃO E NAVEGAÇÃO
# ==============================================================================
st.set_page_config(page_title="Zion Tecnologia", layout="centered")

def conectar_planilha():
    try:
        # Puxa as credenciais do Secrets do Streamlit
        b64_content = st.secrets["gcp_service_account"]["content"]
        json_info = json.loads(base64.b64decode(b64_content).decode('utf-8'))
        json_info["private_key"] = json_info["private_key"].replace("\\n", "\n")
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(json_info, scopes=scopes)
        return gspread.authorize(creds).open("Zion")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

# Inicializador de página
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
            min-height: 850px;
            background-color: {cor_fundo_interna};
            border: 12px solid #333;
            border-radius: 45px;
            padding: 30px 20px;
            margin-top: 10px;
            box-shadow: 0px 0px 30px rgba(0,0,0,0.9);
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
            font-size: 32px;
            font-weight: 900;
            text-shadow: 2px 2px 2px #000;
            margin-bottom: 25px;
        }}

        /* Estilo dos campos de entrada */
        .stTextInput input, .stSelectbox select, .stDateInput input {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 10px !important;
            height: 45px !important;
        }}

        /* Botões Laranja 3D */
        div.stButton > button {{
            background-color: #FF8C00;
            color: white;
            border-radius: 12px;
            width: 100%;
            height: 58px;
            font-size: 17px;
            font-weight: bold;
            box-shadow: 0px 5px 0px #B26200;
            margin-bottom: 15px;
            border: none;
        }}
        div.stButton > button:active {{
            box-shadow: 0px 2px 0px #B26200;
            transform: translateY(3px);
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BLOCO 3: TELA DE LOGIN / INÍCIO
# ==============================================================================
if st.session_state['pagina'] == 'inicio':
    aplicar_visual_celular("#333333") 
    st.markdown('<div class="texto-branco">', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 35px;">Seja Bem Vindo</h1><p style="font-size: 20px;">ao</p><h1 style="font-size: 35px;">Zion Tecnologia</h1><br><br><h2 style="font-size: 26px; color: #FFD700 !important;">Transdourado</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    for _ in range(8): st.write("")
    if st.button("ACESSO"):
        st.session_state['pagina'] = 'menu'
        st.rerun()

# ==============================================================================
# BLOCO 4: TELA DE MENU PRINCIPAL (COM DIRECIONAMENTO)
# ==============================================================================
elif st.session_state['pagina'] == 'menu':
    aplicar_visual_celular("#002366") 
    st.markdown('<h1 class="titulo-amarelo">MENU</h1>', unsafe_allow_html=True)
    
    # O clique aqui "arremessa" para a Logística
    if st.button("Logistica Patio / ETC"):
        st.session_state['pagina'] = 'logistica'
        st.rerun()

    if st.button("Classificação"): pass
    if st.button("Balança"): pass
    if st.button("Tombador"): pass
    if st.button("Tabela Ent/Said"): pass
    if st.button("Dashboard"): pass

    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("SAIR DO SISTEMA"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()

# ==============================================================================
# BLOCO 5: TELA LOGÍSTICA PÁTIO / ETC
# ==============================================================================
elif st.session_state['pagina'] == 'logistica':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LOGÍSTICA PÁTIO</h1>', unsafe_allow_html=True)
    
    # Formulário para manter os dados na tela até clicar em salvar
    with st.form("form_logistica", clear_on_submit=True):
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">PLACA</p>', unsafe_allow_html=True)
        placa = st.text_input("", placeholder="Placa do Veículo", label_visibility="collapsed")
        
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">TIPO DE CAMINHÃO</p>', unsafe_allow_html=True)
        tipo_camiao = st.selectbox("", ["Bitrem", "Rodotrem", "Vanderleia", "Truck", "Carreta"], label_visibility="collapsed")
        
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">DATA</p>', unsafe_allow_html=True)
        # Configuração de data em PT-BR automática pelo navegador + format
        data_registro = st.date_input("", datetime.now(), format="DD/MM/YYYY", label_visibility="collapsed")
        
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">SAÍDA DO PÁTIO (00:00:00)</p>', unsafe_allow_html=True)
        saida_patio = st.text_input("", value="00:00:00", label_visibility="collapsed")
        
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">CHEGADA ETC (00:00:00)</p>', unsafe_allow_html=True)
        chegada_etc = st.text_input("", value="00:00:00", label_visibility="collapsed")

        st.write("")
        btn_salvar = st.form_submit_button("SALVAR REGISTRO")

        if btn_salvar:
            planilha = conectar_planilha()
            if planilha:
                try:
                    aba = planilha.worksheet("Tempo")
                    aba.append_row([str(data_registro), placa, tipo_camiao, saida_patio, chegada_etc])
                    st.success("Dados enviados para a Planilha Zion!")
                except:
                    st.error("Aba 'Tempo' não encontrada!")
            else:
                st.error("Erro na conexão!")

    if st.button("VOLTAR AO MENU"):
        st.session_state['pagina'] = 'menu'
        st.rerun()
