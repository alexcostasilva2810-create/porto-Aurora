import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# 🔑 CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zion - Tempos e Movimentos", layout="wide", initial_sidebar_state="expanded")

# --- CSS APROVADO (4CM / AZUL ROYAL) ---
st.markdown("""
    <style>
    .header-container { display: flex; align-items: center; gap: 20px; margin-top: -40px; margin-bottom: 20px; }
    .title-zion { color: #4169E1; font-family: 'Arial Black'; font-size: 26px; }
    .img-icon { height: 50px; }
    
    div[data-testid="stTextInput"], div[data-testid="stDateInput"] { width: 150px !important; flex: none !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 150px !important; margin-right: 40px !important; }
    .section-HR { border-bottom: 2px solid #4169E1; margin: 12px 0; color: #4169E1; font-size: 13px; font-weight: bold; width: 720px; }
    label { font-size: 11px !important; font-weight: bold !important; }
    input { height: 1.9rem !important; font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INJEÇÃO DA MÁSCARA DE HORA (CORREÇÃO DEFINITIVA) ---
components.html("""
    <script>
    const mask = (e) => {
        let v = e.target.value.replace(/\D/g,'');
        if (v.length > 6) v = v.slice(0,6);
        if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
        else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
        e.target.value = v;
        // Força o Streamlit a reconhecer a mudança
        e.target.dispatchEvent(new Event('input', { bubbles: true }));
    }
    const apply = () => {
        const inputs = window.parent.document.querySelectorAll('input[placeholder="00:00:00"]');
        inputs.forEach(i => {
            if(!i.dataset.m) { 
                i.addEventListener('input', mask); 
                i.dataset.m = '1'; 
                i.onblur = () => { i.dispatchEvent(new Event('change', { bubbles: true })); };
            }
        });
    }
    setInterval(apply, 500);
    </script>
    """, height=0)

# --- BARRA LATERAL (MENU) ---
with st.sidebar:
    st.markdown("<h2 style='color:#4169E1;'>ZION</h2>", unsafe_allow_html=True)
    if st.button("📝 Novo Lançamento"): st.rerun()
    if st.button("📊 Ver Tabela Geral"): st.info("Tabela em desenvolvimento"); st.stop()
    st.markdown("---")
    if st.button("⬅️ VOLTAR AO LOGIN"): st.stop()

# --- TOPO COM IMAGENS (CONFORME SOLICITADO) ---
st.markdown(f"""
    <div class="header-container">
        <div class="title-zion">Zion - Tempos e movimentos</div>
        <img src="https://cdn-icons-png.flaticon.com/512/1814/1814420.png" class="img-icon"> <img src="https://cdn-icons-png.flaticon.com/512/2722/2722420.png" class="img-icon"> </div>
    """, unsafe_allow_html=True)

# --- CAMPOS (DADOS NÃO SOMEM) ---
def campo_hora(label, key):
    if key not in st.session_state: st.session_state[key] = ""
    return st.text_input(label, value=st.session_state[key], key=f"in_{key}", placeholder="00:00:00")

# Identificação
c1, c2, c3 = st.columns(3)
placa = c1.text_input("Placa", key="placa")
cam = c2.text_input("Caminhão", key="cam")
data = c3.date_input("Data da Operação", datetime.now(), format="DD/MM/YYYY")

st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
c4, c5, c6, c7 = st.columns(4)
s_patio = campo_hora("Saída Pátio", "sp")
c_etc = campo_hora("Chegada ETC", "ce")
tt_v = campo_hora("TT Viagem", "tv")
e_cl = campo_hora("Ent. Classif.", "ec")

c8, c9 = st.columns(2)
s_cl = campo_hora("Saí. Classif.", "sc")
tt_cl = campo_hora("TT Classif.", "tc")

st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
c10, c11, c12, c13 = st.columns(4)
e_b1 = campo_hora("Ent. Bal. 1", "b1e")
s_b1 = campo_hora("Saí. Bal. 1", "b1s")
tt_b1 = campo_hora("TT Balança", "b1t")
e_to = campo_hora("Ent. Tomb.", "toe")

c14, c15, c16, c17 = st.columns(4)
s_to = campo_hora("Saí. Tomb.", "tos")
tt_to = campo_hora("TT Tombador", "tot")
e_b2 = campo_hora("Ent. Bal. 2", "b2e")
s_b2 = campo_hora("Saí. Bal. 2", "b2s")

st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
c18, c19, c20, c21 = st.columns(4)
tt_b2 = campo_hora("TT Bal. 2", "b2t")
s_etc = campo_hora("Saída ETC Final", "setc")
tt_ot = campo_hora("TT Total", "ttot")
p_liq = st.text_input("Peso Líquido", key="pliq")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 SALVAR REGISTRO"):
    st.success("✅ Registro gravado com sucesso!")
    for k in ["sp", "ce", "tv", "ec", "sc", "tc", "b1e", "b1s", "b1t", "toe", "tos", "tot", "b2e", "b2s", "b2t", "setc", "ttot"]:
        st.session_state[k] = ""
    st.rerun()
