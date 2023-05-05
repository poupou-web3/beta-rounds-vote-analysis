import os
from pathlib import Path
import numpy as np

import pandas as pd

from sbdata.FlipsideApi import FlipsideApi

# absolute_path = os.fspath(Path.cwd().parent.parent)
# if absolute_path not in sys.path:
#     sys.path.append(absolute_path)

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent, 'tx_data', 'community_beta_rounds')
DATA_DIR = os.path.join(current_dir.parent.parent, 'data-regen-rangers')

# read the address from oss grant

api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, max_address=300)
PATH_TO_VOTES = os.path.join(DATA_DIR, "beta_round_votes.csv")
PATH_TO_GRANTS = os.path.join(DATA_DIR, "all-allo-rounds.csv")

# 0x12BB5bBbFE596dbc489d209299B8302c3300fa40,Web3 Open Source Software Round,58

df_votes = pd.read_csv(PATH_TO_VOTES)
df_grants = pd.read_csv(PATH_TO_GRANTS)
round_id = df_grants[df_grants['Round name'] == 'Web3 Community and Education']['Round ID'].values[0]

array_unique_address = df_votes[df_votes['roundId'] == round_id]['voter'].unique()

array_unique_address = np.char.lower(array_unique_address.astype(str))
flipside_api.extract_transactions_net(PATH_TO_EXPORT, array_unique_address, 'ethereum')

print("End mining transactions")
