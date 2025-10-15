# Código-Fonte

Esta pasta contém todo o código-fonte da aplicação "Monitor de Preços Agro".

## Estrutura

- **`main.py`**: Ponto de entrada da aplicação, responsável pela interface de linha de comando (CLI) e orquestração dos serviços.
- **`config/`**: Módulo de configuração para carregar parâmetros de arquivos e variáveis de ambiente.
- **`models/`**: Define as estruturas de dados (dataclasses) utilizadas na aplicação, como `RegistroPreco`.
- **`services/`**: Contém a lógica de negócio da aplicação, separada em diferentes módulos:
  - `arquivos.py`: Funções para manipulação de arquivos JSON, logs e exportações.
  - `db.py`: Funções para interação com o banco de dados Oracle.
  - `regras.py`: Implementação das regras de negócio, como cálculos de indicadores e detecção de alertas.
  - `validacao.py`: Funções para validar os dados de entrada do usuário.
- **`tests/`**: Testes unitários para garantir a qualidade e o correto funcionamento das regras de negócio.

