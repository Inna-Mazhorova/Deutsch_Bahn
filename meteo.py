import http.client
import json
import pandas as pd
import requests

conn2 = http.client.HTTPSConnection("api.open-meteo.com")

conn2.request("GET", "/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max&timezone=GMT")
res2 = conn2.getresponse()
data2 = json.loads(res2.read().decode("utf-8"))

print(data2['daily'])