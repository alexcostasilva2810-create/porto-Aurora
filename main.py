import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA (ESTILO COMPACTO)
st.set_page_config(page_title="Zion Operacional", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS PARA VISUAL COMPACTO E FUNDO
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    /* Reduzir espaços e fontes para modo COMPACTO */
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    h1, h2, h3 { margin-bottom: 0.5rem !important; padding-top: 0rem !important; color: black !important; font-size: 1.2rem !important; }
    label { color: black !important; font-weight: bold !important; font-size: 0.85rem !important; margin-bottom: 0px !important; }
    .stTextInput { margin-bottom: -10px !important; }
    div[data-testid="stForm"] { border: 1px solid #ccc; padding: 10px; border-radius: 10px; background: rgba(255,255,255,0.8); }
    </style>
    """, unsafe_allow_html=True)

# 3. INICIALIZAÇÃO DE VARIÁVEIS DE ESTADO
for key in ['logado', 'perfil', 'placa', 'tipo']:
    if key not in st.session_state:
        st.session_state[key] = False if key == 'logado' else ""

# 4. FUNÇÃO DE CONEXÃO REFORÇADA
def conectar_google():
    try:
        if "gcp_service_account" not in st.secrets:
            st.error("⚠️ Erro: Credenciais (Secrets) não encontradas no Streamlit Cloud.")
            return None
        
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # Abre a planilha 'Zion' na aba 'Tempo'
        return client.open("Zion").worksheet("Tempo")
    except Exception as e:
        st.error(f"❌ Falha na conexão com Google Sheets: {e}")
        return None

# --- FLUXO DO SISTEMA ---

# TELA DE LOGIN
if not st.session_state.logado:
    st.markdown("<h1 style='text-align:center;'>ZION - LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        _, col, _ = st.columns([1,1,1])
        u = col.text_input("USUÁRIO").strip().lower()
        s = col.text_input("SENHA", type="password")
        if col.button("ENTRAR"):
            if s == "zion123":
                st.session_state.logado = True
                st.session_state.perfil = "GESTOR" if u in ['admin', 'supervisor'] else "OPERADOR"
                st.rerun()
            else: st.error("Senha inválida")

# INTERFACE PRINCIPAL
else:
    st.sidebar.subheader(f"Usuário: {st.session_state.perfil}")
    if st.sidebar.button("SAIR"):
        st.session_state.logado = False
        st.rerun()

    tab1, tab2 = st.tabs(["📝 LANÇAMENTOS", "📊 TABELA DE CONFERÊNCIA"])

    with tab1:
        # FORMULÁRIO COMPACTO
        with st.form("form_operacao", clear_on_submit=False):
            c1, c2, c3 = st.columns(3)
            placa = c1.text_input("PLACA", value=st.session_state.placa)
            tipo = c2.text_input("TIPO CAMINHÃO", value=st.session_state.tipo)
            data = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))

            st.markdown("---")
            
            # Blocos de Horários (Organizados para caber tudo)
            st.write("⏱️ **HORÁRIOS DE OPERAÇÃO**")
            h1, h2, h3, h4 = st.columns(4)
            v1 = h1.text_input("SAÍDA PÁTIO", placeholder="00:00:00")
            v2 = h2.text_input("CHEGADA ETC", placeholder="00:00:00")
            v3 = h3.text_input("ENTRADA CLASS", placeholder="00:00:00")
            v4 = h4.text_input("SAÍDA CLASS", placeholder="00:00:00")

            h5, h6, h7, h8 = st.columns(4)
            v5 = h5.text_input("ENTRADA BAL", placeholder="00:00:00")
            v6 = h6.text_input("SAÍDA BAL", placeholder="00:00:00")
            v7 = h7.text_input("ENTRADA TOMB", placeholder="00:00:00")
            v8 = h8.text_input("SAÍDA TOMB", placeholder="00:00:00")

            # Botão de envio
            if st.form_submit_button("🚀 SALVAR REGISTRO"):
                # Salva Placa e Tipo na memória para a próxima tela
                st.session_state.placa = placa
                st.session_state.tipo = tipo
                
                sheet = conectar_google()
                if sheet:
                    # Monta a linha com 21 campos para evitar erro de dimensão
                    registro = [placa, tipo, data, v1, v2, v3, v4, v5, v6, v7, v8] + ([""] * 10)
                    sheet.append_row(registro)
                    st.success("✅ Salvo na Planilha com sucesso!")

    with tab2:
        st.write("### ÚLTIMOS LANÇAMENTOS")
        if st.button("🔄 ATUALIZAR TABELA"):
            sheet = conectar_google()
            if sheet:
                df = pd.DataFrame(sheet.get_all_records())
                st.dataframe(df.tail(15), use_container_width=True)
