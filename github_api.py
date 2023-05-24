import requests
import time
from decouple import config
import types
import sys
from base64 import b64encode
from nacl import encoding, public

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


def get_variables(repository):
        variables = []
       
        page = 1
        max_page = 10
        end_pagination = False
        while end_pagination == False:
            url =  url = f'{__HOST}/repos/{repository}/actions/variables?page={page}'
            print(url)
            s = requests.get(url, headers=__HEADER)
            res = s.json()

            if s.status_code > 299:
                sys.exit(f"GUTHUB_GET_VARIABLES:\n {res} \n URL: {url}")

            if res['total_count'] > page * max_page:
                page = page + 1
            else:
                end_pagination = True
            res = [dict(r, env="*") for r in res['variables']]
            variables = variables + res
                
        return variables


def get_secrets(repository):
        secrets = []
        page = 1
        max_page = 30
        end_pagination = False
        while end_pagination == False:
            url =  url = f'{__HOST}/repos/{repository}/actions/secrets?page={page}'
            print(url)
            s = requests.get(url, headers=__HEADER)
            res = s.json()

            if s.status_code > 299:
                sys.exit(f"GUTHUB_GET_SECRETS:\n {res} \n URL: {url}")
            
            if res['total_count'] > page * max_page:
                page = page + 1
            else:
                end_pagination = True
            
            res = [dict(r, env="*") for r in res['secrets']]
            secrets = secrets + res
        return secrets

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
                    sys.exit(f"GUTHUB_GET_VARIABLES_BY_ENV:\n {res} \n URL: {url}")

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
                    sys.exit(f"GUTHUB_GET_SECRETS_BY_ENV:\n {res} \n URL: {url}")
                
                if res['total_count'] > page * max_page:
                    page = page + 1
                else:
                    end_pagination = True
                
                res = [dict(r, env=env) for r in res['secrets']]
                secrets = secrets + res
        return secrets
    
def get_public_key(repo_name):
    url = f"{__HOST}/repos/{repo_name}/actions/secrets/public-key"
    print(url)
    s = requests.get(url, headers=__HEADER)

    res = s.json()
    if s.status_code > 299:
        sys.exit(f"GUTHUB_CREATE_VARIABLE:\n {res} \n URL: {url}")

    return  res

def get_public_key_by_env(repo_id):
    env_key = {}

    for env in __ENVS:
        url = f"{__HOST}/repositories/{repo_id}/environments/{env}/secrets/public-key"
        print(url)
        s = requests.get(url, headers=__HEADER)
        res = s.json()
        if s.status_code > 299:
            sys.exit(f"GITHUB_GET_PUBLIC_KEY_BY_ENV:\n {res} \n URL: {url}")
        
        env_key[env] = res

    return env_key


def create_variable(repo_name, repo_id, key, value, env):
    url = f"repositories/{repo_id}/environments/{env}" if env != None else f"repos/{repo_name}/actions"
    url = f"{__HOST}/{url}/variables"
    print(url, key)
    data = {"name": key, "value": value}
    s = requests.post(url, json=data, headers=__HEADER)

    res = s.json()
    if s.status_code > 299:
        sys.exit(f"GUTHUB_CREATE_VARIABLE:\n {res} \n URL: {url}")

    return

def create_secret(repo_name, repo_id, key, value, env, public_key_id, public_key_value):

    url = f"repositories/{repo_id}/environments/{env}" if env != None else f"repos/{repo_name}/actions"
    url = f"{__HOST}/{url}/secrets/{key}"

    enc_value = encrypt(public_key_value, value)
    data = {'key_id': public_key_id, "encrypted_value":enc_value}
    
    print(url, key)
    s = requests.put(url, json=data, headers=__HEADER)

    res = s.json()
    if s.status_code > 299:
        sys.exit(f"GUTHUB_CREATE_SECRET:\n {res} \n URL: {url}")

    return


def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")