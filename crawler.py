import requests
from xml.etree import ElementTree
from datetime import datetime
import csv
from typing import List
from model import ClimateData, ObsrSpot, get_obsr_spots
from utils import get_365_day_interval

data_output_path = "raw_data/writer/"


def runner(start_date_str):
    records: List[ClimateData] = []
    obsr_spots: List[ObsrSpot] = get_obsr_spots()
    for spot in obsr_spots:
        records += get_obsr_year_data(spot, start_date_str)
    write_csv(records, start_date_str)


# 365일간의 데이터를 가져온다.
def get_obsr_year_data(spot: ObsrSpot, date: str):
    start_date, end_date = get_365_day_interval(date)
    records = get_half_week_data(spot.code, start_date, end_date)
    return records


def write_csv(records: List[ClimateData], date: str):
    attributes = list(records[0].__dict__.keys())
    with open(data_output_path + date + ".csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=attributes)
        writer.writeheader()
        for record in records:
            writer.writerow(vars(record))


# api 제한사항으로 page_size <= 100, begin_date ~ end_date <= 365
def get_half_week_data(obsr_code, begin_date, end_date, page_no=1, page_size=100):
    general_endpoint = (
        "http://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/InsttWeather"
    )
    encoding_auth_key = "gqOFkbCIrB5kn5SVgm7ar7w7xh%2B5cOyzh02t%2BtP7WvHqaErq6Pt5ke52sCBNuVSYVOUCabVBKrxgAZGoIg3taQ%3D%3D"
    decoding_auth_key = "gqOFkbCIrB5kn5SVgm7ar7w7xh+5cOyzh02t+tP7WvHqaErq6Pt5ke52sCBNuVSYVOUCabVBKrxgAZGoIg3taQ=="
    half_week_data_endpoint = general_endpoint + "/getWeatherTermBsunList"

    query_params = {
        "serviceKey": decoding_auth_key,
        "Page_No": str(page_no),
        "Page_Size": str(page_size),
        "begin_Date": begin_date.strftime("%Y-%m-%d"),
        "end_Date": end_date.strftime("%Y-%m-%d"),
        "obsr_Spot_Code": obsr_code,
    }
    response = requests.get(half_week_data_endpoint, params=query_params)
    return parse_obsr_xml(response)


def parse_obsr_xml(xml_resp):
    climate_data: List[ClimateData] = []
    root = ElementTree.fromstring(xml_resp.content)
    for item in root.findall(".//item"):
        climate_data.append(ClimateData(item))

    return climate_data
