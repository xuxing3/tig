
# INFLUXDB_TOKEN=Zt2lpPOocc2PWMLR0uX4_UmUmgJ-s4UsqSgZpzBdSDsfE7MJRqMLvz7Ji7dUWRdvCP24vDweTWJN8oB3PngRkw==

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# token = os.environ.get("INFLUXDB_TOKEN")

token = 'Zt2lpPOocc2PWMLR0uX4_UmUmgJ-s4UsqSgZpzBdSDsfE7MJRqMLvz7Ji7dUWRdvCP24vDweTWJN8oB3PngRkw=='
org = "organization"
url = "http://10.70.79.190:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="xuxing"


query_api = write_client.query_api()

query = """from(bucket: "xuxing")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="organization")

for table in tables:
  for record in table.records:
    print(record)