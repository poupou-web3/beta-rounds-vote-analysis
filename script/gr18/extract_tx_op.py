import pandas as pd
import json
from sbscorer.sbdata.FlipsideApi import FlipsideApi
import os
import numpy as np
from pathlib import Path


FOLDER_NAME = 'gr18' # the name of the folder where the data will be stored
CHAIN = 'optimism' # the name of the chain to be queried
N_DAYS = 51 # number of days to be queried at a time, to avoid query timeout
PAGE_SIZE = 30000 # Flipside API page size, decrease it if the page size errors is thrown
TOTAL_DAYS = 657 # Number of days since chain inception, here set for optimism, be mindful that setting this to a large number will result in a long query time and consume credits
TYPE = 'TOKEN_TRANSFERS' # 'TRANSACTIONS' or 'TOKEN_TRANSFERS'
QUERY_TIMEOUT = 10 # minutes

# Set path to data folder, set these according to your folder structure
current_dir = Path(os.getcwd())
PATH_TO_EXPORT = os.path.join(current_dir.parent.parent.parent, 'tx_data', FOLDER_NAME)

# Initialize Flipside API
api_key = os.environ['FLIPSIDE_API_KEY'] # set your API key as an environment variable, you need to set it

# SQL query to be executed
if TYPE == 'TRANSACTIONS':
    print('Extracting transactions')
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
        block_timestamp between '2023-08-15 12:00:00.000'
        and '2023-08-29 12:00:00.000'
        and contract_address = '0xda10009cbd5d07dd0cecc66161fc93d7c9000da1'
        and origin_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
    ),
    eth_time AS (
    SELECT
        tx_hash,
        block_timestamp,
        origin_from_address as voter,
        amount_usd,
    origin_to_address,
    eth_to_address
    from
        optimism.core.ez_eth_transfers
    where
        block_timestamp between '2023-08-15 12:00:00.000'
        and '2023-08-29 12:00:00.000'
    ),
    eth_direct as (
    SELECT
        tx_hash,
        block_timestamp,
        voter,
        'ETH' as token,
        amount_usd
    FROM
        eth_time
    WHERE
        origin_to_address IN (
        '0x8de918f0163b2021839a8d84954dd7e8e151326d',
        '0xb6be0ecafdb66dd848b0480db40056ff94a9465d',
        '0x2871742b184633f8dc8546c6301cbc209945033e',
        '0x10be322de44389ded49c0b2b73d8c3a1e3b6d871',
        '0x5b95acf46c73fd116f0fedadcbef453530e35d0',
        '0xc5fdf5cff79e92fac1d6efa725c319248d279200',
        '0xf591e42dffe8e62c2085ccaadfe05f84d89d0c6',
        '0x9331fde4db7b9d9d1498c09d30149929f24cf9d5',
        '0x30c381033aa2830ceb0aa372c2e4d28f004b3db9',
        '0x69e423181f1d3e6bebf8ab88030c36da73785f26'
        )
        and eth_to_address IN (
        '0x8de918f0163b2021839a8d84954dd7e8e151326d',
        '0xb6be0ecafdb66dd848b0480db40056ff94a9465d',
        '0x2871742b184633f8dc8546c6301cbc209945033e',
        '0x10be322de44389ded49c0b2b73d8c3a1e3b6d871',
        '0x5b95acf46c73fd116f0fedadcbef453530e35d0',
        '0xc5fdf5cff79e92fac1d6efa725c319248d279200',
        '0xf591e42dffe8e62c2085ccaadfe05f84d89d0c6',
        '0x9331fde4db7b9d9d1498c09d30149929f24cf9d5',
        '0x30c381033aa2830ceb0aa372c2e4d28f004b3db9',
        '0x69e423181f1d3e6bebf8ab88030c36da73785f26'
        )
    ),
    eth_gtc as (
    SELECT
        tx_hash,
        block_timestamp,
        voter,
        'ETH' as token,
        amount_usd
    FROM
        eth_time
    WHERE
        origin_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
        and eth_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
    ),

    all_votes as (
    SELECT * from eth_gtc
    union all 
    select * FROM dai
    union all
    select * from eth_direct
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
    FROM %s.core.fact_transactions tx
    INNER JOIN
    unique_voter v ON tx.FROM_ADDRESS = v.voter OR tx.TO_ADDRESS = v.voter
    WHERE tx.BLOCK_TIMESTAMP 
    between CURRENT_DATE - interval '%d day'
    AND CURRENT_DATE - interval '%d day'
    AND tx.STATUS = 'SUCCESS'  
    """

elif TYPE == 'TOKEN_TRANSFERS':
    print('Extracting token transfers')
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
            block_timestamp between '2023-08-15 12:00:00.000'
            and '2023-08-29 12:00:00.000'
            and contract_address = '0xda10009cbd5d07dd0cecc66161fc93d7c9000da1'
            and origin_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
        ),
        eth_time AS (
        SELECT
            tx_hash,
            block_timestamp,
            origin_from_address as voter,
            amount_usd,
        origin_to_address,
        eth_to_address
        from
            optimism.core.ez_eth_transfers
        where
            block_timestamp between '2023-08-15 12:00:00.000'
            and '2023-08-29 12:00:00.000'
        ),
        eth_direct as (
        SELECT
            tx_hash,
            block_timestamp,
            voter,
            'ETH' as token,
            amount_usd
        FROM
            eth_time
        WHERE
            origin_to_address IN (
            '0x8de918f0163b2021839a8d84954dd7e8e151326d',
            '0xb6be0ecafdb66dd848b0480db40056ff94a9465d',
            '0x2871742b184633f8dc8546c6301cbc209945033e',
            '0x10be322de44389ded49c0b2b73d8c3a1e3b6d871',
            '0x5b95acf46c73fd116f0fedadcbef453530e35d0',
            '0xc5fdf5cff79e92fac1d6efa725c319248d279200',
            '0xf591e42dffe8e62c2085ccaadfe05f84d89d0c6',
            '0x9331fde4db7b9d9d1498c09d30149929f24cf9d5',
            '0x30c381033aa2830ceb0aa372c2e4d28f004b3db9',
            '0x69e423181f1d3e6bebf8ab88030c36da73785f26'
            )
            and eth_to_address IN (
            '0x8de918f0163b2021839a8d84954dd7e8e151326d',
            '0xb6be0ecafdb66dd848b0480db40056ff94a9465d',
            '0x2871742b184633f8dc8546c6301cbc209945033e',
            '0x10be322de44389ded49c0b2b73d8c3a1e3b6d871',
            '0x5b95acf46c73fd116f0fedadcbef453530e35d0',
            '0xc5fdf5cff79e92fac1d6efa725c319248d279200',
            '0xf591e42dffe8e62c2085ccaadfe05f84d89d0c6',
            '0x9331fde4db7b9d9d1498c09d30149929f24cf9d5',
            '0x30c381033aa2830ceb0aa372c2e4d28f004b3db9',
            '0x69e423181f1d3e6bebf8ab88030c36da73785f26'
            )
        ),
        eth_gtc as (
        SELECT
            tx_hash,
            block_timestamp,
            voter,
            'ETH' as token,
            amount_usd
        FROM
            eth_time
        WHERE
            origin_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
            and eth_to_address = '0x15fa08599eb017f89c1712d0fe76138899fdb9db'
        ),

        all_votes as (
        SELECT * from eth_gtc
        union all 
        select * FROM dai
        union all
        select * from eth_direct
        ),

        unique_voter as (SELECT DISTINCT voter from all_votes)

        SELECT 
        tx.TX_HASH, 
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
    df.to_pickle(os.path.join(PATH_TO_EXPORT, f'gr_18_{CHAIN}_{TYPE}.pkl'))
except Exception as e:
    print('Error in exporting pkl')
    print(e)
    df.to_feather(os.path.join(PATH_TO_EXPORT, f'gr_18_{CHAIN}_{TYPE}.feather'))

print('Done')