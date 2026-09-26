import streamlit as st
import requests
import re
import json
import time
import hashlib

# 1. Configuração da Página (Foco no Mobile)
st.set_page_config(
    page_title="Gerador Afiliado", 
    page_icon="📱", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Injeção de CSS para "Cara de Aplicativo"
estilo_mobile = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stTextInput>div>div>input {
        font-size: 16px !important;
        padding: 15px !important;
    }
    
    .stButton>button {
        width: 100%;
        height: 55px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        background-color: #ff4b4b;
        color: white;
    }
    
    .stCode {
        font-size: 16px !important;
    }
    </style>
"""
st.markdown(estilo_mobile, unsafe_allow_html=True)

st.title("🔗 Gerador de link de afiliado do Leozão")
st.write("Cole o link do seu produto shopee ou Mercado Pago para ajudar o Leozão")

# 3. Lógica da API Shopee
def converter_shopee(url_original):
    app_id = st.secrets["shopee"]["app_id"]
    app_secret = st.secrets["shopee"]["app_secret"]
    
    api_url = "https://open-api.affiliate.shopee.com.br/graphql"
    
    payload = {
        "query": """
            mutation generateShortLink($url: String!) {
                generateShortLink(input: {originUrl: $url}) {
                    shortLink
                }
            }
        """,
        "variables": {
            "url": url_original
        }
    }
    
    payload_str = json.dumps(payload, separators=(',', ':'))
    timestamp = str(int(time.time()))
    raw_signature = f"{app_id}{timestamp}{payload_str}{app_secret}"
    signature = hashlib.sha256(raw_signature.encode('utf-8')).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={app_id}, Signature={signature}, Timestamp={timestamp}"
    }
    
    try:
        response = requests.post(api_url, data=payload_str, headers=headers)
        dados = response.json()
        
        if 'data' in dados and dados['data'] is not None:
            return dados['data']['generateShortLink']['shortLink']
        else:
            return f"Erro Shopee: {dados}"
            
    except Exception as e:
        return f"Erro de conexão: {e}"

# 4. Lógica do Mercado Livre / Mercado Pago
def converter_mercadolivre(url_original):
    id_campanha = st.secrets["mercadolivre"]["id_campanha"]
    
    # Limpa rastreadores velhos do link original
    url_base = url_original.split('?')[0]
    
    # Monta o link com a sua estrutura exata de afiliado
    link_convertido = f"{url_base}?matt_word=leozao_udi&matt_tool={id_campanha}"
    return link_convertido

# 5. Interface Principal
url_input = st.text_input("Link Original:", placeholder="Cole o texto ou link aqui...")

if st.button("🚀 Gerar Link", use_container_width=True):
    if url_input:
        match = re.search(r'(https?://[^\s]+)', url_input)
        
        if match:
            url_limpa = match.group(1)
            
            if re.search(r'(shopee\.|shope\.ee|shp\.ee)', url_limpa.lower()):
                with st.spinner("Conectando..."):
                    link_final = converter_shopee(url_limpa)
                    
                st.success("Shopee identificado! 🛍️")
                st.code(link_final, language="text")
                st.link_button("🔗 Abrir Link Gerado", link_final, use_container_width=True)

            elif re.search(r'(mercadolivre\.|meli\.la|mercadopago\.)', url_limpa.lower()):
                with st.spinner("Conectando..."):
                    link_final = converter_mercadolivre(url_limpa)
                    
                st.success("Mercado Pago/Livre identificado! 🤝")
                st.code(link_final, language="text")
                st.link_button("🔗 Abrir Link Gerado", link_final, use_container_width=True)

            else:
                st.error("Link não reconhecido. Verifique se é da Shopee ou Mercado Pago.")
        else:
            st.error("Nenhum link válido (http/https) foi encontrado no texto colado.")
    else:
        st.warning("Cole o link antes de gerar.")