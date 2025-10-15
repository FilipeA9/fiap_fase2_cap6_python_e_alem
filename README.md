# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Monitor de Preços Agro (Atacado/Varejo)

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="#">Nome do integrante 1</a>
- <a href="#">Nome do integrante 2</a>
- <a href="#">Nome do integrante 3</a> 
- <a href="#">Nome do integrante 4</a> 
- <a href="#">Nome do integrante 5</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="#">Nome do Tutor</a>
### Coordenador(a)
- <a href="#">Nome do Coordenador</a>


## 📜 Descrição

O Monitor de Preços Agro é uma aplicação de linha de comando (CLI) desenvolvida em Python para registrar, consolidar e analisar preços de hortifrutis. O sistema é projetado para atender pequenos produtores e comerciantes, permitindo o acompanhamento de preços tanto no atacado (CEASAs) quanto no varejo.

A aplicação normaliza diferentes unidades de medida (ex: caixa de 23kg para kg), calcula indicadores importantes como média móvel e variação percentual, e gera alertas para identificar outliers de preços. A persistência de dados é feita primariamente em um banco de dados Oracle, com um mecanismo de contingência que utiliza arquivos JSON como espelho local para garantir a continuidade da operação mesmo em caso de falha de conexão com o banco.

Para mais detalhes técnicos, consulte a documentação do projeto [ai prject document fiap](document/ai_project_document_fiap.md) e os documentos complementares: [Documento de Especificação de Requisitos (SRS)](document/other/SRS_Monitor_Precos_Agro.pdf) e o [README Técnico](document/other/README_TECNICO.md).

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Contém arquivos de configuração do GitHub, como templates para issues.
- <b>assets</b>: Arquivos não-estruturados, como imagens e logos.
- <b>config</b>: Arquivos de configuração da aplicação, como parâmetros de negócio (`parametros.json`), fatores de conversão de unidades (`unidades.json`) e variáveis de ambiente (`.env.example`).
- <b>data</b>: Contém os arquivos de dados iniciais ou de exemplo, como `produtos.json` e `mercados.json`. O arquivo `observacoes.json` serve como espelho de contingência.
- <b>document</b>: Documentação do projeto, incluindo o SRS, o schema do banco de dados (`schema.sql`) e outros documentos relevantes.
- <b>exports</b>: Pasta onde os relatórios e consultas exportados pela aplicação são salvos.
- <b>logs</b>: Armazena os logs de operação da aplicação, facilitando a auditoria e o troubleshooting.
- <b>scripts</b>: Scripts auxiliares para tarefas como deploy, migração de banco de dados, etc.
- <b>src</b>: Todo o código-fonte da aplicação.
- <b>README.md</b>: Este arquivo, que serve como guia geral do projeto.

## 🔧 Como executar o código

### Pré-requisitos
- Python 3.10+
- Oracle Database (XE, Free, Autonomous ou compatível)
- Cliente Oracle Instant Client configurado

### Instalação

1. **Clonar o repositório**
   ```bash
   git clone <URL do repositório>
   cd monitor-precos-agro-reestruturado
   ```

2. **Criar ambiente virtual e instalar dependências**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configurar variáveis de ambiente**
   Copie o arquivo de exemplo da pasta `config` para a raiz do projeto com o nome `.env`.
   ```bash
   cp config/.env.example .env
   ```
   Edite o arquivo `.env` com as suas credenciais de acesso ao banco de dados Oracle.

4. **Setup do Banco de Dados**
   Execute o script `document/other/schema.sql` no seu banco de dados Oracle para criar as tabelas necessárias.

### Execução

Para iniciar a aplicação, execute o seguinte comando a partir da raiz do projeto:

```bash
python -m src.main
```

## 🗃 Histórico de lançamentos

* 0.1.0 - 09/10/2025
    * Desenvolvimento da primeira versão do projeto.

* 0.1.1 - 15/10/2025
    * Reestruturação inicial do repositório para o padrão FIAP.
    * Ajuste de caminhos e configuração.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

