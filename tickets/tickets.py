import argparse
import stations
import urllib.request
import json
from prettytable import PrettyTable
import sys

query_url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'

def colored(color, text):
    table = {
        'red': '\033[91m',
        'green': '\033[92m',
        'nc': '\033[0m'
            }
    cl = table.get(color)
    no_color = table.get('nc')
    return ''.join([cl, text, no_color])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="query date,like 2016-10-09")
    parser.add_argument("-f", help="from")
    parser.add_argument("-t", help="to")
    args = parser.parse_args()

    stations = stations.stations
    query_url = query_url.format(args.d, stations[args.f], stations[args.t])
    trains = None
    with urllib.request.urlopen(query_url) as response:
        data = response.read().decode('utf-8')
        data = json.loads(data)
        trains = data.get("data").get("datas")
        #print(data.get("data"))

    #print(trains)
    if trains == None:
        sys.exit(1)

    # 显示车次、出发/到达站、 出发/到达时间、历时、一等坐、二等坐、软卧、硬卧、硬座
    header = 'train station time duration first second softsleep hardsleep hardsit'.split()
    pt = PrettyTable()
    pt._set_field_names(header)
    for row in trains:
        train = [
                # 车次
                row['station_train_code'],
                # 出发、到达站
                '\n'.join([colored('red', row['from_station_name']), colored('green', row['to_station_name'])]),
                # 出发、到达时间
                '\n'.join([colored('red', row['start_time']), colored('green', row['arrive_time'])]),
                # 历时
                row['lishi'],
                # 一等坐
                row['zy_num'],
                # 二等坐
                row['ze_num'],
                # 软卧
                row['rw_num'],
                # 软坐
                row['yw_num'],
                # 硬坐
                row['yz_num']
            ]

        pt.add_row(train)

    print(pt)

