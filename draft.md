I'm having some issues with my api calls so I could not complete all the analysis I would have liked.

'seed_suspicious' verify that the first incomming transaction (regular transaction and not internal transaction) is seeding the wallet = providing gas to the wallet. If the first transaction is not a seed, it is suspicious. This happens when the first normal transaction is an outgoing transaction. It is possible if it was funded from an internal transaction.

'has_interaction_toxic' it is a label I retrieve from Flipside crypto table : crosschain.core.address_labels according to the documentation it flags scams, pyrmamids, bad bots, attacks, hackers. The issue I see is that we have no control over which address has been flagged as toxic but still there is probably a reason and it is probably a good idea to flag it as suspicious.

airdrop master - yes it is a tag retrieved from the tag table of Flipside.

I don't think it is a bad thing that an airdrop hunter votes/donate for a project. The issue is that if he is a professionnal airdrop hunter, he is probably not voting for the project from only one wallet. Thats is why looking at other contributors that have interacted with these flag address is important. thus the boolean 'has_interaction_airdrop_m', this is also supported by the fact that the majority of wallets that have interacted with another contribuor have also interacted with a wallet tagged as airdrop master.

Something that could be done is to squelch most of the airdrop master satellite wallets. But choosing the right address to authorize matching may not be easy neither.

Stakeridoo detected sybils using fly trap method. It means he analysed addresses that have received an airdrop and he managed to find clusters of addresses that sent the funds back to the main wallet demonstrating the connection between these wallets. more details here https://app.charmverse.io/anti-sybil/page-950640444535011

Doge analysis is here https://github.com/DistributedDoge/sybilscope/blob/master/sus_on_chain.ipynb he used flagged wallet by hop protocol to detect sybils and as well as jacard similarity using these flags: 
wallets are similar if all vote in short timespan.
wallets are similar if all donate to same set of grants
wallets are similar if they donate similar amounts (albeit some amounts are just more popular than others!)
wallets are similar if they have exact same Gitcoin passport score (same combination of verification stamps)
we have to be careful not to be fooled by randomness - high similarity between pair of single-donation wallets can be coincidence.
If then verify some cluster using graph analysis.

