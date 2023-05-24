# Project

**gitlab import** and **github export** are currently in progress and not yet available

# Steps

1. setup
2. environments
3. run project

# Setup

## Install

```sh
python -m venv env # create environment
source env/bin/activate # activate environment

pip install -r requirements.txt # install all dependencies
```

## Environments

You need to create a **.env** file in the root project

```
GITLAB_URL=          # gitlab host url, for example 'https://gitlab.com'
GITLAB_ACCESS_TOKEN= # gitlab access token
GITLAB_PROJECT_ID=   # gitlab project id, for exaple 202
PROJECT=             # project name, the export file will be created with this name
GITHUB_TOKEN=        # github token
GITHUB_REPO_NAME=    # 'owner/repo' for example if your repository is 'https://github.com/ncostamagna/matrix', You'll set 'ncostamagna/matrix' in this environment
ENVS=                # environments with comma, for example 'qa,prod'
```

## 'Files' folder

You need to create a **files** folder in the root project

# Export

```sh
python main.py gitlab export
```

# Import

```sh
python main.py github import --file=my_file.csv
```
