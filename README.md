# nepremicnine

Analizirala bom oglase za prodajo stanovanj v Sloveniji. Podatke sem pridobila na strani
[Nepremicnine.net](https://www.nepremicnine.net/).

Za vsako stanovanje sem zajela:
* id oglasa
* naslov oglasa
* regijo, v kateri se stanovanje nahaja (označeno s številkami)
* velikost stanovanja (v m^2)
* velikost zemljišča (v m^2)
* tip stanovanja(koliko sobno stanovanje je, pri čemer 0 pomeni garsonjera)
* leto izgradnje
* morebitno leto obnove
* opis
* ime agencije, ki stanovanje prodaja
* ceno stanovanja

Ti podatki se nahajajo v datoteki nepremicnine.csv.
V datoteki regije.csv so zabeležene povezave med imeni regij in njihovimi indeksi.

Ukvarjala se bom z naslednjimi vprašanji:
* Kako je cena kvadratnega metra stanovanja odvisna od regije?
* Ali so manjša stanovanja dražja glede na kvadratni meter?
* Koliko zemljišče pripomore k višji ceni stanovanja?
* Katera lastnost stanovanj najbolj vpliva na njihovo ceno?