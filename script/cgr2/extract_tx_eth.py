import pandas as pd
import json
from sbscorer.sbdata.FlipsideApi import FlipsideApi
import os
import numpy as np
from pathlib import Path


FOLDER_NAME = 'cgr2' # the name of the folder where the data will be stored
CHAIN = 'ethereum' # the name of the chain to be queried
N_DAYS = 500 # number of days to be queried at a time, to avoid query timeout
PAGE_SIZE = 30000 # Flipside API page size, decrease it if the page size errors is thrown
TOTAL_DAYS = 3000 # Number of days since chain inception, here set for optimism, be mindful that setting this to a large number will result in a long query time and consume credits
TYPE = 'TRANSACTIONS' # 'TRANSACTIONS' or 'TOKEN_TRANSFERS'
QUERY_TIMEOUT = 10 # minutes

# Set path to data folder, set these according to your folder structure
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent.parent, 'tx_data', FOLDER_NAME)
PATH_TO_VOTES = os.path.join(current_dir.parent.parent.parent, 'cgr2', 'votes_with_time.csv')
print(PATH_TO_EXPORT)
print(PATH_TO_VOTES)
assert os.path.exists(PATH_TO_VOTES), 'Path to votes not found'
assert os.path.exists(PATH_TO_EXPORT), 'Path to export not found'

df_votes = pd.read_csv(PATH_TO_VOTES)
json_votes = df_votes.to_json(orient='records')
parsed_json = json.loads(json_votes)
escaped_json_string = json.dumps(parsed_json)

# Initialize Flipside API
api_key = os.environ['FLIPSIDE_API_KEY'] # set your API key as an environment variable, you need to set it



# SQL query to be executed
if TYPE == 'TRANSACTIONS':
    print('Extracting transactions')
    sql_template = """
    with vote_query AS (
SELECT 
  value[0]::STRING AS id,
  LOWER(value[1]::STRING) AS transaction,
  value[2]::NUMBER AS block_number,
  value[3]::STRING AS project_id,
  value[4]::NUMBER AS application_id,
  value[5]::STRING AS round_id,
  LOWER(value[6]::STRING) AS voter,
  LOWER(value[7]::STRING) AS grant_address,
  LOWER(value[8]::STRING) AS token,
  value[9]::NUMBER AS amount,
  value[10]::FLOAT AS amount_USD,
  value[11]::FLOAT AS amount_round_token,
  value[12]::TIMESTAMP_NTZ AS block_time,
  value[13]::NUMBER AS unix_time
FROM (
  SELECT
    livequery.live.udf_api('https://flipsidecrypto.xyz/api/queries/cb6373b7-9e55-4df4-9643-6117da959924/latest-run') as response
  ), lateral FLATTEN (input => response:data:data)
)
,
unique_voter as (
SELECT
  DISTINCT(voter) as voter 
FROM vote_query
)

SELECT 
    tx.TX_HASH,
    tx.BLOCK_NUMBER,
    tx.BLOCK_TIMESTAMP,
    tx.FROM_ADDRESS,
    tx.TO_ADDRESS,
    tx.GAS_LIMIT,
    tx.GAS_USED,
    tx.TX_FEE,
    tx.ETH_VALUE
FROM %s.core.fact_transactions tx
INNER JOIN
unique_voter v ON tx.FROM_ADDRESS = v.voter OR tx.TO_ADDRESS = v.voter
WHERE tx.BLOCK_TIMESTAMP 
    between CURRENT_DATE - interval '%d day' -- 3000
    AND CURRENT_DATE - interval '%d day'
AND tx.STATUS = 'SUCCESS'
    """

elif TYPE == 'TOKEN_TRANSFERS':
    print('Extracting token transfers')
    sql_template = """
    with vote_query AS (
    SELECT 
    value[0]::STRING AS id,
    LOWER(value[1]::STRING) AS transaction,
    value[2]::NUMBER AS block_number,
    value[3]::STRING AS project_id,
    value[4]::NUMBER AS application_id,
    value[5]::STRING AS round_id,
    LOWER(value[6]::STRING) AS voter,
    LOWER(value[7]::STRING) AS grant_address,
    LOWER(value[8]::STRING) AS token,
    value[9]::NUMBER AS amount,
    value[10]::FLOAT AS amount_USD,
    value[11]::FLOAT AS amount_round_token,
    value[12]::TIMESTAMP_NTZ AS block_time,
    value[13]::NUMBER AS unix_time
    FROM (
    SELECT
        livequery.live.udf_api('https://flipsidecrypto.xyz/api/queries/cb6373b7-9e55-4df4-9643-6117da959924/latest-run') as response
    ), lateral FLATTEN (input => response:data:data)
    )
    ,
    unique_voter as (
    SELECT
    DISTINCT(voter) as voter 
    FROM vote_query
    )

        SELECT 
        tx.TX_HASH, 
        tx.BLOCK_NUMBER,
        tx.BLOCK_TIMESTAMP,
        tx.CONTRACT_ADDRESS,
        tx.ORIGIN_FROM_ADDRESS,
        tx.ORIGIN_TO_ADDRESS,
        tx.FROM_ADDRESS,
        tx.TO_ADDRESS,
        tx.SYMBOL,
        tx.RAW_AMOUNT,
        tx.AMOUNT_USD
        FROM %s.core.ez_token_transfers tx
        INNER JOIN
        unique_voter v ON tx.ORIGIN_FROM_ADDRESS = v.voter -- sender of a token
        OR tx.TO_ADDRESS = v.voter -- receiver of a token
        WHERE tx.BLOCK_TIMESTAMP
        between CURRENT_DATE - interval '%d day'
        AND CURRENT_DATE - interval '%d day'
    """
else:
    raise ValueError('Type must be either TRANSACTIONS or TOKEN_TRANSFERS')

# Initialize Flipside API using sbscorer from sybil-scorer
flipside_api = FlipsideApi(api_key, page_size=PAGE_SIZE, timeout_minutes=QUERY_TIMEOUT)

ls_df = []
for i in range (0, (TOTAL_DAYS//N_DAYS)+1):
    print('Processing days from today-%d days to today-%d days' % ((i+1)*N_DAYS, i*N_DAYS))
    sql = sql_template % (CHAIN, (i+1)*N_DAYS, i*N_DAYS) # between oldest date and current date
    ls_df.append(flipside_api.execute_query(sql))

print('Concatenating dataframes')
df = pd.concat(ls_df)


if not os.path.exists(PATH_TO_EXPORT):
    os.makedirs(PATH_TO_EXPORT)

print('Exporting to csv and pkl to %s' % PATH_TO_EXPORT)
try :
    df.to_csv(os.path.join(PATH_TO_EXPORT, f'gr_18_{CHAIN}_{TYPE}.csv'), index=False, escapechar='\\')
except Exception as e: 
    print('Error in exporting csv')
    print(e)

try : 
    df.to_pickle(os.path.join(PATH_TO_EXPORT, f'gr_18_{CHAIN}_{TYPE}.pkl'), compression='gzip')
except Exception as e:
    print('Error in exporting pkl')
    print(e)
    df.to_feather(os.path.join(PATH_TO_EXPORT, f'gr_18_{CHAIN}_{TYPE}.feather'))

print('Done')