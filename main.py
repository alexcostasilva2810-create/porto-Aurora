import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================================================
# 🔑 GESTÃO DE USUÁRIOS E PERMISSÕES (ALERE AQUI)
# =========================================================
# Formato: "usuario": {"senha": "123", "perfil": "supervisor" ou "operador"}
USUARIOS = {
    "admin": {"senha": "123", "perfil": "supervisor"},
    "alex": {"senha": "porto", "perfil": "supervisor"},
    "operador1": {"senha": "123", "perfil": "operador"}
}
# =========================================================

# Configuração da página
st.set_page_config(page_title="Aurora Port - Grãos", layout="wide")

# Estilo visual
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004b87; color: white; }
    .title-text { text-align: center; color: #004b87; font-family: 'Arial Black'; font-size: 50px; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Banco de Dados
DB_FILE = "dados_porto.csv"
COLUNAS = [
    "SAÍDA DO PÁTIO", "CHEGADA ETC", "TT VIAGEM", "ENTR. CLASSIFIC", 
    "SAÍDA CLASSIFICAÇÃO", "TT CLASSIFIC", "ENTR. BALANÇA", "SAÍDA BALANÇA", 
    "TT BALANÇA", "ENTRADA TOMBADOR", "SAÍDA TOMBADOR", "TT TOMBADOR"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUNAS).to_csv(DB_FILE, index=False)

# Controle de Sessão
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'perfil' not in st.session_state:
    st.session_state.perfil = None

# Função para calcular diferença de tempo simples (HH:MM)
def calc_tt(inicio, fim):
    try:
        fmt = '%H:%M'
        tdelta = datetime.strptime(fim, fmt) - datetime.strptime(inicio, fmt)
        return str(tdelta)
    except:
        return "00:00"

# --- TELA 1: LOGIN ---
if st.session_state.page == 'login':
    st.markdown("<h1 class='title-text'>AURORA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Sistema de Monitoramento Portuário</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ACESSAR"):
            if u in USUARIOS and USUARIOS[u]["senha"] == p:
                st.session_state.page = 'lancamento'
                st.session_state.perfil = USUARIOS[u]["perfil"]
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

# --- TELA 2: LANÇAMENTOS ---
elif st.session_state.page == 'lancamento':
    st.sidebar.title(f"Perfil: {st.session_state.perfil.upper()}")
    if st.sidebar.button("📊 Visualizar Tabela"):
        st.session_state.page = 'visualizacao'
        st.rerun()
    if st.sidebar.button("🚪 Sair"):
        st.session_state.page = 'login'
        st.rerun()

    st.markdown("## 📝 Registro de Tempos e Movimentos")
    
    with st.form("form_dados"):
        c1, c2, c3 = st.columns(3)
        
        # Grupo 1: Viagem
        s_patio = c1.text_input("SAÍDA DO PÁTIO (HH:MM)")
        c_etc = c1.text_input("CHEGADA ETC (HH:MM)")
        
        # Grupo 2: Classificação
        e_class = c2.text_input("ENTR. CLASSIFIC (HH:MM)")
        s_class = c2.text_input("SAÍDA CLASSIFICAÇÃO (HH:MM)")
        
        # Grupo 3: Balança
        e_bal = c3.text_input("ENTR. BALANÇA (HH:MM)")
        s_bal = c3.text_input("SAÍDA BALANÇA (HH:MM)")
        
        # Grupo 4: Tombador (abaixo)
        c4, c5, c6 = st.columns(3)
        e_tom = c4.text_input("ENTRADA TOMBADOR (HH:MM)")
        s_tom = c4.text_input("SAÍDA TOMBADOR (HH:MM)")

        if st.form_submit_button("SALVAR REGISTRO"):
            novo_dado = {
                "SAÍDA DO PÁTIO": s_patio, "CHEGADA ETC": c_etc,
                "TT VIAGEM": calc_tt(s_patio, c_etc),
                "ENTR. CLASSIFIC": e_class, "SAÍDA CLASSIFICAÇÃO": s_class,
                "TT CLASSIFIC": calc_tt(e_class, s_class),
                "ENTR. BALANÇA": e_bal, "SAÍDA BALANÇA": s_bal,
                "TT BALANÇA": calc_tt(e_bal, s_bal),
                "ENTRADA TOMBADOR": e_tom, "SAÍDA TOMBADOR": s_tom,
                "TT TOMBADOR": calc_tt(e_tom, s_tom)
            }
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ Lançado com sucesso!")

# --- TELA 3: VISUALIZAÇÃO E EXPORTAÇÃO ---
elif st.session_state.page == 'visualizacao':
    st.sidebar.button("⬅️ Voltar ao Lançamento", on_click=lambda: st.session_state.update(page='lancamento'))
    
    st.markdown("## 📊 Tabela Geral")
    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)

    # --- ÁREA EXCLUSIVA DO SUPERVISOR ---
    if st.session_state.perfil == "supervisor":
        st.markdown("---")
        st.markdown("### 🛠️ Área do Supervisor (Exportação)")
        col_ex1, col_ex2 = st.columns(2)
        
        # Exportar Excel
        with col_ex1:
            st.download_button(
                label="📥 Baixar em Excel",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"Relatorio_Aurora_{datetime.now().strftime('%d%m%Y')}.csv",
                mime="text/csv"
            )
        
        with col_ex2:
            st.info("Para PDF: Use a opção 'Imprimir' (Ctrl+P) do seu navegador e salve como PDF. É a forma mais estável para relatórios web.")
    else:
        st.warning("⚠️ Você não tem permissão para exportar dados. Apenas supervisores.")
