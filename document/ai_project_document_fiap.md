
<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=30% height=30%>

# AI Project Document - Módulo 1 - FIAP

## Nome do Grupo

#### Nomes dos integrantes do grupo

Filipe Augusto Lima Silva
filipe09093@gmail.com

Laisa Cristina Capodifoglio Andrade
laisaandradedev@gmail.com

Johnathan da Cruz Gatti
johnathan.gatti@gmail.com

Diogo Ferreira Pereira
diogo.zfp@gmail.com

André Victor Gonçalves Toledo
andrevgtoledo@gmail.com

## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

O mercado de hortifrutis no Brasil apresenta desafios significativos relacionados à volatilidade de preços, que impactam diretamente pequenos produtores e comerciantes. A aplicação de técnicas de análise de dados e algoritmos estatísticos para monitoramento e detecção de anomalias em séries temporais de preços representa uma área de crescente interesse na agricultura de precisão e gestão comercial.

A Inteligência Artificial aplicada ao agronegócio tem se expandido globalmente, com foco em otimização de processos, previsão de demanda e análise preditiva. No contexto brasileiro, onde o agronegócio representa parcela significativa do PIB, soluções que auxiliam na tomada de decisão baseada em dados históricos e indicadores estatísticos são fundamentais para profissionalizar o setor, especialmente para pequenos e médios produtores que não têm acesso a ferramentas corporativas complexas.

O projeto "Monitor de Preços Agro" se insere neste contexto ao fornecer uma ferramenta acessível e auditável que utiliza algoritmos de análise estatística para processar dados de preços de hortifrutis, tanto no atacado (CEASAs) quanto no varejo, gerando insights acionáveis através de indicadores e alertas automatizados.

### 1.1.2. Descrição da Solução Desenvolvida

O Monitor de Preços Agro é uma aplicação de linha de comando (CLI) desenvolvida em Python que permite o registro, consolidação e análise de preços de produtos hortifrutis. A solução foi projetada especificamente para atender pequenos produtores e comerciantes, oferecendo funcionalidades essenciais para acompanhamento de tendências de mercado.

A aplicação implementa algoritmos estatísticos para normalização de unidades de medida, cálculo de médias móveis, desvio padrão e variação percentual. O sistema utiliza detecção de outliers baseada em z-score e identifica quedas acentuadas de preços, gerando alertas automáticos que auxiliam na tomada de decisão para negociações e planejamento de compras.

A arquitetura da solução combina persistência em banco de dados Oracle com um mecanismo de contingência baseado em arquivos JSON, garantindo a continuidade operacional mesmo em cenários de indisponibilidade do banco de dados. Esta abordagem híbrida assegura que nenhum dado seja perdido e que o sistema mantenha sua funcionalidade em diferentes contextos de infraestrutura.

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

O projeto tem como objetivo principal disponibilizar um monitor de preços simples, confiável e extensível que consolide preços de hortifrutis do atacado e, opcionalmente, do varejo, normalizando unidades e produzindo indicadores e alertas que auxiliem na tomada de decisão comercial.

Os objetivos específicos incluem:

- Implementar um sistema de normalização de unidades de medida para permitir comparações consistentes entre diferentes formas de comercialização (caixas, dúzias, quilogramas, etc.)
- Desenvolver algoritmos de cálculo de indicadores estatísticos, incluindo média móvel de 7 dias, desvio padrão e variação percentual diária
- Criar um mecanismo de detecção de anomalias baseado em z-score para identificar outliers de preços (alta e baixa)
- Implementar sistema de alertas para quedas acentuadas de preços (superiores a 5%)
- Garantir a persistência confiável de dados através de banco de dados Oracle com mecanismo de contingência local
- Fornecer funcionalidades de consulta histórica com filtros por produto, mercado, tipo de preço e intervalo de datas
- Permitir exportação de dados e relatórios em formatos JSON e texto para análises posteriores
- Manter logs detalhados de operações para auditoria e troubleshooting

## 2.2. Público-Alvo

O público-alvo do projeto é composto por diferentes perfis de usuários do setor de hortifrutis:

