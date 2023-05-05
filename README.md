# grant-exploration

This repository explores and tries to find Sybils using the library sybil-scorer.
You can find the sybil-scorer repository here: https://github.com/poupou-web3/sybil-scorer
And available as a python package at: https://pypi.org/project/sybil-scorer/

## Installation

```
pip install sybil-scorer
pip install jupyterlab
```

## Required data to run the notebook

Transactions data are located in the transaction_full of the notebook. The data set can be downloaded using Ocean from https://market.oceanprotocol.com/asset/did:op:826780ac16a444d65a0699e0e7629e67688c7b6a31ba2d1e672e3a2b398cab08

## Flaged sybil wallets and the associated boolean are available in the csv file in output


## Findings :

1. Many wallet addresses have the same seed wallet around 50%. This number can be lowered using tags to remove funding addresses coming from centralized exchanges.
2. When the flag has_suspicious_seed_behavior is raised, the wallet should be investigated, and raised concerns for any wallet address linked to that address.
3. If has_interacted_with_other_contributor is raised the wallet should be investigated.
4. Simple heuristics on the number of transactions reveal many potential farmers or Sybils that should be squelched if they don't have more transactions on other chains.
5. The method has similar behavior is highly processing intensive and should be used only on a per-project basis to prevent having to manage a large number of transactions.
