from decouple import config
import github_api
import pandas as pd


def import_environment(replace, file):
    GITHUB_REPO_NAME = config('GITHUB_REPO_NAME')

    # data to import
    df_import = pd.read_csv(f'files/{file}')

    # get repo
    id = github_api.get_repository_id(GITHUB_REPO_NAME)

    # get vars
    vars_env = github_api.get_variables_by_env(id)
    vars_rep = github_api.get_variables(GITHUB_REPO_NAME)
    var_df = pd.DataFrame.from_dict(vars_env + vars_rep)
    var_df['secret'] = 0

    # get secrets
    sec_env = github_api.get_secrets_by_env(id)
    sec_rep = github_api.get_secrets(GITHUB_REPO_NAME)
    sec_df = pd.DataFrame.from_dict(sec_env + sec_rep)
    sec_df['secret'] = 1
    
    # remove import data that existing in github
    df_check = pd.concat([var_df, sec_df],axis=0)
    df = None
    if df_check.empty == False:
        df_check = pd.concat([var_df, sec_df],axis=0)[['name', 'env', 'secret']]
        df = df_import.merge(df_check, left_on=['key', 'env', 'secret'], right_on=['name', 'env', 'secret'], suffixes=('_import', '_github'),  how='left', indicator=True)
        df = df.loc[df['_merge'] == 'left_only',['key', 'value', 'env', 'secret']]
    else:
        df = df_import[['key', 'value', 'env', 'secret']]
    

    print(df, '\n')
    print(df['env'].value_counts(), '\n')
    print(df['secret'].value_counts(), '\n')
    user_input = input('Do you want to run the process (yes/no): ')

    if not (user_input.lower() == 'yes' or  user_input.lower() == 'y'):  
        print("exit")      
        return

    print("running variables and secrets:")
    pkey = github_api.get_public_key(GITHUB_REPO_NAME)
    pkey_env = github_api.get_public_key_by_env(id)

    for index, row in df.iterrows():
        env = row['env']
        if row['secret'] == 1:
            if env == "*":
                github_api.create_secret(GITHUB_REPO_NAME, None, row['key'], row['value'], None, pkey['key_id'], pkey['key'])
            else:
                github_api.create_secret(None, id, row['key'], row['value'], env, pkey_env[env]['key_id'], pkey_env[env]['key'])
        else:    
            if env == "*":
                github_api.create_variable(GITHUB_REPO_NAME, None, row['key'], row['value'], None)
            else:
                github_api.create_variable(None, id, row['key'], row['value'], env)
    
    print("The process has completed successfully")
