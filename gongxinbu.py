import sys
import csv
import requests
from pathlib import Path
from bs4 import BeautifulSoup

def get_detail(url):
    detail=[]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', {'class': 'gMain'})
    detail.append(div.hl.text)
    td = div.findAll('td')
    detail = detail + [td[i].text.strip() for i in range(1, 86, 2)]
    detail = detail + [td[i].text.strip() for i in range(92, 97)]
    detail.append(td[98].text.strip())
    return detail

def get_notice_page(soup):
    div = soup.find('div', {'class': 'gMain'})
    td = div.findAll('td')
    return [td[i].a.attrs['href'] for i in range(0, len(td), 3)]




def get_notice_index(notice):
    url = 'http://www.cn357.com/notice_' +  str(notice)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    span = soup.find('span', {'class': 'pageList'})
    total = int(span.findChildren()[-2].text)
    index = get_notice_page(soup)
    for i in range(2, total+1):
        r = requests.get(url + '_' + str(i))
        soup = BeautifulSoup(r.text, 'html.parser')
        index = index + get_notice_page(soup)
    return index

def crawl(index, out_filename):
    url = 'http://www.cn357.com'
    header = ['标题', '变更(扩展)记录', '公告型号', '公告批次', '品牌',
              '类型', '额定质量', '总质量', '整备质量', '燃料种类',
              '排放依据标准', '轴数', '轴距', '轴荷', '弹簧片数',
              '轮胎数', '轮胎规格', '接近离去角', '前悬后悬', '前轮距',
              '后轮距', '识别代号', '整车长', '整车宽', '整车高',
              '货厢长', '货厢宽', '货厢高', '最高车速', '额定载客',
              '驾驶室准乘人数', '转向形式', '准拖挂车总质量', '载质量利用系数',
              '半挂车鞍座最大承载质量',
              '企业名称', '企业地址', '电话号码', '传真号码', '邮政编码',
              '底盘1', '底盘2', '底盘3', '底盘4', '发动机型号',
              '发动机生产企业', '发动机商标', '排量', '功率', '备注']
    with open(out_filename, 'w', newline='') as csvfile:
        detail_wirter = csv.writer(csvfile, dialect=csv.excel())
        detail_wirter.writerow(header)
        for x in index:
            try:
                detail = get_detail(url + x)
                detail_wirter.writerow(detail)
            except Exception as e:
                print(x,e)



if __name__=='__main__':
    for notice in range(1, 305):
        index=get_notice_index(notice)
        crawl(index, str(notice))