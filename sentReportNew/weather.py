import json, sys, requests
from wxpy import *


class weather:

    def __init__(self):
        return

    def getwehther(self,cityname):
        outputstr = ''
        # 输入地点
        print('输出地址：' + cityname)
        weatherPlace = cityname
        if weatherPlace == 'E' or weatherPlace == 'e':
            sys.exit(0)  # 关闭程序
        # 下载天气JSON
        weatherJsonUrl = "http://wthrcdn.etouch.cn/weather_mini?city=%s" % (
            weatherPlace)
        response = requests.get(weatherJsonUrl)
        try:
            response.raise_for_status()
        except BaseException:
            print("网址请求出错")
            # 将json文件格式导入成python的格式
        weatherData = json.loads(response.text)
        # 以好看的形式打印字典与列表表格
        # import pprint
        # pprint.pprint(weatherData)
        w = weatherData['data']
        outputstr += ("\t\r" + w['city'])
        # 日期
        date_a = []
        # 最高温与最低温
        highTemp = []
        lowTemp = []
        # 天气
        weather = []
        # 进行五天的天气遍历
        for i in range(len(w['forecast'])):
            date_a.append(w['forecast'][i]['date'])
            highTemp.append(w['forecast'][i]['high'])
            lowTemp.append(w['forecast'][i]['low'])
            weather.append(w['forecast'][i]['type'])
            # 输出
            outputstr += ("\t\r日期：" + date_a[i])
            outputstr += ("\t\r天气：" + weather[i])
            outputstr += ("\t\r温度：最" + lowTemp[i] + '℃~最' + highTemp[i] + '℃')
            outputstr += ("\t\r")
        outputstr += ("\n\r今日着装：" + w['ganmao'])
        outputstr += ("\t\r当前温度：" + w['wendu'] + "℃")
        print("完结获取")
        print(outputstr)
        return outputstr
