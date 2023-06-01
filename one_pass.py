from decouple import config
import github_api
import pandas as pd


def generate(file):
    # data to import
    df = pd.read_csv(f'files/{file}')

    df = df.loc[df['secret'] == 1, ["key","value","env"]]

    df.loc[df['env'] == "*", ["env"]] = "default"
    df['key'] = df['env'] + " - " + df['key']
    df.drop(columns=['env'], inplace=True)

    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]

    project_name = config('PROJECT') 
    df.insert(0,'title',project_name)
  
    df.to_csv(f"files/{project_name}_1p.csv", index=False)
