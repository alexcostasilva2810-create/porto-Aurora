import streamlit as st
import base64
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ==============================================================================
# BLOCO 1: CONFIGURAÇÕES E CONEXÃO
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
            font-size: 28px;
            font-weight: 900;
            text-shadow: 2px 2px 2px #000;
            margin-bottom: 20px;
        }}
        .stTextInput input, .stSelectbox select, .stDateInput input {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 10px !important;
            height: 45px !important;
        }}
        div.stButton > button {{
            background-color: #FF8C00;
            color: white;
            border-radius: 12px;
            width: 100%;
            height: 55px;
            font-size: 16px;
            font-weight: bold;
            box-shadow: 0px 5px 0px #B26200;
            margin-top: 15px;
            border: none;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BLOCO 3: TELA DE LOGIN
# ==============================================================================
if st.session_state['pagina'] == 'inicio':
    aplicar_visual_celular("#2D2D2D") 
    st.markdown('<div class="texto-branco"><h1 style="font-size: 35px;">Seja Bem Vindo</h1><p style="font-size: 20px;">ao</p><h1 style="font-size: 35px;">Zion Tecnologia</h1><br><br><h2 style="font-size: 28px; color: #FFD700 !important;">Transdourado</h2></div>', unsafe_allow_html=True)
    for _ in range(8): st.write("")
    if st.button("ACESSO"):
        st.session_state['pagina'] = 'menu'
        st.rerun()

# ==============================================================================
# BLOCO 4: TELA DE MENU
# ==============================================================================
elif st.session_state['pagina'] == 'menu':
    aplicar_visual_celular("#002366") 
    st.markdown('<h1 class="titulo-amarelo">MENU</h1>', unsafe_allow_html=True)
    if st.button("Logistica Patio / ETC"):
        st.session_state['pagina'] = 'logistica'
        st.rerun()
    if st.button("Classificação"): pass
    if st.button("Balança"): pass
    if st.button("Tombador"): pass
    if st.button("Tabela Ent/Said"): pass
    if st.button("Dashboard"): pass
    st.write("")
    if st.button("SAIR DO SISTEMA"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()

# ==============================================================================
# BLOCO 5: TELA LOGÍSTICA PÁTIO / ETC (CORREÇÃO DE COLUNAS E CÁLCULO)
# ==============================================================================
elif st.session_state['pagina'] == 'logistica':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LOGÍSTICA PÁTIO</h1>', unsafe_allow_html=True)
    
    with st.form("form_logistica", clear_on_submit=True):
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">PLACA</p>', unsafe_allow_html=True)
        placa = st.text_input("placa_input", placeholder="JVV-7606", label_visibility="collapsed")
        
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">TIPO DE CAMINHÃO</p>', unsafe_allow_html=True)
        tipo_camiao = st.selectbox("tipo_input", ["Bitrem", "Rodotrem", "Vanderleia", "Truck", "Carreta"], label_visibility="collapsed")
        
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">DATA</p>', unsafe_allow_html=True)
        data_input = st.date_input("data_input", datetime.now(), format="DD/MM/YYYY", label_visibility="collapsed")
        
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">SAÍDA DO PÁTIO (HH:MM:SS)</p>', unsafe_allow_html=True)
        saida_patio = st.text_input("saida_input", value="08:10:00", key="saida_key", label_visibility="collapsed")
        
        st.markdown('<p style="color:white; font-weight:bold; margin-bottom:-5px;">CHEGADA ETC (HH:MM:SS)</p>', unsafe_allow_html=True)
        chegada_etc = st.text_input("chegada_input", value="10:00:00", key="chegada_key", label_visibility="collapsed")

        btn_salvar = st.form_submit_button("SALVAR REGISTRO")

        if btn_salvar:
            try:
                # 1. Ajuste da Data para padrão BR
                data_br = data_input.strftime("%d/%m/%Y")
                
                # 2. Cálculo do TT. VIAGEM
                fmt = '%H:%M:%S'
                t_saida = datetime.strptime(saida_patio, fmt)
                t_chegada = datetime.strptime(chegada_etc, fmt)
                delta = t_chegada - t_saida
                tt_viagem = str(delta)

                planilha = conectar_planilha()
                if planilha:
                    aba = planilha.worksheet("Tempo")
                    
                    # 3. Ordem correta das colunas conforme sua planilha
                    # PLACA | CAMINHÃO | DATA | SAÍDA DO PATIO | CHEGADA ETC | TT. VIAGEM
                    nova_linha = [placa, tipo_camiao, data_br, saida_patio, chegada_etc, tt_viagem]
                    
                    aba.append_row(nova_linha)
                    st.success(f"Salvo! Viagem de {tt_viagem}")
                else:
                    st.error("Erro na planilha!")
            except Exception as e:
                st.error(f"Erro nos dados: Verifique se o horário está como 00:00:00")

    if st.button("VOLTAR AO MENU"):
        st.session_state['pagina'] = 'menu'
        st.rerun()
