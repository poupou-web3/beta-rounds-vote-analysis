import os
from pathlib import Path
import numpy as np

import pandas as pd

from sbdata.FlipsideApi import FlipsideApi

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent, 'tx_data', 'community_beta_rounds')
DATA_DIR = os.path.join(current_dir.parent.parent, 'data-regen-rangers')

# read the address from oss grant

api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, max_address=400)
PATH_TO_VOTES = os.path.join(DATA_DIR, "beta_round_votes.csv")
PATH_TO_GRANTS = os.path.join(DATA_DIR, "all-allo-rounds.csv")
PATH_TO_PROJECTS = os.path.join(DATA_DIR, "beta-projects.csv")

# 0x12BB5bBbFE596dbc489d209299B8302c3300fa40,Web3 Open Source Software Round,58

df_votes = pd.read_csv(PATH_TO_VOTES)
df_grants = pd.read_csv(PATH_TO_GRANTS)
df_application = pd.read_csv(PATH_TO_PROJECTS)
# Lowercase all addresses
df_grants['Round ID'] = df_grants['Round ID'].str.lower()
str_columns_votes = ['id', 'transaction', 'projectId', 'roundId', 'voter', 'grantAddress']
df_votes[str_columns_votes] = df_votes[str_columns_votes].applymap(lambda x: x.lower())

df_application

round_id = df_grants[df_grants['Round name'] == 'Web3 Community and Education']['Round ID'].values[0]
array_unique_address = df_votes[df_votes['roundId'] == round_id]['voter'].unique()

array_unique_address = np.char.lower(array_unique_address.astype(str))


from sbutils import LoadData

# Load data
data_loader = LoadData.LoadData(PATH_TO_EXPORT)

# Load the transactions of the addresses in a dataframe
df_tx = data_loader.create_df_tx('ethereum')

