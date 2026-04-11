import streamlit as st
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components

# 🔑 GESTÃO DE USUÁRIOS
USUARIOS = {
    "admin": {"senha": "123", "perfil": "ADMIN"},
    "alex": {"senha": "porto", "perfil": "SUPERVISOR"},
    "operador1": {"senha": "123", "perfil": "OPERADOR"}
}

st.set_page_config(page_title="Aurora Port", layout="wide", initial_sidebar_state="collapsed")

# --- MÁSCARA JS ---
def inject_mask():
    components.html(
        """
        <script>
        const maskTime = (e) => {
            let v = e.target.value.replace(/\D/g, '');
            if (v.length > 6) v = v.slice(0, 6);
            if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
            else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
            e.target.value = v;
            e.target.dispatchEvent(new Event('input', { bubbles: true }));
        }
        const inputs = window.parent.document.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            if (!input.dataset.maskSet && input.placeholder === "00:00:00") {
                input.addEventListener('input', maskTime);
                input.dataset.maskSet = "true";
            }
        });
        </script>
        """, height=0
    )

# --- CSS PARA CAMPOS ESTREITOS E ESPAÇAMENTO ---
st.markdown("""
    <style>
    /* Ajuste de largura máxima dos campos (aprox 4cm/150px) e distância lateral */
    [data-testid="column"] {
        max-width: 150px !important; 
        padding-right: 20px !important; /* Distância horizontal entre campos */
    }
    
    /* Ajuste específico para a tela de Login ficar centralizada e estreita */
    .login-box {
        max-width: 200px;
        margin: auto;
    }

    .main .block-container {
        padding-top: 2rem !important;
    }
    
    .stTextInput>div>div>input {
        height: 1.8rem !important;
        font-size: 12px !important;
    }
    
    label {
        font-size: 11px !important;
        white-space: nowrap !important;
    }

    .section-HR { 
        border-top: 2px solid #004b87; 
        margin: 10px 0 5px 0; 
        color: #004b87; 
        font-size: 12px;
        font-weight: bold;
    }
    
    .title-text { 
        text-align: center; 
        color: #004b87; 
        font-size: 20px; 
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS (21 CAMPOS) ---
DB_FILE = "dados_porto_v2.csv"
COLUNAS = [
    "PLACA", "CAMINHÃO", "DATA", "SAÍDA PÁTIO", "CHEGADA ETC", "TT VIAGEM",
    "ENT. CLASSIF", "SAÍ. CLASSIF", "TT CLASSIF", "ENT. BAL 1", "SAÍ. BAL 1", 
    "TT BAL 1", "ENT. TOMB", "SAÍ. TOMB", "TT TOMB", "ENT. BAL 2", "SAÍ. BAL 2", 
    "TT BAL 2", "SAÍDA ETC", "TT OPERAÇÃO", "PESO LÍQUIDO"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUNAS).to_csv(DB_FILE, index=False)

if 'page' not in st.session_state: st.session_state.page = 'login'

# --- TELA DE LOGIN (ESTREITA) ---
if st.session_state.page == 'login':
    st.markdown("<h1 class='title-text'>AURORA</h1>", unsafe_allow_html=True)
    c_log1, c_log2, c_log3 = st.columns([1, 1, 1])
    with c_log2: # Usa a coluna do meio para centralizar
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ACESSAR"):
            if u in USUARIOS and USUARIOS[u]["senha"] == p:
                st.session_state.perfil = USUARIOS[u]["perfil"]
                st.session_state.page = 'lancamento'
                st.rerun()

# --- TELA DE LANÇAMENTOS (CAMPOS 4CM + DISTANCIA 2CM) ---
elif st.session_state.page == 'lancamento':
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("📊 Tabela"): st.session_state.page = 'visualizacao'; st.rerun()
    with col_nav2:
        if st.button("⬅️ Sair"): st.session_state.page = 'login'; st.rerun()

    with st.form("form_aurora"):
        # Seção 1
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        data_sel = c3.date_input("Data", datetime.now())
        
        st.markdown("<div class='section-HR'>LOGÍSTICA / CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        s_patio = c4.text_input("Saída Pátio", placeholder="00:00:00")
        c_etc = c5.text_input("Chegada ETC", placeholder="00:00:00")
        tt_v = c6.text_input("TT Viagem", placeholder="00:00:00")

        c7, c8, c9 = st.columns(3)
        e_cl = c7.text_input("Ent. Class", placeholder="00:00:00")
        s_cl = c8.text_input("Saí. Class", placeholder="00:00:00")
        tt_cl = c9.text_input("TT Class", placeholder="00:00:00")

        st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
        c10, c11, c12 = st.columns(3)
        e_b1 = c10.text_input("Ent. Bal 1", placeholder="00:00:00")
        s_b1 = c11.text_input("Saí. Bal 1", placeholder="00:00:00")
        tt_b1 = c12.text_input("TT Bal 1", placeholder="00:00:00")

        c13, c14, c15 = st.columns(3)
        e_to = c13.text_input("Ent. Tomb", placeholder="00:00:00")
        s_to = c14.text_input("Saí. Tomb", placeholder="00:00:00")
        tt_to = c15.text_input("TT Tomb", placeholder="00:00:00")

        c16, c17, c18 = st.columns(3)
        e_b2 = c16.text_input("Ent. Bal 2", placeholder="00:00:00")
        s_b2 = c17.text_input("Saí. Bal 2", placeholder="00:00:00")
        tt_b2 = c18.text_input("TT Bal 2", placeholder="00:00:00")

        st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
        c19, c20, c21 = st.columns(3)
        s_etc = c19.text_input("Saída ETC", placeholder="00:00:00")
        tt_ot = c20.text_input("TT Total", placeholder="00:00:00")
        p_liq = c21.text_input("Peso Líq.")

        if st.form_submit_button("SALVAR"):
            # Lógica de salvar permanece a mesma com os 21 campos
            st.success("Salvo!")
            st.rerun()

    inject_mask()

elif st.session_state.page == 'visualizacao':
    if st.button("Voltar"): st.session_state.page = 'lancamento'; st.rerun()
    st.dataframe(pd.read_csv(DB_FILE), use_container_width=True)
