import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# --- BANCO DE DADOS (Persistência entre telas) ---
def init_db():
    conn = sqlite3.connect('zion_operacao.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS registros 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, placa TEXT, caminhao TEXT, data TEXT, 
         s_patio TEXT, c_etc TEXT, tt_v TEXT, e_cl TEXT, s_cl TEXT, tt_cl TEXT,
         e_b1 TEXT, s_b1 TEXT, tt_b1 TEXT, e_to TEXT, s_to TEXT, tt_to TEXT,
         e_b2 TEXT, s_b2 TEXT, tt_b2 TEXT, s_etc TEXT, tt_ot TEXT, p_liq TEXT,
         status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- CSS: FUNDO PORTUÁRIO E ESTILO ZION ---
st.markdown("""
    <style>
    /* Fundo da tela de Login */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
        url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
    }
    /* Estilo dos Cards do Menu */
    .menu-card {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #4169E1;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .menu-card:hover { transform: scale(1.05); background-color: #f0f2f6; }
    .title-zion { color: #4169E1; font-family: 'Arial Black'; font-size: 32px; text-align: center; background: white; padding: 10px; border-radius: 10px; }
    div[data-testid="stTextInput"] { width: 150px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MÁSCARA DE HORA JS ---
def inject_mask():
    components.html("""
        <script>
        const mask = (e) => {
            let v = e.target.value.replace(/\D/g,'');
            if (v.length > 6) v = v.slice(0,6);
            if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
            else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
            e.target.value = v;
            e.target.dispatchEvent(new Event('input', { bubbles: true }));
        }
        setInterval(() => {
            window.parent.document.querySelectorAll('input[placeholder="00:00:00"]').forEach(i => {
                if(!i.dataset.m) { i.addEventListener('input', mask); i.dataset.m = '1'; }
            });
        }, 500);
        </script>
        """, height=0)

# --- LÓGICA DE NAVEGAÇÃO ---
if 'page' not in st.session_state: st.session_state.page = 'login'

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- 1. TELA DE LOGIN ---
if st.session_state.page == 'login':
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br><div class='title-zion'>ZION - SISTEMA PORTUÁRIO</div>", unsafe_allow_html=True)
        with st.container():
            st.write("")
            user = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.button("ACESSAR SISTEMA", use_container_width=True):
                go_to('menu')

# --- 2. TELA DE MENU (ÍCONES DE JANELA) ---
elif st.session_state.page == 'menu':
    st.markdown("<div class='title-zion'>PAINEL DE OPERAÇÕES</div>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='menu-card'><h3>🚚</h3><b>LOGÍSTICA</b><br>Classificação</div>", unsafe_allow_html=True)
        if st.button("Abrir Logística", key="btn1"): go_to('logistica')
        
    with col2:
        st.markdown("<div class='menu-card'><h3>⚖️</h3><b>BALANÇA</b><br>Pesagem Ent/Saí</div>", unsafe_allow_html=True)
        if st.button("Abrir Balança", key="btn2"): go_to('balanca')
        
    with col3:
        st.markdown("<div class='menu-card'><h3>🏗️</h3><b>TOMBADOR</b><br>Descarga</div>", unsafe_allow_html=True)
        if st.button("Abrir Tombador", key="btn3"): go_to('tombador')
        
    with col4:
        st.markdown("<div class='menu-card'><h3>📝</h3><b>FECHAMENTO</b><br>Finalizar Processo</div>", unsafe_allow_html=True)
        if st.button("Abrir Fechamento", key="btn4"): go_to('fechamento')

    if st.button("⬅️ Sair"): go_to('login')

# --- 3. TELAS DE ESTAÇÃO (Exemplo: Logística) ---
elif st.session_state.page == 'logistica':
    st.markdown("<div class='title-zion'>ESTAÇÃO: LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
    if st.button("⬅️ Voltar ao Menu"): go_to('menu')
    
    with st.form("form_log"):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("PLACA")
        cam = c2.text_input("CAMINHÃO")
        data = c3.date_input("DATA DA OPERAÇÃO", format="DD/MM/YYYY")
        
        st.markdown("---")
        c4, c5, c6 = st.columns(3)
        sp = c4.text_input("Saída Pátio", placeholder="00:00:00")
        ce = c5.text_input("Chegada ETC", placeholder="00:00:00")
        ec = c6.text_input("Ent. Class", placeholder="00:00:00")
        
        if st.form_submit_button("✅ INICIAR PROCESSO"):
            conn = sqlite3.connect('zion_operacao.db')
            c = conn.cursor()
            c.execute("INSERT INTO registros (placa, caminhao, data, s_patio, c_etc, e_cl, status) VALUES (?,?,?,?,?,?,'Em curso')", 
                      (placa, cam, str(data), sp, ce, ec))
            conn.commit()
            conn.close()
            st.success("Caminhão registrado! Próxima etapa: Balança.")
    inject_mask()

# --- 4. TELA BALANÇA (Busca o que a logística fez) ---
elif st.session_state.page == 'balanca':
    st.markdown("<div class='title-zion'>ESTAÇÃO: BALANÇA</div>", unsafe_allow_html=True)
    if st.button("⬅️ Voltar"): go_to('menu')
    
    # Busca placas que estão no pátio
    conn = sqlite3.connect('zion_operacao.db')
    df = pd.read_sql("SELECT id, placa, caminhao FROM registros WHERE status = 'Em curso'", conn)
    conn.close()
    
    if not df.empty:
        escolha = st.selectbox("Selecione o veículo para pesagem:", df['placa'] + " - " + df['caminhao'])
        id_sel = df.iloc[st.session_state.get('index', 0)]['id'] # Simplificado
        
        with st.form("form_bal"):
            c1, c2, c3 = st.columns(3)
            eb1 = c1.text_input("Ent. Bal 1", placeholder="00:00:00")
            sb1 = c2.text_input("Saí. Bal 1", placeholder="00:00:00")
            ttb1 = c3.text_input("TT Bal 1", placeholder="00:00:00")
            if st.form_submit_button("💾 SALVAR PESAGEM"):
                st.success("Pesagem salva!")
    else:
        st.warning("Nenhum caminhão aguardando balança.")
    inject_mask()
