import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# =========================================================
# 🔑 GESTÃO DE USUÁRIOS E PERMISSÕES
# =========================================================
USUARIOS = {
    "admin": {"senha": "123", "perfil": "supervisor"},
    "alex": {"senha": "porto", "perfil": "supervisor"},
    "operador1": {"senha": "123", "perfil": "operador"}
}

# Configuração da página
st.set_page_config(page_title="Aurora Port - Monitoramento", layout="wide")

# Estilo visual para separadores e botões
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004b87; color: white; font-weight: bold; }
    .title-text { text-align: center; color: #004b87; font-family: 'Arial Black'; font-size: 40px; margin-bottom: 0; }
    .section-HR { border-top: 2px solid #004b87; margin: 20px 0; padding-top: 10px; font-weight: bold; color: #004b87; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def formatar_hora(texto):
    """Formata entrada numérica para HH:MM:SS"""
    apenas_numeros = "".join(filter(str.isdigit, texto))
    if len(apenas_numeros) == 4:
        return f"{apenas_numeros[:2]}:{apenas_numeros[2:]}:00"
    elif len(apenas_numeros) == 6:
        return f"{apenas_numeros[:2]}:{apenas_numeros[2:4]}:{apenas_numeros[4:]}"
    return "00:00:00" if not apenas_numeros else texto

def calc_diff(inicio, fim):
    """Calcula a diferença entre dois horários"""
    try:
        fmt = '%H:%M:%S'
        t1 = datetime.strptime(formatar_hora(inicio), fmt)
        t2 = datetime.strptime(formatar_hora(fim), fmt)
        if t2 < t1: t2 += timedelta(days=1) # Caso passe da meia-noite
        return t2 - t1
    except:
        return timedelta(0)

def td_to_str(td):
    """Converte timedelta para string formatada"""
    total_sec = int(td.total_seconds())
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- BANCO DE DADOS ---
DB_FILE = "dados_porto_v2.csv"
COLUNAS = [
    "PLACA", "CAMINHÃO", "DATA", 
    "SAÍDA PÁTIO", "CHEGADA ETC", "TT VIAGEM",
    "ENTR. CLASSIF", "SAÍDA CLASSIF", "TT CLASSIF",
    "ENTR. BALANÇA 1", "SAÍDA BALANÇA 1", "TT BALANÇA 1",
    "ENT. TOMBADOR", "SAÍDA TOMBADOR", "TT TOMBADOR",
    "ENT. BALANÇA 2", "SAÍDA BALANÇA 2", "TT BALANÇA 2",
    "SAÍDA ETC", "TT OPERAÇÃO", "PESO LÍQUIDO"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUNAS).to_csv(DB_FILE, index=False)

if 'page' not in st.session_state: st.session_state.page = 'login'
if 'perfil' not in st.session_state: st.session_state.perfil = None

# --- TELA 1: LOGIN ---
if st.session_state.page == 'login':
    st.markdown("<h1 class='title-text'>AURORA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Logística de Grãos - PT-BR</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ACESSAR"):
            if u in USUARIOS and USUARIOS[u]["senha"] == p:
                st.session_state.perfil = USUARIOS[u]["perfil"]; st.session_state.page = 'lancamento'; st.rerun()
            else: st.error("Usuário ou senha inválidos.")

# --- TELA 2: LANÇAMENTOS ---
elif st.session_state.page == 'lancamento':
    st.sidebar.title(f"Perfil: {str(st.session_state.perfil).upper()}")
    if st.sidebar.button("📊 Visualizar Tabela"): st.session_state.page = 'visualizacao'; st.rerun()
    if st.sidebar.button("🚪 Sair"): st.session_state.page = 'login'; st.rerun()

    st.markdown("## 📝 Novo Registro de Operação")
    
    with st.form("form_aurora", clear_on_submit=True):
        # CABEÇALHO
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        # DATA FORMATADA PT-BR
        data_input = c3.date_input("Data", datetime.now())
        data_br = data_input.strftime("%d/%m/%Y")

        # BLOCO 1: VIAGEM
        st.markdown("<div class='section-HR'>LOGÍSTICA: PÁTIO -> ETC</div>", unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        s_patio = c4.text_input("Saída do Pátio (HHMM)")
        c_etc = c5.text_input("Chegada ETC (HHMM)")

        # BLOCO 2: CLASSIFICAÇÃO
        st.markdown("<div class='section-HR'>CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        c6, c7 = st.columns(2)
        e_class = c6.text_input("Entrada Classificação")
        s_class = c7.text_input("Saída Classificação")

        # BLOCO 3: BALANÇA 1
        st.markdown("<div class='section-HR'>BALANÇA 1 (ENTRADA)</div>", unsafe_allow_html=True)
        c8, c9 = st.columns(2)
        e_bal1 = c8.text_input("Entrada Balança 1")
        s_bal1 = c9.text_input("Saída Balança 1")

        # BLOCO 4
