import asyncio
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from settings.config import bot_alert_sectors_and_events
from telegram.send_message import generate_message_to_send_from_module_parse_sectors

ORIGINAL_HREF = 'https://spb.ticketland.ru/teatry/bdt-imtovstonogova/leto-odnogo-goda/'

this_dir = Path(__file__).parent
file_with_text = this_dir.joinpath('original_text')
with open(file_with_text, 'r', encoding='utf-8') as f:
    original_text = f.read()


async def get_href():
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
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 '
                      'YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36'
    }
    url = 'https://bdt.spb.ru/spektakli/leto-odnogo-goda/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        url_to_buy_tickets = soup.select(
            'a.tl_button.btn.btn-lg.btn-bdt.slow-pulse'
        )[0]
        url_to_buy_tickets = url_to_buy_tickets.get('href')
        if url_to_buy_tickets != ORIGINAL_HREF:
            message_to_send = (
                'ЛЕТО ОДНОГО ГОДА изменилась ссылка для покупки билета '
                f'С {ORIGINAL_HREF} на {url_to_buy_tickets}\n'
                'https://bdt.spb.ru/spektakli/leto-odnogo-goda/'
            )
            await generate_message_to_send_from_module_parse_sectors(
                bot_alert_sectors_and_events,
                message_to_send
            )
        return url_to_buy_tickets
    else:
        message_to_send = (
            f'{url = } {response.status_code = }'
        )
        await generate_message_to_send_from_module_parse_sectors(
            bot_alert_sectors_and_events,
            message_to_send
        )
        return ORIGINAL_HREF


async def check_event_in_ticketland(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, utf-8',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'no-cache',
        'connection': 'keep-alive',
        'host': 'spb.ticketland.ru',
        'pragma': 'no-cache',
        'referer': 'https://bdt.spb.ru/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", '
                     '"YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 '
                      'YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    container = str(soup.find('div', class_='performances'))
    with open('original_html', 'w', encoding='utf-8') as f:
        f.write(container)

    if response.status_code == 200:
        global original_text
        if original_text not in container:
            with open(file_with_text, 'w', encoding='utf-8') as f:
                f.write(container)
            original_text = container
            message_to_send = (
                'ЛЕТО ОДНОГО ГОДА изменился html\n'
                'https://bdt.spb.ru/spektakli/leto-odnogo-goda/'
            )
            await generate_message_to_send_from_module_parse_sectors(
                bot_alert_sectors_and_events,
                message_to_send
            )
    else:
        message_to_send = (
            f'{url = } {response.status_code = }'
        )
        await generate_message_to_send_from_module_parse_sectors(
            bot_alert_sectors_and_events,
            message_to_send
        )


async def main_if_change_event():
    while True:
        url_to_buy_tickets = await get_href()
        await check_event_in_ticketland(url_to_buy_tickets)
        await asyncio.sleep(600)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main_if_change_event())
