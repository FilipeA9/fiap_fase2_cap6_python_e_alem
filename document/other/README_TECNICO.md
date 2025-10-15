# Monitor de Preços Agro (Atacado/Varejo)

Sistema em Python (CLI) para acompanhar preços de hortifrutis em mercados atacadistas (CEASAs) e varejistas, com cálculos de indicadores, alertas e contingência local via JSON.

## Sumário

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Modelo de Dados](#modelo-de-dados)
4. [Configuração do Ambiente](#configuração-do-ambiente)
5. [Setup do Banco Oracle](#setup-do-banco-oracle)
6. [Executando a Aplicação](#executando-a-aplicação)
7. [Tutoriais de Uso](#tutoriais-de-uso)
8. [Indicadores e Alertas](#indicadores-e-alertas)
9. [Contingência e Sincronização](#contingência-e-sincronização)
10. [Testes](#testes)
11. [Troubleshooting](#troubleshooting)
12. [Roadmap](#roadmap)

## Visão Geral

O monitor coleta preços diários de produtos hortifrutis, normaliza os valores para preço por kg, calcula média móvel, desvio padrão, variação percentual e gera alertas de outliers e quedas acentuadas. A persistência principal é em Oracle e, em caso de falha, os registros ficam armazenados no espelho local `data/observacoes.json` até a sincronização.

## Arquitetura

```
CLI (src/main.py)
│
├── Serviços (src/services)
│   ├── regras.py      → cálculos e alertas
│   ├── validacao.py   → regras de validação
│   ├── arquivos.py    → JSON, exportação e logs
│   └── db.py          → acesso Oracle (parametrizado)
│
├── Config (src/config/params.py) → parâmetros dinâmicos (janela média, z-score, unidades)
└── Models (src/models/entidades.py) → dataclasses de domínio
```

Os testes unitários vivem em `src/tests`. A aplicação segue camadas claras: CLI orquestra, services aplicam regras/IO, models tipam as estruturas.

## Modelo de Dados

As tabelas e restrições estão definidas em [`schema.sql`](schema.sql):

- `MARKETS(market_id, nome, tipo)`
- `PRODUCTS(product_id, codigo, nome, categoria)`
- `PRICES(price_id, data_ref, product_id, market_id, tipo_preco, unidade_orig, preco_orig, preco_kg, fonte)` com chave única `(data_ref, product_id, market_id, tipo_preco)`
- Índices para consultas por produto/mercado/data e view `VW_PRICES_RECENTES`.

## Configuração do Ambiente

1. **Pré-requisitos**
   - Python 3.10+
   - Oracle Database (XE, Free, Autonomous ou compatível). Exemplos: Oracle XE 21c com serviço `XEPDB1` ou Free `FREEPDB1`.
   - Oracle SQL Developer para executar o `schema.sql` (opcionalmente SQL*Plus).

2. **Clonar o repositório**

   ```bash
   git clone <repo>
   cd monitor-precos-agro
   ```

3. **Criar ambiente virtual e instalar dependências**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Variáveis de ambiente (.env)**

   Copie `.env.example` para `.env` e informe suas credenciais Oracle:

   ```bash
   cp .env.example .env
   ```

   Edite `.env` conforme o seu ambiente (usuário, senha e DSN `host:porta/SERVICE`).

5. **Parâmetros de negócio**

   - `data/unidades.json`: fatores de conversão para kg (`{"cx23kg": 23, "duzia": 12, ...}`)
   - `data/parametros.json` (opcional): ajuste de janela da média, z-score limite e limiar de queda. Exemplo:

     ```json
     {
       "media_window": 7,
       "zscore_limite": 2,
       "limiar_queda": -5
     }
     ```

   Alterações requerem reiniciar a aplicação.

## Setup do Banco Oracle

1. Abra o Oracle SQL Developer.
2. Crie uma conexão com o usuário definido no `.env`.
3. Execute o conteúdo de [`schema.sql`](schema.sql) para criar tabelas, índices e view:

   ```sql
   @/caminho/para/schema.sql
   ```

4. Opcional: cadastre produtos/mercados iniciais via CLI ou scripts SQL (inserindo em `PRODUCTS` e `MARKETS`).

## Executando a Aplicação

1. Ative o ambiente virtual (se ainda não estiver ativo).
2. Execute:

   ```bash
   python -m src.main
   ```

3. Menu principal:

   ```
   1. Cadastrar produto
   2. Cadastrar mercado
   3. Registrar preço
   4. Consultar histórico
   5. Exportar resultados
   6. Parâmetros
   0. Sair
   ```

## Tutoriais de Uso

### 1. Cadastrar Produto

Exemplo: `TOM_LV` – Tomate Longa Vida, categoria `hortalica`.

```
-- Cadastrar produto --
Código (ex.: TOM_LV): TOM_LV
Nome: Tomate Longa Vida
Categoria: hortalica
```

O produto é gravado no Oracle (quando disponível) e atualizado em `data/produtos.json`.

### 2. Cadastrar Mercado

```
-- Cadastrar mercado --
Nome (ex.: CEASA-GO): CEASA-GO
Tipo [ATACADO/VAREJO]: ATACADO
```

### 3. Registrar Preço

Registre preços diários para cada tipo (`ATACADO_MIN`, `ATACADO_MED`, `ATACADO_MAX`, `VAREJO`). Exemplo com unidade `cx23kg`:

```
-- Registrar preço --
Data (YYYY-MM-DD): 2024-05-01
Produto (código): TOM_LV
Mercado (nome): CEASA-GO
Tipo de preço [...] : ATACADO_MED
Unidade original (ex.: kg, cx23kg): cx23kg
Preço original: 230
Fonte (CEASA, Coleta manual...): CEASA
```

Saída esperada:

```
Resumo do registro:
Preço normalizado (kg): R$ 10.00
Média móvel (7d): 10.50
Desvio padrão: 0.58
Variação diária: -5.00%
ALERTA: QUEDA - Queda de -5.00% em relação ao dia anterior
```

### 4. Consultar Histórico

Utilize filtros (produto, mercado, tipo, intervalo). Exemplo de saída:

```
| Data       | Produto   | Mercado  | Tipo         | Preco/kg   | Media7 | Var%    | Alerta        |
|------------|-----------|----------|--------------|------------|--------|--------|---------------|
| 2024-05-01 | TOM_LV    | CEASA-GO | ATACADO_MIN  | R$ 9.50    | —      | —      |               |
| 2024-05-01 | TOM_LV    | CEASA-GO | ATACADO_MED  | R$ 10.00   | —      | —      |               |
| 2024-05-01 | TOM_LV    | CEASA-GO | ATACADO_MAX  | R$ 10.40   | —      | —      |               |
| 2024-05-02 | TOM_LV    | CEASA-GO | ATACADO_MIN  | R$ 9.30    | 9.40   | -2.11% | QUEDA         |
| 2024-05-02 | TOM_LV    | CEASA-GO | ATACADO_MED  | R$ 9.80    | 9.90   | -2.00% |               |
| 2024-05-02 | TOM_LV    | CEASA-GO | ATACADO_MAX  | R$ 10.60   | 10.50  | 1.92%  | OUTLIER_ALTA  |
```

### 5. Exportar Resultados

Após uma consulta, selecione "Exportar resultados". Serão gerados:

- `exports/consulta-YYYYMMDD-HHMM.json`
- `exports/relatorio-YYYYMMDD-HHMM.txt`

O relatório `.txt` inclui o sumário de alertas do período.

## Indicadores e Alertas

- **Normalização**: `preco_kg = preco_original / fator_unidade`. Fatores em `data/unidades.json`.
- **Média móvel (até 7 dias)**: média simples das últimas observações do par produto/mercado/tipo.
- **Desvio padrão**: desvio padrão amostral da mesma janela.
- **Variação diária**: `((preco_hoje - preco_ontem) / preco_ontem) * 100`.
- **Alertas**:
  - `OUTLIER_ALTA`: `preco_hoje > media7 + zscore_limite * desvio`.
  - `OUTLIER_BAIXA`: `preco_hoje < media7 - zscore_limite * desvio`.
  - `QUEDA`: `variacao_percentual <= limiar_queda` (padrão -5%).

## Contingência e Sincronização

- Ao inserir um preço, o sistema tenta persistir no Oracle.
- Se ocorrer `OracleError` ou indisponibilidade do driver, o registro é guardado em `data/observacoes.json` com `"pendente_sync": true`.
- Na inicialização, a aplicação tenta sincronizar estes registros com Oracle. Quando o envio é bem-sucedido, o campo `pendente_sync` é atualizado e o JSON regravado.

## Testes

Executar a suíte de testes (necessário `pytest`):

```bash
python -m pytest src/tests
```

Os testes cobrem funções críticas de cálculo e validação.

## Troubleshooting

| Problema | Diagnóstico | Solução |
|----------|-------------|---------|
| **Erro de conexão Oracle** | Mensagem "Driver Oracle não disponível" ou credenciais inválidas | Instale o cliente Instant Client, confira DSN e variáveis no `.env` |
| **Unidade inválida** | "Unidade desconhecida" ao registrar preço | Consulte e ajuste `data/unidades.json` |
| **Deduplicação** | "Já existe registro" | Verifique se a combinação data/produto/mercado/tipo já foi cadastrada |
| **Sem exportação** | Opção 5 não gera arquivos | Realize uma consulta (opção 4) antes de exportar |

Os logs detalhados ficam em `logs/operacoes.txt`.

## Roadmap

- Suporte completo a mercados VAREJO (fluxos dedicados e indicadores comparativos).
- Comparativo atacado × varejo e dashboards de tendências.
- Importação em massa via CSV (CEASA, lojas) e API.
- Interface web responsiva e autenticação.
