import requests
import xmltodict
import json
from datetime import datetime

# 실시간 get
date = datetime.today()
today = date.strftime("%Y%m%d")

json_item = []
clean_datum = []


def api_data(request):

    """국립 수산과학원 실시간 정보"""

    service_key = "mIbNkLmoozdnC%2F2o%2BYbyUKgZGbqJaNXk%2FIuKx2aFRuHqJ4hSmn3tBlLU%2FfcIG3BbjEACC114ejlHzJpeI%2FpXPA%3D%3D"
    service_url = "http://apis.data.go.kr/1520635/OceanMensurationService"
    operation = "getOceanMesurationListrisa"

    # 특정 관측소
    # observatory =

    # 해양
    ocean = ["001", "002", "003"]

    # 시작
    start_time = today

    # 실시간
    end_time = today

    for i in ocean:
        data_request = requests.get(
            f"{service_url}/{operation}?ServiceKey={service_key}&GRU_NAM={i}&SDATE={start_time}&EDATE={end_time}&numOfRows=100"
        )
        # 데이터 포멧 xml에서 json으로 변환
        data = xmltodict.parse(data_request.text)
        json_data = json.dumps(data)
        json_api = json.loads(json_data)
        json_response = json_api.get("response").get("body").get("items")
        json_item.extend(json_response.get("item"))

    print("API Data...")
    return json_item


def gps_get(request):

    """GPS 좌표를 가져오기 위한 세부사항 get"""

    service_key = "mIbNkLmoozdnC%2F2o%2BYbyUKgZGbqJaNXk%2FIuKx2aFRuHqJ4hSmn3tBlLU%2FfcIG3BbjEACC114ejlHzJpeI%2FpXPA%3D%3D"
    service_url = "http://apis.data.go.kr/1520635/OceanMensurationService"
    operation = "getOceanMesurationDetailrisa"

    data_request = requests.get(
        f"{service_url}/{operation}?ServiceKey={service_key}&numOfRows=1000"
    )

    data = xmltodict.parse(data_request.text)
    json_data = json.dumps(data)
    json_api = json.loads(json_data)
    json_response = json_api.get("response").get("body").get("items")
    json_detail_item = json_response.get("item")

    print("GPS Get...")
    return json_detail_item


def clean_data(request):

    """실시간 정보에 GPS 더하기, 필요 데이터 get, 필요없는 데이터 정리"""

    datum = api_data(request)
    detail_datum = gps_get(request)

    for i in datum:
        for j in detail_datum:
            if i["staCde"] == j["staCde"]:
                i["lat"] = j["lat"]
                i["lon"] = j["lon"]
                clean_data = {
                    "ocean": i.get("gruNam"),
                    "lat": i.get("lat"),
                    "lng": i.get("lon"),
                    "temperature": i.get("wtrTmp_1"),
                    "oxygen": i.get("dox_1"),
                    "salt": i.get("cdt_1"),
                    "measurement_time": i.get("obsDtm"),
                }
                clean_datum.append(clean_data)

    print("Data Clean...")
    return clean_datum


# 2021/09/25일 각 데이터들의 lat,lng의 중복값을 정리하여 고유 넘버 붙여주자
