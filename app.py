import streamlit as st
from openai import OpenAI
import time

# Configurações da Página
st.set_page_config(page_title="Terminal IA", page_icon="📟", layout="centered")

# --- ESTILO CSS CUSTOMIZADO (O "Tapa" no Visual) ---
st.markdown("""
    <style>
    /* Fundo Animado Simples (Gradiente) */
    .stApp {
        background: linear-gradient(45deg, #000000, #0a0a0a, #001a00);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #ffffff;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Estilo das mensagens */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid #00ff41;
        border-radius: 10px;
        color: white !important;
    }

    /* Customização do Input */
    .stChatInput {
        border-top: 1px solid #00ff41 !important;
    }

    /* Esconder o menu padrão do Streamlit para ficar mais 'clean' */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- INTRO COM ANIMAÇÃO ---
if "intro_done" not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("<h1 style='text-align: center; color: #00ff41;'>INICIALIZANDO SISTEMA...</h1>", unsafe_allow_html=True)
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        st.success("CONEXÃO ESTABELECIDA")
        time.sleep(1)
    placeholder.empty()
    st.session_state["intro_done"] = True

# --- LÓGICA DO CHAT ---
st.markdown("<h1 style='color: #00ff41; font-family: monospace;'>📟 TERMINAL_IA v1.0</h1>", unsafe_allow_html=True)

# Sidebar para a chave
with st.sidebar:
    st.title("Configurações")
    api_key = st.text_input("Insira sua OpenAI API Key", type="password")
    st.info("O fundo verde neon indica que o sistema está pronto.")

# Inicializa histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite um comando..."):
    if not api_key:
        st.error("ERRO: API KEY AUSENTE")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client = OpenAI(api_key=api_key)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Request para a API (com efeito de streaming/digitação)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
