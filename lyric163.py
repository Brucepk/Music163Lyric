import requests
from bs4 import BeautifulSoup
import re
import json
import time

'''
作者：pk哥
公众号：Python知识圈
日期：2018/08/08
代码解析详见公众号「Python知识圈」。

'''


def get_html(url):
    proxy_addr = {'http': '61.135.217.7:80'}
    # 用的代理 ip，如果被封的，在http://www.xicidaili.com/换一个
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        html = requests.get(url, headers=headers, proxies=proxy_addr).text
        return html
    except BaseException:
        print('request error')
        pass


def get_top50(html):
    soup = BeautifulSoup(html, 'lxml')
    info = soup.select('.f-hide #song-list-pre-cache a')
    songname = []
    songids = []
    for sn in info:
        songnames = sn.getText()
        songname.append(songnames)
    for si in info:
        songid = str(re.findall('href="(.*?)"', str(si))).strip().split('=')[-1].split('\'')[0]    # 用re查找，查找对象一定要是str类型
        songids.append(songid)
    return zip(songname, songids)


def get_lyrics(songids):
    url = 'http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1'.format(songids)
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    json_obj = json.loads(html)
    initial_lyric = json_obj['lrc']['lyric']
    reg = re.compile(r'\[.*\]')
    lyric = re.sub(reg, '', initial_lyric).strip()
    return lyric


def save2txt(songname, lyric):
    print('正在保存歌曲：{}'.format(songname))
    with open('E:\\歌词\\{}.txt'.format(songname), 'a', encoding='utf-8')as f:
        f.write(lyric)


if __name__ == '__main__':
    # id = '10562'  张韶涵
    id = input('请输入歌手id：')
    top50url = 'https://music.163.com/artist?id={}'.format(id)
    html = get_html(top50url)
    singer_infos = get_top50(html)
    for singer_info in singer_infos:
        lyric = get_lyrics(singer_info[1])
        save2txt(singer_info[0], lyric)
        time.sleep(1)