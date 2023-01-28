import http.client
import json
import pandas as pd
import requests
import config
import pymysql

from sqlalchemy import create_engine

API_KEY = config.api_key
CLIENT_ID = config.client_id

response_list = []

conn = http.client.HTTPSConnection("apis.deutschebahn.com")

headers = {
    'DB-Client-Id': CLIENT_ID,
    'DB-Api-Key': API_KEY,
    'accept': "application/json"
    }

conn.request("GET", "/db-api-marketplace/apis/fasta/v2/facilities", headers=headers)
res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))

df = pd.DataFrame.from_records(data)
with pd.option_context("display.max_rows", None, "display.max_columns", None):
    print((df['description'][2174]))
equipment = df[["equipmentnumber", "geocoordX", "geocoordY", "description", "operatorname", "stationnumber", "type"]]#.head(2000)
unique_stations = df.drop_duplicates(subset=['stationnumber'])
#list_of_unique_stations = df.stationnumber.unique()
#unique_stations = pd.Series(list_of_unique_stations, name = "stationnumber")

#df_stations = unique_stations.join(df, how='left')
list_latitude = unique_stations['geocoordY'].tolist()
list_longitude = unique_stations['geocoordX'].tolist()

conn2 = http.client.HTTPSConnection("api.open-meteo.com")

conn2.request("GET", "/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max&timezone=GMT")
res2 = conn2.getresponse()
data2 = res2.read()

#with pd.option_context("display.max_rows", None, "display.max_columns", None):

    #print(df.columns)
    #print(equipment.head())

# Credentials to database connection
hostname="localhost:3306"
dbname="mydb"
uname="Lantana"
pwd="db1234567!"

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))

# Convert dataframe to sql table
equipment.to_sql('equipment', engine, index=False, if_exists='append')#replace append
