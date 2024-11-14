# market_analysis

Projeto de Análise de Opções

Este projeto tem como objetivo realizar a análise de opções financeiras utilizando diversas estratégias e cálculos de métricas importantes. Ele é desenvolvido em Python e faz uso da biblioteca MetaTrader5 para obter dados de mercado.

## Funcionalidades

- **Análise de Opções**: O projeto permite a análise de opções de compra (call) e venda (put) com base em diferentes critérios, como preço, volatilidade histórica e gregas.
- **Estratégias de Opções**: Implementa várias estratégias de negociação de opções, incluindo:
  - Box Spread
  - Broken Wing Butterfly
  - Butterfly Spread
  - Conversion Reversal
  - Calendar Spread Arbitrage
  - Iron Condor
  - Straddle Arbitrage
  - Synthetic Arbitrage
  - Tree Point Box
- **Cálculo de Gregas**: Calcula as gregas das opções, que são métricas importantes para a análise de risco.
- **Previsão com Machine Learning**: Utiliza técnicas de aprendizado de máquina para prever movimentos de mercado.
- **Visualização de Dados**: Gera gráficos para visualização dos dados de mercado e resultados das análises.

## Estrutura do Projeto

- [`_credentials`](_credentials ): Contém arquivos de credenciais (não incluídos no repositório).
- [`configs`](configs ): Scripts de configuração, incluindo a inicialização do MetaTrader5.
- [`flow_analysis`](flow_analysis ): Scripts para análise de fluxo de ordens e posições de jogadores.
- [`graphs`](graphs ): Scripts para geração de gráficos.
- [`machine_learning`](machine_learning ): Scripts de aprendizado de máquina para previsão de mercado.
- [`options`](options ): Scripts principais para análise de opções e implementação de estratégias.
- [`services`](services ): Serviços auxiliares (detalhes não fornecidos).
- [`stocks`](stocks ): Scripts para análise de ações.
- [`main.py`](main.py ): Script principal para execução das análises e estratégias.

## Como Executar

1. **Instale as dependências**:
   ```sh
   pip install -r requirements.txt
   ```

2. **Configure as credenciais**: Adicione suas credenciais no diretório [`_credentials`](_credentials ).

3. **Inicialize o MetaTrader5**:
   ```sh
   python configs/Initialize_mt5.py
   ```

4. **Execute o script principal**:
   ```sh
   python main.py analisys
   ```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autor

Bruno Eduardo Ferreira

## Contribuinte

Nunes Evandrus

---

Este README fornece uma visão geral do projeto e suas funcionalidades. Para mais detalhes, consulte a documentação nos arquivos de código.
```