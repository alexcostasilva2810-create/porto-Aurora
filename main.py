import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components
from datetime import datetime

# --- CONEXÃO COM GOOGLE SHEETS (VIA SECRETS) ---
def conectar_planilha():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Lê a chave configurada no painel 'Secrets' do Streamlit
    creds_info = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    client = gspread.authorize(creds)
    # Abre a planilha 'Zion' na aba 'Tempo'
    return client.open("Zion").worksheet("Tempo")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zion Portuário", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS CUSTOMIZADA ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
        url("https://raw.githubusercontent.com/Claudio-Zion/zion-port/main/image_fb1881.jpg");
        background-size: cover;
        background-attachment: fixed;
    }}
    .header-zion {{
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 6px solid #4169E1;
        text-align: center;
        margin-bottom: 30px;
    }}
    .header-zion h1 {{ color: #4169E1; font-family: 'Arial Black'; margin: 0; }}
    .card-operacional {{
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        color: black;
    }}
    input {{ font-weight: bold !important; font-size: 18px !important; color: #1E1E1E !important; }}
    label {{ font-weight: bold !important; color: #333 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- MÁSCARA JAVASCRIPT (IMPEDE A HORA DE SUMIR) ---
components.html("""
    <script>
    const maskTime = (e) => {
        let v = e.target.value.replace(/\D/g,'');
        if (v.length > 6) v = v.slice(0,6);
        if (v.length > 4) v = v.replace(/(\d{2})(\d{2})(\d{2})/, "$1:$2:$3");
        else if (v.length > 2) v = v.replace(/(\d{2})(\d{2})/, "$1:$2");
        e.target.value = v;
    }
    setInterval(() => {
        window.parent.document.querySelectorAll('input[placeholder="00:00:00"]').forEach(input => {
            if(!input.dataset.maskSet) { 
                input.addEventListener('input', maskTime); 
                input.dataset.maskSet = '1';
                // Garante que o Streamlit só processe após o foco sair do campo
                input.onblur = () => { input.dispatchEvent(new Event('change', { bubbles: true })); };
            }
        });
    }, 500);
    </script>
    """, height=0)

# --- SISTEMA DE LOGIN E PERFIS ---
if 'perfil' not in st.session_state:
    st.session_state.perfil = None

if not st.session_state.perfil:
    st.markdown("<div class='header-zion'><h1>ZION PORTUÁRIO - LOGIN</h1></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container():
            st.markdown("<div class='card-operacional'>", unsafe_allow_html=True)
            user = st.selectbox("IDENTIFIQUE SEU PERFIL", ["SELECIONE", "OPERADOR LOGÍSTICA", "OPERADOR BALANÇA", "OPERADOR TOMBADOR", "SUPERVISOR / ADM"])
            if st.button("ACESSAR SISTEMA", use_container_width=True):
                if user != "SELECIONE":
                    st.session_state.perfil = user
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- CABEÇALHO DO PAINEL ---
    st.markdown(f"<div class='header-zion'><h1>PAINEL OPERACIONAL: {st.session_state.perfil}</h1></div>", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 LOGOUT / SAIR"):
        st.session_state.perfil = None
        st.rerun()

    perfil = st.session_state.perfil

    # --- LÓGICA DE VISIBILIDADE DE CAMPOS ---
    with st.container():
        st.markdown("<div class='card-operacional'>", unsafe_allow_html=True)
        
        with st.form("form_operacao", clear_on_submit=True):
            # CAMPOS COMUNS (Aparecem para todos)
            c1, c2, c3 = st.columns(3)
            placa = c1.text_input("PLACA")
            caminhao = c2.text_input("CAMINHÃO")
            data_hoje = c3.text_input("DATA", value=datetime.now().strftime("%d/%m/%Y"))

            st.markdown("---")

            # SEÇÃO LOGÍSTICA
            if perfil in ["OPERADOR LOGÍSTICA", "SUPERVISOR / ADM"]:
                st.subheader("🚚 LOGÍSTICA E CLASSIFICAÇÃO")
                l1, l2, l3 = st.columns(3)
                s_patio = l1.text_input("SAÍDA DO PÁTIO", placeholder="00:00:00")
                c_etc = l2.text_input("CHEGADA ETC", placeholder="00:00:00")
                e_class = l3.text_input("ENTR. CLASSIFIC", placeholder="00:00:00")
            
            # SEÇÃO BALANÇA
            if perfil in ["OPERADOR BALANÇA", "SUPERVISOR / ADM"]:
                st.subheader("⚖️ PESAGEM (BALANÇA)")
                b1, b2 = st.columns(2)
                e_bal = b1.text_input("ENTR. BALANÇA", placeholder="00:00:00")
                s_bal = b2.text_input("SAÍDA BALANÇA", placeholder="00:00:00")

            # SEÇÃO TOMBADOR
            if perfil in ["OPERADOR TOMBADOR", "SUPERVISOR / ADM"]:
                st.subheader("🏗️ TOMBADOR")
                t1, t2 = st.columns(2)
                e_tom = t1.text_input("ENTRADA TOMBADOR", placeholder="00:00:00")
                s_tom = t2.text_input("SAÍDA TOMBADOR", placeholder="00:00:00")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # BOTÃO DE SALVAR
            btn_save = st.form_submit_button("✅ SALVAR E ENVIAR PARA PLANILHA", use_container_width=True)
            
            if btn_save:
                try:
                    sheet = conectar_planilha()
                    # Mapeamento exato das colunas conforme sua planilha
                    # Ordem: Placa, Caminhão, Data, Saída Pátio, Chegada ETC, TT Viagem (vazio), Entr Classific...
                    # Nota: As colunas TT (vermelhas) a planilha calcula sozinha, enviamos "" para elas.
                    dados = [
                        placa, caminhao, data_hoje, 
                        s_patio if 's_patio' in locals() else "", 
                        c_etc if 'c_etc' in locals() else "", 
                        "", # TT Viagem
                        e_class if 'e_class' in locals() else "",
                        "", # Saída Classific
                        "", # TT Classific
                        e_bal if 'e_bal' in locals() else "",
                        s_bal if 's_bal' in locals() else "",
                        "", # TT Balança
                        e_tom if 'e_tom' in locals() else "",
                        s_tom if 's_tom' in locals() else ""
                    ]
                    sheet.append_row(dados)
                    st.success(f"Dados da placa {placa} registrados com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao conectar: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    # --- TABELA GERAL (ÍCONE DE TABELA PARA SUPERVISOR) ---
    if perfil == "SUPERVISOR / ADM":
        st.write("---")
        st.subheader("📊 VISUALIZAÇÃO DA TABELA GERAL (GOOGLE SHEETS)")
        if st.button("CARREGAR DADOS EM TEMPO REAL"):
            sheet = conectar_planilha()
            df = pd.DataFrame(sheet.get_all_records())
            st.dataframe(df, use_container_width=True)
