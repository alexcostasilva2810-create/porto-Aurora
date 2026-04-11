import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
# Importante: Você precisará instalar esta biblioteca: pip install streamlit-mask-text-input
from streamlit_mask_text_input import mask_text_input

# =========================================================
# 🔑 GESTÃO DE USUÁRIOS
# =========================================================
USUARIOS = {
    "admin": {"senha": "123", "perfil": "ADMIN"},
    "alex": {"senha": "porto", "perfil": "SUPERVISOR"},
    "operador1": {"senha": "123", "perfil": "OPERADOR"}
}

# Configuração da página
st.set_page_config(page_title="Aurora Port", layout="wide")

# Estilo visual
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004b87; color: white; font-weight: bold; }
    .title-text { text-align: center; color: #004b87; font-family: 'Arial Black'; font-size: 40px; }
    .section-HR { border-top: 2px solid #004b87; margin: 20px 0; padding-top: 10px; font-weight: bold; color: #004b87; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def calc_diff(inicio, fim):
    try:
        fmt = '%H:%M:%S'
        t1 = datetime.strptime(inicio, fmt)
        t2 = datetime.strptime(fim, fmt)
        if t2 < t1: t2 += timedelta(days=1)
        return t2 - t1
    except:
        return timedelta(0)

def td_to_str(td):
    ts = int(td.total_seconds())
    h, rem = divmod(ts, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- BANCO DE DADOS ---
DB_FILE = "dados_porto_v2.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=[
        "PLACA", "CAMINHÃO", "DATA", "SAÍDA PÁTIO", "CHEGADA ETC", "TT VIAGEM",
        "ENT. CLASSIF", "SAÍ. CLASSIF", "TT CLASSIF", "ENT. BAL 1", "SAÍ. BAL 1", 
        "TT BAL 1", "ENT. TOMB", "SAÍ. TOMB", "TT TOMB", "ENT. BAL 2", "SAÍ. BAL 2", 
        "TT BAL 2", "SAÍDA ETC", "TT OPERAÇÃO", "PESO LÍQUIDO"
    ]).to_csv(DB_FILE, index=False)

if 'page' not in st.session_state: st.session_state.page = 'login'
if 'perfil' not in st.session_state: st.session_state.perfil = ""

# --- TELA 1: LOGIN ---
if st.session_state.page == 'login':
    st.markdown("<h1 class='title-text'>AURORA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ACESSAR"):
            if u in USUARIOS and USUARIOS[u]["senha"] == p:
                st.session_state.perfil = USUARIOS[u]["perfil"]
                st.session_state.page = 'lancamento'
                st.rerun()
            else: st.error("Acesso negado.")

# --- TELA 2: LANÇAMENTOS ---
elif st.session_state.page == 'lancamento':
    # Mostra apenas o cargo (ADMIN, SUPERVISOR, etc)
    st.sidebar.markdown(f"## {st.session_state.perfil}")
    if st.sidebar.button("📊 Ver Tabela Geral"): st.session_state.page = 'visualizacao'; st.rerun()
    st.sidebar.markdown("---")
    if st.sidebar.button("⬅️ VOLTAR AO LOGIN"): 
        st.session_state.page = 'login'
        st.rerun()

    st.markdown("## 📝 Novo Registro")
    
    with st.form("form_aurora"):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        data_sel = c3.date_input("Data da Operação", datetime.now(), format="DD/MM/YYYY")
        
        # MÁSCARA AUTOMÁTICA DE HORA: 99:99:99
        st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        c4, c5, c6, c7 = st.columns(4)
        s_patio = mask_text_input(label="Saída Pátio", mask="99:99:99", placeholder="00:00:00", key="s_patio")
        c_etc = mask_text_input(label="Chegada ETC", mask="99:99:99", placeholder="00:00:00", key="c_etc")
        e_class = mask_text_input(label="Ent. Classif.", mask="99:99:99", placeholder="00:00:00", key="e_class")
        s_class = mask_text_input(label="Saí. Classif.", mask="99:99:99", placeholder="00:00:00", key="s_class")

        st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
        c8, c9, c10, c11, c12, c13 = st.columns(6)
        e_bal1 = mask_text_input(label="Ent. Bal. 1", mask="99:99:99", placeholder="00:00:00", key="e_bal1")
        s_bal1 = mask_text_input(label="Saí. Bal. 1", mask="99:99:99", placeholder="00:00:00", key="s_bal1")
        e_tom = mask_text_input(label="Ent. Tomb.", mask="99:99:99", placeholder="00:00:00", key="e_tom")
        s_tom = mask_text_input(label="Saí. Tomb.", mask="99:99:99", placeholder="00:00:00", key="s_tom")
        e_bal2 = mask_text_input(label="Ent. Bal. 2", mask="99:99:99", placeholder="00:00:00", key="e_bal2")
        s_bal2 = mask_text_input(label="Saí. Bal. 2", mask="99:99:99", placeholder="00:00:00", key="s_bal2")

        st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
        c14, c15 = st.columns(2)
        s_etc_final = mask_text_input(label="Saída ETC Final", mask="99:99:99", placeholder="00:00:00", key="s_etc")
        p_liq = c14.text_input("Peso Líquido")

        if st.form_submit_button("SALVAR REGISTRO"):
            # Cálculos
            t_viagem = calc_diff(s_patio, c_etc)
            t_class = calc_diff(e_class, s_class)
            t_bal1 = calc_diff(e_bal1, s_bal1)
            t_tomb = calc_diff(e_tom, s_tom)
            t_bal2 = calc_diff(e_bal2, s_bal2)
            tt_operacao = t_viagem + t_class + t_bal1 + t_tomb + t_bal2

            novo = {
                "PLACA": placa.upper(), "CAMINHÃO": caminhao.upper(), 
                "DATA": data_sel.strftime("%d/%m/%Y"),
                "SAÍDA PÁTIO": s_patio, "CHEGADA ETC": c_etc, "TT VIAGEM": td_to_str(t_viagem),
                "ENT. CLASSIF": e_class, "SAÍ. CLASSIF": s_class, "TT CLASSIF": td_to_str(t_class),
                "ENT. BAL 1": e_bal1, "SAÍ. BAL 1": s_bal1, "TT BAL 1": td_to_str(t_bal1),
                "ENT. TOMB": e_tom, "SAÍ. TOMB": s_tom, "TT TOMB": td_to_str(t_tomb),
                "ENT. BAL 2": e_bal2, "SAÍ. BAL 2": s_bal2, "TT BAL 2": td_to_str(t_bal2),
                "SAÍDA ETC": s_etc_final, "TT OPERAÇÃO": td_to_str(tt_operacao), "PESO LÍQUIDO": p_liq
            }
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ Registro Salvo com Sucesso!")

# --- TELA 3: VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.sidebar.button("⬅️ Voltar", on_click=lambda: st.session_state.update(page='lancamento'))
    st.markdown("## 📊 Tabela de Movimentação")
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False, sep=';', encoding='latin1').encode('latin1')
    st.download_button("📥 Baixar Planilha Excel", csv, "relatorio_aurora.csv", "text/csv")
