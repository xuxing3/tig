import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# token = os.environ.get("INFLUXDB_TOKEN")

token = 'my-super-secret-auth-token'
org = "organization"
url = "http://x.x.x.x:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="xuxing"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="organization", record=point)
  time.sleep(1) 