**Produtor/Atacadista (Operador)**: Profissional que registra preços observados ou negociados em CEASAs e consulta tendências para definir preços diários de venda. Este usuário necessita de informações rápidas e confiáveis para tomar decisões de precificação em um mercado volátil.

**Comerciante Varejista (Operador)**: Profissional que consulta histórico de preços para precificação de produtos em sua loja e identificação de oportunidades de promoções. Futuramente, este usuário também poderá registrar preços de gôndola para análise comparativa com o atacado.

**Analista (Leitor/Power User)**: Profissional responsável por cruzar séries históricas, exportar relatórios consolidados e gerar visões estratégicas para a diretoria. Este usuário necessita de funcionalidades avançadas de consulta e exportação de dados.

**Administrador**: Profissional responsável por gerenciar cadastros de produtos e mercados, realizar backups, ajustar parâmetros de cálculo (janelas de média, limites de alerta) e garantir a integridade operacional do sistema.

## 2.3. Metodologia

O desenvolvimento do projeto seguiu uma abordagem estruturada em camadas, priorizando a separação de responsabilidades e a testabilidade do código. A metodologia adotada incluiu as seguintes etapas:

**Levantamento de Requisitos**: Análise do contexto de negócio do setor de hortifrutis, identificação de stakeholders e definição de requisitos funcionais e não funcionais através do documento SRS (Software Requirements Specification).

**Modelagem de Dados**: Definição do modelo de dados relacional para Oracle, incluindo tabelas de produtos, mercados e preços, com restrições de integridade e índices para otimização de consultas.

**Arquitetura em Camadas**: Implementação de uma arquitetura modular com separação clara entre interface (CLI), lógica de negócio (services), modelos de dados (models) e configuração (config).

**Desenvolvimento Iterativo**: Implementação incremental de funcionalidades, começando pelas operações básicas de CRUD (Create, Read, Update, Delete) e evoluindo para cálculos estatísticos e detecção de anomalias.

**Testes Unitários**: Desenvolvimento de testes automatizados usando pytest para validar funções críticas de cálculo e validação, garantindo a qualidade e confiabilidade dos algoritmos implementados.

**Documentação Técnica**: Elaboração de documentação detalhada incluindo README técnico, schema do banco de dados, e guias de instalação e uso.

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias, ferramentas e bibliotecas:

**Linguagem de Programação**:
- Python 3.10+ como linguagem principal, escolhida por sua ampla adoção em análise de dados, rica biblioteca padrão e facilidade de manutenção

**Banco de Dados**:
- Oracle Database (XE, Free, Autonomous ou compatível) para persistência principal dos dados
- Driver `oracledb` para conexão e operações com Oracle

**Bibliotecas Python**:
- `python-dotenv`: Gerenciamento de variáveis de ambiente e configurações sensíveis
- `tabulate`: Formatação de tabelas para exibição no terminal
- `pytest`: Framework para testes unitários
- Biblioteca padrão Python: `statistics`, `math`, `json`, `datetime`, `pathlib` para operações de cálculo e manipulação de dados

**Ferramentas de Desenvolvimento**:
- Git para controle de versão
- Oracle SQL Developer para gerenciamento do banco de dados
- Ambientes virtuais Python (venv) para isolamento de dependências

**Arquitetura de Dados**:
- JSON para armazenamento de configurações (unidades, parâmetros) e contingência local
- Arquivos de texto para logs de operações

## 3.2. Modelagem e Algoritmos

O projeto implementa diversos algoritmos estatísticos e de processamento de dados, organizados em módulos especializados:

**Normalização de Unidades** (`regras.py`):
Algoritmo que converte preços em diferentes unidades de medida para uma unidade padrão (kg), permitindo comparações consistentes. A fórmula implementada é:

```
preco_kg = preco_original / fator_unidade
```

Onde `fator_unidade` é obtido de um dicionário de conversão configurável (ex: cx23kg = 23, dúzia = 12).

**Média Móvel Simples** (`regras.py`):
Implementação de média móvel com janela configurável (padrão 7 dias) para suavizar flutuações de curto prazo e identificar tendências. O algoritmo utiliza a função `mean()` da biblioteca `statistics` sobre os últimos N valores válidos da série temporal.

