from django.shortcuts import render
from environ.models import Environ
from environ.api import geocode


# Create your views here.

# 2021/09/25 좌표값과 행정구역 / 측정값과 측정시간 이렇게 분리하여 프론트엔드로 보내주자.
def environ_data(request):
    # 이 함수는 좌표값과 행정구역으로 변경할 거임
    coordnate = []
    environs = Environ.objects.values().order_by("-measurement_time")
    env_dist = environs.values("lat", "lng").distinct()
    for i in env_dist:
        for j in environs:
            if i["lat"] == j["lat"] and i["lng"] == j["lng"]:
                environ = {
                    "ocean": j["ocean"],
                    "lat": j["lat"],
                    "lng": j["lng"],
                    "area1": j["area1"],
                    "area2": j["area2"],
                    "area3": j["area3"],
                    "area4": j["area4"],
                    "measurement_time": str(j["measurement_time"]),
                    "temperature": j["temperature"],
                }
                coordnate.append(environ)
                break
        continue
    print(coordnate)
    return render(request, "environ/environ_list.html", {"coordinate": coordnate})


"""
    "temperature": str(i.temperature),
    "oxygen": str(i.oxygen),
    "hydrogen": str(i.hydrogen),
    "salt": str(i.salt),
    "turbidity": str(i.turbidity),
    "measurement_time": str(i.measurement_time),
"""


def api_view(request):

    datum = geocode.geo_reverse(request)
    for i in datum:
        ocean = i.get("ocean")
        lat = i.get("lat")
        lng = i.get("lng")
        area1 = i.get("area1")
        area2 = i.get("area2")
        area3 = i.get("area3")
        area4 = i.get("area4")
        measurement_time = i.get("measurement_time")
        temperature = i.get("temperature")
        oxygen = i.get("oxygen")
        hydrogen = i.get("hydrogen")
        salt = i.get("salt")
        turbidity = i.get("turbidity")
        if temperature is None:
            continue
        if oxygen is None:
            oxygen = 0
        if hydrogen is None:
            hydrogen = 0
        if salt is None:
            salt = 0
        if turbidity is None:
            turbidity = 0

        if Environ.objects.filter(lat=lat, lng=lng, measurement_time=measurement_time):
            continue

        else:
            data = Environ.objects.create(
                ocean=ocean,
                lat=lat,
                lng=lng,
                area1=area1,
                area2=area2,
                area3=area3,
                area4=area4,
                temperature=temperature,
                oxygen=oxygen,
                hydrogen=hydrogen,
                salt=salt,
                turbidity=turbidity,
                measurement_time=measurement_time,
            )
            data.save()
