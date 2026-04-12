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
# BLOCO 2: ENGINE DE ESTILO (MÁSCARA MOBILE E BOTÕES)
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
        div.stButton > button {{
            background-color: #FF8C00;
            color: white;
            border-radius: 12px;
            width: 100%;
            height: 50px;
            font-weight: bold;
            box-shadow: 0px 4px 0px #B26200;
            margin-bottom: 10px;
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
# BLOCO 4: MENU PRINCIPAL (TODOS OS BOTÕES RECUPERADOS)
# ==============================================================================
elif st.session_state['pagina'] == 'menu':
    aplicar_visual_celular("#002366") 
    st.markdown('<h1 class="titulo-amarelo">MENU</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Logistica Patio / ETC"):
            st.session_state['pagina'] = 'logistica'
            st.rerun()
        if st.button("Tombador"): pass
        if st.button("Balança"): pass
    with col2:
        if st.button("Classificação"): pass
        if st.button("Tabela Ent/Said"): pass
        if st.button("Dashboard"): pass
    
    st.markdown("---")
    if st.button("Visualizar Lançamentos"):
        st.session_state['pagina'] = 'visualizar'
        st.rerun()
    
    if st.button("SAIR DO SISTEMA"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()

# ==============================================================================
# BLOCO 5: TELA LOGÍSTICA PÁTIO (SALVAR E LIMPAR)
# ==============================================================================
elif st.session_state['pagina'] == 'logistica':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LOGÍSTICA PÁTIO</h1>', unsafe_allow_html=True)
    
    with st.form("form_logistica", clear_on_submit=True):
        placa = st.text_input("PLACA", placeholder="JVV-7606")
        tipo = st.selectbox("TIPO", ["Bitrem", "Rodotrem", "Vanderleia", "Truck", "Carreta"])
        data_f = st.date_input("DATA", datetime.now(), format="DD/MM/YYYY")
        saida = st.text_input("SAÍDA (HH:MM:SS)", value="00:00:00")
        chegada = st.text_input("CHEGADA (HH:MM:SS)", value="00:00:00")

        if st.form_submit_button("SALVAR REGISTRO"):
            try:
                # Cálculo TT. VIAGEM
                fmt = '%H:%M:%S'
                t_viagem = str(datetime.strptime(chegada, fmt) - datetime.strptime(saida, fmt))
                data_br = data_f.strftime("%d/%m/%Y")
                
                planilha = conectar_planilha()
                if planilha:
                    aba = planilha.worksheet("Tempo")
                    # Ordem: PLACA | CAMINHÃO | DATA | SAÍDA | CHEGADA | TT. VIAGEM
                    aba.append_row([placa, tipo, data_br, saida, chegada, t_viagem])
                    st.success("Salvo com sucesso!")
                else: st.error("Erro na conexão!")
            except: st.error("Erro nos dados!")

    if st.button("VOLTAR"):
        st.session_state['pagina'] = 'menu'
        st.rerun()

# ==============================================================================
# BLOCO 6: VISUALIZAR E EXPORTAR (CORRIGIDO)
# ==============================================================================
elif st.session_state['pagina'] == 'visualizar':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LANÇAMENTOS</h1>', unsafe_allow_html=True)
    
    planilha = conectar_planilha()
    if planilha:
        try:
            aba = planilha.worksheet("Tempo")
            # Usando get_all_values para evitar erro de cabeçalho
            lista_dados = aba.get_all_values()
            if len(lista_dados) > 1:
                df = pd.DataFrame(lista_dados[1:], columns=lista_dados[0])
                st.dataframe(df, height=300)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("EXPORTAR PARA EXCEL (CSV)", csv, "relatorio.csv", "text/csv")
            else: st.warning("Planilha Vazia")
        except: st.error("Erro ao ler aba 'Tempo'")

    if st.button("VOLTAR"):
        st.session_state['pagina'] = 'menu'
        st.rerun()
