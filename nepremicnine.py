import os
import requests
import re
import csv


nepremicnine_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/'

nepremicnine_directory = 'podatki_nepremicnine'

frontpage_filename = 'nepremicnine.html'

csv_filename = 'nepremicnine.csv'


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
    'oglasi prodaja > (?P<regija>.*?) > stanovanje".*' +
    '<span class="title">(?P<naslov>.*?)</span></a></h2>.*' +
    'Leto: <strong>(?P<leto>.*?)</strong>.*' +
    'itemprop="description">(?P<opis>.*?)</div>.*' +
    '(<span class="velikost" lang="sl">(?P<velikost>.*?)</span>)?.*' +
    '<span class="agencija">(?P<agencija>.*?)</span>.*' +
    'itemprop="price" content="(?P<cena>.*?)" />')
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
    return seznam_slovarjev

def write_csv(polja, vrstice, directory, filename):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, filename)

    with open(pot, 'w', encoding='utf-8') as dat:
        writer = csv.DictWriter(dat, fieldnames=polja)
        writer.writeheader()
        for vrstica in vrstice:
            if vrstica != None:
                writer.writerow(vrstica)
    return

def main():
    #Pridobi vsebino strani, jo razdeli na posamezne oglase, prebere ustrezne podatke in jih vrne kot seznam slovarjev.
    spletna_stran = download_url_to_string(nepremicnine_frontpage_url)
    save_string_to_file(spletna_stran, nepremicnine_directory, frontpage_filename)

    podatki = ads_from_file(nepremicnine_directory, frontpage_filename)
    print(podatki)

    write_csv(['id', 'regija', 'naslov', 'leto', 'opis', 'velikost', 'agencija', 'cena'], podatki, nepremicnine_directory, csv_filename)




main()