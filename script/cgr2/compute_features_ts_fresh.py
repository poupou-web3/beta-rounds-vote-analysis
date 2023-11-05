import os 
from pathlib import Path
import time

import pandas as pd
import numpy as np

from sbscorer.sblegos.FeatureCreator import FeatureCreator

start_time = time.time()
FOLDER_NAME = 'cgr2'
CHAIN = 'ethereum'
CONTRACT_CREATION_AD_NAME = '0x_contract_creation'

# Set path to data folder
current_dir = Path(os.getcwd())
src_dir = current_dir.parent.parent.parent
PATH_TO_EXPORT = os.path.join(src_dir, 'tx_data', FOLDER_NAME)
PATH_TO_VOTES = os.path.join(current_dir.parent.parent.parent, 'cgr2', 'votes_with_time.csv')
print(PATH_TO_EXPORT)
print(PATH_TO_VOTES)
assert os.path.exists(PATH_TO_VOTES), 'Path to votes not found'
assert os.path.exists(PATH_TO_EXPORT), 'Path to export not found'

df_votes = pd.read_csv(PATH_TO_VOTES)

round_names =['gitcoin-citizen-round-2']

# Load tx data
df_tx = pd.read_csv(os.path.join(PATH_TO_EXPORT, f'{FOLDER_NAME}_{CHAIN}_TRANSACTIONS.csv'))

df_tx.loc[df_tx['to_address'].isna(), 'to_address'] = CONTRACT_CREATION_AD_NAME

assert df_tx.isna().sum().sum() == 0

if '__row_index' in df_tx.columns:
    df_tx.drop(columns=['__row_index'], inplace=True)

print(f'df transaction shape : {df_tx.shape}')

# add EOA to df_tx
df_tx_EOA_FROM = df_tx.copy()
df_tx_EOA_FROM['eoa'] = df_tx_EOA_FROM['from_address']

df_tx_EOA_TO = df_tx.copy()
df_tx_EOA_TO['eoa'] = df_tx_EOA_TO['to_address']

df_tx_eoa = pd.concat([df_tx_EOA_FROM, df_tx_EOA_TO])
df_tx_eoa = df_tx_eoa.loc[df_tx_eoa['eoa'] != CONTRACT_CREATION_AD_NAME, :]


# iterate through rounds
# for round_name in round_names:
round_name = round_names[0]
print(f'Round: {round_name}')
# votes_round = votes.loc[votes['round_name'] == round_name, :].copy()
round_voters = df_votes['voter'].unique()
print(f'Number of voters in round {round_name}: {len(round_voters)}')

print(f'Shape of df tx: {len(df_tx_eoa)}')

df_tx_eoa.rename(columns={"eth_value": "value"}, inplace=True)
# in df tx columns are:
# tx_hash,block_number,block_timestamp,from_address,to_address,gas_limit,gas_used,tx_fee,eth_value,__row_index
#  'eoa', 'block_timestamp', 'value', 'tx_fee', 'gas_used', 'gas_limit' expected columns
fc = FeatureCreator(df_tx_eoa.copy())

print('Start computing features')
df_features = fc.create_feature_df()
print('Done computing features')

df_features.to_csv(os.path.join(PATH_TO_EXPORT, f'features_tsfresh_{round_name}.csv'), index=False)
df_features.to_parquet(os.path.join(PATH_TO_EXPORT, f'features_tsfresh_{round_name}.parquet'), compression='gzip', engine='pyarrow')
print(f'Features saved to {os.path.join(PATH_TO_EXPORT, f"features_tsfresh_{round_name}.csv")}')

print(f'Total time: {time.time() - start_time}')
print('Done')
