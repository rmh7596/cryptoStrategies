## Key Features
- **Momentum Calculation**: Utilizes historical price data to calculate momentum using percentage changes over a 24-hour window.
  - Caluclation inspired from "Quantitative Momentum: A Practitioner's Guide to Building a Momentum-Based Stock Selection System" by Wesley Gray and Jack Vogel.
- **Trade Execution**: Automates trade execution based on momentum signals. Executes long positions if momentum is below a threshold and short positions if momentum exceeds a threshold. Aims to profit from reversals after large movements. 
- **Risk Management**: Integrates risk and take-profit parameters from an optimizer to manage trade quantities and set stop-loss and take-profit levels.
- **Scheduler**: Employs a background scheduler to run the trading algorithm every hour, checking for open orders and making trading decisions based on current market conditions.
- **APIs**: Utilizes Binance US API for retrieving market data, account information, and executing trades.
