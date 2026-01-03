import requests
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from dotenv import load_dotenv
import os 

load_dotenv()

DEBUG=False
HWIZ_BASEURL = os.getenv("HWIZ_BASEURL")
HWIZ_STATUS_ENDPOINT = "/api"
HWIZ_ELEC_METRICS_ENDPOINT = "/api/v1/data"
REQUEST_TIMEOUT = 10

HWIZ_COMMS_HEADER = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Connection": "close"
    }

INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
RUN_INTERVAL = 60

client = influxdb_client.InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)
session = requests.Session()

if DEBUG:
    print(f"[Debug] Debug is ON")

while True:
    print(f"[Info] Gathering info from {HWIZ_BASEURL}")

    try:
        hwiz_node_status_req = session.get(url=HWIZ_BASEURL+HWIZ_STATUS_ENDPOINT, headers=HWIZ_COMMS_HEADER, timeout=REQUEST_TIMEOUT)
        if hwiz_node_status_req.status_code == 200:
            hwiz_node_status_data = hwiz_node_status_req.json()
            hwiz_node_product_name = hwiz_node_status_data.get('product_name', 'Unknown')
            hwiz_node_product_type = hwiz_node_status_data.get('product_type', 'Unknown')
            hwiz_node_serial  = hwiz_node_status_data.get('serial', 'Unknown')
            hwiz_node_fver    = hwiz_node_status_data.get('firmware_version', 'Unknown')
            hwiz_node_apiver  = hwiz_node_status_data.get('api_version', 'Unknown')
            if DEBUG:
                print(hwiz_node_status_data)
                print(f"hwiz_node_product_name:{hwiz_node_product_name}\nhwiz_node_product_type:{hwiz_node_product_type}\nhwiz_node_serial:{hwiz_node_serial}\nhwiz_node_fver:{hwiz_node_fver}\nhwiz_node_apiver:{hwiz_node_apiver}")
        else:
            print(f"[Critical] cannot get data from node at {HWIZ_BASEURL}{HWIZ_STATUS_ENDPOINT} - {hwiz_node_status_req.status_code}")

        try:
            hwiz_last_elec_metrics_req = session.get(url=HWIZ_BASEURL+HWIZ_ELEC_METRICS_ENDPOINT, headers=HWIZ_COMMS_HEADER, timeout=REQUEST_TIMEOUT)
            if hwiz_last_elec_metrics_req.status_code == 200:
                hwiz_last_elec_metrics_data = hwiz_last_elec_metrics_req.json()
                hwiz_node_wifi_ssid = hwiz_last_elec_metrics_data.get('wifi_ssid', 'Unknown')
                hwiz_node_wifi_strength = hwiz_last_elec_metrics_data.get('wifi_strength', 'Unknown')
                hwiz_node_meter_model = hwiz_last_elec_metrics_data.get('meter_model', 'Unknown')
                hwiz_node_metric_active_tariff = hwiz_last_elec_metrics_data.get('active_tariff', 'Unknown')
                hwiz_node_metric_total_power_import_kwh = hwiz_last_elec_metrics_data.get('total_power_import_kwh', 'Unknown')
                hwiz_node_metric_total_power_import_t1_kwh = hwiz_last_elec_metrics_data.get('total_power_import_t1_kwh', 'Unknown')
                hwiz_node_metric_total_power_import_t2_kwh = hwiz_last_elec_metrics_data.get('total_power_import_t2_kwh', 'Unknown')
                hwiz_node_metric_total_power_export_kwh = hwiz_last_elec_metrics_data.get('total_power_export_kwh', 'Unknown')
                hwiz_node_metric_total_power_export_t1_kwh = hwiz_last_elec_metrics_data.get('total_power_export_t1_kwh', 'Unknown')
                hwiz_node_metric_total_power_export_t2_kwh = hwiz_last_elec_metrics_data.get('total_power_export_t2_kwh', 'Unknown')
                hwiz_node_metric_active_power_w = hwiz_last_elec_metrics_data.get('active_power_w', 'Unknown')
                
                # influx_output_data = f"p1_meter, api_version={hwiz_node_apiver}, firmware_version={hwiz_node_fver}, meter_model={hwiz_node_meter_model}, product_name={hwiz_node_product_name}, product_type={hwiz_node_product_type}, serial={hwiz_node_serial} active_power={hwiz_node_metric_active_power_w}i, active_tariff={hwiz_node_metric_active_tariff}, ssid_name={hwiz_node_wifi_ssid}, ssid_strength={hwiz_node_wifi_strength}i, total_power_export_kwh={hwiz_node_metric_total_power_export_kwh}i, total_power_export_t1_kwh={hwiz_node_metric_total_power_export_t1_kwh}i, total_power_export_t2_kwh={hwiz_node_metric_total_power_export_t2_kwh}i, total_power_import_kwh={hwiz_node_metric_total_power_import_kwh}i, total_power_import_t1_kwh={hwiz_node_metric_total_power_import_t1_kwh}i, total_power_import_t2_kwh={hwiz_node_metric_total_power_import_t2_kwh}i"
                point_data = influxdb_client.Point("p1-meter").tag("api_version", hwiz_node_apiver).tag("firmware_version", hwiz_node_fver).tag("meter_model", hwiz_node_meter_model).tag("product_name", hwiz_node_product_name).tag("product_type", hwiz_node_product_type).tag("serial", hwiz_node_serial).field("active_power", hwiz_node_metric_active_power_w).field("active_tariff", hwiz_node_metric_active_tariff).field("ssid_name", hwiz_node_wifi_ssid).field("ssid_strength", hwiz_node_wifi_strength).field("total_power_export_kwh", hwiz_node_metric_total_power_export_kwh).field("total_power_export_t1_kwh", hwiz_node_metric_total_power_export_t1_kwh).field("total_power_export_t2_kwh", hwiz_node_metric_total_power_export_t2_kwh).field("total_power_import_kwh", hwiz_node_metric_total_power_import_kwh).field("total_power_import_t1_kwh", hwiz_node_metric_total_power_import_t1_kwh).field("total_power_import_t2_kwh", hwiz_node_metric_total_power_import_t2_kwh)

                try:
                    print(f"[Info] Writing point to Influxdbv2")
                    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point_data)
                except Exception as e:
                    print("[Error] Failed to write point to Influxdbv2")

                if DEBUG:
                    print(hwiz_last_elec_metrics_data)
                    print(f'''
                        hwiz_last_elec_metrics_data: {hwiz_last_elec_metrics_data}
                            hwiz_node_wifi_ssid: {hwiz_node_wifi_ssid}
                            hwiz_node_wifi_strength: {hwiz_node_wifi_strength}
                            hwiz_node_meter_model: {hwiz_node_meter_model}
                            hwiz_node_metric_active_tariff: {hwiz_node_metric_active_tariff}
                            hwiz_node_metric_total_power_import_kwh: {hwiz_node_metric_total_power_import_kwh}
                            hwiz_node_metric_total_power_import_t1_kwh: {hwiz_node_metric_total_power_import_t1_kwh}
                            hwiz_node_metric_total_power_import_t2_kwh: {hwiz_node_metric_total_power_import_t2_kwh}
                            hwiz_node_metric_total_power_export_kwh: {hwiz_node_metric_total_power_export_kwh}
                            hwiz_node_metric_total_power_export_t1_kwh: {hwiz_node_metric_total_power_export_t1_kwh}
                            hwiz_node_metric_total_power_export_t2_kwh: {hwiz_node_metric_total_power_export_t2_kwh}
                            hwiz_node_metric_active_power_w: {hwiz_node_metric_active_power_w}
                        ''')

            else:
                print(f"[Warning] cannot get last electricity metrics from {HWIZ_BASEURL}{HWIZ_ELEC_METRICS_ENDPOINT} - {hwiz_node_status_req.status_code}")
        except Exception as e:
            print(f"[Critical] failed to get last electricity metrics from {HWIZ_BASEURL}{HWIZ_ELEC_METRICS_ENDPOINT} - {e}")
    except Exception as e:
        print(f"[Critical] failed node status request to: {HWIZ_BASEURL}{HWIZ_STATUS_ENDPOINT} - {e}")       

    print(f"[Info] Sleeping {RUN_INTERVAL} before next run.")
    time.sleep(RUN_INTERVAL)
