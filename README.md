<h1>Reinforcement Learning Crypto Trading Bot</h1>

Commits note: Previous project work was done on Quantconnect which autosaves and does not use commits. The colab notebook transferred core work from Quantconnect to a notebook to have more control over data input.

## Description:
Crypto trading bot that uses Deep Reinforcement Learning to make and act on predictions using the Polygon API. Can be expanded to use batch training and GANs to create synthetic training data.

## Goals:
1. Create a crypto trading system using deep reinforcement learning
2. Learn how to train in batches to train when new data is added without having to retrain the whole system

## MVP:
Crypto trading bot that uses Deep Reinforcement Learning to make and act on predictions using the Polygon API.

## Stretch Goals:
- Use a GAN to create synthetic data to train with

## Implementation Timeline:
- Week 1: Finish Proposal and gather and prepare data
- Week 2: Implement training/backtesting system
- Week 3: Implement Deep Reinforcement Learning Models
- Week 4: Tune model paramaters
- Week 5: Implement batch training to better live trading models
- Week 6: Test models on live training data
- Week 7: Implement GANs to create synthetic data to train with to improve model performance


## Research Summary:
- This team built a Ensemble Deep Reinforcement Learning model for trading equities. Will be a great resource for guidance in implementing models and backtesting architecture.
    - https://towardsdatascience.com/deep-reinforcement-learning-for-automated-stock-trading-f1dad0126a02
- Guide for understanding DRL in a manner that makes it easy to explain in my documentation.
    - https://towardsdatascience.com/drl-01-a-gentle-introduction-to-deep-reinforcement-learning-405b79866bf4
- Good guide to general structure of a DRL crypto trading agent
    - https://towardsdatascience.com/creating-bitcoin-trading-bots-that-dont-lose-money-2e7165fb0b29
- Good guide to creating synthetic data with GANs
    - https://towardsdatascience.com/synthetic-time-series-data-a-gan-approach-869a984f2239
- Good point of reference when looking to deploy model to run with live trading
    - https://maharshi-yeluri.medium.com/a-guide-to-production-level-deep-learning-784de4f34da
- Good resource for sure model predictions to construct optimal portfolio
    - https://towardsdatascience.com/finrl-for-quantitative-finance-tutorial-for-portfolio-allocation-9b417660c7cd

## Data:
- Polygon.io for historical prices
    - https://polygon.io/crypto
- Coinbase API for current prices
    - https://docs.pro.coinbase.com/
    - https://github.com/danpaquin/coinbasepro-python
