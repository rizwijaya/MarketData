# Market Data Cryptocurrency
---
#### Daftar Isi
- [Market Data Cryptocurrency](#market-data-cryptocurrency)
- [Struktur Project](#struktur-project)
- [Panduan Instalasi](#panduan-instalasi-installation-guide)
- [Konfigurasi pada Home Assistant](#konfigurasi-pada-home-assistant)
    - [Konfigurasi Project](#konfigurasi-project)
    - [Konfigurasi Tampilan](#konfigurasi-tampilan)
- [Tampilan pada Home Assistant](#beranda-home-assitant)
---
#### Market Data Cryptocurrency
Market Data Cryptocurrency merupakan kustom komponen Home Assistant yang memberikan informasi harga aset digital / Cryptocurrency yang mana dalam kustom komponen ini akan mengambil data pasar cryptocurrency secara realtime dan akurat sesuai dengan kondisi pasar saat ini.

---

#### Struktur Project
Berikut merupakan struktur project yang digunakan dalam kustom komponen market data ini:
```
    ├── custom_components
    │   ├── MarketData
    │   │   ├── __init__.py
    │   │   ├── const.py
    │   │   ├── manifest.json
    │   │   └── sensor.py
    │   └── __init__.py
    ├── example
    │   ├── configuration.yaml
    │   ├── layout.yaml 
    │   └── secrets.yaml
    ├── hacs.json
    └── Readme.md
```
Pada struktur project tersebut terdapat dua folder dimana folder custom_components akan berisi file konfigurasi sensor dan program yang digunakan dalam project sedangkan folder yang kedua adalah example berisi contoh konfigurasi dan layout yang digunakan dalam Home Assistant.

---

#### Panduan Instalasi (Installation Guide)
##### Instalasi awal
Langkah awal sebelum menggunakan project ini adalah melakukan instalasi plugins dan extensions yang akan digunakan nantinya.
1. Download dan Install Home Assistant Community Store. Untuk instalasi dan konfigurasi dari Home Assistant Community Store dapat dilihat di website resmi dari HACS sebagai berikut.
    - [Install Home Assistant Community Store](https://hacs.xyz/docs/installation/installation)
    - [Konfigurasi Home Assistant Community Store](https://hacs.xyz/docs/configuration/basic)

2. Apabila ingin menggunakan tampilan dari kartu entitas Home Assistant saya ikuti langkah berikut, jika tidak anda dapat melewatinya.
    - Download dan install plugin css yang digunakan untuk membuat tampilan dari kartu pada link berikut.
        - [Download Plugins CSS](https://github.com/thomasloven/lovelace-card-mod)
        - [Instalasi dan Konfigurasi Plugin](https://github.com/thomasloven/hass-config/wiki/Lovelace-Plugins)
    - Download dan install plugin yang nantinya digunakan untuk menampilkan baris entitas pada setiap kartu.
        - [Download Plugins Entitas](https://github.com/thomasloven/lovelace-template-entity-row)
        - [Instalasi dan Konfigurasi Plugin](https://github.com/thomasloven/hass-config/wiki/Lovelace-Plugins)
    - Download dan Install plugin vertical stack in card, plugin ini digunakan untuk mengelompokkan banyak kartu dalam satu kartu dan menghapus batas pada kartu.
        - [Download Plugin Vertical Stack In Card](https://github.com/ofekashery/vertical-stack-in-card)
        - [Instalasi dan Konfigurasi Plugin](https://github.com/ofekashery/vertical-stack-in-card)
##### Install Market Data ke Home Assistant
###### Instalasi dengan Home Assistant Community Store
Pada proses instalasi market data ini menggunakan Home Assistant Community Store yang telah kita install sebelumnya.
1. Buka HACS pada Home Assistant, kemudian pilih Integrations.
2. Pada tampilan integrations selanjutnya pilih menu titik tiga dipojok kanan atas dan pilih Custom Repositories.
3. Selanjutnya masukan link repository berikut pada form Add Custom Repository URL.
    ```
    https://github.com/rizwijaya/MarketData_HomeAssistant
    ```
    Untuk kategori pilih Integration, kemudian pilih Add untuk menambahkan repository Market Data Crytocurrency.
4. Apabila Market Data Cryptocurrency berhasil ditambahkan akan menampilkan tampilan berikut pada HACS.
![Instalasi dengan HACS](/Screenshot/1.install.JPG)
5. Kemudian Pilih Market Data Cryptocurrency dan pilih install, maka HACS akan melakukan instalasi.
6. Setelah instalasi selesai selanjutnya lakukan restart server Home Assistant anda.
###### Instalasi manual pada Custom Component.
Selain menggunakan Home Assistant Community Store anda dapat melakukan instalasi manual dari Market Data Cryptocurrency ini yaitu dengan mensalin file di folder `/custom_components/MarketData` pada repository ini ke folder dari Home Assistant yaitu `[homeassistant]/config/custom_components/MarketData`.

---
#### Konfigurasi pada Home Assistant
Setelah project Market Data Cryptocurrency berhasil terinstal pada Home Assistant langkah berikutnya adalah melakukan konfigurasi Market Data ke Home Assitant.

##### Konfigurasi project
Lakukan konfigurasi pada file [configuration.yaml](/example/configuration.yaml) yang terletak di Home Assistant. Berikut merupakan konfigurasi yang digunakan.

```yaml
sensor:
  - platform: MarketData
    api_key: !secret marketData
    cryptocurrency_name: ETH (default = "BTC") Koin yang ingin digunakan
    update_frequency: (default = 60) Frekuensi update pada sensor dalam menit.
  - platform: MarketData
    api_key: !secret marketData
    cryptocurrency_name: DOGE (default = "BTC") Koin yang ingin digunakan
    update_frequency: 15 (default = 60) Frekuensi update pada sensor dalam menit.
```
Untuk daftar lengkap Mata Uang kripto yang didukung dapat dicek pada website resmi dari [nomics](https://nomics.com/). 

Setelah melakukan konfigurasi dari file [configuration.yaml](/example/configuration.yaml) langkah berikutnya lakukan konfigurasi API Key pada file [secrets.yaml](/example/secrets.yaml) berikut merupakan contoh konfigurasinya:
```yaml
marketData: your-api-key (Masukan Api Key anda)
```
Apabila belum memiliki Api Key dari Nomics anda dapat melakukan pendaftaran pada website resmi dari [Nomics untuk mendapatkan Api Key](https://p.nomics.com/cryptocurrency-bitcoin-api).

##### Konfigurasi Tampilan
Apabila anda ingin menggunakan tampilan yang saya gunakan, berikut merupakan konfigurasi dari tampilan yang saya gunakan.
```yaml
type: 'custom:vertical-stack-in-card'
cards:
  - type: entities
    entities:
      - type: 'custom:template-entity-row'
        entity: sensor.marketdata_btcusd
        name: '{{ state_attr(config.entity, ''name'') }}'
        secondary: '{{ state_attr(config.entity, ''symbol'') }}'
        image: '{{ state_attr(config.entity, ''logo_url'') }}'
        state: '${{ state_attr(config.entity, ''price'') | round(2) }}'
      - type: 'custom:template-entity-row'
        entity: sensor.marketdata_btcusd
        name: High
        icon: 'mdi:currency-usd'
        state: '${{ state_attr(config.entity, ''high'') | round (2)}}'
        secondary: >-
          {{ as_timestamp(state_attr(config.entity, 'high_timestamp')) |
          timestamp_custom('%d-%m-%Y %H:%M ') }}
      - type: 'custom:template-entity-row'
        entity: sensor.marketdata_btcusd
        name: Crypto Rank
        icon: 'mdi:chart-line'
        state: '{{ state_attr(config.entity, ''rank'') }}'
        secondary: '${{"{:,}".format(state_attr(config.entity, ''market_cap'')|int)}}'
  - type: 'custom:mini-graph-card'
    hours_to_show: 3
    points_per_hour: 60
    show:
      icon: false
      name: false
    entities:
      - entity: sensor.marketdata_btcusd
  - type: entities
    entities:
      - entity: sensor.marketdata_btcusd
        name: 1 Hour
        type: 'custom:template-entity-row'
        state: '${{ state_attr(config.entity, ''price_change_h1'') | round(2) }}'
        secondary: >-
          {{ state_attr(config.entity, 'price_change_pct_h1')  | multiply(100) |
          round(4) }}%
        icon: |
          {% if state_attr(config.entity, 'price_change_h1') | float > 0 %}
             mdi:arrow-up-bold
          {% elif state_attr(config.entity, 'price_change_h1') | float < 0 %}
             mdi:arrow-down-bold
          {% else %}
             mdi:arrow-right-bold
          {% endif %}
        card_mod:
          style: |
            {% if state_attr(config.entity, 'price_change_h1') | float > 0 %}
               :host {
                 --paper-item-icon-color: green;
                 color: green
               }
            {% elif state_attr(config.entity, 'price_change_h1') | float < 0 %}
               :host {
                 --paper-item-icon-color: red;
                 color: red
               }
            {% else %}
               :host {
                 --paper-item-icon-color: black;
                 color: black
               }
            {% endif %}
```
Dari konfigurasi tersebut maka akan menghasilkan tampilan kartu sebagai berikut.
![Instalasi dengan HACS](/Screenshot/tampilankartu.JPG)

---
#### Tampilan Pada Home Assitant
##### Beranda Home Assitant
![Instalasi dengan HACS](/Screenshot/beranda.JPG)
##### Pada Alat Pengembang Home Assitant
![Instalasi dengan HACS](/Screenshot/debugging.JPG)
