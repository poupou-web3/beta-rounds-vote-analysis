import os
from pathlib import Path

import pandas as pd
import numpy as np

from sbdata.FlipsideApi import FlipsideApi
from sbutils import LoadData


FOLDER_NAME = 'all_beta_rounds'
CHAIN = 'ethereum'
extract_all = False

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent, 'tx_data', FOLDER_NAME)
DATA_DIR = os.path.join(current_dir.parent.parent, 'data-regen-rangers')

# Initialize Flipside API
api_key = os.environ['FLIPSIDE_API_KEY2']
flipside_api = FlipsideApi(api_key, max_address=100)

# Load data
PATH_TO_VOTES_OLD = os.path.join(DATA_DIR, "beta_round_votes.csv")
PATH_TO_VOTES = os.path.join(DATA_DIR, "votes_baoki.csv")
PATH_TO_GRANTS = os.path.join(DATA_DIR, "all-allo-rounds.csv")

df_votes = pd.read_csv(PATH_TO_VOTES)
df_votes_old = pd.read_csv(PATH_TO_VOTES_OLD)
df_grants = pd.read_csv(PATH_TO_GRANTS)

# Lowercase all addresses
df_grants['Round ID'] = df_grants['Round ID'].str.lower()
str_columns_votes = ['id', 'transaction', 'projectId', 'roundId', 'voter', 'grantAddress']
df_votes[str_columns_votes] = df_votes[str_columns_votes].applymap(lambda x: x.lower())

array_unique_address = df_votes['voter'].unique()

# Load the files that have already been extracted
loader = LoadData.LoadData(PATH_TO_EXPORT)
list_files = loader.get_files_in_address(CHAIN, array_unique_address)
list_files = [str(f).replace('_tx', '') for f in list_files]

not_in = np.setdiff1d(np.array(list_files), array_unique_address)

if extract_all:
    print('Extracting all transactions')
    to_extract = array_unique_address
else:
    print('Extracting transactions not yet extracted')
    to_extract = not_in
# extract transactions to the path
print(f'Extracting transactions, number of addresses: {len(to_extract)}')
flipside_api.extract_transactions_net(PATH_TO_EXPORT, to_extract, CHAIN)

print("End mining transactions")
