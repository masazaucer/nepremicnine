import requests

STEVILO_STRANI = 2
STEVILO_OGLASOV_NA_STRAN = 30
REGIJE = ['severna-primorska', 'gorenjska', 'juzna-primorska', 'notranjska', 'ljubljana-okolica', 'ljubljana-mesto', 'dolenjska', 'posavska', 'zasavska', 'savinjska', 'koroška', 'podravska', 'pomurska']


def nalozi_stran(url):
    print(f'Nalagam {url}...')
    headers = {'Accept-Language': 'de-at;it-it;en-us'}
    odziv = requests.get(url, headers=headers)
    return odziv.text


for regija in REGIJE:
    url = f'https://www.nepremicnine.net/oglasi-prodaja/{regija}/stanovanje/'
    vsebina = nalozi_stran(url)
    with open(f'nepremicnine-{regija}.html', 'w', encoding='utf-8') as f:
        f.write(vsebina)