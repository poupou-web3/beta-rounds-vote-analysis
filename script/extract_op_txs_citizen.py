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

# Load votes citizen round from gitcoin csv
file = "vote_coefficients-0x984e29dCB4286c2D9cbAA2c238AfDd8A191Eefbc.csv"
PATH_TO_VOTES_GITCOIN = os.path.join(DATA_DIR_GITCOIN, file)
df_votes = pd.read_csv(PATH_TO_VOTES_GITCOIN)

# df_votes = load_round_votes_data('10', '0x984e29dCB4286c2D9cbAA2c238AfDd8A191Eefbc')
# str_columns_votes = ['id', 'projectId', 'roundId', 'voter', 'grantAddress']
# df_votes[str_columns_votes] = df_votes[str_columns_votes].applymap(lambda x: x.lower())

# Use flipside api to get the votes from the citizen round
# sql = """with projects_name as ( select '0x745ce2af76e9a6eba65cc0cacaa9ea109bb7fabd' as address, 'BanklessDAO`s Gitcoin Citizens' as project_name union all select '0xc98786d5a7a03c1e74affcb97ff7ef8a710da09b' as address, 'Karma' as project_name union all select '0xe1887ff140bfa9d3b45d0b2077b7471124acd242' as address, 'Bankless Academy' as project_name union all select '0xeb0cf83c80e4b4cd82196dac94e2c579672b6b1c' as address, 'Biteye' as project_name union all select '0x7904667c340601aab73939372c016dc5102732a2' as address, 'Dune Analytics dashboard - Vitalik Digital Book' as project_name union all select '0x8615b6ed9468cbb58cfdf45c120b87e15add787f' as address, 'Gitcoin Onboarding with Regens Unite' as project_name union all select '0x13257e783dc8ded7e227a28edb0428c42d31202e' as address, 'Kairos Research' as project_name union all select '0xbec643bd5b7f5e9190617ca4187ef0455950c51c' as address, 'ITU Blockchain' as project_name union all select '0x88c379caef7965c49b17c2a18c43af36f213fbd5' as address, 'DeSci Round Operators' as project_name union all select '0x924f5821f991f366df954536e9a408867f962637' as address, 'Gitcoin Gas Optimization' as project_name union all select '0xb62e762af637b49eb4870bce8fe21bfff189e495' as address, 'ZER8`s Gitcoin Citizen Round Application' as project_name union all select '0x298f7f66ba43f0efecf4bc324b0016f822c783a4' as address, 'All for Climate DAO: Gitcoin support since GR12' as project_name union all select '0xa51e0a99b53d5b00937a2631d5865468a3543b7d' as address, 'Keith Comito: Gitcoin Citizen' as project_name union all select '0x9dcba70b2dfe5807e2a847e065ebb666791f8b8a' as address, 'Borderless' as project_name union all select '0xf55d40d1e5255a639ab36834f93d44ce8125e047' as address, 'Eartbased soul' as project_name union all select '0xa30ab83e693ad49f3f651085dad11d049c818923' as address, 'Quadratic Trust - Anne Connelly' as project_name union all select '0x3fb0d1e89693b8709de60d835452a4712d1c9b04' as address, 'Gitcoin Awareness and Female Founder Amplification ' as project_name union all select '0x91fbd3447077bfd97f5af4d2c033ecbc25788f89' as address, 'greenpill.network' as project_name union all select '0x8cfb71682feb93317d1eb4e0b3ca7fa9044169cf' as address, 'Bankless Hindi' as project_name union all select '0x8d36bbb74973dd04e31dcbce5778b16dd310bd9b' as address, 'Owocki/Supermodular.xyz (FBO Gitcoin Matching Pool)' as project_name union all select '0x850a146d7478daaa98fc26fd85e6a24e50846a9d' as address, 'Zuzalu Gitcoin Hype Squad' as project_name union all select '0x9531c059098e3d194ff87febb587ab07b30b1306' as address, 'Lefteris Karapetsas' as project_name union all select '0xc4450c8d1009160883e44f24d66d92436ae4b4c5' as address, 'Archimedes Lever' as project_name union all select '0x4486907312143049ac5c6280cba9ba4cd5f30511' as address, 'Blu3 Global' as project_name union all select '0x74afec0c8564ddc09e9fac9493c611eeafcca0e7' as address, 'Indigenous Voices in Gitcoin by Mycelia' as project_name union all select '0x6b5918d8ef9094679f4b4e1bf397a66ea411b118' as address, 'OpenLore Library' as project_name union all select '0xdc71a1bdeabd3c347dc21e9354aff91ad375eb97' as address, 'Jon Ruth - Discord and Telegram Superhero' as project_name union all select '0xa40ba205add80c214ec7a710e790a54d738c4c27' as address, '40acres DAO' as project_name union all select '0xfc9265a28f66cf4561d74a4e25d7bbd3f482b8e6' as address, 'Jimi Cohen - Gitcoin Radio' as project_name union all select '0x85a363699c6864248a6ffca66e4a1a5ccf9f5567' as address, '🐙 Mars - Gitcoin citizen' as project_name union all select '0x5a5d9ab7b1bd978f80909503ebb828879daca9c3' as address, 'Carl Cervone - Onchain Impact Evaluatooooor' as project_name union all select '0x521aacb43d89e1b8ffd64d9ef76b0a1074dedaf8' as address, 'Bob Jiang' as project_name union all select '0xca72c93172ba6eff168e59e7f17c3c7a8fea9b62' as address, 'Carlos Melgar - Community Supportooooooor' as project_name ), eth_price as (select date_trunc(day, HOUR) as hour, avg(PRICE) as PRICE from optimism.core.fact_hourly_token_prices where TOKEN_ADDRESS='0x4200000000000000000000000000000000000006' group by 1), git_eth_donates as ( select a.BLOCK_TIMESTAMP, a.ORIGIN_FROM_ADDRESS as user, b.ETH_TO_ADDRESS as project, b.AMOUNT as amount, b.AMOUNT*price as amount_usd, a.tx_hash, 'ETH' as token from optimism.core.ez_eth_transfers a left join eth_price on hour=date_trunc(day, a.BLOCK_TIMESTAMP) left join optimism.core.ez_eth_transfers b on a.tx_hash=b.tx_hash where a.ORIGIN_TO_ADDRESS='0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc' and a.ORIGIN_FUNCTION_SIGNATURE='0x7aa54b68' and a.ETH_FROM_ADDRESS=a.ORIGIN_FROM_ADDRESS and a.BLOCK_TIMESTAMP>='2023-06-01' and b.ETH_FROM_ADDRESS='0x0e5e1f6a82d1ec6ce5c6d5568096fca96ecde651'), git_dai_donates as (select BLOCK_TIMESTAMP, ORIGIN_FROM_ADDRESS as user, TO_ADDRESS as project, amount, amount as amount_usd, tx_hash, 'DAI' as token from optimism.core.ez_token_transfers where ORIGIN_TO_ADDRESS='0x984e29dcb4286c2d9cbaa2c238afdd8a191eefbc' and ORIGIN_FUNCTION_SIGNATURE='0x7aa54b68' and CONTRACT_ADDRESS='0xda10009cbd5d07dd0cecc66161fc93d7c9000da1' and FROM_ADDRESS=ORIGIN_FROM_ADDRESS) select DISTINCT(user) as voter from (select * from git_eth_donates union all select * from git_dai_donates) a join projects_name on address=project"""
# print("Retrieving votes from Flipside API")
# df_votes = flipside_api.execute_query(sql)

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
