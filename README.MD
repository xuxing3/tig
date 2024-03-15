## TIG

This project is based on the following version.

If you have problems using other versions, please try to modify the docker images version in the docker-compose file.

- Grafana v10.2.2
- Influxdb v2.7.4
- telegraf v1.29.0

## Pre-Installation Requirements

- Docker Engine, Docker Compose
- Git

## Usage

1. Clone to Your server

> git clone https://github.com/xuxing3/tig.git

2. Pay attention to modify the address in telegraf.conf to your own server address

```
[[outputs.influxdb_v2]]
  urls = ["http://x.x.x.x:8086"]
  token = "my-super-secret-auth-token"
  organization = "organization"
  bucket = "xuxing"

# [[outputs.file]]
#   files = ["stdout"]
#   data_format = "influx"

[[inputs.cisco_telemetry_mdt]]
 ## Telemetry transport can be "tcp" or "grpc".  TLS is only supported when
 ## using the grpc transport.
 transport = "tcp"

 ## Address and port to host telemetry listener
 service_address = ":57000"

 ## Grpc Maximum Message Size, default is 4MB, increase the size.
 max_msg_size = 4000000

```

3. Bring up docker container by docker-compose

> docker-compose build; docker-compose up -d

4. Access to Grafana and configure database

Access to Grafana GUI

http://(your-server-ip):3000

Initial username/password = admin/admin

Add your first data source > Add data source > Choose "InfluxDB"

URL: http://(your-server-ip):8086
Basic auth:

- User: admin
- Password: cisco!123

Custom HTTP Headers:

- Header:Authorization
- Value:"Token my-super-secret-auth-token" (无引号，注意有空格)

- Database:xuxing
- User:admin
- Password:cisco!123
- HTTP Method:GET

(The configuration is filled in according to the Docker compose file, you can change it to your own settings)

"Save & Test"

5.Configure your router (e.g. XR)

The protocol is set to tcp, and grpc is not easy to use after testing.

```
telemetry model-driven
 destination-group xuxing
  address-family ipv4 x.x.x.x port 57000
   encoding self-describing-gpb
   protocol tcp
  !
 !
 sensor-group SYSTEM-CPU-MEMORY-COUNTERS
  sensor-path Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization
 !
 subscription TIG
  sensor-group-id SYSTEM-CPU-MEMORY-COUNTERS sample-interval 10000
  destination-id xuxing
 !
!
```

## Reference

[InfluxDB2.0+Grafana+Telegraf の構築](https://qiita.com/sammrai/items/0c329ac7aa8b100b66a8)

[influxDB + Grafana に入門する](https://qiita.com/chroju/items/355f3c6da9f8c4867ba5)

[InfluxDB+Grafana 構築 on docker](https://qiita.com/7280ayubihs/items/ace07b14d934dca4744c)

## Influxdb + Python Write and Query

Add two example file to help you Write and Query the data from Influxdb.
