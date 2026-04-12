import streamlit as st
import base64
import json

# ==========================================
# BLOCO 1: MÁSCARA DE CELULAR (CSS)
# ==========================================
st.set_page_config(page_title="Zion Mobile", layout="centered")

def aplicar_estilo_mobile(cor_fundo):
    st.markdown(f"""
        <style>
        /* Simula a tela do celular no computador */
        .main .block-container {{
            max-width: 400px;
            padding-top: 2rem;
            padding-bottom: 2rem;
            background-color: {cor_fundo};
            border-radius: 30px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            margin-top: 20px;
            min-height: 85vh;
        }}
        
        /* Ajuste do fundo da página externa */
        .stApp {{
            background-color: #262730; 
        }}

        /* Título Amarelo */
        .titulo-amarelo {{
            color: yellow;
            text-align: center;
            font-family: sans-serif;
            font-weight: bold;
            font-size: 32px;
            margin-bottom: 30px;
        }}

        /* Botões Laranja 3D Estilo Mobile */
        div.stButton > button {{
            background-color: #FF8C00;
            color: white;
            font-weight: bold;
            border-radius: 15px;
            border: none;
            width: 100%;
            height: 60px;
            font-size: 16px;
            box-shadow: 0px 6px 0px #CC7000;
            margin-bottom: 15px; /* Espaço vertical entre botões */
            transition: all 0.1s ease;
        }}
        div.stButton > button:active {{
            box-shadow: 0px 2px 0px #CC7000;
            transform: translateY(4px);
        }}
        
        /* Botão Voltar Cinza no fundo */
        .btn-voltar-mobile button {{
            background-color: #4A4A4A !important;
            box-shadow: 0px 4px 0px #222 !important;
            height: 45px !important;
            margin-top: 40px !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# Controle de Navegação
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

# ==========================================
# BLOCO 2: TELA INICIAL (MÁSCARA CINZA)
# ==========================================
if st.session_state['pagina'] == 'inicio':
    aplicar_estilo_mobile("#C0C0C0")
    
    st.markdown("""
        <div style="text-align: center; color: #333;">
            <h1 style="font-size: 35px; margin-bottom:0;">Seja Bem Vindo</h1>
            <p style="font-size: 20px;">ao</p>
            <h1 style="font-size: 35px;">Zion Tecnologia</h1>
            <br><br><br>
            <h3 style="font-size: 22px;">Transdourado</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Espaçamento para o botão de acesso no final
    for _ in range(8): st.write("")
    
    if st.button("ACESSO"):
        st.session_state['pagina'] = 'menu'
        st.rerun()

# ==========================================
# BLOCO 3: TELA DE MENU (MÁSCARA AZUL ROYAL)
# ==========================================
elif st.session_state['pagina'] == 'menu':
    aplicar_estilo_mobile("#002366")
    
    st.markdown('<h1 class="titulo-amarelo">MENU</h1>', unsafe_allow_html=True)
    
    # No mobile, os botões ficam em uma única coluna centralizada
    if st.button("Logistica Patio / ETC"): pass
    if st.button("Classificação"): pass
    if st.button("Balança"): pass
    if st.button("Tombador"): pass
    if st.button("Tabela Ent/Said"): pass
    if st.button("Dashboard"): pass

    # Botão de Voltar centralizado no final
    st.markdown('<div class="btn-voltar-mobile">', unsafe_allow_html=True)
    if st.button("VOLTAR PARA LOGIN"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
