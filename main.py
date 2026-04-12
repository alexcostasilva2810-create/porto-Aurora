import streamlit as st
import base64
import json

# ==========================================
# BLOCO 1: MOLDURA SMARTPHONE E ESTILO NITIDEZ
# ==========================================
st.set_page_config(page_title="Zion Mobile", layout="centered")

def aplicar_visual_celular(cor_fundo_interna):
    st.markdown(f"""
        <style>
        /* Fundo externo escuro para destacar o celular */
        .stApp {{
            background-color: #121212;
        }}

        /* Container que simula o corpo do celular */
        .main .block-container {{
            max-width: 380px;
            min-height: 800px;
            background-color: {cor_fundo_interna};
            border: 12px solid #333; /* Moldura do celular */
            border-radius: 45px;
            padding: 40px 20px;
            margin-top: 20px;
            box-shadow: 0px 0px 30px rgba(0,0,0,0.8);
            position: relative;
        }}

        /* Texto com nitidez máxima (Cor sólida e sombra leve) */
        .texto-nitido {{
            color: #FFFFFF !important;
            text-align: center;
            font-family: 'Helvetica', sans-serif;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            line-height: 1.2;
        }}

        /* Título Amarelo Vibrante */
        .titulo-menu {{
            color: #FFFF00 !important;
            text-align: center;
            font-size: 45px;
            font-weight: 900;
            margin-bottom: 40px;
            text-shadow: 2px 2px 0px #000;
        }}

        /* Botões Laranja 3D */
        div.stButton > button {{
            background-color: #FF8C00;
            color: white;
            font-weight: bold;
            border-radius: 15px;
            border: none;
            width: 100%;
            height: 65px;
            font-size: 18px;
            box-shadow: 0px 6px 0px #CC7000;
            margin-bottom: 25px; /* Distância de 3cm visual */
            transition: all 0.1s ease;
        }}
        div.stButton > button:active {{
            box-shadow: 0px 2px 0px #CC7000;
            transform: translateY(4px);
        }}
        </style>
    """, unsafe_allow_html=True)

# Inicializa navegação
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

# ==========================================
# BLOCO 2: TELA INICIAL (MOLDURA CINZA)
# ==========================================
if st.session_state['pagina'] == 'inicio':
    aplicar_visual_celular("#C0C0C0") # Cinza Prata
    
    st.markdown('<div class="texto-nitido">', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 40px; color: #1a1a1a;">Seja Bem Vindo</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 25px; color: #333;">ao</p>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 40px; color: #1a1a1a;">Zion Tecnologia</h1>', unsafe_allow_html=True)
    st.markdown('<br><br><br>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size: 28px; color: #1a1a1a;">Transdourado</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    for _ in range(5): st.write("")
    
    if st.button("ACESSO"):
        st.session_state['pagina'] = 'menu'
        st.rerun()

# ==========================================
# BLOCO 3: TELA DE MENU (MOLDURA AZUL ROYAL)
# ==========================================
elif st.session_state['pagina'] == 'menu':
    aplicar_visual_celular("#002366") # Azul Royal
    
    st.markdown('<h1 class="titulo-menu">MENU</h1>', unsafe_allow_html=True)
    
    # Botões empilhados para Mobile
    if st.button("Logistica Patio / ETC"): pass
    if st.button("Classificação"): pass
    if st.button("Balança"): pass
    if st.button("Tombador"): pass
    if st.button("Tabela Ent/Said"): pass
    if st.button("Dashboard"): pass

    # Botão de Voltar centralizado no pé do celular
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("VOLTAR PARA LOGIN"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()
