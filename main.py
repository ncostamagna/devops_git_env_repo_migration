import gitlab_sdk
import github_sdk
from decouple import config
import pandas as pd
import argparse
import one_pass

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("repository", choices=['gitlab', 'github'], type = str, help='repository')
    parser.add_argument("operation", choices=['export', 'import'], type = str, help='export or import operation')
    parser.add_argument('-f', '--file')
    args = parser.parse_args()
    project_name = config('PROJECT') 
    if args.operation == 'export':
        if args.repository == 'gitlab':
            l = gitlab_sdk.get_gitlab_repository_environments()
            df = pd.DataFrame.from_dict(l)
            df.to_csv(f'files/{project_name}.csv')
    else:
        if args.file == None:
            print("error: file is required")
            return 

        if args.repository == "github":
            github_sdk.import_environment(args.file)
            one_pass.generate(args.file)


if __name__ == "__main__":
    main()