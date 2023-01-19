#!/Users/linkunhui/anaconda3/bin/python3

import requests
import json
import sys
from time import strftime, localtime

KEY = "5a77cf8b06082b43cf52ce19f58143ec"
DRIVING = 'driving'
PUBLIC_TRANSPORT = 'public_transport'
NAME = 'name'
DISTANCE = 'distance'
LOCATION = 'location'


def address_to_location(address):
    """
    地址转经纬度
    """
    # TODO CACHE
    req = f'https://restapi.amap.com/v3/geocode/geo?city=上海市&address={address}&key={KEY}&output=json'
    location = json.loads(requests.get(req).text)['geocodes'][0]['location']
    return location


def req_metro_duration(start_loc, end_loc, time=None):
    """
    公共交通时间 / min
    """
    params = {"origin": start_loc
            , "destination": end_loc
            , "city": "上海"
            , "key": KEY
            , "time": time if time is not None else strftime('%H:%M', localtime())}
    req = f'https://restapi.amap.com/v3/direction/transit/integrated?{generate_param(params)}'
    info = json.loads(requests.get(req).text)
    return int(int(info['route']['transits'][0]['duration']) / 60)


def req_car_duration(start_loc, end_loc, time=None):
    """
    开车时间 / min
    """
    params = {"origin": start_loc
            , "destination": end_loc
            , "city": "上海"
            , "key": KEY
            , "time": time if time is not None else strftime('%H:%M', localtime())}
    req = f'https://restapi.amap.com/v3/direction/driving?{generate_param(params)}'
    info = json.loads(requests.get(req).text)
    return int(int(info['route']['paths'][0]['duration']) / 60)


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
    search_result = []
    for each in response['pois']:
        search_result.append({NAME: each['name'], DISTANCE: int(each['distance']), LOCATION: each['location']})
    return sorted(search_result, key=lambda x: x[DISTANCE])


def route_info(start_loc, end_loc):
    """
    通行时间
    """
    public = req_metro_duration(start_loc, end_loc)
    driving = req_car_duration(start_loc, end_loc)

    return {PUBLIC_TRANSPORT: public, DRIVING: driving}


def generate_param(argvs):
    kvs = []
    for k, v in argvs.items():
        kvs.append("%s=%s" % (k, v))
    return '&'.join(kvs)


def address():
    kv = {"阿里": "上海市浦东新区纳贤路800号"
        , "腾讯": "上海市徐汇区漕河泾新兴技术开发区虹梅路1801号"
        , "字节": "上海市闵行区宜山路1999号"
        , "蚂蚁": "浦东新区南泉北路447号"
        , "美团": "蒲松北路60号"
        , "拼多多": "娄山关路533号"
        , "b站": "杨浦区政立路485号"
        , "滴滴": "嘉定区高潮路318号"
        , "携程": "浦东新区金海路2505宝龙商场1号"
        , "阅文": "碧波路690号"
        , "哈啰": "闵行区秀文路898弄"
        , "百度": "浦东新区纳贤路701号"
        , "京东": "嘉定区叶城路1118号"
        , "网易": "青浦区诸光路1588弄"
        , "得物": "杨浦区大桥街道互联宝地c3号楼"
        , "唯品会": "浦东新区启帆路6288号"
        , "叮咚": "浦东新区创运路256号"
        , "小红书": "黄浦区马当路388号"
        , "米哈游": "徐汇区宜山路700号"
        , "莉莉丝": "徐汇区宜州路188号"
          }
    return kv


if __name__ == '__main__':
    start = '蟠龙路1366弄'
    company_map = address()
    start_loc = address_to_location(start)
    # for name, end in company_map.items():
    #     end_loc = address_to_location(end)
    #     info = route_info(start_loc, end_loc)
    #     print("%s->%s %s" % (start, name, info))

    for each in  search_around(start_loc, 2000, "地铁站"):
        print(each )
