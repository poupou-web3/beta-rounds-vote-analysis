import os 
from pathlib import Path
import time

import pandas as pd
import numpy as np


from sbscorer.sblegos.TransactionAnalyser import TransactionAnalyser as txa

start_time = time.time()
FOLDER_NAME = 'gr18'
CHAIN = 'optimism'
CONTRACT_CREATION_AD_NAME = '0x_contract_creation'

# Set path to data folder
current_dir = Path(os.getcwd())
src_dir = current_dir.parent.parent.parent
PATH_TO_EXPORT = os.path.join(src_dir, 'tx_data', FOLDER_NAME)
PATH_TO_GR18 = os.path.join(src_dir, FOLDER_NAME)
voter_tx_file_name = 'gg18_votes.csv'
passport_file_name = 'gg18_voter_passports.csv'

tx_file_name = 'gr_18_optimism_all_tx.csv'

votes = pd.read_csv(os.path.join(PATH_TO_GR18, voter_tx_file_name))
passports = pd.read_csv(os.path.join(PATH_TO_GR18, passport_file_name))

# round_names = votes['round_name'].unique()
# ['Climate Round', 'Web3 Open Source Software',
#        'Web3 Community and Education ',
#        'Global Chinese Community for Public Goods - GR18', 'Web3 Social',
#        'Zuzalu Continuous Innovation', 'Meta Pool LatAm GG18',
#        'ReFi DAO Local Node ', 'Token Engineering',
#        'Ethereum Infrastructure', 'Arbitrum Domain Round']

round_names =['Climate Round',
       'Web3 Community and Education ',
       'Global Chinese Community for Public Goods - GR18',
        'Web3 Social',
       'Zuzalu Continuous Innovation',
        'Meta Pool LatAm GG18',
       'ReFi DAO Local Node ',
        'Token Engineering']

# round_names =['Web3 Open Source Software']

# Load tx data
df_tx = pd.read_csv(os.path.join(PATH_TO_EXPORT, tx_file_name))

df_tx.loc[df_tx['to_address'].isna(), 'to_address'] = CONTRACT_CREATION_AD_NAME

assert df_tx.isna().sum().sum() == 0

df_tx.drop(columns=['__row_index'], inplace=True)

print(f'df transaction shape : {df_tx.shape}')

# add EOA to df_tx
df_tx_EOA_FROM = df_tx.copy()
df_tx_EOA_FROM['EOA'] = df_tx_EOA_FROM['from_address']

df_tx_EOA_TO = df_tx.copy()
df_tx_EOA_TO['EOA'] = df_tx_EOA_TO['to_address']

df_tx_eoa = pd.concat([df_tx_EOA_FROM, df_tx_EOA_TO])
df_tx_eoa = df_tx_eoa.loc[df_tx_eoa['EOA'] != CONTRACT_CREATION_AD_NAME, :]


# iterate through rounds
for round_name in round_names:
    print(f'Round: {round_name}')
    votes_round = votes.loc[votes['round_name'] == round_name, :].copy()
    round_voters = votes_round['voter'].unique()
    print(f'Number of voters in round {round_name}: {len(round_voters)}')

    lowercase_converter = np.vectorize(str.lower)
    round_voters = lowercase_converter(round_voters)

    tx_analyser = txa(df_tx_eoa.copy(), round_voters)

    print(f'Shape of df tx: {len(tx_analyser.df_transactions)}')

    print('Start computing features')
    df_features = tx_analyser.get_df_features(['count_tx', 'less_10_tx', 'lcs'])
    print('Done computing features')

    df_features.to_csv(os.path.join(PATH_TO_EXPORT, f'features_{round_name}_lcs.csv'), index=False)

print(f'Total time: {time.time() - start_time}')
print('Done')
