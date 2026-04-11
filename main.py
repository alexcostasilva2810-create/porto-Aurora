import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# 🔑 CONFIGURAÇÃO
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: FUNDO PORTUÁRIO (IMAGEM ENVIADA) E ESTILO ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2070&auto=format&fit=crop"); /* Substituir pela sua imagem local se necessário */
        background-size: cover;
    }}
    .title-zion {{ color: #4169E1; font-family: 'Arial Black'; font-size: 30px; text-align: center; background: white; padding: 10px; border-radius: 10px; margin-bottom: 20px; }}
    .menu-card {{ background: rgba(255,255,255,0.9); padding: 20px; border-radius: 15px; border-left: 8px solid #4169E1; text-align: center; margin-bottom: 10px; }}
    div[data-testid="stTextInput"] {{ width: 150px !important; }}
    .section-HR {{ border-bottom: 2px solid #4169E1; margin: 15px 0; color: #4169E1; font-weight: bold; width: 720px; }}
    </style>
    """, unsafe_allow_html=True)

# --- MÁSCARA JS (TRAVA A HORA SEM SUMIR) ---
components.html("""
    <script>
    const mask = (e) => {
        let v = e.target.value.replace(/\D/g,'');
        if (v.length > 6) v = v.slice(0,6);
        if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
        else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
        e.target.value = v;
    }
    setInterval(() => {
        window.parent.document.querySelectorAll('input[placeholder="00:00:00"]').forEach(i => {
            if(!i.dataset.m) { 
                i.addEventListener('input', mask); 
                i.dataset.m = '1';
                // Garante que o valor não suma ao perder o foco
                i.onblur = (e) => { i.dispatchEvent(new Event('change', { bubbles: true })); };
            }
        });
    }, 500);
    </script>
    """, height=0)

# --- NAVEGAÇÃO ---
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'dados' not in st.session_state: st.session_state.dados = {}

# --- TELA 1: LOGIN ---
if st.session_state.page == 'login':
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div class='title-zion'>ZION - ACESSO PORTUÁRIO</div>", unsafe_allow_html=True)
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ENTRAR", use_container_width=True):
            st.session_state.page = 'menu'; st.rerun()

# --- TELA 2: MENU COM ÍCONES ---
elif st.session_state.page == 'menu':
    st.markdown("<div class='title-zion'>MENU DE OPERAÇÕES</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='menu-card'><h3>🚚</h3><b>LOGÍSTICA</b></div>", unsafe_allow_html=True)
        if st.button("Abrir Estação 1", use_container_width=True): st.session_state.page = 'est_log'; st.rerun()
        
    with col2:
        st.markdown("<div class='menu-card'><h3>⚖️</h3><b>BALANÇA / TOMB.</b></div>", unsafe_allow_html=True)
        if st.button("Abrir Estação 2", use_container_width=True): st.session_state.page = 'est_bal'; st.rerun()
        
    with col3:
        st.markdown("<div class='menu-card'><h3>📝</h3><b>FECHAMENTO</b></div>", unsafe_allow_html=True)
        if st.button("Abrir Estação 3", use_container_width=True): st.session_state.page = 'est_fec'; st.rerun()

# --- TELA 3: ESTAÇÃO LOGÍSTICA ---
elif st.session_state.page == 'est_log':
    st.markdown("<div class='title-zion'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
    if st.button("⬅️ Voltar"): st.session_state.page = 'menu'; st.rerun()
    
    c1, c2, c3 = st.columns(3)
    st.session_state.dados['placa'] = c1.text_input("PLACA", value=st.session_state.dados.get('placa',''))
    st.session_state.dados['cam'] = c2.text_input("CAMINHÃO", value=st.session_state.dados.get('cam',''))
    st.date_input("DATA DA OPERAÇÃO", format="DD/MM/YYYY")
    
    st.markdown("<div class='section-HR'>HORÁRIOS INICIAIS</div>", unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    st.session_state.dados['sp'] = c4.text_input("Saída Pátio", placeholder="00:00:00", value=st.session_state.dados.get('sp',''))
    st.session_state.dados['ce'] = c5.text_input("Chegada ETC", placeholder="00:00:00", value=st.session_state.dados.get('ce',''))
    
    if st.button("💾 SALVAR ETAPA"): st.success("Dados da Logística salvos!")

# Adicione as outras estações seguindo o mesmo padrão de session_state.dados...
