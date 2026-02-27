import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Terminal IA", page_icon="📟", layout="centered")

# --- ESTILO CSS (Preto, Branco e Verde) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(45deg, #000000, #050505, #001200);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #ffffff;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stChatMessage {
        background-color: rgba(0, 255, 65, 0.05) !important;
        border: 1px solid #00ff41;
        border-radius: 10px;
    }
    code { color: #00ff41 !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API (GEMINI) ---
# Dica: No Streamlit Cloud, use st.secrets["GEMINI_KEY"] por segurança
GOOGLE_API_KEY = "COLE_SUA_CHAVE_AQUI" 

if GOOGLE_API_KEY == "COLE_SUA_CHAVE_AQUI":
    st.error("ERRO CRÍTICO: CHAVE DE API NÃO CONFIGURADA NO CÓDIGO.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- INTRO ANIMADA ---
if "intro_done" not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("<h1 style='text-align: center; color: #00ff41; font-family: monospace;'>[ SISTEMA INICIALIZANDO ]</h1>", unsafe_allow_html=True)
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        st.markdown("<p style='text-align: center; color: #00ff41;'>CONEXÃO ESTABELECIDA COM SUCESSO...</p>", unsafe_allow_html=True)
        time.sleep(1)
    placeholder.empty()
    st.session_state["intro_done"] = True

# --- LÓGICA DO CHAT ---
st.markdown("<h1 style='color: #00ff41; font-family: monospace;'>📟 TERMINAL_IA v1.0</h1>", unsafe_allow_html=True)

# Inicializa o chat no estado da sessão
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Exibe mensagens anteriores
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Input de comando
if prompt := st.chat_input("Digite um comando para a IA..."):
    # Mostra o que o usuário digitou
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Resposta em tempo real (Stream)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"ERRO DE CONEXÃO: {e}")
