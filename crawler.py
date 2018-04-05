import sys
import csv
import requests
from pathlib import Path
from bs4 import BeautifulSoup


def get_detail_engines_imgs(url):
    # detail:
    detail = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', class_='gMain')
    detail.append(div.h1.text)
    tds = div.find_all('td')
    detail = detail + [tds[i].text.strip() for i in range(1, 86, 2)]
    detail.append(tds[-1].text.strip())
    # engines:
    engines = []
    if len(tds) > 92:
        engines = [' '.join(tds[i].stripped_strings) for i in range(92, 97)]
    # imgs:
    imgs = []
    tmp = soup.find('div', id='noticeImage')
    if tmp is not None:
        imgs = [img.attrs['src'] for img in tmp.ul.find_all('img')]
    return detail, engines, imgs


def download_imgs(path, prefix, imgs):
    for i in range(0, len(imgs)):
        r = requests.get(imgs[i])
        filename = '{}_{:02d}.jpg'.format(prefix, i)
        with open(Path(path).joinpath(filename), 'wb') as f:
            for chunk in r:
                f.write(chunk)


def get_notice_page(soup):
    div = soup.find('div', class_='gMain')
    td = div.find_all('td')
    return [td[i].a.attrs['href'] for i in range(0, len(td), 3)]


def get_notice_index(notice):
    url = 'http://www.cn357.com/notice_' + notice
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    span = soup.find('span', class_='pageList')
    if span is None:
        index = get_notice_page(soup)
    else:
        total = int(span.findChildren()[-2].text)
        index = get_notice_page(soup)
        for i in range(2, total + 1):
            r = requests.get(url + '_' + str(i))
            soup = BeautifulSoup(r.text, 'html.parser')
            index = index + get_notice_page(soup)
    return index


def crawl(index, out_filename, img_path):
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
              '底盘1', '底盘2', '底盘3', '底盘4',  '备注',
              '发动机型号', '发动机生产企业', '发动机商标', '排量', '功率']
    with open(out_filename, 'w', newline='') as csvfile:
        detail_wirter = csv.writer(csvfile, dialect=csv.excel())
        detail_wirter.writerow(header)
        for x in index:
            try:
                detail, engines, imgs = get_detail_engines_imgs(url + x)
                detail_wirter.writerow(detail + engines)
                download_imgs(img_path, x[7:], imgs)
            except Exception as e:
                print(x, e)


if __name__ == '__main__':
    notice, out_filename, img_path = sys.argv[1], sys.argv[2], sys.argv[3]
    index = get_notice_index(notice)
    crawl(index, out_filename, img_path)