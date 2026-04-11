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

# Inicializa o estado dos campos para eles não sumirem
campos_hora = [
    "s_patio", "c_etc", "e_class", "s_class", 
    "e_bal1", "s_bal1", "e_tom", "s_tom", 
    "e_bal2", "s_bal2", "s_etc"
]
for campo in campos_hora:
    if campo not in st.session_state:
        st.session_state[campo] = ""

# --- JAVASCRIPT MELHORADO PARA NÃO CONFLITAR COM O STREAMLIT ---
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
            
            // Força o Streamlit a reconhecer o valor sem resetar
            e.target.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        const inputs = window.parent.document.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            input.addEventListener('input', maskTime);
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
    
    # Removido o clear_on_submit do form para os dados não sumirem antes da hora
    with st.form("form_aurora"):
        c1, c2, c3 = st.columns(3)
        placa = c1.text_input("Placa")
        caminhao = c2.text_input("Caminhão")
        data_sel = c3.date_input("Data da Operação", datetime.now(), format="DD/MM/YYYY")
        
        st.markdown("<div class='section-HR'>LOGÍSTICA E CLASSIFICAÇÃO</div>", unsafe_allow_html=True)
        c4, c5, c6, c7 = st.columns(4)
        s_patio = c4.text_input("Saída Pátio", key="s_patio_in", value=st.session_state.s_patio)
        c_etc = c5.text_input("Chegada ETC", key="c_etc_in", value=st.session_state.c_etc)
        e_class = c6.text_input("Ent. Classif.", key="e_class_in", value=st.session_state.e_class)
        s_class = c7.text_input("Saí. Classif.", key="s_class_in", value=st.session_state.s_class)

        st.markdown("<div class='section-HR'>BALANÇAS E TOMBADOR</div>", unsafe_allow_html=True)
        c8, c9, c10, c11, c12, c13 = st.columns(6)
        e_bal1 = c8.text_input("Ent. Bal. 1", key="e_bal1_in")
        s_bal1 = c9.text_input("Saí. Bal. 1", key="s_bal1_in")
        e_tom = c10.text_input("Ent. Tomb.", key="e_tom_in")
        s_tom = c11.text_input("Saí. Tomb.", key="s_tom_in")
        e_bal2 = c12.text_input("Ent. Bal. 2", key="e_bal2_in")
        s_bal2 = c13.text_input("Saí. Bal. 2", key="s_bal2_in")

        st.markdown("<div class='section-HR'>FECHAMENTO</div>", unsafe_allow_html=True)
        c14, c15 = st.columns(2)
        s_etc_final = c14.text_input("Saída ETC Final", key="s_etc_in")
        p_liq = c15.text_input("Peso Líquido")

        if st.form_submit_button("SALVAR REGISTRO"):
            # Cálculos
            t_v = calc_diff(s_patio, c_etc)
            t_c = calc_diff(e_class, s_class)
            tt_total = t_v + t_c # Adicione as outras diferenças aqui
            
            novo = {
                "PLACA": placa.upper(), "CAMINHÃO": caminhao.upper(), 
                "DATA": data_sel.strftime("%d/%m/%Y"),
                "SAÍDA PÁTIO": s_patio, "CHEGADA ETC": c_etc,
                "TT OPERAÇÃO": td_to_str(tt_total), "PESO LÍQUIDO": p_liq
            }
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            
            st.success("✅ Registro salvo com sucesso!")
            # Limpa os campos apenas após salvar
            for campo in campos_hora: st.session_state[campo] = ""
            st.rerun()

    inject_mask()

elif st.session_state.page == 'visualizacao':
    st.sidebar.button("⬅️ Voltar", on_click=lambda: st.session_state.update(page='lancamento'))
    st.dataframe(pd.read_csv(DB_FILE), use_container_width=True)
