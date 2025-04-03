import requests
from lxml import etree
import re
import json
import csv

url = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
# https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
# https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
# https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
response = requests.get(url)

if response.status_code == 200:
    # html = etree.parse(response.text, etree.HTMLParser())
    # result = html.xpath('//div[@id="repo-content-pjax-container"]/rect-app/script/text()')
    # print(result)
    #
    pattern = re.compile('<script type="application/json" data-target="react-app.embeddedData">(.*?)</script>')
    result2 = re.search(pattern, response.text).group(1)
    # json = json.loads(result2)
    # data = json['payload']['blob']['rawLines']
    # print(json['blob']['rawLines'])

    with open("covid_confirmed_global.csv", 'w') as file:
         file.write(result2)
    print("数据下载成功")
else:
    print(f"下载失败，{response.status_code},{response.reason}")

