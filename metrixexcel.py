import requests
import pandas as pd

SONAR_URL = 'http://localhost:9000'
TOKEN = 'squ_cfb9a12eff55b1f109a0cfa506f9c26feba690d1'
# Using the token for authentication
auth = (TOKEN, '')

# Get the list of all metrics
metrics_url = f'{SONAR_URL}/api/metrics/search'
metrics_response = requests.get(metrics_url, auth=auth)
metrics = metrics_response.json()['metrics']
metric_keys = [metric['key'] for metric in metrics]

# Get the list of all projects
projects_url = f'{SONAR_URL}/api/projects/search'
projects_response = requests.get(projects_url, auth=auth)
projects = projects_response.json()['components']

# Create a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter('D:\\deneme3\\metric_results2.xlsx', engine='openpyxl') as writer:
    # For each project, get the metrics
    for project in projects:
        project_key = project['key']
        project_name = project['name']

        # Get the list of all metrics
        metrics_url = f'{SONAR_URL}/api/measures/component'
        metrics_params = {'component': project_key, 'metricKeys': ','.join(metric_keys)}
        metrics_response = requests.get(metrics_url, params=metrics_params, auth=auth)

        measures = metrics_response.json()['component']['measures'] if 'component' in metrics_response.json() else []

        # Prepare the data for Excel
        excel_data = []
        for measure in measures:
            metric_key = measure['metric']
            metric_value = measure['value']
            excel_data.append({'Metric': metric_key, 'Value': metric_value})

        # Write the data into a sheet named after the project name
        if excel_data:
            df = pd.DataFrame(excel_data)
            df.to_excel(writer, sheet_name=project_name[:31], index=False)  # Excel has a 31 character limit for sheet names

