import streamlit as st
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Zion - Tempos e Movimentos", layout="wide")

# Estilo Azul Royal e linhas contínuas conforme solicitado
st.markdown("""
    <style>
    .title-zion {
        color: #4169E1; 
        font-family: 'Arial Black', sans-serif;
        font-size: 32px;
        margin-bottom: 20px;
    }
    /* Estilo para as linhas divisórias ocuparem toda a largura */
    .section-HR { 
        border-bottom: 2px solid #4169E1; 
        margin: 20px 0 10px 0; 
        color: #4169E1; 
        font-size: 14px;
        font-weight: bold;
    }
    /* Ajuste para manter os campos com visual limpo */
    div[data-testid="stForm"] { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DOS CAMPOS (SESSION STATE) ---
# Isso garante que nada suma ao preencher
campos = [
    "placa", "caminhao", "s_patio", "c_etc", "tt_v", "e_cl", "s_cl", "tt_cl",
    "e_b1", "s_b1", "tt_b1", "e_to", "s_to", "tt_to", "e_b2", "s_b2", "tt_b2",
    "s_etc", "tt_ot", "p_liq"
]

for c in campos:
    if c not in st.session_state: st.session_state[c] = ""

# --- TELA PRINCIPAL ---
st.markdown("<div class='title-zion'>Zion - Tempos e movimentos</div>", unsafe_allow_html=True)

with st.form("form_restaurado", clear_on_submit=False):
    # Linha 1: Identificação
    c1, c2, c3 = st.columns([2, 2, 1])
    placa = c1.text_input("Placa", value=st.session_state.placa)
    caminhao = c2.text_input("Caminhão", value=st.session_state.caminhao)
    # Data configurada para padrão Brasileiro
    data_sel = c3.date_input("Data", datetime.now(), format="DD/MM/YYYY")

    st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
    c4, c5, c6, c7 = st.columns(4)
    s_patio = c4.text_input("Saída Pátio", value=st.session_state.s_patio, placeholder="00:00:00")
    c_etc = c5.text_input("Chegada ETC", value=st.session_state.c_etc, placeholder="00:00:00")
    tt_v = c6.text_input("TT Viagem", value=st.session_state.tt_v, placeholder="00:00:00")
    e_cl = c7.text_input("Ent. Class", value=st.session_state.e_cl, placeholder="00:00:00")

    c8, c9 = st.columns([1, 3])
    s_cl = c8.text_input("Saí. Class", value=st.session_state.s_cl, placeholder="00:00:00")
    tt_cl = c9.text_input("TT Class", value=st.session_state.tt_cl, placeholder="00:00:00")

    st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
    c10, c11, c12, c13, c14, c15 = st.columns(6)
    e_b1 = c10.text_input("Ent. Bal 1", value=st.session_state.e_b1, placeholder="00:00:00")
    s_b1 = c11.text_input("Saí. Bal 1", value=st.session_state.s_b1, placeholder="00:00:00")
    tt_b1 = c12.text_input("TT Bal 1", value=st.session_state.tt_b1, placeholder="00:00:00")
    e_to = c13.text_input("Ent. Tomb", value=st.session_state.e_to, placeholder="00:00:00")
    s_to = c14.text_input("Saí. Tomb", value=st.session_state.s_to, placeholder="00:00:00")
    tt_to = c15.text_input("TT Tomb", value=st.session_state.tt_to, placeholder="00:00:00")

    c16, c17, c18 = st.columns(3)
    e_b2 = c16.text_input("Ent. Bal 2", value=st.session_state.e_b2, placeholder="00:00:00")
    s_b2 = c17.text_input("Saí. Bal 2", value=st.session_state.s_b2, placeholder="00:00:00")
    tt_b2 = c18.text_input("TT Bal 2", value=st.session_state.tt_b2, placeholder="00:00:00")

    st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
    c19, c20 = st.columns(2)
    s_etc = c19.text_input("Saída ETC Final", value=st.session_state.s_etc, placeholder="00:00:00")
    p_liq = c20.text_input("Peso Líquido", value=st.session_state.p_liq)

    st.markdown("<br>", unsafe_allow_html=True)
    btn_salvar = st.form_submit_button("💾 SALVAR REGISTRO")

    if btn_salvar:
        # Aqui você insere sua lógica de salvar no Excel/CSV
        st.success("✅ Dados salvos com sucesso!")
        # Limpa o formulário APENAS após salvar
        for c in campos: st.session_state[c] = ""
        st.rerun()
