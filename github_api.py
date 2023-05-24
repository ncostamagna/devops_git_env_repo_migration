import requests
import time
from decouple import config
import types
import sys


__TOKEN = "Bearer " + config('GITHUB_TOKEN')
__HEADER = {"Content-Type": "application/json; charset=utf-8", 'Authorization': __TOKEN}
__HOST = "https://api.github.com"
__ENVS = config("ENVS").split(',')

def get_repository_id(name):
        url = f'{__HOST}/repos/{name}'
        s = requests.get(url, headers=__HEADER)
        res = s.json()

        if s.status_code > 299:
            sys.exit(f"GUTHUB_GET_REPOSITORY:\n {res} \n URL: {url}")
        return res['id']


def get_variables_by_env(repo_id):
        variables = []
        for env in __ENVS:
            page = 1
            max_page = 10
            end_pagination = False
            while end_pagination == False:
                url =  url = f'{__HOST}/repositories/{repo_id}/environments/{env}/variables?page={page}'
                print(url)
                s = requests.get(url, headers=__HEADER)
                res = s.json()

                if s.status_code > 299:
                    sys.exit(f"GUTHUB_GET_REPOSITORY:\n {res} \n URL: {url}")

                if res['total_count'] > page * max_page:
                    page = page + 1
                else:
                    end_pagination = True
                res = [dict(r, env=env) for r in res['variables']]
                variables = variables + res
                
        return variables

def get_secrets_by_env(repo_id):
        secrets = []
        for env in __ENVS:
            page = 1
            max_page = 30
            end_pagination = False
            while end_pagination == False:
                url =  url = f'{__HOST}/repositories/{repo_id}/environments/{env}/secrets?page={page}'
                print(url)
                s = requests.get(url, headers=__HEADER)
                res = s.json()

                if s.status_code > 299:
                    sys.exit(f"GUTHUB_GET_REPOSITORY:\n {res} \n URL: {url}")
                
                if res['total_count'] > page * max_page:
                    page = page + 1
                else:
                    end_pagination = True
                
                res = [dict(r, env=env) for r in res['secrets']]
                secrets = secrets + res
        return secrets