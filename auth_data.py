def get_headers_modeus(token):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:155.0) Gecko/20100101 Firefox/155.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU',
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/json',
        'Origin': 'https://sfedu.modeus.org',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Priority': 'u=0',
    }