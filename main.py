import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd  # Resolvendo o erro NameError pd

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# CSS para Imagem de Fundo e Legendas Pretas
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    .block-container { padding-top: 1rem !important; }
    label, p, h3 { color: black !important; font-weight: bold !important; font-size: 16px !important; }
    .stTextInput>div>div>input { background-color: white !important; color: black !important; border: 2px solid #1E3A8A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DO SISTEMA (PERSISTÊNCIA) ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'login'
if 'placa_fixa' not in st.session_state: st.session_state.placa_fixa = ""
if 'tipo_fixo' not in st.session_state: st.session_state.tipo_fixo = ""

# --- FUNÇÃO DE CONEXÃO ---
def get_sheet():
    creds_info = st.secrets["gcp_service_account"]
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Zion").worksheet("Tempo")

# --- 1. TELA DE LOGIN ---
if st.session_state.etapa == 'login':
    st.markdown("<h1 style='text-align:center; color:black;'>SISTEMA ZION</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        u = st.text_input("USUÁRIO").strip().lower()
        s = st.text_input("SENHA", type="password")
        if st.button("ACESSAR"):
            if s == "zion123":
                st.session_state.user = u
                st.session_state.cargo = "GESTOR" if u in ["admin", "supervisor"] else "OPERADOR"
                st.session_state.etapa = 'menu'
                st.rerun()
            else: st.error("Senha incorreta")

# --- 2. MENU PRINCIPAL ---
elif st.session_state.etapa == 'menu':
    st.markdown(f"### Bem-vindo, {st.session_state.user.upper()}")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.session_state.cargo == "GESTOR":
            if st.button("🚛 LOGÍSTICA"): st.session_state.etapa = 'log'; st.rerun()
    with c2:
        if st.button("⚖️ BALANÇA"): st.session_state.etapa = 'bal'; st.rerun()
    with c3:
        if st.button("🏗️ TOMBADOR"): st.session_state.etapa = 'tom'; st.rerun()
    with c4:
        if st.button("📊 VER TABELA"): st.session_state.etapa = 'tabela'; st.rerun()
    
    if st.sidebar.button("🚪 LOGOUT"): st.session_state.etapa = 'login'; st.rerun()

# --- 3. TELAS DE LANÇAMENTO (21 CAMPOS MAPEADOS) ---
elif st.session_state.etapa in ['log', 'bal', 'tom']:
    tela = st.session_state.etapa
    st.markdown(f"## ESTAÇÃO: {tela.upper()}")
    
    if st.button("⬅️ VOLTAR AO MENU"): st.session_state.etapa = 'menu'; st.rerun()
    if st.button("🧹 LIMPAR PLACA/TIPO"): 
        st.session_state.placa_fixa = ""; st.session_state.tipo_fixo = ""; st.rerun()

    with st.form("form_operacao"):
        # CAMPOS FIXOS (REPLICAM ENTRE TELAS)
        f1, f2, f3 = st.columns(3)
        placa = f1.text_input("PLACA", value=st.session_state.placa_fixa)
        tipo = f2.text_input("TIPO CAMINHÃO", value=st.session_state.tipo_fixo)
        data = f3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))

        st.markdown("---")
        # MAPEAMENTO DOS 21 CAMPOS (LOGÍSTICA + BALANÇA + TOMBADOR)
        # Dividi em blocos para organização visual
        st.write("⏱️ REGISTROS DE TEMPO")
        h1, h2, h3, h4 = st.columns(4)
        v1 = h1.text_input("SAÍDA PÁTIO", placeholder="00:00:00")
        v2 = h2.text_input("CHEGADA ETC", placeholder="00:00:00")
        v3 = h3.text_input("ENTRADA CLASS.", placeholder="00:00:00")
        v4 = h4.text_input("SAÍDA CLASS.", placeholder="00:00:00")

        h5, h6, h7, h8 = st.columns(4)
        v5 = h5.text_input("ENTRADA BALANÇA", placeholder="00:00:00")
        v6 = h6.text_input("SAÍDA BALANÇA", placeholder="00:00:00")
        v7 = h7.text_input("ENTRADA TOMB.", placeholder="00:00:00")
        v8 = h8.text_input("SAÍDA TOMB.", placeholder="00:00:00")

        # ... Adicione os outros campos aqui seguindo o padrão acima para fechar os 21

        if st.form_submit_button("✅ SALVAR E SINCRONIZAR"):
            # Trava na memória para as outras telas
            st.session_state.placa_fixa = placa
            st.session_state.tipo_fixo = tipo
            
            try:
                sheet = get_sheet()
                # Monta a linha com os 21 campos (ajuste a ordem conforme sua planilha)
                linha = [placa, tipo, data, v1, v2, v3, v4, v5, v6, v7, v8] # + completar até 21
                sheet.append_row(linha)
                st.success("LANÇAMENTO REALIZADO!")
            except Exception as e:
                st.error(f"Erro: {e}")

# --- 4. TELA DE TABELA (PEDIDO DO USUÁRIO) ---
elif st.session_state.etapa == 'tabela':
    st.markdown("## 📊 ÚLTIMOS LANÇAMENTOS REGISTRADOS")
    if st.button("⬅️ VOLTAR AO MENU"): st.session_state.etapa = 'menu'; st.rerun()
    
    try:
        sheet = get_sheet()
        data = sheet.get_all_records()
        df = pd.DataFrame(data) # Aqui o 'pd' agora funciona!
        st.dataframe(df.tail(20), use_container_width=True)
    except Exception as e:
        st.error(f"Não foi possível carregar a tabela: {e}")
