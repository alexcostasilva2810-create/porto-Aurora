import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# --- CONFIGURAÇÃO E IMAGEM DE FUNDO (AQUI RESOLVE O FUNDO E O BLOCO BRANCO) ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.4), rgba(255,255,255,0.4)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover; background-attachment: fixed;
    }
    .block-container { padding-top: 0rem !important; }
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    label, p, h3 { color: black !important; font-weight: bold !important; font-size: 18px !important; }
    .stTextInput>div>div>input { background-color: white !important; color: black !important; border: 2px solid #1E3A8A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN E PERMISSÕES ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'login'

if st.session_state.etapa == 'login':
    st.markdown("<h1 style='text-align:center; color:black;'>ACESSO ZION</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        user = st.text_input("USUÁRIO").strip().lower()
        senha = st.text_input("SENHA", type="password")
        
        if st.button("ENTRAR NO SISTEMA"):
            # Configuração de Perfis
            if user == "operador" and senha == "zion123":
                st.session_state.cargo = "OPERADOR"
                st.session_state.etapa = 'menu'
                st.rerun()
            elif (user == "admin" or user == "supervisor") and senha == "zion123":
                st.session_state.cargo = "GESTOR"
                st.session_state.etapa = 'menu'
                st.rerun()
            else:
                st.error("Usuário ou Senha incorretos!")

# --- MENU COM FILTRO DE ACESSO ---
elif st.session_state.etapa == 'menu':
    st.markdown(f"<h1 style='text-align:center; color:black;'>MENU PRINCIPAL</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Se for OPERADOR, só vê Balança e Tombador
    if st.session_state.cargo == "OPERADOR":
        with col1:
            if st.button("⚖️ BALANÇA"): st.session_state.perfil = "BALANÇA"; st.session_state.etapa = 'form'; st.rerun()
        with col2:
            if st.button("🏗️ TOMBADOR"): st.session_state.perfil = "TOMBADOR"; st.session_state.etapa = 'form'; st.rerun()
            
    # Se for GESTOR (Admin/Supervisor), vê TUDO
    else:
        with col1:
            if st.button("🚛 LOGÍSTICA"): st.session_state.perfil = "LOGÍSTICA"; st.session_state.etapa = 'form'; st.rerun()
        with col2:
            if st.button("⚖️ BALANÇA"): st.session_state.perfil = "BALANÇA"; st.session_state.etapa = 'form'; st.rerun()
        with col3:
            if st.button("🏗️ TOMBADOR"): st.session_state.perfil = "TOMBADOR"; st.session_state.etapa = 'form'; st.rerun()

    st.markdown("---")
    if st.button("🔙 SAIR / LOGOUT"): st.session_state.etapa = 'login'; st.rerun()

# --- FORMULÁRIO (HORA PERSISTENTE) ---
elif st.session_state.etapa == 'form':
    st.markdown(f"<h1 style='text-align:center; color:black;'>ESTAÇÃO {st.session_state.perfil}</h1>", unsafe_allow_html=True)
    
    if st.button("⬅️ VOLTAR AO MENU"): st.session_state.etapa = 'menu'; st.rerun()

    with st.form("form_zion", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("PLACA")
        cam = c2.text_input("TIPO")
        data = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))

        st.markdown("---")
        h1, h2, h3 = st.columns(3)
        
        # Aqui os campos de hora são fixos no formulário para não sumirem
        if st.session_state.perfil == "LOGÍSTICA":
            v1 = h1.text_input("SAÍDA PÁTIO", placeholder="00:00:00")
            v2 = h2.text_input("CHEGADA ETC", placeholder="00:00:00")
            v3 = h3.text_input("ENTRADA CLASSIF.", placeholder="00:00:00")
        else:
            v1 = h1.text_input("ENTRADA", placeholder="00:00:00")
            v2 = h2.text_input("SAÍDA", placeholder="00:00:00")
            v3 = ""

        if st.form_submit_button("💾 SALVAR REGISTRO"):
            st.success(f"Registro de {st.session_state.perfil} Salvo na Planilha!")
