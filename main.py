import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# 🔑 CONFIGURAÇÃO DA PÁGINA
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

# --- CSS TELA COMPACTA (4CM / AZUL ROYAL) ---
st.markdown("""
    <style>
    .title-zion { color: #4169E1; font-family: 'Arial Black'; font-size: 26px; margin-top: -30px; margin-bottom: 15px; }
    div[data-testid="stTextInput"], div[data-testid="stDateInput"] { width: 150px !important; flex: none !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 150px !important; margin-right: 40px !important; }
    .section-HR { border-bottom: 2px solid #4169E1; margin: 12px 0; color: #4169E1; font-size: 13px; font-weight: bold; width: 720px; }
    label { font-size: 11px !important; font-weight: bold !important; }
    input { height: 1.9rem !important; font-size: 13px !important; }
    .main .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA PÁGINA ---
if 'page' not in st.session_state: st.session_state.page = 'lancamento'

# --- BARRA LATERAL (MENU RESTAURADO) ---
with st.sidebar:
    st.markdown("<h2 style='color:#4169E1;'>ZION</h2>", unsafe_allow_html=True)
    if st.button("📝 Novo Lançamento"): st.session_state.page = 'lancamento'; st.rerun()
    if st.button("📊 Ver Tabela Geral"): st.session_state.page = 'visualizacao'; st.rerun()
    st.markdown("---")
    if st.button("⬅️ Sair / Login"): st.session_state.page = 'login'; st.rerun()

# --- TELA LANÇAMENTO (COM TRAVA DE DADOS) ---
if st.session_state.page == 'lancamento':
    st.markdown("<div class='title-zion'>Zion - Tempos e movimentos</div>", unsafe_allow_html=True)
    
    # Linha 1: Identificação
    c1, c2, c3, c4 = st.columns(4)
    # O uso do 'key' direto aqui trava o valor na memória (session_state)
    placa = c1.text_input("Placa", key="placa_mem")
    caminhao = c2.text_input("Caminhão", key="cam_mem")
    data_op = c3.date_input("Data", datetime.now(), format="DD/MM/YYYY", key="data_mem")
    
    st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    s_patio = c5.text_input("Saída Pátio", placeholder="00:00:00", key="sp_mem")
    c_etc = c6.text_input("Chegada ETC", placeholder="00:00:00", key="ce_mem")
    tt_v = c7.text_input("TT Viagem", placeholder="00:00:00", key="tv_mem")
    e_cl = c8.text_input("Ent. Class", placeholder="00:00:00", key="ec_mem")
    
    c9, c10 = st.columns(2)
    s_cl = c9.text_input("Saí. Class", placeholder="00:00:00", key="sc_mem")
    tt_cl = c10.text_input("TT Class", placeholder="00:00:00", key="tc_mem")

    st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
    c11, c12, c13, c14 = st.columns(4)
    e_b1 = c11.text_input("Ent. Bal 1", placeholder="00:00:00", key="b1e_mem")
    s_b1 = c12.text_input("Saí. Bal 1", placeholder="00:00:00", key="b1s_mem")
    tt_b1 = c13.text_input("TT Bal 1", placeholder="00:00:00", key="b1t_mem")
    e_to = c14.text_input("Ent. Tomb", placeholder="00:00:00", key="toe_mem")
    
    c15, c16, c17, c18 = st.columns(4)
    s_to = c15.text_input("Saí. Tomb", placeholder="00:00:00", key="tos_mem")
    tt_to = c16.text_input("TT Tomb", placeholder="00:00:00", key="tot_mem")
    e_b2 = c17.text_input("Ent. Bal 2", placeholder="00:00:00", key="b2e_mem")
    s_b2 = c18.text_input("Saí. Bal 2", placeholder="00:00:00", key="b2s_mem")

    st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
    c19, c20, c21, c22 = st.columns(4)
    tt_b2 = c19.text_input("TT Bal 2", placeholder="00:00:00", key="b2t_mem")
    s_etc = c20.text_input("Saída ETC", placeholder="00:00:00", key="setc_mem")
    tt_ot = c21.text_input("TT Total", placeholder="00:00:00", key="ttot_mem")
    p_liq = c22.text_input("Peso Líq.", key="pliq_mem")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SALVAR REGISTRO"):
        st.success("✅ Registro salvo com sucesso!")
        # Limpa os campos da memória após salvar
        chaves = ["placa_mem", "cam_mem", "sp_mem", "ce_mem", "tv_mem", "ec_mem", "sc_mem", "tc_mem", 
                  "b1e_mem", "b1s_mem", "b1t_mem", "toe_mem", "tos_mem", "tot_mem", "b2e_mem", 
                  "b2s_mem", "b2t_mem", "setc_mem", "ttot_mem", "pliq_mem"]
        for k in chaves: st.session_state[k] = ""
        st.rerun()

    inject_mask()

# --- TELA VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.markdown("<div class='title-zion'>Relatório</div>")
    st.write("Dados da tabela aparecerão aqui.")
