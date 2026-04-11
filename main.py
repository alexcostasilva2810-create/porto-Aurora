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

# --- MÁSCARA JS (Otimizada) ---
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

# --- CSS PARA NÃO ENGOLIR O TOPO E COMPACTAR GERAL ---
st.markdown("""
    <style>
    /* Ajuste para o conteúdo não subir demais e sumir */
    .main .block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    /* Diminuir altura dos campos e fontes para mobile */
    .stTextInput>div>div>input {
        height: 2rem !important;
        font-size: 14px !important;
    }
    label {
        font-size: 13px !important;
        margin-bottom: 0px !important;
    }
    .section-HR { 
        border-top: 2px solid #004b87; 
        margin: 10px 0 5px 0; 
        padding-top: 3px; 
        font-weight: bold; 
        color: #004b87; 
        font-size: 13px;
    }
    .title-text { 
        text-align: center; 
        color: #004b87; 
        font-family: 'Arial Black'; 
        font-size: 24px; 
        margin-top: -20px;
    }
    /* Compactar espaço entre colunas */
    [data-testid="column"] {
        padding: 0 5px !important;
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

# --- TELA DE LOGIN ---
if st.session_state.page == 'login':
    st.markdown("<h1 class='title-text'>AURORA</h1>", unsafe_allow_html=True)
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("ACESSAR"):
        if u in USUARIOS and USUARIOS[u]["senha"] == p:
            st.session_state.perfil = USUARIOS[u]["perfil"]
            st.session_state.page = 'lancamento'
            st.rerun()

# --- TELA DE LANÇAMENTOS (LAYOUT COMPACTO E SEGURO) ---
elif st.session_state.page == 'lancamento':
    st.markdown(f"<p style='text-align:right; font-size:12px;'>Acesso: {st.session_state.perfil}</p>", unsafe_allow_html=True)
    
    col_nav1, col_nav2 = st.columns(2)
    if col_nav1.button("📊 Ver Tabela"): st.session_state.page = 'visualizacao'; st.rerun()
    if col_nav2.button("⬅️ Sair"): st.session_state.page = 'login'; st.rerun()

    with st.form("form_aurora"):
        # Seção 1: Identificação
        c1, c2 = st.columns(2)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        data_sel = st.date_input("Data", datetime.now(), format="DD/MM/YYYY")
        
        # Seção 2: Logística e Classificação
        st.markdown("<div class='section-HR'>LOGÍSTICA / CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        c3, c4, c5 = st.columns(3)
        s_patio = c3.text_input("Saída Pátio", placeholder="00:00:00")
        c_etc = c4.text_input("Chegada ETC", placeholder="00:00:00")
        tt_viagem = c5.text_input("TT Viagem", placeholder="00:00:00")

        c6, c7, c8 = st.columns(3)
        e_class = c6.text_input("Ent. Classif.", placeholder="00:00:00")
        s_class = c7.text_input("Saí. Classif.", placeholder="00:00:00")
        tt_classif = c8.text_input("TT Classif.", placeholder="00:00:00")

        # Seção 3: Balanças e Tombador
        st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
        c9, c10, c11 = st.columns(3)
        e_bal1 = c9.text_input("Ent. Bal. 1", placeholder="00:00:00")
        s_bal1 = c10.text_input("Saí. Bal. 1", placeholder="00:00:00")
        tt_bal1 = c11.text_input("TT Bal. 1", placeholder="00:00:00")

        c12, c13, c14 = st.columns(3)
        e_tom = c12.text_input("Ent. Tomb.", placeholder="00:00:00")
        s_tom = c13.text_input("Saí. Tomb.", placeholder="00:00:00")
        tt_tomb = c14.text_input("TT Tomb.", placeholder="00:00:00")

        c15, c16, c17 = st.columns(3)
        e_bal2 = c15.text_input("Ent. Bal. 2", placeholder="00:00:00")
        s_bal2 = c16.text_input("Saí. Bal. 2", placeholder="00:00:00")
        tt_bal2 = c17.text_input("TT Bal. 2", placeholder="00:00:00")

        # Seção 4: Fechamento
        st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
        c18, c19, c20 = st.columns(3)
        s_etc_final = c18.text_input("Saída ETC", placeholder="00:00:00")
        tt_total = c19.text_input("TT Total", placeholder="00:00:00")
        p_liq = c20.text_input("Peso Líq.")

        if st.form_submit_button("SALVAR REGISTRO"):
            novo = {
                "PLACA": placa.upper(), "CAMINHÃO": caminhao.upper(), "DATA": data_sel.strftime("%d/%m/%Y"),
                "SAÍDA PÁTIO": s_patio, "CHEGADA ETC": c_etc, "TT VIAGEM": tt_viagem,
                "ENT. CLASSIF": e_class, "SAÍ. CLASSIF": s_class, "TT CLASSIF": tt_classif,
                "ENT. BAL 1": e_bal1, "SAÍ. BAL 1": s_bal1, "TT BAL 1": tt_bal1,
                "ENT. TOMB": e_tom, "SAÍ. TOMB": s_tom, "TT TOMB": tt_tomb,
                "ENT. BAL 2": e_bal2, "SAÍ. BAL 2": s_bal2, "TT BAL 2": tt_bal2,
                "SAÍDA ETC": s_etc_final, "TT OPERAÇÃO": tt_total, "PESO LÍQUIDO": p_liq
            }
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ Salvo!")
            st.rerun()

    inject_mask()

# --- TELA DE VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    if st.button("⬅️ Voltar"): st.session_state.page = 'lancamento'; st.rerun()
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
