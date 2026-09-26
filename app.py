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
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {app_secret}",
        "App-Id": app_id
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Converte a resposta da Shopee para um dicionário Python
        dados = response.json()
        
        # Verifica se a Shopee mandou a chave 'data' com sucesso
        if 'data' in dados and dados['data'] is not None:
            link_curto = dados['data']['generateShortLink']['shortLink']
            return link_curto
        else:
            # Se deu errado, ele vai imprimir na sua tela EXATAMENTE o que a Shopee respondeu
            return f"A Shopee recusou a conexão. Motivo: {dados}"
            
    except Exception as e:
        return f"Erro no código Python. Detalhe: {e}"