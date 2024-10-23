import requests
import time
import json  
import os
from dotenv import load_dotenv

# constants
RETRY_LIMIT = 3 # no. of retry attempts for api requests
BASE_URL = 'https://api.github.com/orgs/{}/repos?page={}&per_page=100'
RATE_LIMIT_SLEEP = 60  # sleep time when rate limit is exceeded

load_dotenv()
headers = {
    'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'  
}

# fetch all repo for the specified organization from github
def get_repositories(org):
    repositories = [] # list to store all fetched repositories
    page = 1 # page counter for pagination
    
    while True:
        url = BASE_URL.format(org, page) # to construct the url for the current page of repo
        response = fetch_with_retry(url) # fetch data from the constructed url with the retry mechanism
        
        if response is None: # if response is none, stop the fetching
            break

        repos = response.json() # parse the json response to extract repo data
        if not repos: # if no repo are returned, exit the loop
            break
        
        repositories.extend(repos) # to add the fetched repo to the main list
        page += 1 # increment page no. for the next iteration
    
    return repositories # return the complete list of repo

# fetch data from the url with retry on failure due to rate limits etc
def fetch_with_retry(url):
    for attempt in range(RETRY_LIMIT): # attempt to fetch data up to RETRY_LIMIT times
        response = requests.get(url, headers=headers) # send get requests to the specified url with the authorization header
        
        if response.status_code == 200:
            return response # return the successful response
        elif response.status_code == 403 and 'rate limit' in response.text.lower(): #handle rate limit errors
            print("Rate limit exceeded, retrying...") # notify
            time.sleep(RATE_LIMIT_SLEEP * (attempt + 1)) # sleep before retrying, with expo backoff
        else: # log the failure
            print(f"Failed with status code: {response.status_code}. URL: {url}")
            return None
            
    print("Max retries reached. Unable to fetch the data.")
    return None

# process the list of repo to do the analysis
def process_repositories(repositories):
    total_stars = 0
    total_forks = 0
    language_count = {}
    top_repos = []

    for repo in repositories: # iterate thru the each repo in the list
        stars = repo.get('stargazers_count', 0) # get the no. of stars for the repo
        forks = repo.get('forks_count', 0)  # get the number of forks for the repo
        description = repo.get('description', 'No description')  # get the description of the repo, default set to 'No description'

        total_stars += stars  # accumulate the total stars across all repos
        total_forks += forks  # accumulate the total forks across all repos

        language = repo.get('language', 'Unknown') # get the programming language in the repo, default set ot 'Unknown'
        language_count[language] = language_count.get(language, 0) + 1 # update the language count in hte dict

        # append the repo name and stars to the top repos list
        top_repos.append({
            'name': repo.get('name'),
            'stars': stars,
            'forks': forks,
            'description': description
        })

    top_repos = sorted(top_repos, key=lambda x: x['stars'], reverse=True)[:5] # sort the top_repos by the np. of stars and keep the top 5
    most_popular_language = max(language_count, key=language_count.get) # to get the most popular language based on counts

    # return a dict containing the results
    return {
        'total_repositories': len(repositories),
        'total_stars': total_stars,
        'most_popular_language': most_popular_language,
        'top_5_repositories': [{'name': repo['name'], 'stars': repo['stars']} for repo in top_repos]
    }

# convert the results into json string for display
def display_analysis(analysis):
    return json.dumps(analysis, indent=2) 

# execute the analysis for the specified organization and display the results
def run_github_analysis(organization):
    print(f"Fetching repositories for organization: {organization}")
    repos = get_repositories(organization) # retrieve repo for the given organization

    # to check if any repo were retrieved successfully
    if repos:
        analysis = process_repositories(repos)
        result = display_analysis(analysis)
        print(result) 
    else:
        print("No repositories found or an error occurred.") # inform if no repo were found

if __name__ == '__main__':
    organization = 'microsoft' # specify the organization
    run_github_analysis(organization)
