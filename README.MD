## TIG

- Grafana v10.2.2
- Influxdb v2.7.4
- telegraf v1.29.0

## Pre-Installation Requirements

- Docker Engine, Docker Compose
- Git

## Usage

1. Clone to Your server

> git clone https://github.com/xuxing3/tig.git

2. Bring up docker container by docker-compose

> docker-compose build; docker-compose up -d

3. Access to Grafana and configure database

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

Database:xuxing
User:admin
Password:cisco!123
HTTP Method:GET

(配置根据 Docker compose 文件填写， 你可以更改为自己的设定)

"Save & Test"

4.Configure your router (e.g. XR)

protocol 设置为 tcp，测试过 grpc 不好用。

```
telemetry model-driven
 destination-group xuxing
  address-family ipv4 10.70.79.190 port 57000
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

5. 注意修改 telegraf.conf 中地址为自己的服务器地址

```
[[outputs.influxdb_v2]]
  urls = ["http://10.70.79.190:8086"]
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

## Reference

[InfluxDB2.0+Grafana+Telegraf の構築](https://qiita.com/sammrai/items/0c329ac7aa8b100b66a8)
[influxDB + Grafana に入門する](https://qiita.com/chroju/items/355f3c6da9f8c4867ba5)
[InfluxDB+Grafana 構築 on docker](https://qiita.com/7280ayubihs/items/ace07b14d934dca4744c)

## Influxdb + Python Write and Query

Add two example file to help you Write and Query the data from Influxdb.
