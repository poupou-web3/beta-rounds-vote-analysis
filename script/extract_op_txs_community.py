import os
from pathlib import Path

import pandas as pd
import numpy as np
import requests

from sbdata.FlipsideApi import FlipsideApi
from sbutils import LoadData

def load_round_votes_data(chain_id, round_id):
    votes_url = 'https://indexer-grants-stack.gitcoin.co/data/' + chain_id + '/rounds/' + round_id + '/votes.json'
    try:
        # download the Votes JSON data from the URL
        response = requests.get(votes_url)
        if response.status_code == 200:
            votes_data = response.json()
        df = pd.DataFrame(votes_data)
        return df
    except:
        return pd.DataFrame()



FOLDER_NAME = 'community_round'
CHAIN = 'optimism'
extract_all = False

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent, 'tx_data', FOLDER_NAME)
DATA_DIR = os.path.join(current_dir.parent.parent, 'data-regen-rangers')
DATA_DIR_GITCOIN = os.path.join(current_dir.parent.parent, 'data-gitcoin')


# Initialize Flipside API
api_key = os.environ['FLIPSIDE_API_KEY2']
flipside_api = FlipsideApi(api_key, max_address=100)

# Load data
PATH_TO_VOTES_OLD = os.path.join(DATA_DIR, "beta_round_votes.csv")
PATH_TO_VOTES = os.path.join(DATA_DIR, "votes_baoki.csv")
PATH_TO_GRANTS = os.path.join(DATA_DIR, "all-allo-rounds.csv")

# Load data from gitcoin
# t_votes_gitcoin = []
# for file in os.listdir(DATA_DIR_GITCOIN):
#     if file.endswith(".csv"):
#         PATH_TO_VOTES_GITCOIN = os.path.join(DATA_DIR_GITCOIN, file)
#         t_votes_gitcoin.append(pd.read_csv(PATH_TO_VOTES_GITCOIN))
# df_votes = pd.concat(t_votes_gitcoin)

df_votes = load_round_votes_data('10', '0x984e29dCB4286c2D9cbAA2c238AfDd8A191Eefbc')


str_columns_votes = ['id', 'projectId', 'roundId', 'voter', 'grantAddress']
df_votes[str_columns_votes] = df_votes[str_columns_votes].applymap(lambda x: x.lower())


array_unique_address = df_votes['voter'].unique()

# Load the files that have already been extracted
try :
    loader = LoadData.LoadData(PATH_TO_EXPORT)
    list_files = loader.get_files_in_address(CHAIN, array_unique_address)
    list_files = [str(f).replace('_tx.csv', '') for f in list_files]
except:
    list_files = []

not_in = np.setdiff1d(array_unique_address, np.array(list_files))

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
