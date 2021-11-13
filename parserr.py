import json
import requests
import time
from bs4 import BeautifulSoup
from requests import RequestException


def get_proxy():
    proxy = requests.get(
        'https://gimmeproxy.com/api/getProxy?country=RU&get=true&supportsHttps=true&protocol=http')
    proxy_json = json.loads(proxy.content)
    if proxy.status_code != 200 and 'ip' not in proxy_json:
        raise RequestException
    else:
        return 'http://' + proxy_json['ip'] + ':' + proxy_json['port']


def get_html(url):
    import random
    USER_AGENTS = [
        'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv)',
        'Chrome/70.0.3538.77 Safari/537.36',
        'Opera/9.68 (X11; Linux i686; en-US) Presto/2.9.344 Version/11.00',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows 95; Trident/5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_6) AppleWebKit/5342 (KHTML, like Gecko) Chrome/37.0.896.0 Mobile Safari/5342',
        'Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/533.49.2 (KHTML, like Gecko) Version/5.0 Safari/533.49.2',
        'Mozilla/5.0 (Windows NT 5.0; sl-SI; rv:1.9.2.20) Gecko/20110831 Firefox/37.0'
    ]
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    proxy = {
        # 'https': get_proxy()
    }
    response = requests.get(url, headers=headers)
    return response.content


def get_ads_list(avito_search_url):
    """
    :param avito_search_url: url like https://m.avito.ru/kazan/avtomobili/inomarki?pmax=200000&pmin=50000
    :return: ads list
    """
    html = get_html(avito_search_url)
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find_all(class_='iva-item-root-Nj_hb photo-slider-slider-_PvpN iva-item-list-H_dpX iva-item-redesign-nV4C4 iva-item-responsive-gIKjW items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum')

    ads_list = []
    for ad in ads:
        ad_url = ad.find(class_ = 'link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes').get('href')

        ad_url = 'https://m.avito.ru' + ad_url
        ad_header = ad.find(class_ = 'title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO').get_text()

        ad_price = ad.find(class_='price-text-E1Y7h text-text-LurtD text-size-s-BxGpL').get_text()
        try:
            ad_img_raw = ad.find(class_='photo-slider-list-item-_fUPr')
            ad_img_raw = str(ad_img_raw)
            ad_img = ad_img_raw.split('https:')
            ad_img = ad_img[2].split('"')
            ad_img = 'https:' + ad_img[0]

        except:
            ad_img = None

        ads_list.append({
            'title': ad_header,
            'price': ad_price,
            'url': ad_url,
            'img': ad_img
        })

    return ads_list


def get_new_ads(new, old):
    _ = []
    for ad in new:
        if ad not in old:
            _.append(ad)
    return _
