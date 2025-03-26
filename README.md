# ProjetoPI

Repositório do script Python que coleta a previsão do tempo dos últimos 10 dias de uma estação meteorológica do INMET e armazena as informações em um banco de dados MongoDB.

O que o script faz?

    Pega a previsão de tempo: Ele faz uma requisição à API do INMET para obter as previsões de 10 dias para uma estação meteorológica específica.

    Filtra e organiza os dados: O script verifica os dados e garante que eles estão no formato correto antes de gravar no banco.

    Armazena no MongoDB: Os dados são salvos em um banco de dados MongoDB, com a data e hora da coleta, para você poder consultar sempre que precisar.

Dependências

Antes de rodar o script, você precisa instalar algumas dependências. Basta rodar o comando:

pip install requests pymongo

Essas bibliotecas são necessárias para fazer a requisição à API e interagir com o MongoDB.
Como usar

    Configurações iniciais:

        No código, altere o valor de ESTACAO_CODIGO para o código da estação que você quer consultar.

        Defina sua URI de conexão com o MongoDB na variável MONGO_URI.

    Rodar o script: Com tudo configurado, basta executar o script:

    python previsao_tempo.py

    Ver os dados: Depois de rodar o script, os dados vão ser armazenados na coleção tempo_real dentro do banco de dados dados no MongoDB.

Exemplo

Os dados são salvos em formato JSON e têm a seguinte aparência:

{
    "previsao_10dias": [
        {
            "data": "2025-03-25",
            "descricao": "Nublado",
            "temperatura_min": 18,
            "temperatura_max": 28,
            ...
        },
        {
            "data": "2025-03-26",
            "descricao": "Chuva",
            "temperatura_min": 19,
            "temperatura_max": 27,
            ...
        },
        ...
    ],
    "timestamp": "2025-03-25T14:30:00+00:00"
}

    previsao_10dias: Uma lista com as previsões para os próximos 10 dias.

    timestamp: A data e hora no momento que os dados foram coletados.

Algumas observações

    Limitações da API: Caso o código da estação não esteja correto ou a estrutura dos dados mude, é necessário consulta o site do INMET.

Licença

Este projeto está sob a Licença MIT. Para mais detalhes, veja o arquivo LICENSE.
