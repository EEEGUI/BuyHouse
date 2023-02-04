import requests
import json
import sys
from time import strftime, localtime
from utils import *


def address_to_location(address):
    """
    地址转经纬度坐标
    """
    # TODO CACHE
    req = f'https://restapi.amap.com/v3/geocode/geo?city=上海市&address={address}&key={KEY}&output=json'
    info = json.loads(requests.get(req).text)
    if info['status'] == '1':
        location = info['geocodes'][0]['location']
    else:
        ERROR(f"request location failed, address:{address}. return default location: 0,0.")
        location = '0,0'
    return location


def req_public_transport_duration(origin_loc, destination_loc, time=None):
    """
    公共交通时间 / min
    """
    params = {"origin": origin_loc
            , "destination": destination_loc
            , "city": "上海"
            , "key": KEY
            , "time": time if time is not None else strftime('%H:%M', localtime())}
    req = f'https://restapi.amap.com/v3/direction/transit/integrated?{generate_param(params)}'
    info = json.loads(requests.get(req).text)
    if len(info['route']['transits']) > 0:
        return int(int(info['route']['transits'][0]['duration']) / 60)
    else:
        return 9999


def req_driving_duration(origin_loc, destination_loc, time=None):
    """
    开车时间 / min
    """
    params = {"origin": origin_loc
            , "destination": destination_loc
            , "city": "上海"
            , "key": KEY
            , "time": time if time is not None else strftime('%H:%M', localtime())}
    req = f'https://restapi.amap.com/v3/direction/driving?{generate_param(params)}'
    info = json.loads(requests.get(req).text)
    return int(int(info['route']['paths'][0]['duration']) / 60)


def req_walking_duration(origin_loc, destination_loc):
    """
    步行时间 / min
    """
    params = {"origin": origin_loc
            , "destination": destination_loc
            , "key": KEY}
    req = f'https://restapi.amap.com/v3/direction/walking?{generate_param(params)}'
    info = json.loads(requests.get(req).text)
    # print(info)
    return int(int(info['route']['paths'][0]['duration']) / 60)


def req_bicycling_duration(origin_loc, destination_loc):
    """
    骑自行车时间 / min
    """
    params = {"origin": origin_loc
            , "destination": destination_loc
            , "key": KEY}
    req = f'https://restapi.amap.com/v4/direction/bicycling?{generate_param(params)}'
    info = json.loads(requests.get(req).text)
    return int(int(info['data']['paths'][0]['duration']) / 60)


def req_durations(origin_loc, destination_loc):
    """
    通行时间 / min
    """
    public = req_public_transport_duration(origin_loc, destination_loc)
    driving = req_driving_duration(origin_loc, destination_loc)
    walking = req_walking_duration(origin_loc, destination_loc)
    bicycling = req_bicycling_duration(origin_loc, destination_loc)

    return {PUBLIC_TRANSPORT: public, DRIVING: driving, WALKING: walking, BICYCLING: bicycling}


def search_around(location, radius, keywords):
    """
    搜周边
    """
    params = {"location": location
            , "radius": radius
            , "key": KEY
            , "keywords": keywords
            , "offset": 100
            , "page": 1
            , "extensions": "all"}
    req = f'https://restapi.amap.com/v3/place/around?{generate_param(params)}'
    response = json.loads(requests.get(req).text)
    search_results = []
    for each in response['pois']:
        target = {NAME: each['name'], DISTANCE: int(each['distance']), LOCATION: each['location']}
        durations = req_durations(location, target[LOCATION])
        target.update(durations)
        search_results.append(target)
    return sorted(search_results, key=lambda x: x[DISTANCE])


def generate_param(argvs):
    kvs = []
    for k, v in argvs.items():
        kvs.append("%s=%s" % (k, v))
    return '&'.join(kvs)


if __name__ == '__main__':
    start = '沪青平公路1638弄'
    origin_loc = address_to_location(start)
    for each in search_around(origin_loc, 2000, "地铁站"):
        print(each)