import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# token = os.environ.get("INFLUXDB_TOKEN")

token = 'my-super-secret-auth-token'
org = "organization"
url = "http://x.x.x.x:8086"

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