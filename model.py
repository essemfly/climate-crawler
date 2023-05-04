import csv
from typing import List


obsr_spots_csv_path = "/Users/Seokmin/Desktop/crop_navigator/raw_data/obsr_spot_sites.csv"


class ObsrSpot:
    def __init__(self, args):
        self.sido = args[0]
        self.name = args[1]
        self.code = args[2]
        self.lat = args[3]
        self.lng = args[4]
        self.alt = args[5]
        self.addr = args[6]
        self.record_start_at = args[7]


def get_obsr_spots():
    spots: List[ObsrSpot] = []
    with open(obsr_spots_csv_path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        next(reader)
        for row in reader:
            spots.append(ObsrSpot(row))
    return spots


class ClimateData:
    def __init__(self, item):
        self.obsr_Spot_Code = item.find("obsr_Spot_Code").text
        self.obsr_Spot_Nm = item.find("obsr_Spot_Nm").text
        self.date_Time = item.find("date_Time").text
        self.tmprt_50 = item.find("tmprt_50").text
        self.tmprt_50Top = item.find("tmprt_50Top").text
        self.tmprt_50Lwet = item.find("tmprt_50Lwet").text
        self.tmprt_150 = item.find("tmprt_150").text
        self.tmprt_150Top = item.find("tmprt_150Top").text
        self.tmprt_150Lwet = item.find("tmprt_150Lwet").text
        self.tmprt_400 = item.find("tmprt_400").text
        self.tmprt_400Top = item.find("tmprt_400Top").text
        self.tmprt_400Lwet = item.find("tmprt_400Lwet").text
        self.hd_50 = item.find("hd_50").text
        self.hd_150 = item.find("hd_150").text
        self.hd_400 = item.find("hd_400").text
        self.afp = item.find("afp").text  ## 강수량
        self.afv = item.find("afv").text  ## 증발량
        self.sunshn_Time = item.find("sunshn_Time").text  ## 일조시간
        self.solrad_Qy = item.find("solrad_Qy").text  ## 일사량 (MJ/m^2)
        self.dwcn_Time = item.find("dwcn_Time").text  ## 결로시간
        self.frfr_Tp = item.find("frfr_Tp").text  ## 초상온도
        self.udgr_Tp_10 = item.find("udgr_Tp_10").text  ## 지중온도10cm
        self.udgr_Tp_5 = item.find("udgr_Tp_5").text  ##지중온도5cm
        self.udgr_Tp_20 = item.find("udgr_Tp_20").text  ##지중온도20cm
        self.soil_Mitr_10 = item.find("soil_Mitr_10").text  ## 토양수분10cm(%)
        self.soil_Mitr_30 = item.find("soil_Mitr_30").text  ## 토양수분30cm(%)

    def get_spot_info(self):
        obsr_spots = get_obsr_spots()
        matching_spots = [
            spot for spot in obsr_spots if spot.code == self.obsr_Spot_Code
        ]
        if len(matching_spots) == 0:
            Exception("No matching spot found")
        if len(matching_spots) > 1:
            Exception("matching spot is not unique")
        return matching_spots[0]
