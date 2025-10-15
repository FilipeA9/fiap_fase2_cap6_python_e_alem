# Arquivos de Configuração

Esta pasta contém os arquivos de configuração utilizados para definir parâmetros e ajustes do projeto.

- **`.env.example`**: Arquivo de exemplo para as variáveis de ambiente. Copie este arquivo para a raiz do projeto como `.env` e preencha com as credenciais do seu banco de dados Oracle.

- **`unidades.json`**: Define os fatores de conversão de diferentes unidades de medida para quilogramas (kg). É utilizado para normalizar os preços registrados.
  - Exemplo: `{"cx23kg": 23, "dz": 12}`

- **`parametros.json`**: (Opcional) Permite ajustar os parâmetros de negócio da aplicação, como a janela da média móvel, o limite do z-score para detecção de outliers e o limiar de queda de preço para alertas. Se este arquivo não existir, a aplicação utilizará os valores padrão definidos no código.
  - Exemplo: `{"media_window": 7, "zscore_limite": 2.0, "limiar_queda": -5.0}`

