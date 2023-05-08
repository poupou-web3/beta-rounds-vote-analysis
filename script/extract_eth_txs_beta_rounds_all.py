import os
from pathlib import Path
import numpy as np

import pandas as pd

from sbdata.FlipsideApi import FlipsideApi

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent, 'tx_data', 'all-rounds')
DATA_DIR = os.path.join(current_dir.parent.parent, 'data-regen-rangers')

# read the address from oss grant

api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, max_address=400)
PATH_TO_VOTES = os.path.join(DATA_DIR, "beta_round_votes.csv")
PATH_TO_GRANTS = os.path.join(DATA_DIR, "all-allo-rounds.csv")

# 0x12BB5bBbFE596dbc489d209299B8302c3300fa40,Web3 Open Source Software Round,58

df_votes = pd.read_csv(PATH_TO_VOTES)
df_grants = pd.read_csv(PATH_TO_GRANTS)

array_unique_address = np.char.lower(df_votes.voter.unique().astype(str))
flipside_api.extract_transactions_net(PATH_TO_EXPORT, array_unique_address, 'ethereum')

print("End mining transactions")
