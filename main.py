import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# --- CONEXÃO SEGURA ---
def conectar_planilha():
    creds_info = st.secrets["gcp_service_account"]
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    return gspread.authorize(creds).open("Zion").worksheet("Tempo")

# --- CONFIGURAÇÃO VISUAL (RESOLVE FUNDO E BLOCOS BRANCOS) ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.4), rgba(255,255,255,0.4)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    /* Remove retângulos brancos e espaços vazios no topo */
    .block-container { padding-top: 0rem !important; }
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    
    /* Legendas Pretas e Nítidas */
    label, p, h3 { color: black !important; font-weight: bold !important; font-size: 18px !important; }
    
    /* Estilo dos Inputs */
    .stTextInput>div>div>input { background-color: white !important; color: black !important; border: 2px solid #1E3A8A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MÁSCARA JAVASCRIPT ---
components.html("""
    <script>
    const maskTime = (e) => {
        let v = e.target.value.replace(/\D/g,'');
        if (v.length > 6) v = v.slice(0,6);
        if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
        else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
        e.target.value = v;
    }
    setInterval(() => {
        window.parent.document.querySelectorAll('input[placeholder="00:00:00"]').forEach(i => {
            if(!i.dataset.maskOn) { 
                i.addEventListener('input', maskTime); i.dataset.maskOn = '1';
                i.onblur = () => { i.dispatchEvent(new Event('change', { bubbles: true })); };
            }
        });
    }, 500);
    </script>
    """, height=0)

# --- GERENCIAMENTO DE TELAS E MEMÓRIA ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'login'
# Memória dos campos para a hora não sumir
for campo in ['h1', 'h2', 'h3', 'placa', 'cam']:
    if campo not in st.session_state: st.session_state[campo] = ""

# --- 1. LOGIN ---
if st.session_state.etapa == 'login':
    st.markdown("<h1 style='text-align:center; color:black;'>ACESSO ZION</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        user = st.text_input("USUÁRIO")
        senha = st.text_input("SENHA", type="password")
        perf = st.selectbox("ESTAÇÃO", ["LOGÍSTICA", "BALANÇA", "TOMBADOR"])
        if st.button("ENTRAR NO SISTEMA"):
            if user == "admin" and senha == "zion123":
                st.session_state.perfil = perf
                st.session_state.etapa = 'menu'
                st.rerun()

# --- 2. MENU ---
elif st.session_state.etapa == 'menu':
    st.markdown(f"<h1 style='text-align:center; color:black;'>MENU: {st.session_state.perfil}</h1>", unsafe_allow_html=True)
    if st.button("📝 INICIAR LANÇAMENTOS"): st.session_state.etapa = 'form'; st.rerun()
    if st.button("🔙 VOLTAR PARA LOGIN"): st.session_state.etapa = 'login'; st.rerun()

# --- 3. FORMULÁRIO (AQUI A HORA FICA PRESA) ---
elif st.session_state.etapa == 'form':
    st.markdown(f"<h1 style='text-align:center; color:black;'>ESTAÇÃO {st.session_state.perfil}</h1>", unsafe_allow_html=True)
    
    if st.button("⬅️ VOLTAR AO MENU"): st.session_state.etapa = 'menu'; st.rerun()

    with st.form("meu_formulario", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("PLACA DO VEÍCULO", value=st.session_state.placa)
        cam = c2.text_input("TIPO DE CAMINHÃO", value=st.session_state.cam)
        data = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))

        st.markdown("---")
        h1_col, h2_col, h3_col = st.columns(3)
        
        # Atribuindo os valores à memória da sessão
        if st.session_state.perfil == "LOGÍSTICA":
            v1 = h1_col.text_input("SAÍDA PÁTIO", placeholder="00:00:00", value=st.session_state.h1)
            v2 = h2_col.text_input("CHEGADA ETC", placeholder="00:00:00", value=st.session_state.h2)
            v3 = h3_col.text_input("ENTRADA CLASSIFIC.", placeholder="00:00:00", value=st.session_state.h3)
        else:
            v1 = h1_col.text_input("ENTRADA", placeholder="00:00:00")
            v2 = h2_col.text_input("SAÍDA", placeholder="00:00:00")
            v3 = ""

        if st.form_submit_button("✅ SALVAR NA PLANILHA"):
            try:
                sheet = conectar_planilha()
                sheet.append_row([placa, cam, data, v1, v2, "", v3])
                st.success("LANÇAMENTO REALIZADO!")
                # Limpa a memória após salvar
                for k in ['h1', 'h2', 'h3', 'placa', 'cam']: st.session_state[k] = ""
            except Exception as e: st.error(f"Erro: {e}")

    # --- TABELA DE CONFERÊNCIA (PONTO 5) ---
    st.markdown("### 📊 ÚLTIMOS REGISTROS NA PLANILHA")
    if st.button("🔄 ATUALIZAR TABELA"):
        try:
            df = pd.DataFrame(conectar_planilha().get_all_records())
            st.dataframe(df.tail(10), use_container_width=True)
        except: st.info("Carregando dados...")
