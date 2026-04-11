import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# --- CONEXÃO COM A PLANILHA ---
def conectar_planilha():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds_info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    client = gspread.authorize(creds)
    # Abre a planilha 'Zion' na aba 'Tempo'
    return client.open("Zion").worksheet("Tempo")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS (LEGENDA PRETA E FUNDO DE GRÃOS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.4), rgba(255,255,255,0.4)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    /* Legendas em preto e negrito */
    label { color: black !important; font-weight: bold !important; font-size: 16px !important; }
    .main-title { color: #1E3A8A; text-align: center; font-family: 'Arial Black'; font-size: 40px; background: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 8px; height: 3em; }
    .card-branco { background: rgba(255, 255, 255, 0.9); padding: 25px; border-radius: 15px; border: 1px solid #ccc; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- MÁSCARA JS (A SOLUÇÃO PARA A HORA NÃO SUMIR) ---
components.html("""
    <script>
    const applyMask = (e) => {
        let v = e.target.value.replace(/\D/g,'');
        if (v.length > 6) v = v.slice(0,6);
        if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
        else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
        e.target.value = v;
    }
    setInterval(() => {
        window.parent.document.querySelectorAll('input[placeholder="00:00:00"]').forEach(i => {
            if(!i.dataset.maskOn) { 
                i.addEventListener('input', applyMask); i.dataset.maskOn = '1';
                i.onblur = () => { i.dispatchEvent(new Event('change', { bubbles: true })); };
            }
        });
    }, 500);
    </script>
    """, height=0)

# --- CONTROLE DE FLUXO ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'apresentacao'

# --- 1. TELA DE APRESENTAÇÃO ---
if st.session_state.etapa == 'apresentacao':
    st.markdown("<h1 class='main-title'>ZION PORTUÁRIO</h1>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg", use_column_width=True)
    if st.button("👉 CLIQUE PARA ENTRAR NO SISTEMA"):
        st.session_state.etapa = 'login'
        st.rerun()

# --- 2. TELA DE LOGIN ---
elif st.session_state.etapa == 'login':
    st.markdown("<h1 class='main-title'>LOGIN DE ACESSO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown("<div class='card-branco'>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        s = st.text_input("SENHA", type="password")
        perf = st.selectbox("PERFIL", ["LOGÍSTICA", "BALANÇA", "TOMBADOR", "FECHAMENTO"])
        if st.button("ENTRAR"):
            if u == "admin" and s == "zion123":
                st.session_state.perfil = perf
                st.session_state.etapa = 'menu'
                st.rerun()
            else: st.error("Acesso Negado")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. MENU PRINCIPAL ---
elif st.session_state.etapa == 'menu':
    st.markdown(f"<h1 class='main-title'>MENU: {st.session_state.perfil}</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 REALIZAR LANÇAMENTOS"): st.session_state.etapa = 'operacao'; st.rerun()
    with col2:
        if st.button("🚪 SAIR DO SISTEMA"): st.session_state.etapa = 'login'; st.rerun()

# --- 4. TELA DE OPERAÇÃO ---
elif st.session_state.etapa == 'operacao':
    st.markdown(f"<h1 class='main-title'>ESTAÇÃO {st.session_state.perfil}</h1>", unsafe_allow_html=True)
    
    # Botão de Voltar ao Menu
    if st.button("⬅️ VOLTAR AO MENU"):
        st.session_state.etapa = 'menu'
        st.rerun()

    st.markdown("<div class='card-branco'>", unsafe_allow_html=True)
    with st.form("form_dados", clear_on_submit=True):
        # Campos de Identificação
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("PLACA DO VEÍCULO")
        cam = c2.text_input("TIPO DE CAMINHÃO")
        data = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))

        st.markdown("---")
        # Campos Dinâmicos conforme Perfil
        h1, h2, h3 = st.columns(3)
        if st.session_state.perfil == "LOGÍSTICA":
            val1 = h1.text_input("SAÍDA PÁTIO", placeholder="00:00:00")
            val2 = h2.text_input("CHEGADA ETC", placeholder="00:00:00")
            val3 = h3.text_input("ENTRADA CLASSIFIC.", placeholder="00:00:00")
        elif st.session_state.perfil == "BALANÇA":
            val1 = h1.text_input("ENTRADA BALANÇA", placeholder="00:00:00")
            val2 = h2.text_input("SAÍDA BALANÇA", placeholder="00:00:00")
            val3 = ""
        elif st.session_state.perfil == "TOMBADOR":
            val1 = h1.text_input("ENTRADA TOMBADOR", placeholder="00:00:00")
            val2 = h2.text_input("SAÍDA TOMBADOR", placeholder="00:00:00")
            val3 = ""

        if st.form_submit_button("🚀 SALVAR REGISTRO"):
            try:
                sheet = conectar_planilha()
                # Segue a ordem da planilha image_057281.png
                sheet.append_row([placa, cam, data, val1, val2, "", val3])
                st.success("✅ Lançamento realizado com sucesso!")
            except Exception as e: st.error(f"Erro ao salvar: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- TABELA DE CONFERÊNCIA (Ponto 5 solicitado) ---
    st.markdown("<div class='card-branco'>", unsafe_allow_html=True)
    st.subheader("📋 Conferência de Lançamentos")
    if st.button("🔄 ATUALIZAR TABELA"):
        sheet = conectar_planilha()
        df = pd.DataFrame(sheet.get_all_records())
        st.dataframe(df.tail(10), use_container_width=True) # Mostra os últimos 10
    st.markdown("</div>", unsafe_allow_html=True)
