import requests
import re

REGIJE = {'severna-primorska': 1, 'gorenjska' : 2, 'juzna-primorska' : 3, 'notranjska' : 4, 'ljubljana-okolica' : 5, 'ljubljana-mesto' : 6, 'dolenjska' : 7, 'posavska' : 8, 'zasavska' : 9, 'savinjska' : 10, 'koroška' : 11, 'podravska' : 12, 'pomurska' : 13}
STEVILA_STRANI_ZA_REGIJE = {}
vzorec_za_strani = re.compile(r'<ul data-pages="(?P<strani>\d+?)">', re.DOTALL)


def nalozi_stran(url):
    print(f'Nalagam {url}...')
    headers = {'Accept-Language': 'de-at;it-it;en-us'}
    odziv = requests.get(url, headers=headers)
    return odziv.text

def stevila_strani():
    for regija in REGIJE:
        url = f'https://www.nepremicnine.net/oglasi-prodaja/{regija}/stanovanje/'
        vsebina = nalozi_stran(url)
        strani = re.search(vzorec_za_strani, vsebina)
        strani = (strani.groupdict() if strani else None)
        st_strani = (int(strani['strani']) if strani else 1)
        STEVILA_STRANI_ZA_REGIJE[regija] = st_strani


def poberi_strani():
    stevila_strani()
    for regija in REGIJE:
        for stran in range(1, STEVILA_STRANI_ZA_REGIJE[regija] + 1):
            url = f'https://www.nepremicnine.net/oglasi-prodaja/{regija}/stanovanje/{stran}/'
            vsebina = nalozi_stran(url)
            with open(f'podatki_nepremicnine/nepremicnine-{regija}-{stran}.html', 'w', encoding='utf-8') as f:
                f.write(vsebina)