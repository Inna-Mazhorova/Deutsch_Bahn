import http.client
import pandas as pd
import requests
import config

API_KEY = config.api_key
CLIENT_ID = config.client_id

response_list = []

conn = http.client.HTTPSConnection("apis.deutschebahn.com")

headers = {
    'DB-Client-Id': CLIENT_ID,
    'DB-Api-Key': API_KEY,
    'accept': "application/json"
    }

#conn.request("GET", "/db-api-marketplace/apis/fasta/v2/facilities?type=["ESCALATOR","ELEVATOR"]&state=REPLACE_THIS_VALUE&equipmentnumbers=REPLACE_THIS_VALUE&stationnumber=REPLACE_THIS_VALUE&area=REPLACE_THIS_VALUE", headers=headers)

conn.request("GET", "/db-api-marketplace/apis/fasta/v2/facilities", headers=headers)
res = conn.getresponse()
data = res.read().decode("utf-8")

#df = pd.DataFrame.from_dict(data)
df = pd.DataFrame.from_records(data)
#df=pd.json_normalize(data)
#print(df.head())
print(data.equipmentnumber.unique())