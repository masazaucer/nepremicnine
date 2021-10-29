import requests

STEVILO_STRANI = 3
REGIJE = ['severna-primorska', 'gorenjska', 'juzna-primorska', 'notranjska', 'ljubljana-okolica', 'ljubljana-mesto', 'dolenjska', 'posavska', 'zasavska', 'savinjska', 'koroška', 'podravska', 'pomurska']


def nalozi_stran(url):
    print(f'Nalagam {url}...')
    headers = {'Accept-Language': 'de-at;it-it;en-us'}
    odziv = requests.get(url, headers=headers)
    return odziv.text

def poberi_strani():
    for regija in REGIJE:
        for stran in range(1, STEVILO_STRANI + 1):
            url = f'https://www.nepremicnine.net/oglasi-prodaja/{regija}/stanovanje/{stran}/'
            vsebina = nalozi_stran(url)
            with open(f'podatki_nepremicnine/nepremicnine-{regija}-{stran}.html', 'w', encoding='utf-8') as f:
                f.write(vsebina)