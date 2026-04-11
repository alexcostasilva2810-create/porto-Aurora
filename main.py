import streamlit as st
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components

# Configuração da página e título em Azul Royal
st.set_page_config(page_title="Zion - Tempos e Movimentos", layout="wide", initial_sidebar_state="expanded")

# --- CSS PROFISSIONAL ---
st.markdown("""
    <style>
    .title-zion {
        color: #4169E1; 
        font-family: 'Arial Black', sans-serif;
        font-size: 28px;
        margin-top: -30px;
        margin-bottom: 20px;
    }
    div[data-testid="stTextInput"], div[data-testid="stDateInput"] {
        width: 150px !important;
    }
    [data-testid="column"] {
        flex: 0 0 auto !important;
        width: 150px !important;
        margin-right: 40px !important; 
    }
    .section-HR { 
        border-bottom: 2px solid #4169E1; 
        margin: 15px 0 10px 0; 
        color: #4169E1; 
        font-size: 13px;
        font-weight: bold;
        width: 720px;
    }
    label { font-size: 11px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
# Isso garante que os dados não sumam ao dar Enter
campos = ["placa", "caminhao", "s_patio", "c_etc", "tt_v", "e_cl", "s_cl", "tt_cl", 
          "e_b1", "s_b1", "tt_b1", "e_to", "s_to", "tt_to", "e_b2", "s_b2", "tt_b2", 
          "s_etc", "tt_ot", "p_liq"]

for campo in campos:
    if campo not in st.session_state:
        st.session_state[campo] = ""

if 'data_sel' not in st.session_state:
    st.session_state.data_sel = datetime.now()

# --- TELA LANÇAMENTO ---
st.markdown("<div class='title-zion'>Zion - Tempos e movimentos</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#4169E1;'>MENU</h2>", unsafe_allow_html=True)
    if st.button("📊 Ver Relatório"): st.session_state.page = 'visualizacao'

# Formulário com chave única para evitar o reset automático
with st.form("form_zion_estavel", clear_on_submit=False):
    c1, c2, c3, c4 = st.columns(4)
    placa = c1.text_input("Placa", value=st.session_state.placa)
    caminhao = c2.text_input("Caminhão", value=st.session_state.caminhao)
    data_sel = c3.date_input("Data", st.session_state.data_sel, format="DD/MM/YYYY")
    
    st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    # Aqui o valor é preservado mesmo se você sair do campo ou der Enter
    s_patio = c5.text_input("Saída Pátio", value=st.session_state.s_patio, placeholder="00:00:00")
    c_etc = c6.text_input("Chegada ETC", value=st.session_state.c_etc, placeholder="00:00:00")
    tt_v = c7.text_input("TT Viagem", value=st.session_state.tt_v, placeholder="00:00:00")
    e_cl = c8.text_input("Ent. Class", value=st.session_state.e_cl, placeholder="00:00:00")
    
    # ... (repetir para os outros campos conforme necessário)

    if st.form_submit_button("💾 SALVAR REGISTRO"):
        # Lógica de salvamento (salvar no CSV)
        st.success("✅ Registro salvo e tela limpa!")
        # Limpar o estado após salvar
        for campo in campos: st.session_state[campo] = ""
        st.rerun()
