import os
from pathlib import Path

import pandas as pd

from sbdata.FlipsideApi import FlipsideApi


FOLDER_NAME = 'all_beta_rounds'
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

array_unique_address = df_votes['voter'].unique()

# extract transactions to the path
print(f'Extracting transactions, number of addresses: {len(array_unique_address)}')
flipside_api.extract_transactions_net(PATH_TO_EXPORT, array_unique_address, CHAIN)

print("End mining transactions")
