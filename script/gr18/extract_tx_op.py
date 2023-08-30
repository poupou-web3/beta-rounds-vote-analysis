import pandas as pd
import json
from sbscorer.sbdata.FlipsideApi import FlipsideApi
import os
import numpy as np
from pathlib import Path


FOLDER_NAME = 'gr18'
CHAIN = 'optimism'
N_DAYS = 80
PAGE_SIZE = 50000
TOTAL_DAYS = 657

# Set path to data folder
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent.parent, 'tx_data', FOLDER_NAME)


# Initialize Flipside API
api_key = os.environ['FLIPSIDE_API_KEY']
flipside_api = FlipsideApi(api_key, page_size=PAGE_SIZE)

sql_template = """
 with dai as (
SELECT
  tx_hash,
  block_timestamp,
  origin_from_address as voter,
  'DAI' as token,
  amount_usd
from
  optimism.core.ez_token_transfers
where
  contract_address = '0xda10009cbd5d07dd0cecc66161fc93d7c9000da1'
and origin_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
and block_timestamp between '2023-08-15 12:00:00.000' and '2023-08-29 12:00:00.000'

), eth AS
(
SELECT
  tx_hash,
  block_timestamp,
  origin_from_address as voter,
  'ETH' as token,
  amount_usd
from
  optimism.core.ez_eth_transfers
where
  origin_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
and eth_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
and block_timestamp between '2023-08-15 12:00:00.000' and '2023-08-29 12:00:00.000'
),

all_votes as (
SELECT * from eth
 union all 
select * FROM dai
),

unique_voter as (SELECT DISTINCT voter from all_votes)

SELECT 
tx.TX_HASH,
tx.BLOCK_TIMESTAMP,
tx.FROM_ADDRESS,
tx.TO_ADDRESS,
tx.GAS_LIMIT,
tx.GAS_USED,
tx.TX_FEE,
tx.ETH_VALUE
FROM optimism.core.fact_transactions tx
INNER JOIN
unique_voter v ON tx.FROM_ADDRESS = v.voter OR tx.TO_ADDRESS = v.voter
WHERE tx.BLOCK_TIMESTAMP 
between CURRENT_DATE - interval '%d day'
AND CURRENT_DATE - interval '%d day'
AND tx.STATUS = 'SUCCESS'  
"""

flipside_api = FlipsideApi(api_key, page_size=PAGE_SIZE)

ls_df = []
for i in range (0, (TOTAL_DAYS//N_DAYS)+1):
    print('Processing days %d to %d' % ((i+1)*N_DAYS, i*N_DAYS))
    sql = sql_template % ((i+1)*N_DAYS, i*N_DAYS) # between oldest date and current date
    ls_df.append(flipside_api.execute_query(sql))

print('Concatenating dataframes')
df = pd.concat(ls_df)


if not os.path.exists(PATH_TO_EXPORT):
    os.makedirs(PATH_TO_EXPORT)

print('Exporting to csv and pkl to %s' % PATH_TO_EXPORT)
df.to_csv(os.path.join(PATH_TO_EXPORT, f'gr_18_{CHAIN}_all_tx.csv'), index=False)

df.to_pickle(os.path.join(PATH_TO_EXPORT, f'gr_18_{CHAIN}_all_tx.pkl'))

print('Done')