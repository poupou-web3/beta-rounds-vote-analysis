import os
from pathlib import Path

import pandas as pd

from sbdata.FlipsideApi import FlipsideApi

# 0         Web3 Open Source Software Round
# 1                 Ethereum Infrastructure
# 2                       Climate Solutions
# 3                           ZK Tech Round
# 4            Web3 Community and Education
# 5                       Climate Solutions
# 6                              Metacrisis
# 7                      The Phantom Menace
# 8                       Token Engineering
# 9                             Web3 Social
# 10                        Mantle Grants 1
# 11          DeSci (Decentralized Science)
# 12                              ENS Round
# 14                          ENS Ecosystem
# 15    Global Chinese Community beta round

ROUND_NAME = 'Web3 Community and Education' # choose the name of the round
FOLDER_NAME = ROUND_NAME.replace(' ', '_').lower()
CHAIN = 'ethereum'

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent, 'tx_data', FOLDER_NAME)
DATA_DIR = os.path.join(current_dir.parent.parent, 'data-regen-rangers')

# Initialize Flipside API
api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, max_address=200)

# Load data
PATH_TO_VOTES = os.path.join(DATA_DIR, "beta_round_votes.csv")
PATH_TO_GRANTS = os.path.join(DATA_DIR, "all-allo-rounds.csv")

df_votes = pd.read_csv(PATH_TO_VOTES)
df_grants = pd.read_csv(PATH_TO_GRANTS)

# Lowercase all addresses
df_grants['Round ID'] = df_grants['Round ID'].str.lower()
str_columns_votes = ['id', 'transaction', 'projectId', 'roundId', 'voter', 'grantAddress']
df_votes[str_columns_votes] = df_votes[str_columns_votes].applymap(lambda x: x.lower())

# get unique voter address for the roundFOLDER_NAME = 'community_beta_rounds'
try:
    round_id = df_grants[df_grants['Round name'] == ROUND_NAME]['Round ID'].values[0]
except IndexError:
    print(f'Round name {ROUND_NAME} not found')
    exit(1)

array_unique_address = df_votes[df_votes['roundId'] == round_id]['voter'].unique()

# extract transactions to the path
print(f'Extracting transactions for {ROUND_NAME}, number of addresses: {len(array_unique_address)}')
flipside_api.extract_transactions_net(PATH_TO_EXPORT, array_unique_address, CHAIN)

print("End mining transactions")
