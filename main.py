import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# 🔑 GESTÃO DE USUÁRIOS
USUARIOS = {
    "admin": {"senha": "123", "perfil": "ADMIN"},
    "alex": {"senha": "porto", "perfil": "SUPERVISOR"},
    "operador1": {"senha": "123", "perfil": "OPERADOR"}
}

st.set_page_config(page_title="Aurora Port", layout="wide")

# CSS para esconder o texto "Perfil:" e estilizar
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; background-color: #004b87; color: white; font-weight: bold; }
    .title-text { text-align: center; color: #004b87; font-family: 'Arial Black'; font-size: 40px; }
    .section-HR { border-top: 2px solid #004b87; margin: 20px 0; padding-top: 10px; font-weight: bold; color: #004b87; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE LIMPEZA E CÁLCULO ---
def limpar_e_formatar_hora(texto):
    """Transforma 092300 em 09:23:00 automaticamente"""
    n = "".join(filter(str.isdigit, texto))
    if len(n) == 4: return f"{n[:2]}:{n[2:]}:00"
    if len(n) >= 6: return f"{n[:2]}:{n[2:4]}:{n[4:6]}"
    return "00:00:00" if not n else texto

def calc_diff(inicio, fim):
    try:
        fmt = '%H:%M:%S'
        t1 = datetime.strptime(limpar_e_formatar_hora(inicio), fmt)
        t2 = datetime.strptime(limpar_e_formatar_hora(fim), fmt)
        if t2 < t1: t2 += timedelta(days=1)
        return t2 - t1
    except: return timedelta(0)

def td_to_str(td):
    ts = int(td.total_seconds())
    h, rem = divmod(ts, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- BANCO DE DADOS ---
DB_FILE = "dados_porto_v2.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["PLACA", "CAMINHÃO", "DATA", "TT OPERAÇÃO"]).to_csv(DB_FILE, index=False)

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

# --- TELA 2: LANÇAMENTOS ---
elif st.session_state.page == 'lancamento':
    # AQUI: Removido o texto "Perfil:", deixado apenas o cargo
    st.sidebar.markdown(f"## {st.session_state.perfil}")
    if st.sidebar.button("📊 Ver Tabela Geral"): st.session_state.page = 'visualizacao'; st.rerun()
    if st.sidebar.button("⬅️ VOLTAR AO LOGIN"): st.session_state.page = 'login'; st.rerun()

    st.markdown("## 📝 Novo Registro")
    
    with st.form("form_aurora", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        # DATA: Agora 100% em DD/MM/AAAA na tela
        data_sel = c3.date_input("Data da Operação", datetime.now(), format="DD/MM/YYYY")
        
        st.markdown("<div class='section-HR'>LOGÍSTICA E TEMPOS (Digite apenas números: 092300)</div>", unsafe_allow_html=True)
        c4, c5, c6, c7 = st.columns(4)
        s_patio = c4.text_input("Saída Pátio")
        c_etc = c5.text_input("Chegada ETC")
        e_class = c6.text_input("Ent. Classif.")
        s_class = c7.text_input("Saí. Classif.")

        # BOTÃO SALVAR (Indentaçao correta para não dar erro)
        if st.form_submit_button("SALVAR REGISTRO"):
            t_viagem = calc_diff(s_patio, c_etc)
            t_class = calc_diff(e_class, s_class)
            tt_total = t_viagem + t_class # Adicione os outros aqui
            
            novo = {
                "PLACA": placa.upper(), 
                "CAMINHÃO": caminhao.upper(), 
                "DATA": data_sel.strftime("%d/%m/%Y"),
                "SAÍDA PÁTIO": limpar_e_formatar_hora(s_patio),
                "CHEGADA ETC": limpar_e_formatar_hora(c_etc),
                "TT OPERAÇÃO": td_to_str(tt_total)
            }
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"✅ Salvo! Horário formatado: {limpar_e_formatar_hora(s_patio)}")

# --- TELA 3: VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.sidebar.button("⬅️ Voltar", on_click=lambda: st.session_state.update(page='lancamento'))
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False, sep=';', encoding='latin1').encode('latin1')
    st.download_button("📥 Baixar Excel", csv, "relatorio.csv", "text/csv")
