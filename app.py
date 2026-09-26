import streamlit as st
import requests
import re

# 1. Configuração da Página
st.set_page_config(page_title="Gerador de Links de Afiliado", page_icon="🔗")
st.title("🔗 Gerador de Links Automático")
st.write("Cole o link original do produto abaixo para gerar seu link monetizado.")

# 2. Lógica da API Shopee
def converter_shopee(url_original):
    # Puxa suas credenciais reais cadastradas no Secrets do Streamlit
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
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {app_secret}",
        "App-Id": app_id
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        dados = response.json()
        link_curto = dados['data']['generateShortLink']['shortLink']
        return link_curto
    except Exception as e:
        return f"Erro na API da Shopee. Detalhe: {e}"

# 3. Lógica do Mercado Livre
def converter_mercadolivre(url_original):
    # Puxa o ID do ML cadastrado no Secrets do Streamlit
    id_campanha = st.secrets["mercadolivre"]["id_campanha"]
    
    url_base = url_original.split('?')[0]
    link_convertido = f"{url_base}?camp={id_campanha}"
    return link_convertido

# 4. Interface do Usuário
url_input = st.text_input("Link do Produto (Shopee ou ML):", placeholder="https://...")

if st.button("Gerar Link de Afiliado"):
    if url_input:
        if re.search(r'shopee\.', url_input.lower()):
            with st.spinner("Conectando aos servidores da Shopee..."):
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