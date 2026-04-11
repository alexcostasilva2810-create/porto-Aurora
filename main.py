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

# --- CSS ULTRA COMPACTO (CAMPOS DE 4CM / 150PX) ---
st.markdown("""
    <style>
    /* Trava a largura dos campos em aprox 4cm */
    div[data-testid="stTextInput"], div[data-testid="stDateInput"] {
        width: 150px !important;
    }
    
    /* Remove espaços vazios e compacta o layout */
    .block-container {
        padding-top: 1rem !important;
        max-width: 600px !important; /* Estreita a área total de preenchimento */
        margin-left: 0 !important;   /* Alinha à esquerda */
    }

    .stTextInput>div>div>input {
        height: 1.8rem !important;
        font-size: 12px !important;
    }

    label {
        font-size: 11px !important;
        margin-bottom: 0px !important;
    }

    .section-HR { 
        border-top: 2px solid #004b87; 
        margin: 10px 0 5px 0; 
        color: #004b87; 
        font-size: 12px;
        font-weight: bold;
    }
    
    /* Botões da Sidebar */
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        text-align: left;
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

# --- NAVEGAÇÃO LATERAL ESQUERDA ---
if st.session_state.page != 'login':
    with st.sidebar:
        st.title("AURORA")
        st.write(f"Usuário: **{st.session_state.perfil}**")
        if st.button("📝 Novo Lançamento"): st.session_state.page = 'lancamento'; st.rerun()
        if st.button("📊 Ver Tabela Geral"): st.session_state.page = 'visualizacao'; st.rerun()
        st.markdown("---")
        if st.button("⬅️ Sair"): st.session_state.page = 'login'; st.rerun()

# --- TELA DE LOGIN ---
if st.session_state.page == 'login':
    st.title("AURORA - Login")
    u = st.text_input("Usuário", key="user")
    p = st.text_input("Senha", type="password", key="pass")
    if st.button("ACESSAR"):
        if u in USUARIOS and USUARIOS[u]["senha"] == p:
            st.session_state.perfil = USUARIOS[u]["perfil"]
            st.session_state.page = 'lancamento'
            st.rerun()

# --- TELA DE LANÇAMENTOS (COMPACTA) ---
elif st.session_state.page == 'lancamento':
    with st.form("form_aurora"):
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

        if st.form_submit_button("SALVAR REGISTRO"):
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

# --- TELA DE VISUALIZAÇÃO COM EXPORT EXCEL ---
elif st.session_state.page == 'visualizacao':
    st.subheader("Tabela de Registros")
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
    
    # Botão de Exportação para Excel
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Excel (CSV)",
        data=csv,
        file_name='relatorio_porto.csv',
        mime='text/csv',
    )
