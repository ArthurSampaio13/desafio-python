# Documentação do Projeto

## Visão Geral
Este projeto tem como objetivo realizar a extração de informações de arquivos HTML contendo dados de patentes.  

O projeto foi desenvolvido para lidar com arquivos contendo informações de processos de patentes, como números de pedidos, datas de depósito, títulos, e classificações IPC. Além disso, o relatório gerado apresenta detalhes como o CNPJ do depositante e se houve resultados para cada arquivo analisado.

## Estrutura do Projeto
O projeto é composto pelos seguintes elementos:

- **Pasta `PATENTES`**: Contém os arquivos HTML que serão analisados.
- **SOLUTION.py**: Contém a lógica de extração e geração do relatório.
- **Arquivo de Saída `PATENTES.HTML`**: O relatório final gerado após a análise dos arquivos.

## Tecnologias Utilizadas
### Bibliotecas Python
As seguintes bibliotecas foram utilizadas no desenvolvimento do projeto:

1. **BeautifulSoup**:
   - Justificativa: Realiza o web scraping das páginas HTML, permitindo navegar e extrair dados.

2. **tqdm**:
   - Justificativa: Apresenta uma barra de progresso dinâmica para o processamento dos arquivos. Isso se torna útil em cenários com muitos arquivos para serem analisados.fornecendo feedback visual ao usuário.

3. **re (Regex)**:
   - Justificativa: Facilita a busca de informações dentro do HTML, especialmente em casos onde elementos como `divs` e `font` não possuem identificadores próprios. 

4. **datetime**:
   - Justificativa: Realiza a conversão e formatação de datas no formato DD/MM/YYYY para YYYY-MM-DD.

## Funcionamento
### 1. Extração de Dados
A função `extrair_dados_patentes` lê cada arquivo HTML e realiza as seguintes etapas:
- Identifica o CNPJ do depositante utilizando regex.
- Verifica se há resultados para a pesquisa de patentes.
- Coleta informações detalhadas de cada patente listada no HTML.

### 2. Geração do Relatório
A função `gerar_relatorio` processa os arquivos da pasta `patentes` e cria um arquivo HTML formatado com as informações extraídas. O relatório apresenta:
- Nome do arquivo processado.
- CNPJ do depositante.
- Total de resultados encontrados.
- Detalhes de cada patente (número do pedido, data do depósito, título, e IPC).

## Configuração do Ambiente
Para executar o projeto, siga os passos abaixo para configurar um ambiente virtual e instalar as dependências:

1. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```

2. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. Instale as dependências do arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Execução do Projeto
1. Execute o script Python principal.
   ```bash
   python SOLUTION.py
   ```
2. O relatório será gerado no arquivo `PATENTES.HTML` na mesma pasta do script.

## Exemplo de Saída
O relatório gerado inclui uma tabela responsiva com informações detalhadas, utilizando o framework Bootstrap para estilização.

### Trecho Exemplo
| Arquivo                | CNPJ           | Resultado | Número do Pedido | Data do Depósito | Título       | IPC   |
|------------------------|----------------|-----------|-------------------|----------------|--------------|-------|
| Arq1 |                      CNPJ1          |  2         | PI01...          | YYYY-MM-DD    | Título     | IPC.. |
| Arq1 |                      CNPJ1          |  2         | PI02...          | ...           |...         | ...   |                   
| Arq2 |                      CNPJ2          |  0         | -                |  -            | -          | -     |
| Arq3 |                      CNPJ3          |  10        | PI00...          |...            |...         |...|
|... |                   |                                | PI99...          |...            | ...        |...|

## Requisitos
Certifique-se de ter instalado as bibliotecas necessárias:
```bash
pip install beautifulsoup4 tqdm
```



