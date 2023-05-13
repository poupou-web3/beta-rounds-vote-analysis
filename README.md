# Gitcoin Beta Round Sybil analysis 

This repository contains two main analyses.

The first one is the creation of new stamps for the Gitcoin passport and the verification of relevance using the Thor/Loki data set of known sybils.

The second is an extensive analysis to detect sybils and the grants to which they contributed.

A third analysis was made during the round and it reviewed many project applications by analyzing the description of the projects. The analysis is in the repositories [grant-round-analysis]().


## 1. New Passport stamps creation
The analysis is available in the notebook [analysis-on-chain-passport.ipynb](https://github.com/poupou-web3/beta-rounds-vote-analysis/blob/main/jupyter/analysis-on-chain-passport.ipynb)

The method uses labels from Flipside to label any contract that is a decentralized exchange. By retrieving all the transactions of all donors, we count the number of interactions each donor has with any dex pool.

Then we compare contributors by grouping them by type Thor/Loki.
We try to find a threshold that does not flag too many legitimate donors and try to increase the number of flagged Sybils.

We found that 
- Above 20 transactions with a pool 99% of Sybil addresses do not pass the threshold.
- Around 5 or 6 transactions 90% of Sybil's addresses do not pass the threshold.
Nonetheless, many non-Sybil (Thor) addresses do not pass the threshold either.
Thus this stamp with these two thresholds could be used as proof of humanness but not as flagging behavior for addresses that don't have the stamp.


## 2. Sybil detection and grant analysis of the Web3 Community Round

The analysis is available in the notebook [analysis-votes-web3-community-latest.ipynb](https://github.com/poupou-web3/beta-rounds-vote-analysis/blob/main/jupyter/analysis-votes-web3-community_latest.ipynb)

The analysis uses detection bricks to flag contributors by looking at their on-chain transaction history. 
The following legos were used or built:
- *has same seed*  True if the first incoming transactions are also used by another user (the issue with that Boolean is that it does not filter exchange addresses)
- *Has same seed naive* if the first normal transaction is executed with and
- *Has suspicious seed behavior* if the first normal transaction is not an incoming transaction
- *Has less than 5 transactions*
- *Has less than 10 transactions 
- *Has interacted with a DEX* Has interacted with a pool addresses (Flipside labels)
- *Has interacted with a toxic wallet* using Flipside labels
- *Is airdrop master* according to Flipside tags
- *Has interacted with an airdrop master* True If the address has done any transaction with an airdrop master 
- *Has interacted with another contributor*
- *Has interacted with Disperse smart contract*
- *Has interacted with tornado cash*

Using these Boolean values we investigate any addresses that look suspicious.
Then we also investigate which grant they have been giving and manually review the suspected grants. We try to identify patterns such as giving the same amount to the same grant.  In particular, we note that addresses that have interacted with an airdrop master are suspicious and are often very connected with other donors.
We create a Boolean **flagged** that identifies the most suspicious addresses. 

All the addresses and their Boolean are available in the file : [suspicious_addresses.csv](https://github.com/poupou-web3/beta-rounds-vote-analysis/blob/main/suspicious_addresses.csv)

## 3. Grant Review
The grant review analyzed all beta round project applications by analyzing the description using readability metrics and originalityAI to detect AI-generated text. Then. A list of grants not passing a threshold is reviewed manually by analyzing the website, Twitter, GitHub, and any related information. 
The complete analysis is available in the repository : [grant-round-analysis]().

## Installation

```
pip install -r requirements.txt
```

## Required data to run the notebook

Transactions data are located in the transaction_full of the notebook. The data set can be downloaded using Ocean from 
- All thor/loki  transactions of contributors  | https://market.oceanprotocol.com/asset/did:op:647eec47dfd252c5a56053c8921e5d3aa495e60886e2b1d5d7573ab5dfa0af52
- ALL Web3 community transactions of contributors | https://market.oceanprotocol.com/asset/did:op:278accf3a5d25a6b91886da0b6dd6c436dac1871d67ec5cad0ef1e5b077986c5
Some scripts are provided to demonstrate how to extract that data using Sybil-scorer and the list of addresses.

Other data available on the [FAQ]() of the hackathon to all participants was also used.
In particular :
- The list of project application [IPFS](h) named *projects.csv in the notebook 
- The list of votes to any project [IPFS]() named *votes.csv in the notebooks

