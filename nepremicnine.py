import os
import requests
import re
import csv
from zajemi import *

poberi = False

nepremicnine_directory = 'podatki_nepremicnine'

csv_filename = 'nepremicnine.csv'

"""
def download_url_to_string(url):
    #Pošlje zahtevo za stran in vrne vsebino strani
    try:
        vsebina = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Preveri internetno povezavo!')
        return None
    return vsebina.text

def save_string_to_file(text, directory, filename):
    #Niz shrani v datoteko
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None
"""

def read_file_to_string(directory, filename):
    #Prebere vsebino datoteke
    with open(os.path.join(directory, filename), encoding='utf-8') as input_file:
        return input_file.read()



def page_to_ads(page_content):
    #Niz z vsebino strani razbije na bloke za posamezne oglase
    pattern = r'<div class="oglas_container.*?<span>O ponudniku</span></a>'
    regexp = re.compile(pattern, re.DOTALL)

    return re.findall(regexp, page_content)

def get_dict_from_ad_block(block):
    #Iz niza za posamezen oglas prebere ustrezne podatke ustrezne podatke.
    pattern = (r'id="(?P<id>\w{8})".*' +
    #r'(oglasi prodaja > (?P<regija>.*?) > stanovanje" />)?.*' +
    r'<span class="title">(?P<naslov>.*?)</span></a></h2>.*' +
    r'<span class="tipi">(?P<tip>.*?)</span></span>.*' +
    r'Leto: <strong>(?P<leto>.*?)</strong>.*' +
    r'<span class="atribut">Zemljišče: <strong>(?P<zemljisce>.*?) m2</strong></span>.*' +
    r'itemprop="description">(?P<opis>.*?)</div>.*' +
    r'<span class="velikost" lang="sl">(?P<velikost>.*?) m2</span>.*' +
    r'<span class="agencija">(?P<agencija>.*?)</span>.*' +
    r'itemprop="price" content="(?P<cena>.*?)" />')
    regexp = re.compile(pattern, re.DOTALL)
    najdeno = re.search(regexp, block)
    if najdeno:
        return najdeno.groupdict()
    else:
        return None

def ads_from_file(directory, filename):
    #Prebere podatke v datoteki "directory"/"filename" in jih
    #pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej.
    vsebina = read_file_to_string(directory, filename)
    oglasi = page_to_ads(vsebina)
    seznam_slovarjev = [get_dict_from_ad_block(oglas) for oglas in oglasi]
    print(seznam_slovarjev)
    return seznam_slovarjev

def write_csv(polja, vrstice, directory, filename):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, filename)

    with open(pot, 'w', encoding='utf-8') as dat:
        writer = csv.DictWriter(dat, fieldnames=polja)
        writer.writeheader()
        for vrstica in vrstice:
            writer.writerow(vrstica)
    return

def zberi_oglase():
    oglasi = []
    for regija in REGIJE:
        for stran in range(1, STEVILO_STRANI + 1):
            datoteka = f'nepremicnine-{regija}-{stran}.html'
            print(datoteka)
            podatki = ads_from_file(nepremicnine_directory, datoteka)
            print(podatki)
            for oglas in podatki:
                if oglas != None:
                    oglas['regija'] = regija
                    print(oglas)
                    podatki_oglasa = izloci_podatke(oglas)
                    oglasi.append(podatki_oglasa)
    return oglasi

def izloci_podatke(oglas):
    if oglas:
        oglas['id'] = oglas['id'].lstrip('o')
        oglas['regija'] = oglas['regija'].replace('-', ' ')
        oglas['naslov'] = oglas['naslov']

        try:
            oglas['tip'] = float(oglas['tip'].rstrip('-sobno').replace(',', '.'))
        except ValueError:
            if oglas['tip'] == '5 in večsobno':
                oglas['tip'] = 5
            elif oglas['tip'] == 'Garsonjera':
                oglas['tip'] = 0
            else:
                oglas['tip'] = None

        oglas['leto'] = int(oglas['leto'])
        oglas['zemljisce'] = float(oglas['zemljisce'])
        oglas['opis'] = oglas['opis']
        oglas['velikost'] = float(oglas['velikost'].replace(',', '.'))
        oglas['agencija'] = oglas['agencija']
        oglas['cena'] = float(oglas['cena'])
    return oglas

def main():
    #Pridobi vsebino strani, jo razdeli na posamezne oglase, prebere ustrezne podatke in jih shrani v csv.
    if poberi:
        poberi_strani()

    podatki = zberi_oglase()
    print(podatki)

    write_csv(['id', 'regija', 'naslov', 'tip', 'leto', 'zemljisce', 'opis', 'velikost', 'agencija', 'cena'], podatki, nepremicnine_directory, csv_filename)




main()