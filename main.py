import streamlit as st
import base64
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime

# ==============================================================================
# BLOCO 1: CONEXÃO AUTOMÁTICA (PEGA A PRIMEIRA ABA DISPONÍVEL)
# ==============================================================================
st.set_page_config(page_title="Zion Tecnologia", layout="centered")

def conectar_planilha():
    try:
        b64_content = st.secrets["gcp_service_account"]["content"]
        json_info = json.loads(base64.b64decode(base64_content).decode('utf-8'))
        json_info["private_key"] = json_info["private_key"].replace("\\n", "\n")
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(json_info, scopes=scopes)
        client = gspread.authorize(creds)
        planilha = client.open("Zion")
        # FIX: Pega a primeira aba independente do nome para evitar WorksheetNotFound
        return planilha.get_worksheet(0) 
    except Exception as e:
        return None

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

# ==============================================================================
# BLOCO 2: ENGINE DE ESTILO MOBILE
# ==============================================================================
def aplicar_visual_celular(cor_fundo_interna):
    st.markdown(f"""
        <style>
        .stApp {{ background-color: #121212; }}
        .main .block-container {{
            max-width: 380px;
            min-height: 850px;
            background-color: {cor_fundo_interna};
            border: 10px solid #444;
            border-radius: 40px;
            padding: 25px 15px;
            margin-top: 10px;
            box-shadow: 0px 0px 25px rgba(0,0,0,0.9);
        }}
        .titulo-amarelo {{
            color: #FFFF00 !important;
            text-align: center;
            font-size: 26px;
            font-weight: 900;
            margin-bottom: 20px;
        }}
        div.stButton > button {{
            background-color: #FF8C00;
            color: white;
            border-radius: 12px;
            width: 100%;
            height: 50px;
            font-weight: bold;
            box-shadow: 0px 4px 0px #B26200;
            margin-bottom: 8px;
            border: none;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BLOCO 3: TELAS (LOGIN E MENU)
# ==============================================================================
if st.session_state['pagina'] == 'inicio':
    aplicar_visual_celular("#2D2D2D") 
    st.markdown('<div style="color:white; text-align:center;"><h1>Zion Tecnologia</h1><br><h2 style="color:#FFD700;">Transdourado</h2></div>', unsafe_allow_html=True)
    for _ in range(10): st.write("")
    if st.button("ACESSO"):
        st.session_state['pagina'] = 'menu'
        st.rerun()

elif st.session_state['pagina'] == 'menu':
    aplicar_visual_celular("#002366") 
    st.markdown('<h1 class="titulo-amarelo">MENU</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Logistica Patio / ETC"): st.session_state['pagina'] = 'logistica'; st.rerun()
        if st.button("Tombador"): pass
        if st.button("Balança"): pass
    with c2:
        if st.button("Classificação"): pass
        if st.button("Tabela Ent/Said"): pass
        if st.button("Dashboard"): pass
    st.write("---")
    if st.button("VISUALIZAR LANÇAMENTOS"): st.session_state['pagina'] = 'visualizar'; st.rerun()
    if st.button("SAIR"): st.session_state['pagina'] = 'inicio'; st.rerun()

# ==============================================================================
# BLOCO 4: LOGÍSTICA (SALVA NA PRIMEIRA ABA)
# ==============================================================================
elif st.session_state['pagina'] == 'logistica':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LOGÍSTICA PÁTIO</h1>', unsafe_allow_html=True)
    
    with st.form("logistica_form", clear_on_submit=True):
        placa = st.text_input("PLACA")
        tipo = st.selectbox("TIPO", ["Bitrem", "Rodotrem", "Vanderleia", "Truck", "Carreta"])
        data_sel = st.date_input("DATA", datetime.now(), format="DD/MM/YYYY")
        saida = st.text_input("SAÍDA PÁTIO", value="00:00:00")
        chegada = st.text_input("CHEGADA ETC", value="00:00:00")
        
        if st.form_submit_button("SALVAR REGISTRO"):
            try:
                fmt = '%H:%M:%S'
                tt_viagem = str(datetime.strptime(chegada, fmt) - datetime.strptime(saida, fmt))
                data_br = data_sel.strftime("%d/%m/%Y")
                
                aba = conectar_planilha()
                if aba:
                    aba.append_row([placa, tipo, data_br, saida, chegada, tt_viagem])
                    st.success("Salvo com sucesso!")
                else: st.error("Erro: Verifique se compartilhou a planilha com o e-mail do JSON.")
            except: st.error("Use o formato 00:00:00")

    if st.button("VOLTAR"): st.session_state['pagina'] = 'menu'; st.rerun()

# ==============================================================================
# BLOCO 5: VISUALIZAR (BUSCA AUTOMÁTICA)
# ==============================================================================
elif st.session_state['pagina'] == 'visualizar':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LANÇAMENTOS</h1>', unsafe_allow_html=True)
    
    aba = conectar_planilha()
    if aba:
        try:
            dados = aba.get_all_values()
            if len(dados) > 0:
                df = pd.DataFrame(dados[1:], columns=dados[0])
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("BAIXAR PLANILHA", csv, " Zion.csv", "text/csv")
            else: st.info("Planilha vazia.")
        except: st.error("Erro ao converter dados.")
    else: st.error("Planilha não encontrada!")

    if st.button("VOLTAR"): st.session_state['pagina'] = 'menu'; st.rerun()
