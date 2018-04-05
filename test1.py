import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_item(div):
    item = []
    td = div.table.tbody.tr.td
    table = td.find_all('table', recursive=False)[1]
    td = table.tbody.tr.find_all('td', recursive=False)[1]
    item.append(td.div.strong.text.strip())  # title
    trs = td.table.tbody.find_all('tr', recursive=False)
    item.append(tuple([td.find('strong').text.strip()
                       for td in trs[0].find_all('td')]))  # ID
    for i in range(1, len(trs)):
        item.append(tuple([trs[i].find('th').text.strip()]
                          + [td.text.strip() for td in trs[i].find_all('td')]))
    return item


def get_item_first(div):
    item = []
    td = div.table.tbody.tr.td
    table = td.find_all('table', recursive=False)[1]
    td = table.tbody.tr.find_all('td', recursive=False)[1]
    item.append(td.find_all('div', recursive=False)[2]
                .strong.text.strip())  # title
    trs = td.table.tbody.find_all('tr', recursive=False)
    item.append(tuple([td.find('strong').text.strip()
                       for td in trs[0].find_all('td')]))  # ID
    for i in range(1, len(trs)):
        item.append(tuple([trs[i].find('th').text.strip()]
                          + [td.text.strip() for td in trs[i].find_all('td')]))
    return item


def get_item_middle(div):
    item = []
    table = div.find_all('table', recursive=False)[1]
    table = table.tbody.tr.td.find_all('table', recursive=False)[1]
    td = table.tbody.tr.find_all('td', recursive=False)[1]
    item.append(td.find_all('div', recursive=False)[2]
                .strong.text.strip())  # title
    trs = td.table.tbody.find_all('tr', recursive=False)
    item.append(tuple([td.find('strong').text.strip()
                       for td in trs[0].find_all('td')]))  # ID
    for i in range(1, len(trs)):
        item.append(tuple([trs[i].find('th').text.strip()]
                          + [td.text.strip() for td in trs[i].find_all('td')]))
    return item


def get_contents(notice):
    r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}.html'
                     .format(notice))
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.body.find_all('div', recursive=False)
    divs = [div.find('div', id='divContent') for div in divs]

    i, content0, content1 = 1, [get_item_first(divs[0])], []
    while i < len(divs):
        content0.append(get_item(divs[i]))
        if len(divs[i].find_all('table', recursive=False)) > 1:
            content1.append(get_item_middle(divs[i]))
            i += 1
            break
        i += 1
    while i < len(divs):
        content1.append(get_item(divs[i]))
        i += 1

    return (content0, content1)


def convert_item(item):
    item[0] = ('title', item[0])
    for i in range(1, len(item)):
        item[i] = (item[i][0], ', '.join(item[i][1:]))
    return dict(item)


def contents_to_df(contents):
    df = pd.DataFrame(list(map(convert_item, contents[0] + contents[1])))
    return df.set_index('title')


def crawl(notice, csv_filename):
    contents = get_contents(notice)
    df = contents_to_df(contents)
    df.to_csv(csv_filename)


if __name__ == '__main__':
    notice, csv_filename = sys.argv[1], sys.argv[2]
    crawl(notice, csv_filename)