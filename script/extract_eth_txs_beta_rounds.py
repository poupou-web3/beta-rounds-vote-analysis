import os
from pathlib import Path

import pandas as pd

from sbdata.FlipsideApi import FlipsideApi

FOLDER_NAME = 'community_beta_rounds'
ROUND_NAME = 'Web3 Community and Education'
CHAIN = 'ethereum'

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent, 'tx_data', FOLDER_NAME)
DATA_DIR = os.path.join(current_dir.parent.parent, 'data-regen-rangers')

# Initialize Flipside API
api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, max_address=100)

# 0x12BB5bBbFE596dbc489d209299B8302c3300fa40,Web3 Open Source Software Round,58
# Load data
PATH_TO_VOTES = os.path.join(DATA_DIR, "beta_round_votes.csv")
PATH_TO_GRANTS = os.path.join(DATA_DIR, "all-allo-rounds.csv")

df_votes = pd.read_csv(PATH_TO_VOTES)
df_grants = pd.read_csv(PATH_TO_GRANTS)

# Lowercase all addresses
df_grants['Round ID'] = df_grants['Round ID'].str.lower()
str_columns_votes = ['id', 'transaction', 'projectId', 'roundId', 'voter', 'grantAddress']
df_votes[str_columns_votes] = df_votes[str_columns_votes].applymap(lambda x: x.lower())

# get unique voter address for the round
round_id = df_grants[df_grants['Round name'] == ROUND_NAME]['Round ID'].values[0]
array_unique_address = df_votes[df_votes['roundId'] == round_id]['voter'].unique()

# extract transactions to the path
flipside_api.extract_transactions_net(PATH_TO_EXPORT, array_unique_address, CHAIN)

print("End mining transactions")
