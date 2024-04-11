#Import libraries
import requests
import pandas as pd
import json
from requests_negotiate_sspi import HttpNegotiateAuth

#Configs
url_base = 'http://localhost/reports/api/v2.0/'
endpoint = 'PowerBIReports'

#Load dataset reports
response = requests.get(url_base+endpoint,auth=HttpNegotiateAuth())
object = json.loads(response.text)
reports = pd.json_normalize(object['value'])

#Load dataset datasources
ids = reports['Id']
datasources = pd.DataFrame()
for id in ids:
    response = requests.get(url_base+endpoint+'('+id+')'+'/DataSources',auth=HttpNegotiateAuth())
    object = json.loads(response.text)
    datasources= pd.concat([pd.json_normalize(object['value']),datasources],ignore_index=True)

#Load dataset politicies
politicies = pd.DataFrame()
for id in ids:
    response = requests.get(url_base+endpoint+'('+id+')'+'/Policies',auth=HttpNegotiateAuth())
    object = json.loads(response.text)
    df_temp = pd.json_normalize(object['Policies'])
    df_temp['id'] = id
    politicies = pd.concat([politicies, df_temp], ignore_index=True)


#Export datasets
politicies.to_csv('politicies.csv')
reports.to_csv('reports.csv')
datasources.to_csv('datasources.csv')