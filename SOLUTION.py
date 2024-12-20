from bs4 import BeautifulSoup
import re as regex
from datetime import datetime

"""
Justificativa para escolha das bibliotecas:
1. BeautifulSoup: Por ser um desafio de extração de dados de um arquivo HTML, 
                  optei por utilizar o BeautifulSoup, pois traz uma abstração e simplicidade.

2. tqdm: A utilização da biblioteca tqdm foi para trazer uma melhor visualização do progresso da extração dos dados. 
         Caso sejam adicionados mais arquivos, seria interessante utilizá-la por fornecer uma barra de progresso.

3. re (Regex): A utilização da biblioteca re foi para realizar a busca de padrões no texto. 
               Poderia ter utilizado o BeautifulSoup, mas o site tinha muitas tags parecidas e a utilização do re foi mais eficiente.

4. datetime: A utilização da biblioteca datetime foi para formatar a data, visto que no HTML estava no formato DD/MM/YYYY.
"""

def extrair_dados_patentes(html):
    with open(html, "r", encoding="latin-1") as arquivo:
        conteudo = BeautifulSoup(arquivo.read(), 'html.parser')

    formulario_nenhuma_patente = conteudo.find('form', {'name': 'F_CadastroPatente'}) # O que eu percebi foi que quando o resultado é nenhum, o formulário é diferente
    texto_completo = conteudo.get_text()

    cnpj_encontrado = regex.search(r"CPF ou CNPJ do Depositante:\s*'(\d+)'", texto_completo)
    if cnpj_encontrado:
        cnpj = cnpj_encontrado.group(1)
    else:
        cnpj = "Não encontrado"

    if formulario_nenhuma_patente:
        mensagem_sem_resultado = conteudo.find("td", string=lambda texto: texto and "Nenhum resultado foi encontrado" in texto)
        if mensagem_sem_resultado:
            return cnpj, 0, []

    resultado_encontrado = regex.search(r"Foram encontrados\s*<b>(\d+)</b>\s*processos", str(conteudo))
    if resultado_encontrado:
        total_resultados = resultado_encontrado.group(1)
    else:
        total_resultados = 0

    lista_patentes = []
    linhas_tabela = conteudo.find_all("tr", bgcolor=["#E0E0E0", "white"])
    for linha in linhas_tabela:
        colunas = linha.find_all("td")
        if len(colunas) >= 4:
            lista_patentes.append({
                'numero_pedido': colunas[0].get_text(strip=True),
                'data_deposito': datetime.strptime(colunas[1].get_text(strip=True), "%d/%m/%Y").strftime("%Y-%m-%d"),
                'titulo': colunas[2].get_text(strip=True),
                'ipc': colunas[3].get_text(strip=True)
            })

    return cnpj, total_resultados, lista_patentes