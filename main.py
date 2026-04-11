import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# =========================================================
# 🔑 GESTÃO DE USUÁRIOS
# =========================================================
USUARIOS = {
    "admin": {"senha": "123", "perfil": "supervisor"},
    "alex": {"senha": "porto", "perfil": "supervisor"}
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
def formatar_hora(texto):
    apenas_numeros = "".join(filter(str.isdigit, texto))
    if len(apenas_numeros) == 4:
        return f"{apenas_numeros[:2]}:{apenas_numeros[2:]}:00"
    elif len(apenas_numeros) == 6:
        return f"{apenas_numeros[:2]}:{apenas_numeros[2:4]}:{apenas_numeros[4:]}"
    return "00:00:00" if not apenas_numeros else texto

def calc_diff(inicio, fim):
    try:
        fmt = '%H:%M:%S'
        t1 = datetime.strptime(formatar_hora(inicio), fmt)
        t2 = datetime.strptime(formatar_hora(fim), fmt)
        if t2 < t1: t2 += timedelta(days=1)
        return t2 - t1
    except:
        return timedelta(0)

def td_to_str(td):
    total_sec = int(td.total_seconds())
    h, rem = divmod(total_sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- BANCO DE DADOS ---
DB_FILE = "dados_porto_v2.csv"
COLUNAS = [
    "PLACA", "CAMINHÃO", "DATA", 
    "SAÍDA PÁTIO", "CHEGADA ETC", "TT VIAGEM",
    "ENTR. CLASSIF", "SAÍDA CLASSIF", "TT CLASSIF",
    "ENTR. BALANÇA 1", "SAÍDA BALANÇA 1", "TT BALANÇA 1",
    "ENT. TOMBADOR", "SAÍDA TOMBADOR", "TT TOMBADOR",
    "ENT. BALANÇA 2", "SAÍDA BALANÇA 2", "TT BALANÇA 2",
    "SAÍDA ETC", "TT OPERAÇÃO", "PESO LÍQUIDO"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUNAS).to_csv(DB_FILE, index=False)

if 'page' not in st.session_state: st.session_state.page = 'login'
if 'perfil' not in st.session_state: st.session_state.perfil = None

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
    st.sidebar.title(f"Perfil: {str(st.session_state.perfil).upper()}")
    if st.sidebar.button("📊 Ver Tabela Geral"): st.session_state.page = 'visualizacao'; st.rerun()
    st.sidebar.markdown("---")
    if st.sidebar.button("⬅️ VOLTAR AO LOGIN"): 
        st.session_state.page = 'login'
        st.rerun()

    st.markdown("## 📝 Novo Registro")
    
    with st.form("form_aurora", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        
        # AJUSTE DA DATA (FORMATO BRASILEIRO NA TELA)
        data_selecionada = c3.date_input("Data da Operação", datetime.now(), format="DD/MM/YYYY")
        data_br = data_selecionada.strftime("%d/%m/%Y")

        st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        c4, c5, c6, c7 = st.columns(4)
        s_patio = c4.text_input("Saída Pátio")
        c_etc = c5.text_input("Chegada ETC")
        e_class = c6.text_input("Ent. Classif.")
        s_class = c7.text_input("Saí. Classif.")

        st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
        c8, c9, c10, c11, c12, c13 = st.columns(6)
        e_bal1 = c8.text_input("Ent. Bal. 1")
        s_bal1 = c9.text_input("Saí. Bal. 1")
        e_tom = c10.text_input("Ent. Tomb.")
        s_tom = c11.text_input("Saí. Tomb.")
        e_bal2 = c12.text_input("Ent. Bal. 2")
        s_bal2 = c13.text_input("Saí. Bal. 2")

        st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
        c14, c15 = st.columns(2)
        s_etc = c14.text_input("Saída ETC Final")
        p_liq = c15.text_input("Peso Líquido")

        if st.form_submit_button("SALVAR REGISTRO"):
            tt_v = calc_diff(s_patio, c_etc)
            tt_c = calc_diff(e_class, s_class)
            tt_b1 = calc_diff(e_bal1, s_bal1)
            tt_t = calc_diff(e_tom, s_tom)
            tt_b2 = calc_diff(e_bal2, s_bal2)
            tt_total = tt_v + tt_c + tt_b1 + tt_t + tt_b2

            novo = {
                "PLACA": placa.upper(), "CAMINHÃO": caminhao.upper(), "DATA": data_br,
                "SAÍDA PÁTIO": formatar_hora(s_patio), "CHEGADA ETC": formatar_hora(c_etc), "TT VIAGEM": td_to_str(tt_v),
                "ENTR. CLASSIF": formatar_hora(e_class), "SAÍDA CLASSIF": formatar_hora(s_class), "TT CLASSIF": td_to_str(tt_c),
                "ENTR. BALANÇA 1": formatar_hora(e_bal1), "SAÍDA BALANÇA 1": formatar_hora(s_bal1), "TT BALANÇA 1": td_to_str(tt_b1),
                "ENT. TOMBADOR": formatar_hora(e_tom), "SAÍDA TOMBADOR": formatar_hora(s_tom), "TT TOMBADOR": td_to_str(tt_t),
                "ENT. BALANÇA 2": formatar_hora(e_bal2), "SAÍDA BALANÇA 2": formatar_hora(s_bal2), "TT BALANÇA 2": td_to_str(tt_b2),
                "SAÍDA ETC": formatar_hora(s_etc), "TT OPERAÇÃO": td_to_str(tt_total), "PESO LÍQUIDO": p_liq
            }
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"✅ Salvo! Data: {data_br}")

# --- TELA 3: VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.sidebar.button("⬅️ Voltar", on_click=lambda: st.session_state.update(page='lancamento'))
    st.markdown("## 📊 Histórico")
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False, sep=';', encoding='latin1').encode('latin1')
    st.download_button("📥 Exportar Excel", csv, "relatorio.csv", "text/csv")