**Desvio Padrão Amostral** (`regras.py`):
Cálculo do desvio padrão para medir a dispersão dos preços em relação à média, utilizando a fórmula:

```
desvio = sqrt(sum((x - media)^2) / (n - 1))
```

**Variação Percentual** (`regras.py`):
Cálculo da variação diária de preços para identificar mudanças significativas:

```
variacao = ((preco_hoje - preco_ontem) / preco_ontem) * 100
```

**Detecção de Outliers por Z-Score** (`regras.py`):
Algoritmo de detecção de anomalias baseado em z-score, que identifica preços que se desviam significativamente da média. Um preço é considerado outlier quando:

- **OUTLIER_ALTA**: `preco_hoje > media7 + zscore_limite * desvio` (padrão: z-score > 2)
- **OUTLIER_BAIXA**: `preco_hoje < media7 - zscore_limite * desvio` (padrão: z-score < -2)

**Alerta de Queda Acentuada** (`regras.py`):
Detecção de quedas percentuais significativas que podem indicar oportunidades de compra ou problemas de qualidade:

- **QUEDA**: `variacao_percentual <= limiar_queda` (padrão: -5%)

**Validação de Dados** (`validacao.py`):
Conjunto de regras de validação que garantem a integridade dos dados antes da persistência:
- Validação de formato de data (YYYY-MM-DD)
- Verificação de existência de produto e mercado
- Validação de preço positivo
- Verificação de unidade reconhecida
- Detecção de duplicidade por chave única (data, produto, mercado, tipo_preco)

Estes algoritmos foram escolhidos por sua simplicidade, eficiência computacional e interpretabilidade, características essenciais para uma ferramenta voltada a pequenos produtores que necessitam de resultados claros e acionáveis.

## 3.3. Treinamento e Teste

Como o projeto não utiliza modelos de machine learning que requerem treinamento supervisionado, o processo de validação focou em testes unitários e de integração para garantir a correção dos algoritmos estatísticos e regras de negócio.

**Conjunto de Dados de Teste**:
Foram criados conjuntos de dados sintéticos representando cenários típicos do mercado de hortifrutis:
- Séries temporais com preços estáveis
- Séries com tendência de alta ou baixa
- Séries com outliers simulados (picos e quedas)
- Séries com diferentes unidades de medida

**Testes Unitários** (`src/tests/`):
Implementação de testes automatizados usando pytest para validar:

- **Normalização de unidades**: Verificação de conversões corretas para diferentes fatores
- **Cálculo de média móvel**: Validação com séries de diferentes tamanhos
- **Cálculo de desvio padrão**: Comparação com valores esperados
- **Variação percentual**: Teste de cenários de alta, baixa e estabilidade
- **Detecção de alertas**: Validação de identificação correta de outliers e quedas
- **Validação de entrada**: Teste de rejeição de dados inválidos

**Métricas de Avaliação**:
- Cobertura de código: Objetivo de ≥80% para funções de regras de negócio
- Precisão dos cálculos: Comparação com valores calculados manualmente
- Tempo de execução: Consultas devem retornar em < 2s para até 10.000 registros

**Resultados dos Testes**:
Todos os testes unitários passaram com sucesso, validando a correção dos algoritmos implementados. Os testes de performance confirmaram que o sistema atende aos requisitos não funcionais de desempenho, com consultas históricas retornando em tempo adequado mesmo com volumes significativos de dados.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

O projeto alcançou os objetivos estabelecidos, entregando uma solução funcional e confiável para monitoramento de preços de hortifrutis. Os principais resultados obtidos incluem:

**Funcionalidades Implementadas**:
Todas as funcionalidades previstas no escopo do MVP foram implementadas com sucesso, incluindo cadastro de produtos e mercados, registro de preços com normalização automática, cálculo de indicadores estatísticos, detecção de alertas, consultas históricas com filtros, exportação de dados e logs de auditoria.

**Precisão dos Algoritmos**:
Os algoritmos estatísticos implementados demonstraram precisão adequada nos testes realizados. A normalização de unidades funciona corretamente para diferentes fatores de conversão, e os cálculos de média móvel, desvio padrão e variação percentual produzem resultados consistentes com os valores esperados.

