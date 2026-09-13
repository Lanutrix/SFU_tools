import requests
import config

cookies = {
    'MoodleSession': config.MOODLE_SESSION,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:155.0) Gecko/20100101 Firefox/155.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Priority': 'u=0, i',
}

params = {
    'qrpass': 'fdsd1c',
    'sessid': '39645',
}

response = requests.get('https://lms.sfedu.ru/mod/attendance/attendance.php', params=params, cookies=cookies, headers=headers)