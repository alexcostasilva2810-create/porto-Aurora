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

st.set_page_config(page_title="Aurora Port", layout="wide", initial_sidebar_state="expanded")

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

# --- CSS PROFISSIONAL E COMPACTO (CAMPOS 4CM / 4 COLUNAS) ---
st.markdown("""
    <style>
    /* Trava largura dos campos em aprox 4cm (150px) */
    div[data-testid="stTextInput"], div[data-testid="stDateInput"], .stSelectbox {
        width: 150px !important;
        flex: none !important;
    }
    
    /* Organiza colunas com distância horizontal de 2cm (40px aprox) */
    [data-testid="column"] {
        flex: 0 0 auto !important;
        width: 150px !important;
        margin-right: 40px !important; 
    }

    /* Remove espaços excessivos entre linhas */
    [data-testid="stVerticalBlock"] {
        gap: 0.3rem !important;
    }

    .main .block-container {
        padding-top: 1.5rem !important;
        margin-left: 0 !important;
    }

    .section-HR { 
        border-bottom: 2px solid #004b87; 
        margin: 15px 0 10px 0; 
        color: #004b87; 
        font-size: 13px;
        font-weight: bold;
        width: 720px; /* Largura total das 4 colunas + gaps */
    }

    label { font-size: 11px !important; font-weight: bold !important; }
    input { height: 1.8rem !important; font-size: 13px !important; }

    /* Estilo Sidebar */
    [data-testid="stSidebar"] { background-color: #f0f2f6; width: 200px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
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

# --- BARRA LATERAL (BOTÕES À ESQUERDA) ---
if st.session_state.page != 'login':
    with st.sidebar:
        st.markdown("### 🚢 AURORA PORT")
        st.write(f"ID: **{st.session_state.perfil}**")
        st.markdown("---")
        if st.button("📝 Novo Lançamento"): st.session_state.page = 'lancamento'; st.rerun()
        if st.button("📊 Tabela Geral"): st.session_state.page = 'visualizacao'; st.rerun()
        if st.button("⬅️ Sair"): st.session_state.page = 'login'; st.rerun()

# --- TELA LOGIN ---
if st.session_state.page == 'login':
    st.markdown("<h2 style='color:#004b87;'>AURORA - LOGIN</h2>", unsafe_allow_html=True)
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if u in USUARIOS and USUARIOS[u]["senha"] == p:
            st.session_state.perfil = USUARIOS[u]["perfil"]
            st.session_state.page = 'lancamento'; st.rerun()

# --- TELA LANÇAMENTO (ORGANIZADA EM 4 COLUNAS) ---
elif st.session_state.page == 'lancamento':
    with st.form("form_aurora", clear_on_submit=False):
        # Linha 1: Identificação
        c1, c2, c3, c4 = st.columns(4)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        data_sel = c3.date_input("Data", datetime.now())
        
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
            st.success("✅ Salvo com sucesso!")
            st.rerun()

    inject_mask()

# --- TELA VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.markdown("### 📊 Relatório Geral")
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
    
    # Exportação Excel Profissional
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 EXPORTAR PARA EXCEL (CSV)",
        data=csv,
        file_name=f'relatorio_aurora_{datetime.now().strftime("%d_%m_%H%M")}.csv',
        mime='text/csv',
    )
