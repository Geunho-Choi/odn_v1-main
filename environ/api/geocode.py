import requests
from . import data_api


client_id = "77cm9f6ne5"
client_pw = "w480VLY6nbuefXbG58iQdc6WOiU24l39pnotzNDm"

process_datum = []


def geo_reverse(request):

    """정리한 공공데이터의 gps와 geocoding으로 주소 변환해 데이터 완성"""
    # 가져온 공공데이터 변수로 가져옴
    process_data = data_api.clean_data(request)

    # 공공데이터 gps로 주소를 찾음
    for i in process_data:
        latlng = i["lng"] + "," + i["lat"]
        response = requests.get(
            f"https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?X-NCP-APIGW-API-KEY-ID={client_id}&X-NCP-APIGW-API-KEY={client_pw}&coords={latlng}&output=json"
        )
        if response.status_code == 200:
            try:
                get_json = response.json()
                get_adress = get_json.get("results")[0].get("region")
            except IndexError:
                continue
            try:
                area1 = get_adress.get("area1").get("name")
                area2 = get_adress.get("area2").get("name")
                area3 = get_adress.get("area3").get("name")
            except IndexError:
                continue
            try:
                area4 = get_adress.get("area4").get("name")
            except IndexError:
                area4 = None

            # 찾아온 주소를 딕셔너리에 추가하여 데이터 완성
            i.update(
                area1=area1,
                area2=area2,
                area3=area3,
                area4=area4,
            )
            process_datum.append(i)
    print("Geocoding Reverse...")
    return process_datum
