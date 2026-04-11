import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# 🔑 CONFIGURAÇÃO DA PÁGINA (Botões laterais mantidos)
st.set_page_config(page_title="Zion - Tempos e Movimentos", layout="wide", initial_sidebar_state="expanded")

# --- MÁSCARA JS PROFISSIONAL (CORREÇÃO DEFINITIVA) ---
def inject_mask():
    components.html(
        """
        <script>
        const formatTime = (v) => {
            v = v.replace(/\D/g, '');
            if (v.length > 6) v = v.slice(0, 6);
            if (v.length > 4) return v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
            if (v.length > 2) return v.replace(/(\d{2})(\d{2})/, "$1:$2");
            return v;
        };

        const applyMasks = () => {
            const inputs = window.parent.document.querySelectorAll('input[type="text"]');
            inputs.forEach(input => {
                if (input.placeholder === "00:00:00" && !input.dataset.maskActive) {
                    input.dataset.maskActive = "true";
                    input.addEventListener('input', (e) => {
                        const cursor = e.target.selectionStart;
                        const oldLen = e.target.value.length;
                        e.target.value = formatTime(e.target.value);
                        e.target.dispatchEvent(new Event('input', { bubbles: true }));
                    });
                }
            });
        };
        // Roda a cada 500ms para garantir que novos campos sejam pegos
        setInterval(applyMasks, 500);
        </script>
        """, height=0
    )

# --- CSS APROVADO (4CM / AZUL ROYAL) ---
st.markdown("""
    <style>
    .title-zion { color: #4169E1; font-family: 'Arial Black'; font-size: 26px; margin-top: -30px; margin-bottom: 15px; }
    div[data-testid="stTextInput"], div[data-testid="stDateInput"] { width: 150px !important; flex: none !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 150px !important; margin-right: 40px !important; }
    .section-HR { border-bottom: 2px solid #4169E1; margin: 12px 0; color: #4169E1; font-size: 13px; font-weight: bold; width: 720px; }
    label { font-size: 11px !important; font-weight: bold !important; }
    input { height: 1.9rem !important; font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- GERENCIAMENTO DE ESTADO (TRAVA DE DADOS) ---
chaves_campos = [
    "placa", "cam", "sp", "ce", "tv", "ec", "sc", "tc", 
    "b1e", "b1s", "b1t", "toe", "tos", "tot", "b2e", "b2s", "b2t", "setc", "ttot", "pliq"
]

for k in chaves_campos:
    if f"val_{k}" not in st.session_state: st.session_state[f"val_{k}"] = ""

if 'page' not in st.session_state: st.session_state.page = 'lancamento'

# --- BARRA LATERAL (RESTAURADA) ---
with st.sidebar:
    st.markdown("<h2 style='color:#4169E1;'>ZION</h2>", unsafe_allow_html=True)
    if st.button("📝 Novo Lançamento"): st.session_state.page = 'lancamento'; st.rerun()
    if st.button("📊 Ver Tabela Geral"): st.session_state.page = 'visualizacao'; st.rerun()
    st.markdown("---")
    if st.button("⬅️ Sair / Login"): st.session_state.page = 'login'; st.rerun()

# --- TELA LANÇAMENTO ---
if st.session_state.page == 'lancamento':
    st.markdown("<div class='title-zion'>Zion - Tempos e movimentos</div>", unsafe_allow_html=True)
    
    # Linha 1
    c1, c2, c3 = st.columns(3)
    st.text_input("Placa", key="val_placa")
    st.text_input("Caminhão", key="val_cam")
    st.date_input("Data", datetime.now(), format="DD/MM/YYYY", key="val_data")
    
    st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
    c4, c5, c6, c7 = st.columns(4)
    c4.text_input("Saída Pátio", placeholder="00:00:00", key="val_sp")
    c5.text_input("Chegada ETC", placeholder="00:00:00", key="val_ce")
    c6.text_input("TT Viagem", placeholder="00:00:00", key="val_tv")
    c7.text_input("Ent. Class", placeholder="00:00:00", key="val_ec")
    
    c8, c9 = st.columns(2)
    c8.text_input("Saí. Class", placeholder="00:00:00", key="val_sc")
    c9.text_input("TT Class", placeholder="00:00:00", key="val_tc")

    st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
    c10, c11, c12, c13 = st.columns(4)
    c10.text_input("Ent. Bal 1", placeholder="00:00:00", key="val_b1e")
    c11.text_input("Saí. Bal 1", placeholder="00:00:00", key="val_b1s")
    c12.text_input("TT Bal 1", placeholder="00:00:00", key="val_b1t")
    c13.text_input("Ent. Tomb", placeholder="00:00:00", key="val_toe")
    
    c14, c15, c16, c17 = st.columns(4)
    c14.text_input("Saí. Tomb", placeholder="00:00:00", key="val_tos")
    c15.text_input("TT Tomb", placeholder="00:00:00", key="val_tot")
    c16.text_input("Ent. Bal 2", placeholder="00:00:00", key="val_b2e")
    c17.text_input("Saí. Bal 2", placeholder="00:00:00", key="val_b2s")

    st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
    c18, c19, c20, c21 = st.columns(4)
    c18.text_input("TT Bal 2", placeholder="00:00:00", key="val_b2t")
    c19.text_input("Saída ETC", placeholder="00:00:00", key="val_setc")
    c20.text_input("TT Total", placeholder="00:00:00", key="val_ttot")
    c21.text_input("Peso Líq.", key="val_pliq")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SALVAR REGISTRO"):
        st.success("✅ Salvo!")
        for k in chaves_campos: st.session_state[f"val_{k}"] = ""
        st.rerun()

    inject_mask()

elif st.session_state.page == 'visualizacao':
    st.markdown("<div class='title-zion'>Relatório</div>")
    st.write("Tabela de dados...")
