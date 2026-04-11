import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 🔑 GESTÃO DE USUÁRIOS
USUARIOS = {
    "admin": {"senha": "123", "perfil": "ADMIN"},
    "alex": {"senha": "porto", "perfil": "SUPERVISOR"},
    "operador1": {"senha": "123", "perfil": "OPERADOR"}
}

st.set_page_config(page_title="Aurora Port", layout="wide")

# --- JAVASCRIPT PARA MÁSCARA EM TEMPO REAL ---
# Esse bloco faz com que, ao digitar, os ":" apareçam sozinhos
def inject_mask():
    components.html(
        """
        <script>
        const maskTime = (e) => {
            let v = e.target.value.replace(/\D/g, '');
            if (v.length > 6) v = v.slice(0, 6);
            if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
            else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
            e.target.value = v;
        }
        
        // Aplica a máscara em todos os inputs de texto que pareçam campos de hora
        const inputs = window.parent.document.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            if (input.getAttribute('aria-label') && 
               (input.getAttribute('aria-label').includes('Pátio') || 
                input.getAttribute('aria-label').includes('ETC') || 
                input.getAttribute('aria-label').includes('Classif') || 
                input.getAttribute('aria-label').includes('Bal') || 
                input.getAttribute('aria-label').includes('Tomb'))) {
                input.addEventListener('input', maskTime);
            }
        });
        </script>
        """, height=0
    )

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; background-color: #004b87; color: white; font-weight: bold; }
    .title-text { text-align: center; color: #004b87; font-family: 'Arial Black'; font-size: 40px; }
    .section-HR { border-top: 2px solid #004b87; margin: 20px 0; padding-top: 10px; font-weight: bold; color: #004b87; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE CÁLCULO ---
def calc_diff(inicio, fim):
    try:
        fmt = '%H:%M:%S'
        t1 = datetime.strptime(inicio, fmt)
        t2 = datetime.strptime(fim, fmt)
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
    st.sidebar.markdown(f"## {st.session_state.perfil}")
    if st.sidebar.button("📊 Ver Tabela Geral"): st.session_state.page = 'visualizacao'; st.rerun()
    if st.sidebar.button("⬅️ VOLTAR AO LOGIN"): st.session_state.page = 'login'; st.rerun()

    st.markdown("## 📝 Novo Registro")
    
    with st.form("form_aurora", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        data_sel = c3.date_input("Data da Operação", datetime.now(), format="DD/MM/YYYY")
        
        st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        c4, c5, c6, c7 = st.columns(4)
        s_patio = c4.text_input("Saída Pátio", placeholder="00:00:00")
        c_etc = c5.text_input("Chegada ETC", placeholder="00:00:00")
        e_class = c6.text_input("Ent. Classif.", placeholder="00:00:00")
        s_class = c7.text_input("Saí. Classif.", placeholder="00:00:00")

        st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
        c8, c9, c10, c11, c12, c13 = st.columns(6)
        e_bal1 = c8.text_input("Ent. Bal. 1", placeholder="00:00:00")
        s_bal1 = c9.text_input("Saí. Bal. 1", placeholder="00:00:00")
        e_tom = c10.text_input("Ent. Tomb.", placeholder="00:00:00")
        s_tom = c11.text_input("Saí. Tomb.", placeholder="00:00:00")
        e_bal2 = c12.text_input("Ent. Bal. 2", placeholder="00:00:00")
        s_bal2 = c13.text_input("Saí. Bal. 2", placeholder="00:00:00")

        st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
        c14, c15 = st.columns(2)
        s_etc_final = c14.text_input("Saída ETC Final", placeholder="00:00:00")
        p_liq = c15.text_input("Peso Líquido")

        if st.form_submit_button("SALVAR REGISTRO"):
            # Lógica de cálculo (os valores já virão com ":" por causa do JS)
            t_v = calc_diff(s_patio, c_etc)
            t_c = calc_diff(e_class, s_class)
            t_b1 = calc_diff(e_bal1, s_bal1)
            t_t = calc_diff(e_tom, s_tom)
            t_b2 = calc_diff(e_bal2, s_bal2)
            tt_total = t_v + t_c + t_b1 + t_t + t_b2
            
            novo = {
                "PLACA": placa.upper(), "CAMINHÃO": caminhao.upper(), 
                "DATA": data_sel.strftime("%d/%m/%Y"),
                "SAÍDA PÁTIO": s_patio, "CHEGADA ETC": c_etc, "TT VIAGEM": td_to_str(t_v),
                "ENT. CLASSIF": e_class, "SAÍ. CLASSIF": s_class, "TT CLASSIF": td_to_str(t_c),
                "ENT. BAL 1": e_bal1, "SAÍ. BAL 1": s_bal1, "TT BAL 1": td_to_str(t_b1),
                "ENT. TOMB": e_tom, "SAÍ. TOMB": s_tom, "TT TOMB": td_to_str(t_t),
                "ENT. BAL 2": e_bal2, "SAÍ. BAL 2": s_bal2, "TT BAL 2": td_to_str(t_b2),
                "SAÍDA ETC": s_etc_final, "TT OPERAÇÃO": td_to_str(tt_total), "PESO LÍQUIDO": p_liq
            }
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ Registro salvo com sucesso!")

    # Injeta a máscara JavaScript no final da página
    inject_mask()

# --- TELA 3: VISUALIZAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.sidebar.button("⬅️ Voltar", on_click=lambda: st.session_state.update(page='lancamento'))
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False, sep=';', encoding='latin1').encode('latin1')
    st.download_button("📥 Baixar Excel", csv, "relatorio.csv", "text/csv")
