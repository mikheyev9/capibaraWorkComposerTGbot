import requests
from bs4 import BeautifulSoup

ALL_SECTORS = [
    'Сектор C22',
    'Сектор C23',
    'Сектор A23',
    'Сектор A22',
    'Сектор B3',
    'Сектор D2',
    'Сектор B2',
    'Сектор C21',
    'Сектор C24',
    'Сектор A24',
    'Сектор A21'
]


def get_free_sectors():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", '
                     '"YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                      'YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36'
    }
    url = 'https://tickets.cskabasket.ru/ru/event/?id=866'
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    new_free_sectors_list = []
    old_free_sectors_list = []

    svg = soup.select('svg#mainsvg')[0]
    free_sectors = svg.select('g:not([free="0"])')
    for sector in free_sectors:
        new_free_sector_name = sector.get('sector_name')
        if new_free_sector_name not in ALL_SECTORS:
            new_free_sectors_list.append(new_free_sector_name)
            ALL_SECTORS.append(new_free_sector_name)

    for sector_old in ALL_SECTORS:
        for sector in free_sectors:
            new_free_sector_name = sector.get('sector_name')
            if sector_old == new_free_sector_name:
                break
        else:
            old_free_sectors_list.append(sector_old)
            index_sector = ALL_SECTORS.index(sector_old)
            ALL_SECTORS.pop(index_sector)

    return new_free_sectors_list, old_free_sectors_list
