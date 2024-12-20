from bs4 import BeautifulSoup
import re as regex
from datetime import datetime
from tqdm import tqdm

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

def gerar_relatorio(lista_arquivos, diretorio, nome_arquivo_saida="PATENTES.HTML"):
    html_fim = """
    <html>
    <head>
        <title>Relatorio de Patentes</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    <div class="container mt-4">
    <div class="table-responsive">
    <table class="table table-striped table-bordered">
    <thead class="table-dark">
    <tr>
    <th>Arquivo</th>
    <th>CNPJ</th>
    <th>RESULTADO</th>
    <th>NÚMERO DO PEDIDO </th>
    <th>Data do Depósito</th>
    <th>Título</th>
    <th>IPC</th>
    </tr>
    </thead>
    <tbody>
    """

    for arquivo in tqdm(lista_arquivos, desc="Processando arquivos"):
        cnpj, total_resultados, patentes = extrair_dados_patentes(f'{diretorio}/{arquivo}')
        if total_resultados == 0 and not patentes:
            html_fim += f"""
            <tr>
            <td>{arquivo}</td>
            <td>{cnpj}</td>
            <td>0</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            </tr>
            """
        else:
            for patente in patentes:
                html_fim += f"""
                <tr>
                <td>{arquivo}</td>
                <td>{cnpj}</td>
                <td>{total_resultados}</td>
                <td>{patente['numero_pedido']}</td>
                <td>{patente['data_deposito']}</td>
                <td>{patente['titulo']}</td>
                <td>{patente['ipc']}</td>
                </tr>
                """

    html_fim += """
    </tbody>
    </table>
    </div>
    </div>
    </body>
    </html>
    """

    with open(nome_arquivo_saida, "w") as arquivo_saida:
        arquivo_saida.write(html_fim)

if __name__ == "__main__":
    arquivos_html = [
        '00000000000191-01.html', '00001180000126-01.html', 
        '00003516000190-01.html', '00005275000118-01.html',
        '00008354000182-01.html', '00011009000106-01.html',
        '00014522000142-01.html', '00015174000128-01.html',
        '00020777000118-01.html', '00028986000108-01.html'
    ]
    gerar_relatorio(arquivos_html, './PATENTES', 'PATENTES.HTML')