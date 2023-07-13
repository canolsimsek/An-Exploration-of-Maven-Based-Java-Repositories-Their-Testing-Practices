import requests
import pandas as pd

SONAR_URL = 'http://localhost:9000'
TOKEN = 'squ_cfb9a12eff55b1f109a0cfa506f9c26feba690d1'

auth = (TOKEN, '')

# Get the list of all metrics
metrics_url = f'{SONAR_URL}/api/metrics/search'
metrics_response = requests.get(metrics_url, auth=auth)
metrics = metrics_response.json()['metrics']

# Group metrics by domain
metric_domains = {}
for metric in metrics:
    domain = metric['domain']
    if domain not in metric_domains:
        metric_domains[domain] = []
    metric_domains[domain].append(metric['key'])


projects_url = f'{SONAR_URL}/api/projects/search'
projects_response = requests.get(projects_url, auth=auth)
projects = projects_response.json()['components']

domain_dataframes = {domain: pd.DataFrame() for domain in metric_domains.keys()}


for project in projects:
    project_key = project['key']
    project_name = project['name']

    project_metrics = {}
    
    for domain, metric_keys in metric_domains.items():
        metrics_url = f'{SONAR_URL}/api/measures/component'
        metrics_params = {'component': project_key, 'metricKeys': ','.join(metric_keys)}
        metrics_response = requests.get(metrics_url, params=metrics_params, auth=auth)

        measures = metrics_response.json()['component']['measures'] if 'component' in metrics_response.json() else []
        
        
        for measure in measures:
            project_metrics[measure['metric']] = measure['value']
        
      
        if project_metrics:
            project_df = pd.DataFrame(project_metrics, index=[project_name])
            domain_dataframes[domain] = pd.concat([domain_dataframes[domain], project_df])


with pd.ExcelWriter('D:\\deneme3\\metric_results.xlsx', engine='xlsxwriter') as writer:
    for domain, df in domain_dataframes.items():
        if not df.empty:
            df.to_excel(writer, sheet_name=domain)
