import streamlit as st
import requests
import re
import json
import time
import hashlib

# 1. Configuração da Página
st.set_page_config(page_title="Gerador de Links de Afiliado", page_icon="🔗")
st.title("🔗 Gerador de Links Automático")
st.write("Cole o link original do produto abaixo para gerar seu link monetizado.")

# 2. Lógica da API Shopee com Criptografia SHA256
def converter_shopee(url_original):
    app_id = st.secrets["shopee"]["app_id"]
    app_secret = st.secrets["shopee"]["app_secret"]
    
    api_url = "https://open-api.affiliate.shopee.com.br/graphql"
    
    # O corpo da requisição (Payload)
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
    
    # 1. Converte o payload para uma string JSON sem espaços extras (exigência da Shopee)
    payload_str = json.dumps(payload, separators=(',', ':'))
    
    # 2. Captura o Timestamp atual do servidor em segundos
    timestamp = str(int(time.time()))
    
    # 3. Concatena os dados na ordem estrita: AppId + Timestamp + Payload + Secret
    raw_signature = f"{app_id}{timestamp}{payload_str}{app_secret}"
    
    # 4. Gera o hash criptográfico SHA256
    signature = hashlib.sha256(raw_signature.encode('utf-8')).hexdigest()
    
    # 5. Monta o cabeçalho Authorization com a estrutura esperada
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={app_id}, Signature={signature}, Timestamp={timestamp}"
    }
    
    try:
        # Usa data=payload_str em vez de json=payload para garantir que não haja alteração de formato
        response = requests.post(api_url, data=payload_str, headers=headers)
        dados = response.json()
        
        # Verifica se o link foi gerado e devolvido no dicionário
        if 'data' in dados and dados['data'] is not None:
            link_curto = dados['data']['generateShortLink']['shortLink']
            return link_curto
        else:
            return f"A Shopee recusou a conexão. Motivo: {dados}"
            
    except Exception as e:
        return f"Erro interno do script. Detalhe: {e}"

# 3. Lógica do Mercado Livre
def converter_mercadolivre(url_original):
    id_campanha = st.secrets["mercadolivre"]["id_campanha"]
    url_base = url_original.split('?')[0]
    return f"{url_base}?camp={id_campanha}"

# 4. Interface do Usuário
url_input = st.text_input("Link do Produto (Shopee ou ML):", placeholder="https://...")

if st.button("Gerar Link de Afiliado"):
    if url_input:
        if re.search(r'shopee\.', url_input.lower()):
            with st.spinner("Assinando credenciais e conectando à Shopee..."):
                link_final = converter_shopee(url_input)
                
            st.success("Plataforma identificada: Shopee 🛍️")
            st.write("**Seu link monetizado:**")
            st.code(link_final, language="text")

        elif re.search(r'mercadolivre\.', url_input.lower()):
            with st.spinner("Gerando link do Mercado Livre..."):
                link_final = converter_mercadolivre(url_input)
                
            st.success("Plataforma identificada: Mercado Livre 🤝")
            st.write("**Seu link monetizado:**")
            st.code(link_final, language="text")

        else:
            st.error("Link não reconhecido. Certifique-se de que é um link válido.")
    else:
        st.warning("Por favor, cole um link antes de clicar no botão.")