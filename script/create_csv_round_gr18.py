import requests
import pandas as pd

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
df_projects.to_csv(f'projects_GR18_ROUNDS_ID.csv', index=False)


df_projects.to_csv('projects.csv', index=False)
print('Done!')
