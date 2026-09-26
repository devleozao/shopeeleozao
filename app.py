import streamlit as st
import re

# 1. Configuração da Página
st.set_page_config(page_title="Gerador de Links de Afiliado", page_icon="🔗")
st.title("🔗 Gerador de Links de Afiliado")
st.write("Cole o link original do produto abaixo para gerar seu link de parceiro.")

# 2. Funções de Conversão (A Lógica)
def converter_shopee(url_original):
    # AQUI ENTRARÁ A LÓGICA DA SHOPEE (API ou manipulação de texto)
    # Por enquanto, é um exemplo demonstrativo:
    id_afiliado = "SEU_CODIGO_SHOPEE"
    link_convertido = f"{url_original}?aff_id={id_afiliado}"
    return link_convertido

def converter_mercadolivre(url_original):
    # AQUI ENTRARÁ A LÓGICA DO MERCADO LIVRE (API ou manipulação de texto)
    # Por enquanto, é um exemplo demonstrativo:
    id_afiliado = "SEU_CODIGO_ML"
    link_convertido = f"{url_original}&camp={id_afiliado}" 
    return link_convertido

# 3. Interface do Usuário
url_input = st.text_input("Link do Produto (Shopee ou Mercado Livre):", placeholder="https://...")

if st.button("Gerar Link de Afiliado"):
    if url_input:
        # Identifica a plataforma usando Regex simples
        if re.search(r'shopee\.', url_input.lower()):
            st.success("Plataforma identificada: Shopee 🛍️")
            link_final = converter_shopee(url_input)
            
            st.write("**Seu link de afiliado:**")
            # O st.code gera uma caixa de texto com um botão nativo de "Copiar"
            st.code(link_final, language="text")

        elif re.search(r'mercadolivre\.', url_input.lower()):
            st.success("Plataforma identificada: Mercado Livre 🤝")
            link_final = converter_mercadolivre(url_input)
            
            st.write("**Seu link de afiliado:**")
            st.code(link_final, language="text")

        else:
            st.error("Link não reconhecido. Certifique-se de que é um link válido da Shopee ou Mercado Livre.")
    else:
        st.warning("Por favor, cole um link antes de clicar no botão.")