**Detecção de Anomalias**:
O sistema de detecção de outliers baseado em z-score mostrou-se eficaz para identificar preços anormalmente altos ou baixos. Em testes com dados sintéticos contendo outliers simulados, o sistema identificou corretamente 100% dos casos onde o z-score excedia o limite configurado (padrão: 2).

**Mecanismo de Contingência**:
O sistema de contingência baseado em JSON funcionou conforme esperado, permitindo a continuidade das operações mesmo quando o banco de dados Oracle está indisponível. A sincronização automática na reinicialização garante que nenhum dado seja perdido.

**Performance**:
O sistema atende aos requisitos de performance estabelecidos, com consultas históricas retornando em menos de 2 segundos para volumes de até 10.000 registros. A arquitetura em camadas e o uso de índices no banco de dados contribuem para a eficiência das operações.

**Pontos de Melhoria Identificados**:
Durante o desenvolvimento e testes, alguns pontos de melhoria foram identificados para versões futuras, incluindo a necessidade de uma interface gráfica mais amigável, integração com APIs externas de CEASAs para importação automática de dados, e implementação de modelos preditivos para previsão de preços.

## 4.2. Feedback dos Usuários

Como o projeto foi desenvolvido como uma atividade acadêmica, o feedback inicial foi obtido através de revisões técnicas e simulações de uso. Os principais pontos levantados incluem:

**Aspectos Positivos**:
- Interface CLI clara e intuitiva, com menus numerados e mensagens de orientação
- Cálculo automático de indicadores facilita a interpretação dos dados
- Sistema de alertas destaca informações relevantes para tomada de decisão
- Mecanismo de contingência proporciona confiança na continuidade operacional
- Logs detalhados facilitam auditoria e troubleshooting

**Sugestões de Melhoria**:
- Implementação de interface web para facilitar o acesso remoto e uso por múltiplos usuários
- Adição de gráficos e visualizações para melhor compreensão de tendências
- Funcionalidade de importação em massa via CSV para agilizar o registro de múltiplos preços
- Comparativo automático entre atacado e varejo para cálculo de margem
- Notificações automáticas (email/SMS) quando alertas são detectados

**Cenários de Uso Validados**:
Foram validados os principais fluxos de uso através de testes de aceitação:
- Cadastro de novos produtos e mercados
- Registro diário de preços com diferentes unidades
- Consulta de histórico com diversos filtros
- Exportação de relatórios para análise externa
- Recuperação de dados após indisponibilidade do banco

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

O projeto Monitor de Preços Agro atingiu com sucesso os objetivos estabelecidos, entregando uma solução funcional e confiável para o monitoramento de preços de hortifrutis. A aplicação demonstrou capacidade de processar dados de forma consistente, calcular indicadores estatísticos precisos e gerar alertas relevantes para apoiar a tomada de decisão comercial.

**Pontos Fortes da Solução**:

A arquitetura em camadas adotada proporcionou um código organizado, manutenível e testável. A separação clara entre interface, lógica de negócio e persistência facilita futuras extensões e modificações. O mecanismo de contingência baseado em JSON garante a resiliência do sistema, evitando perda de dados em cenários de indisponibilidade do banco de dados Oracle.

Os algoritmos estatísticos implementados são computacionalmente eficientes e produzem resultados interpretáveis, características essenciais para uma ferramenta voltada a pequenos produtores. O sistema de detecção de outliers baseado em z-score é uma abordagem consolidada e confiável para identificação de anomalias em séries temporais.

A documentação técnica completa, incluindo SRS, README técnico e schema do banco de dados, facilita a compreensão do sistema e sua manutenção futura. Os testes unitários implementados garantem a qualidade e confiabilidade dos componentes críticos.

**Pontos a Melhorar**:

A interface CLI, embora funcional, pode ser uma barreira para usuários menos familiarizados com linha de comando. A ausência de visualizações gráficas limita a capacidade de análise de tendências de longo prazo. O processo de registro de preços é manual e pode ser demorado quando há muitos produtos a serem atualizados diariamente.

