import streamlit as st

# 1. Configuração da página
st.set_page_config(page_title="Sistema Zion", layout="wide")

# 2. ESTILIZAÇÃO (Fundo Prata e Botão Customizado)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #C0C0C0;
    }
    
    /* Estilo do botão ACESSO */
    div.stButton > button {
        background-color: #4A4A4A;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
    }

    /* Ajuste para o texto centralizado */
    .central-text {
        font-size: 45px;
        font-weight: bold;
        line-height: 1.2;
        margin-top: 50px;
    }
    
    .transdourado {
        font-size: 25px;
        margin-top: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. CONTEÚDO CENTRALIZADO
# Usamos HTML para garantir o alinhamento exato que você pediu
st.markdown(
    """
    <div style="text-align: center; margin-top: 5%;">
        <h1 style="font-size: 60px;">Seja Bem Vindo</h1>
        <h2 style="font-size: 40px;">ao</h2>
        <h1 style="font-size: 60px;">Zion Tecnologia</h1>
        <br><br>
        <h3 style="font-size: 30px; margin-top: 50px;">Transdourado</h3>
    </div>
    """, 
    unsafe_allow_html=True
)

# 4. TÍTULO NO CANTO (SISTEMA ZION) E BOTÃO INFERIOR
# O título "SISTEMA ZION" que já aparecia na sua imagem
st.sidebar.markdown("# SISTEMA ZION")

# Espaçador para mandar o botão para o fundo
for _ in range(10):
    st.write("")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("ACESSO"):
        st.session_state['logado'] = True
        st.success("Conectando ao banco de dados Zion...")
        # Aqui a gente vai chamar a conexão Base64 que validamos antes
