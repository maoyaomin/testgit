# -*- coding:utf-8 -*-
# from importlib import reload

import requests
import time
from bs4 import BeautifulSoup
from echarts import Echart, Bar, Axis
# from qtpy.py3compat import cmp

TEMPERATURE_LIST = []
CITY_LIST = []
MIN_LIST = []


def get_temperature(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://www.weather.com.cn/textFC/db.shtml',
        'Host': 'www.weather.com.cn'
    }
    # headers操作的目的是为了模仿用鼠标在浏览器上查看天气网的数据操作，骗过网站反侦察机制，防止出现发爬虫机制
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # print(res.text)
    soup = BeautifulSoup(res.text, 'lxml')
    # 所有的城市都是放在属于某个省或者直辖市中的中的表格。
    # 真正有用的数据是从第3个tr开始的，表示的是当前这个表格的省份，或者直辖市的名字。
    # 其余有用的tr的第0个td，实际上就是表示了当前的这个城市的名字了。
    conMidtab = soup.find('div', class_='conMidtab')
    conMidtab2_list = conMidtab.find_all('div', 'conMidtab2')
    for x in conMidtab2_list:
        tr_list = x.find_all('tr')[2:]
        province = ''
        for index, tr in enumerate(tr_list):
            # 如果是第0个tr标签，那么省份名和城市名是放在一起的
            if index == 0:
                td_list = tr.find_all('td')
                province = td_list[0].text.replace('\n', '')
                city = td_list[1].text.replace('\n', '')
                min_temperature = td_list[4].text.replace('\n', '')
            else:
                td_list = tr.find_all('td')
                city = td_list[0].text.replace('\n', '')
                min_temperature = td_list[3].text.replace('\n', '')
            # print('%s|%s'% (province + city, min_temperature))
            # 如果是第0个tr标签，那么这个tr标签中只存放城市名
            TEMPERATURE_LIST.append({
                'city': province + city,
                'min': min_temperature
            })
            CITY_LIST.append(province + city)
            MIN_LIST.append(min_temperature)
    # print(TEMPERATURE_LIST)
    # print(TEMPERATURE_LIST)
    # province_tr = tr_list[2]
    # province_td = province_tr('td')
    # td_list = province_td[0]
    # province = td_list.text
    # print(province.replace('\n', ''))
    # '%|%'%(province+city,min_temprature)


# def dict2list(dic: dict):
#     ''' 将字典转化为列表 '''
#     keys = dic.keys()
#     vals = dic.values()
#     lst = [(key, val) for key, val in zip(keys, vals)]
#     return lst
def main():
    urls = [
        'http://www.weather.com.cn/textFC/hz.shtml']
    # 'http://www.weather.com.cn/textFC/hb.shtml',
    # 'http://www.weather.com.cn/textFC/db.shtml',
    # 'http://www.weather.com.cn/textFC/hd.shtml',
    # 'http://www.weather.com.cn/textFC/hn.shtml',
    # 'http://www.weather.com.cn/textFC/xb.shtml',
    # 'http://www.weather.com.cn/textFC/xn.shtml
    for url in urls:
        get_temperature(url)
        time.sleep(2)

    SORTED_TEMPERATURE_LIST = sorted(TEMPERATURE_LIST, key=lambda x: int(x["min"]), reverse=True)
    TOP20_TEMPERATURE_LIST = SORTED_TEMPERATURE_LIST[0:20]
    print(TOP20_TEMPERATURE_LIST)
    TOP20_CITY_LIST = []
    TOP20_MIN_LIST = []
    for city_min in TOP20_TEMPERATURE_LIST:
        TOP20_CITY_LIST.append(city_min['city'])
        TOP20_MIN_LIST.append(city_min['min'])
    # #获取
    # 排序问题等到后续解决
    echart = Echart(u'全国最高温度排名', u'知了课堂贡献')
    bar = Bar(u'最高温度', TOP20_MIN_LIST)
    axis = Axis('category', 'bottom', data=TOP20_CITY_LIST)
    echart.use(bar)
    echart.use(axis)
    echart.plot()


if __name__ == '__main__':
    main()

# 爬去到数据后接着就是进行数据分析，即数据的可视化