A solução atual não implementa funcionalidades preditivas, limitando-se a análises descritivas e detecção de anomalias. A integração com fontes externas de dados (APIs de CEASAs) ainda não está disponível, exigindo entrada manual de informações.

**Plano de Ações Futuras**:

**Fase 2 - Varejo e Comparativos** (curto prazo):
- Implementar fluxos específicos para registro de preços de varejo por loja/bairro
- Desenvolver funcionalidade de comparativo atacado × varejo para cálculo de margem aproximada
- Criar módulo de detecção de oportunidades de promoções baseado em quedas significativas de preço

**Fase 3 - Interface Web e Visualizações** (médio prazo):
- Desenvolver interface web responsiva usando frameworks modernos (React/Vue.js)
- Implementar dashboards com gráficos de tendências e distribuições de preços
- Adicionar sistema de autenticação e controle de acesso para múltiplos usuários
- Criar funcionalidade de notificações automáticas (email/SMS) para alertas críticos

**Fase 4 - Automação e Inteligência** (longo prazo):
- Implementar importação automática de dados via APIs de CEASAs e outras fontes
- Desenvolver modelos preditivos usando técnicas de séries temporais (ARIMA, Prophet)
- Criar sistema de recomendação de preços baseado em histórico e tendências
- Implementar análise de sazonalidade e identificação de padrões recorrentes

**Fase 5 - Expansão e Integração** (longo prazo):
- Expandir para outras categorias de produtos agrícolas além de hortifrutis
- Integrar com sistemas de gestão (ERPs) através de APIs
- Desenvolver aplicativo móvel para registro de preços em campo
- Criar marketplace para conectar produtores e compradores baseado em dados de preços

O projeto estabelece uma base sólida para evolução contínua, com arquitetura extensível e documentação adequada. As próximas fases de desenvolvimento agregarão valor significativo aos usuários, transformando a solução em uma plataforma completa de inteligência de mercado para o setor de hortifrutis.

# <a name="c6"></a>6. Referências

1. **Python Software Foundation**. Python 3.10 Documentation. Disponível em: https://docs.python.org/3.10/

2. **Oracle Corporation**. Oracle Database Documentation. Disponível em: https://docs.oracle.com/en/database/

3. **Oracle Corporation**. python-oracledb Documentation. Disponível em: https://python-oracledb.readthedocs.io/

4. **pytest Development Team**. pytest Documentation. Disponível em: https://docs.pytest.org/

5. **CEAGESP**. Companhia de Entrepostos e Armazéns Gerais de São Paulo. Disponível em: https://www.ceagesp.gov.br/

6. **CONAB**. Companhia Nacional de Abastecimento - Hortigranjeiros. Disponível em: https://www.conab.gov.br/

7. **Montgomery, D. C., & Runger, G. C.** (2014). Applied Statistics and Probability for Engineers. 6th Edition. Wiley.

8. **Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M.** (2015). Time Series Analysis: Forecasting and Control. 5th Edition. Wiley.

# <a name="c7"></a>Anexos

## Anexo A - Diagrama de Arquitetura

