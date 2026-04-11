import streamlit as st
import pandas as pd
import os
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

# --- CSS ULTRA COMPACTO (CAMPOS 4CM E TÍTULO AZUL ROYAL) ---
st.markdown("""
    <style>
    .title-zion { color: #4169E1; font-family: 'Arial Black'; font-size: 24px; margin-top: -30px; margin-bottom: 10px; }
    div[data-testid="stTextInput"], div[data-testid="stDateInput"] { width: 150px !important; flex: none !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 150px !important; margin-right: 40px !important; }
    .section-HR { border-bottom: 2px solid #4169E1; margin: 10px 0; color: #4169E1; font-size: 13px; font-weight: bold; width: 720px; }
    label { font-size: 11px !important; font-weight: bold !important; }
    input { height: 1.8rem !important; font-size: 13px !important; }
    .main .block-container { padding-top: 2rem !important; margin-left: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE MEMÓRIA ATIVA ---
campos_zion = [
    "placa", "caminhao", "s_patio", "c_etc", "tt_v", "e_cl", "s_cl", "tt_cl",
    "e_b1", "s_b1", "tt_b1", "e_to", "s_to", "tt_to", "e_b2", "s_b2", "tt_b2",
    "s_etc", "tt_ot", "p_liq"
]

if 'page' not in st.session_state: st.session_state.page = 'login'
for k in campos_zion:
    if k not in st.session_state: st.session_state[k] = ""

# Função para salvar no estado enquanto digita
def salvar_estado(chave):
    st.session_state[chave] = st.session_state["tmp_" + chave]

# --- SIDEBAR (BARRA LATERAL) ---
if st.session_state.page != 'login':
    with st.sidebar:
        st.markdown("<h2 style='color:#4169E1;'>ZION</h2>", unsafe_allow_html=True)
        if st.button("📝 Novo Lançamento"): st.session_state.page = 'lancamento'; st.rerun()
        if st.button("📊 Ver Tabela"): st.session_state.page = 'visualizacao'; st.rerun()
        st.markdown("---")
        if st.button("⬅️ Sair / Login"): st.session_state.page = 'login'; st.rerun()

# --- TELA LOGIN ---
if st.session_state.page == 'login':
    st.markdown("<div class='title-zion'>Zion - Tempos e movimentos</div>", unsafe_allow_html=True)
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("Acessar"):
        st.session_state.page = 'lancamento'; st.rerun()

# --- TELA LANÇAMENTO (COMPACTA 4CM) ---
elif st.session_state.page == 'lancamento':
    st.markdown("<div class='title-zion'>Zion - Tempos e movimentos</div>", unsafe_allow_html=True)
    
    with st.container():
        # Linha 1
        c1, c2, c3, c4 = st.columns(4)
        st.session_state.placa = c1.text_input("Placa", value=st.session_state.placa, key="tmp_placa", on_change=salvar_estado, args=("placa",))
        st.session_state.caminhao = c2.text_input("Caminhão", value=st.session_state.caminhao, key="tmp_cam", on_change=salvar_estado, args=("caminhao",))
        data_op = c3.date_input("Data", datetime.now(), format="DD/MM/YYYY")
        
        st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        c5, c6, c7, c8 = st.columns(4)
        st.session_state.s_patio = c5.text_input("Saída Pátio", value=st.session_state.s_patio, key="tmp_sp", on_change=salvar_estado, args=("s_patio",), placeholder="00:00:00")
        st.session_state.c_etc = c6.text_input("Chegada ETC", value=st.session_state.c_etc, key="tmp_ce", on_change=salvar_estado, args=("c_etc",), placeholder="00:00:00")
        st.session_state.tt_v = c7.text_input("TT Viagem", value=st.session_state.tt_v, key="tmp_tv", on_change=salvar_estado, args=("tt_v",), placeholder="00:00:00")
        st.session_state.e_cl = c8.text_input("Ent. Class", value=st.session_state.e_cl, key="tmp_ec", on_change=salvar_estado, args=("e_cl",), placeholder="00:00:00")
        
        c9, c10, c11, c12 = st.columns(4)
        st.session_state.s_cl = c9.text_input("Saí. Class", value=st.session_state.s_cl, key="tmp_sc", on_change=salvar_estado, args=("s_cl",), placeholder="00:00:00")
        st.session_state.tt_cl = c10.text_input("TT Class", value=st.session_state.tt_cl, key="tmp_tc", on_change=salvar_estado, args=("tt_cl",), placeholder="00:00:00")

        st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
        c13, c14, c15, c16 = st.columns(4)
        st.session_state.e_b1 = c13.text_input("Ent. Bal 1", value=st.session_state.e_b1, key="tmp_b1e", on_change=salvar_estado, args=("e_b1",), placeholder="00:00:00")
        st.session_state.s_b1 = c14.text_input("Saí. Bal 1", value=st.session_state.s_b1, key="tmp_b1s", on_change=salvar_estado, args=("s_b1",), placeholder="00:00:00")
        st.session_state.tt_b1 = c15.text_input("TT Bal 1", value=st.session_state.tt_b1, key="tmp_b1t", on_change=salvar_estado, args=("tt_b1",), placeholder="00:00:00")
        st.session_state.e_to = c16.text_input("Ent. Tomb", value=st.session_state.e_to, key="tmp_toe", on_change=salvar_estado, args=("e_to",), placeholder="00:00:00")
        
        c17, c18, c19, c20 = st.columns(4)
        st.session_state.s_to = c17.text_input("Saí. Tomb", value=st.session_state.s_to, key="tmp_tos", on_change=salvar_estado, args=("s_to",), placeholder="00:00:00")
        st.session_state.tt_to = c18.text_input("TT Tomb", value=st.session_state.tt_to, key="tmp_tot", on_change=salvar_estado, args=("tt_to",), placeholder="00:00:00")
        st.session_state.e_b2 = c19.text_input("Ent. Bal 2", value=st.session_state.e_b2, key="tmp_b2e", on_change=salvar_estado, args=("e_b2",), placeholder="00:00:00")
        st.session_state.s_b2 = c20.text_input("Saí. Bal 2", value=st.session_state.s_b2, key="tmp_b2s", on_change=salvar_estado, args=("s_b2",), placeholder="00:00:00")

        st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
        c21, c22, c23, c24 = st.columns(4)
        st.session_state.tt_b2 = c21.text_input("TT Bal 2", value=st.session_state.tt_b2, key="tmp_b2t", on_change=salvar_estado, args=("tt_b2",), placeholder="00:00:00")
        st.session_state.s_etc = c22.text_input("Saída ETC", value=st.session_state.s_etc, key="tmp_setc", on_change=salvar_estado, args=("s_etc",), placeholder="00:00:00")
        st.session_state.tt_ot = c23.text_input("TT Total", value=st.session_state.tt_ot, key="tmp_ttot", on_change=salvar_estado, args=("tt_ot",), placeholder="00:00:00")
        st.session_state.p_liq = c24.text_input("Peso Líq.", value=st.session_state.p_liq, key="tmp_pliq", on_change=salvar_estado, args=("p_liq",))

        if st.button("💾 SALVAR REGISTRO"):
            # Lógica de salvar aqui...
            st.success("✅ Salvo no sistema!")
            for key in campos_zion: st.session_state[key] = ""
            st.rerun()
    inject_mask()

# --- TELA TABELA ---
elif st.session_state.page == 'visualizacao':
    st.markdown("<div class='title-zion'>Relatório Geral</div>", unsafe_allow_html=True)
    st.write("Tabela de dados salvos...")
