'''
curl 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8966' -H 'Accept-Encoding: gzip, deflate, sdch, br' -H 'Accept-Language: en-US,en;q=0.8,zh;q=0.6' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36' -H 'Accept: */*' -H 'Referer: https://kyfw.12306.cn/otn/lcxxcx/init' -H 'Cookie: JSESSIONID=0A01D94CC468256031C0F9B5B4E4B9245F3FB6D2D1; __NRF=39ACF85CE95AF46846CF1794FB876FA5; BIGipServerotn=1289289994.50210.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2016-09-12; _jc_save_wfdc_flag=dc' -H 'Connection: keep-alive' -H 'If-Modified-Since: Sun, 11 Sep 2016 16:30:40 GMT' -H 'Cache-Control: max-age=0' --compressed --insecure

python3 query_stations.py > stations.py
'''
import urllib.request
import re
import pprint
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8966'
station_re = re.compile(r'([A-Z]+)\|([a-z]+)')
stations = {}
with urllib.request.urlopen(url) as response:
    data = response.read().decode("utf-8")
    stations = station_re.findall(data)
    stations = dict(stations) # {}
    stations = dict(zip(stations.values(), stations.keys()))

#pprint.pprint(stations, indent=4)
pprint.pprint(stations)