A aplicação segue uma arquitetura em camadas com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI (src/main.py)                        │
│                  Interface de Linha de Comando               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Camada de Serviços                         │
├─────────────────────────────────────────────────────────────┤
│  regras.py         │  validacao.py  │  arquivos.py  │ db.py │
│  • Normalização    │  • Validações  │  • JSON       │ Oracle│
│  • Média móvel     │  • Sanitização │  • Logs       │ CRUD  │
│  • Desvio padrão   │  • Regras      │  • Exportação │       │
│  • Alertas         │                │               │       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Camada de Modelos e Configuração                │
├─────────────────────────────────────────────────────────────┤
│  models/entidades.py       │  config/params.py              │
│  • RegistroPreco           │  • Parâmetros dinâmicos        │
│  • Dataclasses             │  • Variáveis de ambiente       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Camada de Persistência                    │
├──────────────────────────────┬──────────────────────────────┤
│      Oracle Database         │      Arquivos JSON           │
│  • MARKETS                   │  • produtos.json             │
│  • PRODUCTS                  │  • mercados.json             │
│  • PRICES                    │  • observacoes.json          │
└──────────────────────────────┴──────────────────────────────┘
```

## Anexo B - Modelo de Dados

**Tabela MARKETS**:
```sql
CREATE TABLE MARKETS (
    market_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    tipo VARCHAR2(10) CHECK (tipo IN ('ATACADO','VAREJO'))
);
```

**Tabela PRODUCTS**:
```sql
CREATE TABLE PRODUCTS (
    product_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    codigo VARCHAR2(20) UNIQUE NOT NULL,
    nome VARCHAR2(100) NOT NULL,
    categoria VARCHAR2(50)
);
```

**Tabela PRICES**:
```sql
CREATE TABLE PRICES (
    price_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    data_ref DATE NOT NULL,
    product_id NUMBER NOT NULL REFERENCES PRODUCTS(product_id),
    market_id NUMBER NOT NULL REFERENCES MARKETS(market_id),
    tipo_preco VARCHAR2(15) CHECK (tipo_preco IN 
        ('ATACADO_MIN','ATACADO_MED','ATACADO_MAX','VAREJO')),
    unidade_orig VARCHAR2(20),
    preco_orig NUMBER(12,2) CHECK (preco_orig > 0),
    preco_kg NUMBER(12,4) CHECK (preco_kg > 0),
    fonte VARCHAR2(40),
    CONSTRAINT uq_price UNIQUE (data_ref, product_id, market_id, tipo_preco)
);
```

## Anexo C - Exemplo de Uso

**Cadastro de Produto**:
```
Código: TOM_LV
Nome: Tomate Longa Vida
Categoria: hortalica
```

**Registro de Preço**:
```
Data: 2025-10-15
Produto: TOM_LV
Mercado: CEASA-GO
Tipo: ATACADO_MED
Unidade: cx23kg
Preço: 230.00
Fonte: CEASA
```

**Saída do Sistema**:
```
Resumo do registro:
Preço normalizado (kg): R$ 10.00
Média móvel (7d): 10.50
Desvio padrão: 0.58
Variação diária: -4.76%
```

## Anexo D - Estrutura de Pastas do Projeto

```
monitor-precos-agro/
├── config/              # Arquivos de configuração
│   ├── .env.example
│   ├── unidades.json
│   └── parametros.json
├── data/                # Dados operacionais
│   ├── produtos.json
│   ├── mercados.json
│   └── observacoes.json
├── document/            # Documentação
│   ├── SRS_Monitor_Precos_Agro.pdf
│   ├── schema.sql
│   └── README_TECNICO.md
├── exports/             # Relatórios exportados
├── logs/                # Logs de operação
├── src/                 # Código-fonte
│   ├── config/
│   │   └── params.py
│   ├── models/
│   │   └── entidades.py
│   ├── services/
│   │   ├── arquivos.py
│   │   ├── db.py
│   │   ├── regras.py
│   │   └── validacao.py
│   ├── tests/
│   │   ├── test_regras.py
│   │   └── test_validacao.py
│   └── main.py
└── requirements.txt
```

## Anexo E - Indicadores Calculados

| Indicador | Fórmula | Interpretação |
|-----------|---------|---------------|
| **Preço Normalizado (kg)** | `preco_kg = preco_original / fator_unidade` | Preço padronizado por quilograma |
| **Média Móvel 7d** | `media = sum(ultimos_7_precos) / 7` | Tendência de curto prazo |
| **Desvio Padrão** | `desvio = sqrt(sum((x - media)^2) / (n-1))` | Volatilidade dos preços |
| **Variação Diária (%)** | `var = ((hoje - ontem) / ontem) * 100` | Mudança percentual diária |
| **Z-Score** | `z = (preco - media) / desvio` | Distância da média em desvios padrão |

## Anexo F - Critérios de Alerta

| Tipo de Alerta | Condição | Ação Recomendada |
|----------------|----------|------------------|
| **OUTLIER_ALTA** | `preco > media + 2*desvio` | Investigar causa do preço elevado |
| **OUTLIER_BAIXA** | `preco < media - 2*desvio` | Oportunidade de compra ou problema de qualidade |
| **QUEDA** | `variacao <= -5%` | Avaliar negociação ou estoque |