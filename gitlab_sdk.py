import gitlab
from decouple import config

def get_gitlab_repository_environments() -> list:
    gitlab_url = config('GITLAB_URL')
    access_token = config('GITLAB_ACCESS_TOKEN')
    project_id = config('GITLAB_PROJECT_ID')

    gl = gitlab.Gitlab(gitlab_url, private_token=access_token)
    project = gl.projects.get(project_id)
    variables = project.variables.list(all=True)

    l = []
    for variable in variables:
        d = {
            'variable_type': variable.variable_type,
            'key': variable.key,
            'value': variable.value,
            'env': variable.environment_scope,
            'masked': variable.masked,
        }

        l.append(d)

    return l