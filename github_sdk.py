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
    vars = github_api.get_variables_by_env(id)
    var_df = pd.DataFrame.from_dict(vars)
    var_df['secret'] = 0

    # get secrets
    sec = github_api.get_secrets_by_env(id)
    sec_df = pd.DataFrame.from_dict(sec)
    sec_df['secret'] = 1

    
    # remove import data that existing in github
    df_check = pd.concat([var_df, sec_df],axis=0)[['name', 'value', 'env', 'secret']]
    df = df_import.merge(df_check, left_on=['key', 'env', 'secret'], right_on=['name', 'env', 'secret'], suffixes=('_import', '_github'),  how='left', indicator=True)
    df = df.loc[df['_merge'] == 'left_only',['key', 'value_import', 'env', 'secret']]
    print(df)

    