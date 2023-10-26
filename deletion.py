import requests

SONAR_URL = 'http://localhost:9000'
TOKEN = 'squ_ff508efef681509e67a5d9595c1fefb6c8bdb6a6'  # replace with your admin token
auth = (TOKEN, '')

# Get the list of all projects
projects_url = f'{SONAR_URL}/api/projects/search'
projects_response = requests.get(projects_url, auth=auth)
projects = projects_response.json()['components']

# For each project, delete it from sonarqube
for project in projects:
    project_key = project['key']

    delete_url = f'{SONAR_URL}/api/projects/delete'
    params = {'project': project_key}
    delete_response = requests.post(delete_url, params=params, auth=auth)
    
    if delete_response.status_code == 204:
        print(f'Project {project_key} deleted successfully.')
    else:
        print(f'Failed to delete project {project_key}.')


