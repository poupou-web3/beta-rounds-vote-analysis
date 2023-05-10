import os
from pathlib import Path
import numpy as np

import pandas as pd

from sbdata.FlipsideApi import FlipsideApi

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent, 'tx_data', 'passport2')
DATA_DIR = os.path.join(current_dir.parent.parent, 'data-regen-rangers')
CHAIN = 'ethereum'

# read the address from oss grant

api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, max_address=200)


PATH_TO_LOKI = os.path.join(DATA_DIR, "thor_loki.csv")
PATH_TO_SYBILS_GR15 = os.path.join(DATA_DIR, "alpha_round_sybils.xlsx")


df_loki = pd.read_csv(PATH_TO_LOKI)
df_sybils_gr15_oss = pd.read_excel(PATH_TO_SYBILS_GR15, sheet_name=3)
df_sybils_gr15_eth = pd.read_excel(PATH_TO_SYBILS_GR15, sheet_name=4)
df_sybils_gr15_climate = pd.read_excel(PATH_TO_SYBILS_GR15, sheet_name=5)

df_loki.dropna(subset=['Wallet Address', 'Thor/Loki Indicator'], inplace=True)
df_loki.drop_duplicates(subset=['Wallet Address'], inplace=True)

df_sybils_gr15_oss.dropna(subset=['ID'], inplace=True)
df_sybils_gr15_eth.dropna(subset=['ID'], inplace=True)
df_sybils_gr15_climate.dropna(subset=['ID'], inplace=True)

loki_unique_address = df_loki['Wallet Address'].unique()

other_add = df_sybils_gr15_oss['Source Address'].tolist()
other_add += df_sybils_gr15_eth['Source Address'].tolist()
other_add += df_sybils_gr15_climate['Source Address'].tolist()
other_unique_address = np.unique(np.array(other_add))

# extract loki transactions to the path
print(f'Number of thor/loki address to process: {len(loki_unique_address)}')
flipside_api.extract_transactions_net(PATH_TO_EXPORT, loki_unique_address, CHAIN)
print("End mining loki transactions")

diff_address = np.setdiff1d(other_unique_address, loki_unique_address)
# extract other transactions to the path
print(f'Number of remaining address to process: {len(diff_address)}')
flipside_api2 = FlipsideApi(api_key, max_address=200)
flipside_api2.extract_transactions_net(PATH_TO_EXPORT, diff_address, CHAIN)
print("End mining all transactions")
