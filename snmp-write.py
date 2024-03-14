from pysnmp.hlapi import *
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def get_cpu_utilization(snmp_community, snmp_host, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(snmp_community),
               UdpTransportTarget((snmp_host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                             errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            return varBind[1]
        
snmp_community = 'cisco'
snmp_host = '10.124.50.20'
oid = '1.3.6.1.4.1.9.9.109.1.1.1.1.7.33'




token = 'my-super-secret-auth-token'
org = "organization"
url = "http://10.70.79.190:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="xuxing"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
while True:
  try:
      
    cpu_utilization = get_cpu_utilization(snmp_community, snmp_host, oid)
    print(cpu_utilization)
    point = (
        Point("cpu_measurement")
        .tag("host", "10.125.50.20")
        .field("cpu_utilization", float(cpu_utilization))
    )
    write_api.write(bucket=bucket, org="organization", record=point)
  except Exception as e:
    print(f"An error occurred: {e}")

  time.sleep(60) 
