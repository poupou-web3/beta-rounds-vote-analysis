# Gitcoin Beta Round Sybil analysis 

This repository contains two main analysis.

The first one is the creation of a new stamps for the Gitcoin passport and the verification of relevance using the Thor/Loki data set of known sybils.

The second is an extensive analysis to detect sybils and if possible the grants to which their contributions was made.


## 1. New stamps creation
The analysis is available in the notebook `[analysis-on-chain-passport.ipynb](https://github.com/poupou-web3/beta-rounds-vote-analysis/blob/main/jupyter/analysis-on-chain-passport.ipynb)`


## 2. Sybil detection and grant analysis of the Web3 Community Round
The analysis is available in the notebook `[analysis-votes-web3-community-latest.ipynb](https://github.com/poupou-web3/beta-rounds-vote-analysis/blob/main/jupyter/analysis-votes-web3-community_latest.ipynb)`

[list](https://github.com/poupou-web3/beta-rounds-vote-analysis/blob/main/suspicious_addresses.csv)


## Installation

```
pip install -r requirements.txt
```

## Required data to run the notebook

Transactions data are located in the transaction_full of the notebook. The data set can be downloaded using Ocean from 
- All thor/loki  transactions of contribuotrs  | https://market.oceanprotocol.com/asset/did:op:647eec47dfd252c5a56053c8921e5d3aa495e60886e2b1d5d7573ab5dfa0af52
- ALL Web3 community transactions of contribuotrs | https://market.oceanprotocol.com/asset/did:op:278accf3a5d25a6b91886da0b6dd6c436dac1871d67ec5cad0ef1e5b077986c5
