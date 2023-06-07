import requests
import pandas as pd

def load_round_votes_data(round_id):
    votes_url = 'https://indexer-grants-stack.gitcoin.co/data/1/rounds/' + round_id + '/votes.json'
    try:
        # download the Votes JSON data from the URL
        response = requests.get(votes_url)
        if response.status_code == 200:
            votes_data = response.json()
        df = pd.DataFrame(votes_data)
        return df
    except:
        return pd.DataFrame()

def load_round_projects_data(round_id):
    # prepare the URLs
    projects_url = 'https://indexer-grants-stack.gitcoin.co/data/1/rounds/' + round_id + '/projects.json'
    
    try:
        # download the Projects JSON data from the URL
        response = requests.get(projects_url)
        if response.status_code == 200:
            projects_data = response.json()

        # Extract the relevant data from each project
        projects = []
        for project in projects_data:
            project_data = {
                'id': project['id'],
                'title': project['metadata']['application']['project']['title'],
                'description': project['metadata']['application']['project']['description'],
                'recipient': project['metadata']['application']['recipient'],
                'status': project['status'],
                'amountUSD': project['amountUSD'],
                'votes': project['votes'],
                'uniqueContributors': project['uniqueContributors']
            }
            projects.append(project_data)
        # Create a DataFrame from the extracted data
        dfp = pd.DataFrame(projects)
        # Reorder the columns to match the desired order and rename column id to project_id
        dfp = dfp[['id', 'title', 'description', 'status', 'recipient', 'amountUSD', 'votes', 'uniqueContributors']]
        dfp = dfp.rename(columns={'id': 'project_id'})
        # Filter to only approved projects
        dfp = dfp[dfp['status'] == 'APPROVED']
        return dfp
    except:
        return pd.DataFrame()

ID_ROUND = '0x6e8dC2e623204D61b0E59E668702654aE336c9f7'
df_votes = load_round_votes_data(ID_ROUND)
df_projects = load_round_projects_data(ID_ROUND)

df_votes.to_csv('round.csv', index=False)
df_projects.to_csv('projects.csv', index=False)

s_voters = df_votes['voter'].unique()
pd.DataFrame(s_voters, columns=['address']).to_csv('s_voters.csv', index=False)

df_projects[['project_id', 'title', 'recipient']].to_csv('projects_small.csv', index=False)

print('Done!')
