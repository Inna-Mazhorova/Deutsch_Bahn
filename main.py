import http.client
import json
import pandas as pd
import requests
import config
import pymysql
from ast import literal_eval
from datetime import datetime

from sqlalchemy import create_engine


API_KEY = config.api_key
CLIENT_ID = config.client_id
CURRENT_DATE = datetime.now().date()
PWD = config.pwd


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
df['description'][2174] = 'Parkplatz 4'
#with pd.option_context("display.max_rows", None, "display.max_columns", None):
 #   print((df['description'][2174]))
equipment = df[["equipmentnumber", "geocoordX", "geocoordY", "description", "operatorname", "stationnumber", "type"]]
statuses = df[["equipmentnumber", "state"]]
statuses['date'] = CURRENT_DATE

unique_stations = df.dropna(subset=['geocoordX', 'geocoordY'])
unique_stations = unique_stations.query('geocoordX < 181 and geocoordY <= 181')
unique_stations = unique_stations.drop_duplicates(subset=['stationnumber'])
#list_of_unique_stations = df.stationnumber.unique()
#unique_stations = pd.Series(list_of_unique_stations, name = "stationnumber")
#print(unique_stations.info())
#df_stations = unique_stations.join(df, how='left')
#print(len(unique_stations))
list_stationnumbers = unique_stations['stationnumber'].tolist()
list_latitude = unique_stations['geocoordY'].tolist()
list_longitude = unique_stations['geocoordX'].tolist()

#print(list_stationnumbers[549])
#print(list_latitude[549])
#print(list_longitude[549])

conn2 = http.client.HTTPSConnection("api.open-meteo.com")

meteo_df = pd.DataFrame(columns=['stationnumber', 'geocoordX', 'geocoordY', 'forecast_date', 'temperature'])


for i in range(len(list_stationnumbers)):
    conn2.request("GET", "/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max&timezone=GMT".format(latitude=list_latitude[i], longitude=list_longitude[i]))
    res2 = conn2.getresponse()
    data2 = res2.read()
    data2_dict = literal_eval(data2.decode('utf-8'))
    #print(data2_dict)

    #print(data2_dict['latitude'])
    #print(data2_dict['longitude'])
    #print(data2_dict['daily']['time'][0])
    #print(data2_dict['daily']['temperature_2m_max'][0])
    meteo_df.loc[len(meteo_df.index)] = [list_stationnumbers[i], data2_dict['longitude'], data2_dict['latitude'],data2_dict['daily']['time'][0], data2_dict['daily']['temperature_2m_max'][0]]
    meteo_df.loc[len(meteo_df.index)] = [list_stationnumbers[i], data2_dict['longitude'], data2_dict['latitude'],data2_dict['daily']['time'][1], data2_dict['daily']['temperature_2m_max'][1]]
    meteo_df.loc[len(meteo_df.index)] = [list_stationnumbers[i], data2_dict['longitude'], data2_dict['latitude'],data2_dict['daily']['time'][2], data2_dict['daily']['temperature_2m_max'][2]]
    meteo_df.loc[len(meteo_df.index)] = [list_stationnumbers[i], data2_dict['longitude'], data2_dict['latitude'],data2_dict['daily']['time'][3], data2_dict['daily']['temperature_2m_max'][3]]
    meteo_df.loc[len(meteo_df.index)] = [list_stationnumbers[i], data2_dict['longitude'], data2_dict['latitude'],data2_dict['daily']['time'][4], data2_dict['daily']['temperature_2m_max'][4]]
    meteo_df.loc[len(meteo_df.index)] = [list_stationnumbers[i], data2_dict['longitude'], data2_dict['latitude'],data2_dict['daily']['time'][5], data2_dict['daily']['temperature_2m_max'][5]]
    meteo_df.loc[len(meteo_df.index)] = [list_stationnumbers[i], data2_dict['longitude'], data2_dict['latitude'],data2_dict['daily']['time'][6], data2_dict['daily']['temperature_2m_max'][6]]
    #print(i)
    #print(data2_dict)
meteo_df['report_date'] = CURRENT_DATE
#with pd.option_context("display.max_rows", None, "display.max_columns", None):

    #print(meteo_df)


# Credentials to database connection
hostname="localhost:3306"
dbname="mydb"
uname="Lantana"
pwd=PWD

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))

# Convert dataframe to sql table
#equipment.to_sql('equipment', engine, index=False, if_exists='append')#replace append
statuses.to_sql('statuses', engine, index=False, if_exists='append')
meteo_df.to_sql('forecast_temperature', engine, index=False, if_exists='append')
