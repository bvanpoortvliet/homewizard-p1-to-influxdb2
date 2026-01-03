# HomeWizard P1 to InfluxDB2

Collects electricity metrics from HomeWizard P1 meter's local API and writes them to InfluxDB2.

## Requirements

**InfluxDB2:**
- InfluxDB2 instance (local or cloud)
- Bucket for metrics storage
- Write token with bucket access

**Python Dependencies:**
- Python 3.x
- python-dotenv
- requests
- influxdb-client

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bvanpoortvliet/homewizard-p1-to-influxdb2.git
cd homewizard-p1-to-influxdb2
```

2. Set up virtual environment:
```bash
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Configure environment variables by creating `.env` in project root:
```env
HWIZ_BASEURL=http://<homewizard-ip>
INFLUXDB_BUCKET=<your-bucket-name>
INFLUXDB_ORG=<your-org-name>
INFLUXDB_TOKEN=<your-write-token>
INFLUXDB_URL=<influxdb2-instance-url>
```

## Usage

With virtualenv activated:
```bash
python3 hwiz-to-influx.py
```

The script runs continuously, by default collecting metrics every 60 seconds. This can be changed by editing the *RUN_INTERVAL* variable.

## Collected Metrics

- Active power consumption (W)
- Total import/export energy (kWh)
- Tariff-specific import/export (T1/T2)
- Active tariff
- Device info (WiFi strength, meter model, etc.)

## References

- [HomeWizard API Documentation](https://api-documentation.homewizard.com/docs/v1/measurement)
- [InfluxDB Line Protocol](https://docs.influxdata.com/influxdb/cloud/write-data/developer-tools/line-protocol/)
- [InfluxDB Python Client](https://docs.influxdata.com/influxdb/v2/api-guide/client-libraries/python/)

## TODO
- Make daemonized with input flags like: *-i --interval, -d --debug* ..
