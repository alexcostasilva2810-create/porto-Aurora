import streamlit as st
import base64
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime

# ==============================================================================
# BLOCO 1: CONEXÃO COM A PLANILHA ZION (NOME EXATO DO ARQUIVO)
# ==============================================================================
st.set_page_config(page_title="Zion Tecnologia", layout="centered")

def conectar_planilha():
    try:
        b64_content = st.secrets["gcp_service_account"]["content"]
        json_info = json.loads(base64.b64decode(b64_content).decode('utf-8'))
        json_info["private_key"] = json_info["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(json_info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        client = gspread.authorize(creds)
        # Abre a planilha "Zion"
        planilha = client.open("Zion")
        # Pega a primeira aba disponível (geralmente a 'Tempo')
        return planilha.get_worksheet(0)
    except:
        return None

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

# ==============================================================================
# BLOCO 2: VISUAL MOBILE
# ==============================================================================
def aplicar_visual_celular(cor_fundo_interna):
    st.markdown(f"""
        <style>
        .stApp {{ background-color: #121212; }}
        .main .block-container {{
            max-width: 380px;
            background-color: {cor_fundo_interna};
            border: 10px solid #444;
            border-radius: 40px;
            padding: 25px 15px;
            margin-top: 10px;
        }}
        .titulo-amarelo {{ color: #FFFF00 !important; text-align: center; font-size: 26px; font-weight: 900; }}
        div.stButton > button {{ background-color: #FF8C00; color: white; border-radius: 12px; width: 100%; height: 50px; font-weight: bold; border: none; }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# BLOCO 3: TELAS E LANÇAMENTOS
# ==============================================================================
if st.session_state['pagina'] == 'inicio':
    aplicar_visual_celular("#2D2D2D") 
    st.markdown('<div style="color:white; text-align:center;"><h1>Zion Tecnologia</h1><br><h2 style="color:#FFD700;">Transdourado</h2></div>', unsafe_allow_html=True)
    for _ in range(8): st.write("")
    if st.button("ACESSO"): st.session_state['pagina'] = 'menu'; st.rerun()

elif st.session_state['pagina'] == 'menu':
    aplicar_visual_celular("#002366") 
    st.markdown('<h1 class="titulo-amarelo">MENU</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Logistica Patio"): st.session_state['pagina'] = 'logistica'; st.rerun()
        if st.button("Tombador"): pass
    with c2:
        if st.button("Classificação"): pass
        if st.button("Balança"): pass
    st.write("---")
    if st.button("VISUALIZAR LANÇAMENTOS"): st.session_state['pagina'] = 'visualizar'; st.rerun()

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
                t_saida = datetime.strptime(saida, '%H:%M:%S')
                t_chegada = datetime.strptime(chegada, '%H:%M:%S')
                tt_viagem = str(t_chegada - t_saida)
                data_br = data_sel.strftime("%d/%m/%Y")
                aba = conectar_planilha()
                if aba:
                    aba.append_row([placa, tipo, data_br, saida, chegada, tt_viagem])
                    st.success("Salvo!")
                else: st.error("Erro na conexão!")
            except: st.error("Use o formato 00:00:00")
    if st.button("VOLTAR"): st.session_state['pagina'] = 'menu'; st.rerun()

# ==============================================================================
# BLOCO 4: VISUALIZAÇÃO BLINDADA (RESOLVE O ERRO DE CARREGAMENTO)
# ==============================================================================
elif st.session_state['pagina'] == 'visualizar':
    aplicar_visual_celular("#002366")
    st.markdown('<h1 class="titulo-amarelo">LANÇAMENTOS</h1>', unsafe_allow_html=True)
    
    aba = conectar_planilha()
    if aba:
        try:
            # Pega todos os valores como strings para evitar erro de conversão
            dados = aba.get_all_values()
            if len(dados) > 1:
                # Cria a tabela usando a primeira linha como título
                df = pd.DataFrame(dados[1:], columns=dados[0])
                # Limpa linhas que não tem placa
                df = df[df.iloc[:, 0].str.strip() != ""] 
                
                st.write("Registros encontrados:")
                st.table(df) # Usar st.table é mais seguro contra erros de layout que o st.dataframe
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("BAIXAR CSV", csv, "Zion.csv", "text/csv")
            else:
                st.info("Planilha vazia.")
        except:
            st.error("Erro crítico ao ler a planilha. Verifique se o cabeçalho existe.")
    else:
        st.error("Planilha 'Zion' não encontrada!")
    
    if st.button("VOLTAR"): st.session_state['pagina'] = 'menu'; st.rerun()
