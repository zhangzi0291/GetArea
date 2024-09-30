import requests
import time
from requests_html import HTMLSession

baseurl = 'https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/'


def retryFunction(obj):
    if 'num' not in obj.keys():
        obj['num'] = 0
    obj['num'] = obj['num'] + 1
    if obj['num'] < 5:
        getList(obj['url'], obj['trclass'])
    else:
        return


def getList(url, trclass):
    list = []
    retry = {'url': url, 'trclass': trclass}
    try:
        response = session.get(url)
        response.encoding = 'GBK'
        list = response.html.find(trclass)
        time.sleep(1)
    except Exception as e:
        retryFunction(retry)
    return list


def getNameAndUrl(ele):
    if len(ele.find("td")) == 2:
        if (len(ele.find('td:nth-child(1)>a')) > 0):
            return ele.find('td:nth-child(2)>a')[0].text, ele.find('td:nth-child(1)>a')[0].text, None
        else:
            return ele.find('td:nth-child(2)')[0].text, ele.find('td:nth-child(1)')[0].text, None
    else:
        if (len(ele.find('td:nth-child(1)>a')) > 0):
            return ele.find('td:nth-child(3)>a')[0].text, ele.find('td:nth-child(1)>a')[0].text, \
            ele.find('td:nth-child(2)>a')[0].text
        else:
            return ele.find('td:nth-child(3)')[0].text, ele.find('td:nth-child(1)')[0].text, \
            ele.find('td:nth-child(2)')[0].text


def getData(ele, pcode, level, purl):
    url = None
    if (len(ele.links) > 0):
        url = list(ele.links)[0]

    name, code, type = getNameAndUrl(ele)
    data = {'name': name, 'code': code, 'pcode': pcode, 'region_level': level}
    if not url is None:
        data['url'] = purl[:purl.rfind('/')] + '/' + url
    if not type is None:
        data['type'] = type
    return data


session = HTMLSession()

'''
response = session.get('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/13/1301.html')
response.encoding = 'GBK'
cityList = response.html.find('.countytr')
print(cityList)
for citytr in cityList:     
    city = getData(citytr,'123',2,'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/13/1301.html')
    if 'url' not in city.keys():
      print(city,",")
      continue
    countyresponse = session.get(city['url'])
    countyresponse.encoding = 'GBK'
    countyList = countyresponse.html.find('.countytr')
    print(city,",")
'''

response = session.get(baseurl+"index.html")
response.encoding = 'GBK'
provincetrList = response.html.find('.provincetr>td>a')
print("[")
for provincetr in provincetrList:
    provinceurl = list(provincetr.links)[0];
    province = {'name': provincetr.text, 'url': baseurl + provinceurl, 'code': provinceurl.replace('.html', ''),
                'pcode': '-1', 'region_level': 1}
    print(province, ",")
    if 'url' not in province.keys():
        continue

    cityList = getList(province['url'], '.citytr')
    for citytr in cityList:
        city = getData(citytr, province['code'], 2, province['url'])
        print(city, ",")
        if 'url' not in city.keys():
            continue

        countyList = getList(city['url'], '.countytr')

        for countytr in countyList:
            county = getData(countytr, city['code'], 3, city['url'])
            print(county, ",")
            if 'url' not in county.keys():
                continue

            townList = getList(county['url'], '.towntr')

            for towntr in townList:
                town = getData(towntr, county['code'], 4, county['url'])
                print(town, ",")
                if 'url' not in town.keys():
                    continue

                villageList = getList(town['url'], '.villagetr')
                for villagetr in villageList:
                    village = getData(villagetr, town['code'], 5, town['url'])
                    print(village, ",")
print("]")
