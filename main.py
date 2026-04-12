import streamlit as st
import base64
import json
import gspread
import pandas as pd
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
# BLOCO 2: ENGINE DE ESTILO (MÁSCARA MOBILE)
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
        }}
        div.stButton > button {{
            background-color: #FF8C00;
            color: white;
            border-radius: 12px;
            width: 100%;
            height: 50px;
            font-weight: bold;
            box-shadow: 0px 4px 0px #B26200;
            margin-top: 10px;
            border: none;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BLOCO 3: TELA DE LOGIN
# ==============================================================================
if st.session_state['pagina'] == 'inicio':
    aplicar_visual_celular("#2D2D2D") 
    st.markdown('<div class="texto-branco"><h1 style="font-size: 35px;">Seja Bem Vindo</h1><br><h1 style="font-size: 35px;">Zion Tecnologia</h1><br><h2 style="font-size: 28px; color: #FFD700 !important;">Transdourado</h2></div>', unsafe_allow_html=True)
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
    if st.button("Visualizar Lançamentos"):
        st.session_state['pagina'] = 'visualizar'
        st.rerun()
    if st.button("SAIR DO SISTEMA"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()

# ==============================================================================
# BLOCO 5: TELA LOGÍSTICA PÁTIO (SALVAMENTO E LIMPEZA)
# ==============================================================================
elif st.session_state['pagina'] == 'logistica':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LOGÍSTICA PÁTIO</h1>', unsafe_allow_html=True)
    
    # clear_on_submit=True garante que os campos limpem ao salvar
    with st.form("form_logistica", clear_on_submit=True):
        placa = st.text_input("PLACA", placeholder="JVV-7606")
        tipo_camiao = st.selectbox("TIPO DE CAMINHÃO", ["Bitrem", "Rodotrem", "Vanderleia", "Truck", "Carreta"])
        data_input = st.date_input("DATA", datetime.now(), format="DD/MM/YYYY")
        saida_patio = st.text_input("SAÍDA DO PÁTIO (HH:MM:SS)", value="08:00:00")
        chegada_etc = st.text_input("CHEGADA ETC (HH:MM:SS)", value="10:00:00")

        btn_salvar = st.form_submit_button("SALVAR REGISTRO")

        if btn_salvar:
            try:
                data_br = data_input.strftime("%d/%m/%Y") # Formato 12/04/2026
                fmt = '%H:%M:%S'
                delta = datetime.strptime(chegada_etc, fmt) - datetime.strptime(saida_patio, fmt)
                tt_viagem = str(delta)

                planilha = conectar_planilha()
                if planilha:
                    aba = planilha.worksheet("Tempo")
                    # Ordem: PLACA | CAMINHÃO | DATA | SAÍDA | CHEGADA | TT. VIAGEM
                    aba.append_row([placa, tipo_camiao, data_br, saida_patio, chegada_etc, tt_viagem])
                    st.success(f"Salvo! Viagem: {tt_viagem}")
                else:
                    st.error("Erro na planilha!")
            except:
                st.error("Verifique os horários!")

    if st.button("VOLTAR AO MENU"):
        st.session_state['pagina'] = 'menu'
        st.rerun()

# ==============================================================================
# BLOCO 6: VISUALIZAR E EXPORTAR
# ==============================================================================
elif st.session_state['pagina'] == 'visualizar':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LANÇAMENTOS</h1>', unsafe_allow_html=True)
    
    planilha = conectar_planilha()
    if planilha:
        aba = planilha.worksheet("Tempo")
        dados = aba.get_all_records()
        df = pd.DataFrame(dados)
        
        if not df.empty:
            # Mostra a tabela dentro da máscara
            st.dataframe(df, height=300)
            
            # Exportação para CSV (Excel lê direto)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="EXPORTAR PARA PLANILHA (CSV)",
                data=csv,
                file_name=f'zion_logistica_{datetime.now().strftime("%d_%m_%Y")}.csv',
                mime='text/csv',
            )
        else:
            st.warning("Nenhum dado encontrado.")

    if st.button("VOLTAR AO MENU"):
        st.session_state['pagina'] = 'menu'
        st.rerun()
