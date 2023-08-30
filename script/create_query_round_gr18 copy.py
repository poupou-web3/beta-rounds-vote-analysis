import requests
import pandas as pd
import numpy as np

def safe_get(data, *keys):
    """Safely retrieve nested dictionary keys."""
    temp = data
    for key in keys:
        if isinstance(temp, dict) and key in temp:
            temp = temp[key]
        else:
            return None
    return temp

def load_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch data from {url}. Error: {e}")
        return []

def load_round_projects_data(round_id, chain_id):
    url = f'https://indexer-grants-stack.gitcoin.co/data/{chain_id}/rounds/{round_id}/applications.json'
    data = load_data_from_url(url)
    
    projects = []
    for project in data:
        title = safe_get(project, 'metadata', 'application', 'project', 'title')
        grantAddress = safe_get(project, 'metadata', 'application', 'recipient')
        description = safe_get(project, 'metadata', 'application', 'project', 'description')
        
        if title and grantAddress:  # Ensure required fields are available
            project_data = {
                'projectId': project['projectId'],
                'roundId': project['roundId'],
                'title': title,
                'grantAddress': grantAddress,
                'status': project['status'],
                'amountUSD': project['amountUSD'],
                'votes': project['votes'],
                'uniqueContributors': project['uniqueContributors'],
                'description': description
            }
            projects.append(project_data)
    return pd.DataFrame(projects)


CHAIN_ID = "10"
ID_ROUND = '0x30C381033aA2830cEB0aA372C2e4D28F004b3DB9'

GR18_ROUNDS_ID = ["0x8de918F0163b2021839A8D84954dD7E8e151326D","0xb6Be0eCAfDb66DD848B0480db40056Ff94A9465d","0x2871742B184633f8DC8546c6301cbC209945033e","0x10be322DE44389DeD49c0b2b73d8c3A1E3B6D871","0x5B95acf46c73Fd116F0fEDADcBEDF453530e35d0","0xc5FdF5cFf79e92FAc1d6Efa725c319248D279200","0xf591E42dfDfE8E62C2085CCaAdFE05F84D89D0c6","0x9331FDe4Db7b9d9d1498C09d30149929f24cF9D5","0x30C381033aA2830cEB0aA372C2e4D28F004b3DB9"]

projects = []
for round_id in GR18_ROUNDS_ID:
    projects.append(load_round_projects_data(round_id, CHAIN_ID))

df_projects = pd.concat(projects)
df_projects = df_projects.loc[np.logical_and(df_projects['status'] == 'APPROVED', df_projects['roundId'].isin(GR18_ROUNDS_ID)), : ]
df_projects.drop_duplicates(subset=['grantAddress', 'roundId'], inplace=True)

df_projects['title'] = df_projects['title'].str.replace("'", ' ')
df_projects['grantAddress'] = df_projects['grantAddress'].str.replace("'", ' ')

df_projects.to_csv('projects_GR18_ROUNDS_ID.csv', index=False)
df_projects.to_csv('projects_small_GR18_ROUNDS_ID.csv', columns=['title', 'grantAddress', 'roundId'], index=False)
df_projects.drop_duplicates(subset=['title']).to_csv('projects_title_GR18_ROUNDS_ID.csv', columns=['title'], index=False)

df_projects.reset_index(inplace=True, drop=True)
query = ""
for index, row in df_projects.iterrows():
    title = row['title']
    grantAddress = row['grantAddress']
    roundId = row['roundId']
    if index == 0:
        query += f"SELECT '{title}' as title, {grantAddress} as payout_address, {roundId} as round_id UNION ALL\n"
    elif index != len(df_projects)-1:
        query += f"SELECT '{title}', {grantAddress}, {roundId} UNION ALL\n"
    else:
        query += f"SELECT '{title}', {grantAddress}, {roundId}\n"


# write to text file
with open('query.txt', 'w', encoding='utf-8') as f:
    f.write(query)


df_projects.drop_duplicates(subset=['grantAddress'], inplace=True)
df_projects.reset_index(inplace=True, drop=True)
query = ""
for index, row in df_projects.iterrows():
    title = row['title']
    grantAddress = row['grantAddress']
    roundId = row['roundId']
    if index == 0:
        query += f"SELECT '{title}' as title, {grantAddress} as payout_address, {roundId} as round_id UNION ALL\n"
    elif index != len(df_projects)-1:
        query += f"SELECT '{title}', {grantAddress}, {roundId} UNION ALL\n"
    else:
        query += f"SELECT '{title}', {grantAddress}, {roundId}\n"


# write to text file
with open('query_unique_round.txt', 'w', encoding='utf-8') as f:
    f.write(query)

# small union query
query = ""
for index, row in df_projects.iterrows():
    title = row['title']
    grantAddress = row['grantAddress']
    if index == 0:
        query += f"SELECT '{title}' as title, {grantAddress} as payout_address UNION ALL\n"
    elif index != len(df_projects)-1:
        query += f"SELECT '{title}', {grantAddress} UNION ALL\n"
    else:
        query += f"SELECT '{title}', {grantAddress}\n"


# write to text file
with open('query_small.txt', 'w', encoding='utf-8') as f:
    f.write(query)



df_projects.to_csv('projects.csv', index=False)
print('Done!')
