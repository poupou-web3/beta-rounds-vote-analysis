import os 
from pathlib import Path
import time

import pandas as pd

start_time = time.time()
FOLDER_NAME = 'gr18'
CHAIN = 'optimism'

# Set path to data folder
current_dir = Path(os.getcwd())
src_dir = current_dir.parent.parent.parent
PATH_TO_EXPORT = os.path.join(src_dir, 'tx_data', FOLDER_NAME)
PATH_TO_GR18 = os.path.join(src_dir, FOLDER_NAME)


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

for round_name in round_names:

    try:
        path_feature_file = os.path.join(PATH_TO_EXPORT, f'features_{round_name}.csv')
        path_feature_file_lcs = os.path.join(PATH_TO_EXPORT, f'features_{round_name}_lcs.csv')
        path_feature_file_new = os.path.join(PATH_TO_EXPORT, f'features_{round_name}_new.csv')

        df_features = pd.read_csv(path_feature_file)
        df_features_lcs = pd.read_csv(path_feature_file_lcs)

        df_features = df_features.merge(df_features_lcs[['EOA' ,'lcs', 'cluster_size_lcs', 'mean_score_lcs', 'max_score_lcs', 'has_lcs']], left_on='EOA', right_on='EOA', how='left')

        df_features.to_csv(path_feature_file_new, index=False)
    except Exception as e:
        print(f'Error in round {round_name}')
        print(e)

print(f'Total time: {time.time() - start_time}')
print(f'Path to export: {PATH_TO_EXPORT}')
print('Done')
