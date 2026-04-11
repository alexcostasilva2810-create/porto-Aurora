import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Aurora Port - Grãos", layout="wide")

# Estilização CSS para a "Capa Bonita"
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #004b87;
        color: white;
    }
    .title-text {
        text-align: center;
        color: #004b87;
        font-family: 'Arial Black';
        font-size: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Arquivo de Dados
DB_FILE = "dados_porto.csv"
COLUNAS = [
    "SAÍDA DO PÁTIO", "CHEGADA ETC", "TT VIAGEM", "ENTR. CLASSIFIC", 
    "SAÍDA CLASSIFICAÇÃO", "TT CLASSIFIC", "ENTR. BALANÇA", "SAÍDA BALANÇA", 
    "TT BALANÇA", "ENTRADA TOMBADOR", "SAÍDA TOMBADOR", "TT TOMBADOR"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUNAS).to_csv(DB_FILE, index=False)

# Controle de Navegação
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- TELA 1: LOGIN ---
if st.session_state.page == 'login':
    st.markdown("<h1 class='title-text'>AURORA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Sistema de Monitoramento de Tempos e Movimentos</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("ACESSAR"):
            st.session_state.page = 'lancamento'
            st.rerun()

# --- TELA 2: LANÇAMENTOS ---
elif st.session_state.page == 'lancamento':
    st.sidebar.title("Menu Aurora")
    if st.sidebar.button("Visualizar Tabela"):
        st.session_state.page = 'visualizacao'
        st.rerun()

    st.markdown("## 📝 Novo Lançamento")
    
    with st.form("form_dados"):
        cols = st.columns(3)
        dados = {}
        for i, nome in enumerate(COLUNAS):
            dados[nome] = cols[i % 3].text_input(nome)
        
        if st.form_submit_button("SALVAR"):
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ Lançado com sucesso!")

# --- TELA 3: VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.sidebar.button("Voltar para Lançamentos", on_click=lambda: st.session_state.update(page='lancamento'))
    st.markdown("## 📊 Registros - Porto Aurora")
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
