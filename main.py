import streamlit as st

# 1. Configuração da página (DEVE ser a primeira coisa)
st.set_page_config(page_title="Sistema Zion", layout="wide")

# 2. ESTILIZAÇÃO (Corrigido para não dar erro)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #C0C0C0;
    }
    
    /* Estilo para o botão no canto inferior */
    div.stButton > button {
        background-color: #4A4A4A;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True  # O erro estava aqui!
)

# 3. CONTEÚDO
st.title("SISTEMA ZION")

# 4. BOTÃO NO CANTO INFERIOR ESQUERDO
# Criamos um espaço vazio para empurrar o botão para baixo
for _ in range(15):
    st.write("")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("ACESSO"):
        st.session_state['pagina'] = 'dashboard'
        st.rerun()
