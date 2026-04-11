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

st.set_page_config(page_title="Zion - Tempos e Movimentos", layout="wide", initial_sidebar_state="expanded")

# --- MÁSCARA JS (HORA) ---
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

# --- CSS PROFISSIONAL COM TÍTULO AZUL ROYAL E LINHAS EXTENDIDAS ---
st.markdown("""
    <style>
    /* Título Zion em Azul Royal */
    .title-zion {
        color: #4169E1; /* Royal Blue */
        font-family: 'Arial Black', sans-serif;
        font-size: 28px;
        margin-top: -30px;
        margin-bottom: 20px;
        text-align: left;
    }

    /* Trava largura dos campos em aprox 4cm (150px) */
    div[data-testid="stTextInput"], div[data-testid="stDateInput"], .stSelectbox {
        width: 150px !important;
        flex: none !important;
    }
    
    /* Organiza colunas com distância horizontal de 2cm */
    [data-testid="column"] {
        flex: 0 0 auto !important;
        width: 150px !important;
        margin-right: 40px !important; 
    }

    /* Linha divisória estendida pelos 4 campos */
    .section-HR { 
        border-bottom: 2px solid #4169E1; 
        margin: 15px 0 10px 0; 
        color: #4169E1; 
        font-size: 13px;
        font-weight: bold;
        width: 720px; /* Largura total: (150px * 4) + (40px * 3 gaps) */
    }

    /* Compactação Geral */
    [data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
    label { font-size: 11px !important; font-weight: bold !important; }
    input { height: 1.8rem !important; font-size: 13px !important; }
    
    .main .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
DB_FILE = "dados_porto_zion.csv"
COLUNAS = [
    "PLACA", "CAMINHÃO", "DATA", "SAÍDA PÁTIO", "CHEGADA ETC", "TT VIAGEM",
    "ENT. CLASSIF", "SAÍ. CLASSIF", "TT CLASSIF", "ENT. BAL 1", "SAÍ. BAL 1", 
    "TT BAL 1", "ENT. TOMB", "SAÍ. TOMB", "TT TOMB", "ENT. BAL 2", "SAÍ. BAL 2", 
    "TT BAL 2", "SAÍDA ETC", "TT OPERAÇÃO", "PESO LÍQUIDO"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUNAS).to_csv(DB_FILE, index=False)

if 'page' not in st.session_state: st.session_state.page = 'login'

# --- SIDEBAR ---
if st.session_state.page != 'login':
    with st.sidebar:
        st.markdown("<h2 style='color:#4169E1;'>ZION</h2>", unsafe_allow_html=True)
        st.write(f"Usuário: **{st.session_state.perfil}**")
        st.markdown("---")
        if st.button("📝 Novo Lançamento"): st.session_state.page = 'lancamento'; st.rerun()
        if st.button("📊 Relatório Geral"): st.session_state.page = 'visualizacao'; st.rerun()
        st.markdown("---")
        if st.button("⬅️ Sair"): st.session_state.page = 'login'; st.rerun()

# --- TELA LOGIN ---
if st.session_state.page == 'login':
    st.markdown("<div class='title-zion'>Zion - Tempos e movimentos</div>", unsafe_allow_html=True)
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if u in USUARIOS and USUARIOS[u]["senha"] == p:
            st.session_state.perfil = USUARIOS[u]["perfil"]
            st.session_state.page = 'lancamento'; st.rerun()

# --- TELA LANÇAMENTO ---
elif st.session_state.page == 'lancamento':
    st.markdown("<div class='title-zion'>Zion - Tempos e movimentos</div>", unsafe_allow_html=True)
    
    with st.form("form_zion", clear_on_submit=False):
        # Linha 1
        c1, c2, c3, c4 = st.columns(4)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        # DATA NO FORMATO PT-BR DD/MM/AAAA
        data_sel = c3.date_input("Data", datetime.now(), format="DD/MM/YYYY")
        
        st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        # Linha 2
        c5, c6, c7, c8 = st.columns(4)
        s_patio = c5.text_input("Saída Pátio", placeholder="00:00:00")
        c_etc = c6.text_input("Chegada ETC", placeholder="00:00:00")
        tt_v = c7.text_input("TT Viagem", placeholder="00:00:00")
        e_cl = c8.text_input("Ent. Class", placeholder="00:00:00")
        
        # Linha 3
        c9, c10, c11, c12 = st.columns(4)
        s_cl = c9.text_input("Saí. Class", placeholder="00:00:00")
        tt_cl = c10.text_input("TT Class", placeholder="00:00:00")

        st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
        # Linha 4
        c13, c14, c15, c16 = st.columns(4)
        e_b1 = c13.text_input("Ent. Bal 1", placeholder="00:00:00")
        s_b1 = c14.text_input("Saí. Bal 1", placeholder="00:00:00")
        tt_b1 = c15.text_input("TT Bal 1", placeholder="00:00:00")
        e_to = c16.text_input("Ent. Tomb", placeholder="00:00:00")
        
        # Linha 5
        c17, c18, c19, c20 = st.columns(4)
        s_to = c17.text_input("Saí. Tomb", placeholder="00:00:00")
        tt_to = c18.text_input("TT Tomb", placeholder="00:00:00")
        e_b2 = c19.text_input("Ent. Bal 2", placeholder="00:00:00")
        s_b2 = c20.text_input("Saí. Bal 2", placeholder="00:00:00")

        st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
        # Linha 6
        c21, c22, c23, c24 = st.columns(4)
        tt_b2 = c21.text_input("TT Bal 2", placeholder="00:00:00")
        s_etc = c22.text_input("Saída ETC", placeholder="00:00:00")
        tt_ot = c23.text_input("TT Total", placeholder="00:00:00")
        p_liq = c24.text_input("Peso Líq.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("💾 SALVAR REGISTRO"):
            novo = {
                "PLACA": placa.upper(), "CAMINHÃO": caminhao.upper(), "DATA": data_sel.strftime("%d/%m/%Y"),
                "SAÍDA PÁTIO": s_patio, "CHEGADA ETC": c_etc, "TT VIAGEM": tt_v,
                "ENT. CLASSIF": e_cl, "SAÍ. CLASSIF": s_cl, "TT CLASSIF": tt_cl,
                "ENT. BAL 1": e_b1, "SAÍ. BAL 1": s_b1, "TT BAL 1": tt_b1,
                "ENT. TOMB": e_to, "SAÍ. TOMB": s_to, "TT TOMB": tt_to,
                "ENT. BAL 2": e_b2, "SAÍ. BAL 2": s_b2, "TT BAL 2": tt_b2,
                "SAÍDA ETC": s_etc, "TT OPERAÇÃO": tt_ot, "PESO LÍQUIDO": p_liq
            }
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ Salvo!")
            st.rerun()

    inject_mask()

# --- TELA VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.markdown("<div class='title-zion'>Relatório Geral</div>", unsafe_allow_html=True)
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
    
    # Exportação Excel (CSV formatado)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 EXPORTAR PARA EXCEL",
        data=csv,
        file_name=f'zion_relatorio_{datetime.now().strftime("%d_%m_%Y")}.csv',
        mime='text/csv',
    )
