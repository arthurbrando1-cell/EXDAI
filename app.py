import streamlit as st
from huggingface_hub import InferenceClient
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Terminal IA", page_icon="📟", layout="centered")

# --- ESTILO CSS HACKER ---
st.markdown("""
    <style>
    /* Fundo Preto e Texto Branco */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    /* Estilo das mensagens do Chat */
    .stChatMessage {
        background-color: rgba(0, 255, 65, 0.05) !important;
        border: 1px solid #00ff41 !important;
        border-radius: 10px;
        color: white !important;
    }
    /* Estilo do campo de digitação */
    .stChatInput {
        border: 1px solid #00ff41 !important;
        border-radius: 5px;
    }
    /* Esconder elementos padrão */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO TOKEN (SUA CHAVE AQUI) ---
HF_TOKEN = "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" # <--- APAGUE ISSO E COLE SEU TOKEN hf_...

# Inicializa o cliente com o modelo Llama 3
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)

# --- INTRO ANIMADA (OPCIONAL) ---
if "intro_done" not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("<h1 style='text-align: center; color: #00ff41; font-family: monospace;'>[ SISTEMA INICIALIZANDO ]</h1>", unsafe_allow_html=True)
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        st.markdown("<p style='text-align: center; color: #00ff41;'>CONEXÃO CRIPTOGRAFADA ESTABELECIDA...</p>", unsafe_allow_html=True)
        time.sleep(1)
    placeholder.empty()
    st.session_state["intro_done"] = True

# --- INTERFACE DO CHAT ---
st.markdown("<h1 style='color: #00ff41; font-family: monospace;'>📟 TERMINAL_IA v1.0</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de comando
if prompt := st.chat_input("Digite um comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        
        try:
            # Faz a chamada para a API do Hugging Face
            # O sistema vai "streamar" a resposta (escrever aos poucos)
            output = client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                stream=True,
                temperature=0.7
            )
            
            for chunk in output:
                token = chunk.choices[0].delta.content
                if token:
                    full_text += token
                    placeholder.markdown(full_text + "▌")
            
            placeholder.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
            
        except Exception as e:
            st.error(f"ERRO DE CONEXÃO: Verifique se o seu Token está correto.")
