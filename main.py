import streamlit as st
import base64
import json
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# BLOCO 1: CONFIGURAÇÕES E ESTILIZAÇÃO (CSS)
# ==========================================
st.set_page_config(page_title="Zion Tecnologia", layout="wide", initial_sidebar_state="collapsed")

def aplicar_estilo(cor_fundo):
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {cor_fundo}; }}
        
        /* Título do Menu */
        .titulo-menu {{
            color: white; text-align: center; font-size: 55px; font-weight: bold; margin-bottom: 40px;
            text-shadow: 2px 2px 4px #000000;
        }}

        /* Botões Laranja 3D */
        div.stButton > button {{
            background-color: #FF8C00; color: white; font-weight: bold; border-radius: 12px;
            border: none; width: 100%; height: 90px; font-size: 20px;
            box-shadow: 0px 8px 0px #CC7000; transition: all 0.1s ease;
            margin-bottom: 5px;
        }}
        div.stButton > button:active {{
            box-shadow: 0px 2px 0px #CC7000; transform: translateY(6px);
        }}
        
        /* Centralização de ícones e legendas */
        .icon-box {{ text-align: center; color: white; font-size: 40px; margin-bottom: 20px; }}
        .label-icon {{ font-size: 14px; font-weight: normal; margin-top: -10px; }}

        /* Botão Voltar (Estilo Diferente) */
        .btn-voltar-container {{ display: flex; justify-content: center; margin-top: 50px; }}
        .stButton > button[kind="secondary"] {{
            background-color: #4A4A4A; box-shadow: 0px 5px 0px #222; height: 50px; width: 200px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# BLOCO 2: CONEXÃO COM BANCO DE DADOS (ZION)
# ==========================================
def conectar_zion():
    try:
        # Usa a conexão Base64 que validamos
        b64_content = st.secrets["gcp_service_account"]["content"]
        json_info = json.loads(base64.b64decode(b64_content).decode('utf-8'))
        json_info["private_key"] = json_info["private_key"].replace("\\n", "\n")
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(json_info, scopes=scopes)
        return gspread.authorize(creds).open("Zion")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

# Controle de Navegação
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

# ==========================================
# BLOCO 3: TELA INICIAL (CINZA/PRATA)
# ==========================================
if st.session_state['pagina'] == 'inicio':
    aplicar_estilo("#C0C0C0") # Cinza Prata
    
    st.markdown("""
        <div style="text-align: center; margin-top: 5%;">
            <h1 style="font-size: 60px;">Seja Bem Vindo</h1>
            <h2 style="font-size: 40px;">ao</h2>
            <h1 style="font-size: 60px;">Zion Tecnologia</h1>
            <br><br>
            <h3 style="font-size: 30px; margin-top: 50px;">Transdourado</h3>
        </div>
    """, unsafe_allow_html=True)
    
    for _ in range(8): st.write("")
    
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("ACESSO"):
            st.session_state['pagina'] = 'menu'
            st.rerun()

# ==========================================
# BLOCO 4: TELA DE MENU (AZUL ROYAL) - ÍCONES CENTRALIZADOS
# ==========================================
elif st.session_state['pagina'] == 'menu':
    # Reaplica o estilo para garantir o fundo Azul Royal
    aplicar_estilo("#002366")
    
    st.markdown('<h1 class="titulo-menu">MENU</h1>', unsafe_allow_html=True)
    
    # Grid de botões (3 colunas)
    col1, col2, col3 = st.columns(3)
    
    # Lista organizada: (Nome do Botão, Ícone, Legenda, Coluna)
    botoes = [
        ("Logistica Patio / ETC", "🚚", "Gestão de Pátio", col1),
        ("Classificação", "📋", "Qualidade", col2),
        ("Balança", "⚖️", "Pesagem", col3),
        ("Tombador", "🏗️", "Descarga", col1),
        ("Tabela Ent/Said", "📊", "Registros", col2),
        ("Dashboard", "📈", "Indicadores", col3)
    ]

    for nome, icone, desc, coluna in botoes:
        with coluna:
            # Renderiza o botão
            st.button(nome)
            
            # Renderiza o ícone e a legenda CENTRALIZADOS via HTML/CSS
            st.markdown(f"""
                <div style="
                    display: flex; 
                    flex-direction: column; 
                    align-items: center; 
                    justify-content: center; 
                    width: 100%; 
                    margin-top: 10px; 
                    margin-bottom: 30px;
                    color: white;
                ">
                    <span style="font-size: 45px;">{icone}</span>
                    <span style="font-size: 14px; opacity: 0.8; font-weight: bold;">{desc}</span>
                </div>
            """, unsafe_allow_html=True)

    # --- BOTÃO VOLTAR CENTRALIZADO NO RODAPÉ ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("---")
    
    # Colunas para centralizar o botão de voltar
    _, col_central, _ = st.columns([2, 1, 2])
    with col_central:
        st.markdown('<div class="btn-voltar-estilo">', unsafe_allow_html=True)
        if st.button("VOLTAR PARA LOGIN"):
            st.session_state['pagina'] = 'inicio'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
