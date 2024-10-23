# GitHub Repository Analysis

This Python application integrates with the GitHub API to retrieve, process, and analyze repository data for a specified GitHub organization. It uses a Personal Access Token (PAT) for authentication and handles pagination to ensure all repositories are fetched.

## Requirements
- Python
- `requests` library
- `python-dotenv` library

## Installation
1. Clone the repository:
   ```
   git clone [https://github.com/yourusername/repo-name.git](https://github.com/lzwxxx/GithubRepoAnalyzer.git)
   cd GithubRepoAnalyzer
   ```

2. Install the required packages:
    ```
    pip install requests python-dotenv
    ```

3. Create a .env file in the root directory with your GitHub Personal Access Token:
    ```
    GITHUB_TOKEN="YOUR GITHUB PAT" # replace with your actual Github PAT
    ```

## Usage
To run the application, specify the organization name in the if __name__ == '__main__': section of the script:
```
if __name__ == '__main__':
    organization = 'google'  # specify the organization
    run_github_analysis(organization)
```

Execute the script:
```
python main.py
```
