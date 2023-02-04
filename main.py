import pandas as pd
from gaode_api import *
from utils import *


def cal_location(address):
    """
    计算经纬度
    """
    address = address.replace(' ', '').split('、')[0] # 格式化地址
    return address_to_location(address)


def around_info(location, radius, query):
    """
    搜周边，返回通行时间
    :param location: 经纬坐标
    :param radius: 范围，单位km
    :param query: 查询词
    :return:
    """
    format_info = []
    results = search_around(location, radius * 1000, query)
    format_info.append(f'{radius}km内{query}{len(results)}个')
    for each in results[:TOPN]:
        if each[DISTANCE] < THRESHOLD:
            format_info.append(f'{each[NAME]}:步行{each[WALKING]}min,骑行{each[BICYCLING]}min')
        else:
            format_info.append(f'{each[NAME]}:开车{each[DRIVING]}min,公交{each[PUBLIC_TRANSPORT]}min')
    return ';'.join(format_info)


def commuting_time(location, *companies):
    """
    计算到公司的通勤时间
    """
    result_text = []
    for name in companies:
        if name in COMPANY_ADDRESS:
            destination_loc = address_to_location(COMPANY_ADDRESS[name])
            info = req_durations(location, destination_loc)
            result_text.append(f'{name}:开车{info[DRIVING]}min,公交{info[PUBLIC_TRANSPORT]}min')
        else:
            ERROR(f'please add full address of {name} to COMPANY_ADDRESS in utils.py')
    return ';'.join(result_text)


def batch_process(house_info_path):
    """
    批量处理多个楼盘的信息。
    """
    df = pd.read_excel(house_info_path)
    if PROJECT_ADDRESS not in df:
        ERROR(f'【{PROJECT_ADDRESS}】是必须字段')
    df[PROJECT_LOCATION] = df[PROJECT_ADDRESS].map(cal_location)

    df['地铁站'] = df[PROJECT_LOCATION].apply(around_info, args=(2, '地铁站'))
    df['商场'] = df[PROJECT_LOCATION].apply(around_info, args=(3, '商场'))
    df['医院'] = df[PROJECT_LOCATION].apply(around_info, args=(4, '医院'))

    df['通勤'] = df[PROJECT_LOCATION].apply(commuting_time, args=TARGET_COMPANY)
    df.to_excel(house_info_path)


def process(address):
    """
    处理单个楼盘的信息
    """
    print(address)
    localtion = address_to_location(address)
    print(f'通勤时间：{commuting_time(localtion, *TARGET_COMPANY)}')
    print(around_info(localtion, 2, '地铁站'))
    print(around_info(localtion, 3, '商场'))


if __name__ == '__main__':
    process("虹桥公馆3期")
    batch_process('2022-8.xlsx')


