import streamlit as st

# Configuração da página (deve ser a primeira linha)
st.set_page_config(page_title="Sistema Zion", layout="wide")

# 1. ESTILIZAÇÃO (Cor Prata e Ajustes)
st.markdown(
    """
    <style>
    /* Fundo da aplicação em Prata */
    .stApp {
        background-color: #C0C0C0;
    }
    
    /* Container para empurrar o conteúdo para o fundo da tela */
    .footer-container {
        position: fixed;
        left: 20px;
        bottom: 30px;
    }
    
    /* Estilo customizado para o botão se quiser algo mais específico */
    div.stButton > button {
        background-color: #4A4A4A;
        color: white;
        border-radius: 5px;
        padding: 10px 25px;
    }
    </style>
    """,
    unsafe_allow_stdio=True,
    unsafe_allow_html=True
)

# 2. CONTEÚDO DA TELA
st.title("SISTEMA ZION")
st.subheader("Bem-vindo ao painel de controle.")

# 3. BOTÃO NO CANTO INFERIOR ESQUERDO
# Usamos um container fixado via CSS ou apenas o posicionamento natural com spacers
with st.container():
    # Cria um espaço grande para empurrar o botão para baixo
    for _ in range(20): 
        st.write("")
        
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        if st.button("ACESSO"):
            st.session_state['logado'] = True
            st.rerun()

# Feedback visual simples
if st.session_state.get('logado'):
    st.success("Acesso liberado!")
