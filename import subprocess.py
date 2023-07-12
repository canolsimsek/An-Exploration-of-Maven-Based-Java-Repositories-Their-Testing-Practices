import os
from sonarqube import SonarQubeClient
from sonarqube.utils.exceptions import ValidationError

URL = 'http://localhost:9000'
USERNAME = "admin"
PASSWORD = "wasada1Q"
sonar = SonarQubeClient(sonarqube_url=URL, username=USERNAME, password=PASSWORD)
parent_dir = 'D:\deneme3\gaming'

def upload_to_sonar(sonar, directory, path):
    try:
        result = sonar.projects.create_project(project=directory, name=directory, visibility="public")
        os.chdir(path)
        os.system(('mvn clean verify sonar:sonar -D sonar.projectKey={projectKey} -D maven.test.skip=true -D sonar.host.url=http://localhost:9000 -D sonar.login=squ_ff508efef681509e67a5d9595c1fefb6c8bdb6a6').format(projectKey=directory))

        print(f'Scanned {directory}')

    except ValidationError as e:
        print(f'Failed to scan {directory} due to: {str(e)}')

# List all directories in the parent directory
dirs = os.listdir(parent_dir)

# Attempt to scan each directory
for directory in dirs:
    path = os.path.join(parent_dir, directory)
    upload_to_sonar(sonar, directory, path)
