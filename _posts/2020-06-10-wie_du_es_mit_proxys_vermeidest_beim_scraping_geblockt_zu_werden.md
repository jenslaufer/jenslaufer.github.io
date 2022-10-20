---
title: "Wie du es mit Proxys vermeidest beim Scrapen geblockt zu werden"
subtitle: "Verschiedene Ansätze, die dir mit wenigen Änderungen im Code helfen"
image: "https://res.cloudinary.com/jenslaufer/image/upload/c_scale,w_800/v1592394603/anita-jankovic-KGbX1f3Uxtg-unsplash.jpg"
image_caption: "Photo by Anita Jankovic on Unsplash"
tags: proxies, proxy, scraping
categories: scraping
layout: post
language: de
---

Die letzten Stunden hatte ich einen Scraper geschrieben, um die Produkte eines großen Internetmarktplatzes für eine Nischenanalyse zu ziehen. Der Scraper erforderte einigen Aufwand, weil die Website JavaScript für das Rendering verwendet, d.h. viel Code wird erst im Browser ausgeführt. Dies muss erhöht den Aufwand beim Scraping. Die Verwendung von Selenium mit einem Headless Chromebrowser brachte schliesslich den Erfolg. Nun kam die Stunde der Wahrheit, ich wollte nun zum ersten Mal Rohdaten im großen Stile ziehen. Voll freudiger Erwartung startete ich meinen Scraper, der die Seiten in meine MongoDB-Datenbank schaufeln sollte. Bald würde ich Daten analysieren könne, Scraping ist der nervige Teil auf dem Weg da hin. Hat man erst einmal die Rohdaten dann ist das die halbe Miete, die Extraktion der interessanten Felder ein Kinderspiel. Durch die Parallelverarbeitung sollte das Ganze recht schnell sein. Während ich gespannt wartete passierte es: Die Größe der Files war auf einmal immer gleich und viel kleiner als am Anfang und...

__Http Statuscode: 429__

Mir war sofort klar, was passiert war: __Ich war geblockt worden.__ Selbstverständlich war ich mir dieser Gefahr von Anfang an bewusst gewesen, aber meine Ungeduld hatte mir wieder einmal einen Strich duch die Rechnung gemacht: Der Versuch die Daten  ohne Massnahmen zu holen war gescheitert. Zwar sind Blocks häufig nur temporär, aber sie verhindern, dass du die Menge an Daten ziehen kannst, die du möchtest. Gerade bei Parallelverarbeitung ist die Gefahr sehr groß. Du solltest dir auch bewusst sein, dass du bei wiederholten Verstössen lebenslang geblockt werden kannst.

Du fragst dich nun was man genau tun muss, um ein Blocking zu vermeiden. Die Antwort ist einfach: __Du musst beim Scrapen möglichst viele verschiedene IP-Adressen aus unterschiedlichen, welteit verteilten Subnetzen verwenden__. In einer idealen Welt würde ich jeden Zugriff von einer anderen IP-Adresse machen. Das lässt sich schwer realisieren bzw. wäre mit hohem Aufwand verbunden. Im Folgenden möchte ich dir verschiedene Ansätze näher bringen:

### Der naive Ansatz

Eine erste Idee ist es frei zugängliche Proxies zu verwenden, die du sicher auch schon einmal verwendest um deine IP Adresse zu verschleiern. Leider muss ich dich enttäuschen, weil das dich nicht ans Ziel führen wird. Viele dieser Proxies sind nach einiger Zeit nicht mehr verfügbar oder sie sind extrem langsam. Ausserdem bist du nicht der Einzige auf der Welt mit dieser Idee. Meist bekommst du deine Requests nicht mit diesen Proxies durch.

### Der "Mit Kanonen auf Spatzen schiessen" Ansatz

Als ich das Erstemal vor dem Problem stand, hatte ich die Idee über Cloudservices wie z.B. AWS, Azure oder GCloud eine eigene Proxyfarm aufzusetzen. Beim Durchrechnen wurde mir jedoch schnell klar, dass das nur mit sehr hohen Kosten zu bewerktstelligen ist. Nehmen wir an du möchtest in 20 Threads parallel Daten von einer Websites ziehen und für jeden Thread 10 IP-Adressen zufällig durchrotieren, dann benötigst du dafür 200 IP-Adressen und entsprechende Serverresourcen. Das ist kostenintensiv, ausserdem musst den Aufwand für die Pflege dieser Infrakstruktur einbeziehen. Auf AWS kostet eine IP-Adresse etwa 4 EUR pro Monat. Zusammen mit dem Server macht du also 800-1000 EUR rechenen, dazu noch der Aufwand für Pflege und Wartung deines Systems.

### Kommerzielle Proxylisten verwenden

Eine andere Möglichkeit ist die Kauf von kommerziellen Proxylisten. Du bezahlst eine monatlich Gebühr und erhälst Zugriff auf eine Reihe von Proxies, die du beim Scrapen verwendest. Das funktioniert sehr gut, allerdings musst du deinen Code verändern. Der Aufwand hält sich in Grenzen, was mir jedoch nicht daran gefällt, dass ich die Proxylisten irgendwo vorhalten muss. Ändere ich meinen Vertrag weil ich z.B. mehr Proxies benötige dann muss ich meine lokale Liste nachpflegen. Sicher kann man das z.B in eine getrennte Bibliothek auslagern, aber es ist doch ein wenig unschön. Lange Zeit habe ich [Bonanza Proxies](https://proxybonanza.com/?aff_id=831) verwendet und habe die Proxyliste in einem Python module unter [scrpproxies on Github](https://github.com/jenslaufer/scrpproxies) ausgelagert. Die Proxies von Bonanza funktionieren sehr gut, jedoch gefiel mir das mit der Bibliothek nie wirklich. Wenn ich ehrlich bin interessieren mich die genauen IP-Adressen nicht und ich möchte auch keinen Code pflegen für so etwas. 

Hie ein kleines Codebeipiel, um einen Request mit einem Proxy abzusetzen. Ichinitialisiere zuerst die den Proxydienst. Über get wählt das Modul zufällig eine Proxyadresse aus, die ich dann für den Request benutze.


```python
from scrpproxies import proxy
import requests

# Initialisation of proxy service with credentials
proxies = proxy.BonanzaProxy(username, password)

# Get returns random proxy ip address
proxy = proxies.get()['http']

# use proxy for the request
r = requests.get(url, proxies={"http": proxy})
```

### Proxies per API-Call

Etwas eleganter sind APIs, die einem eine Proxyadressen zurücliefern. Das Schöne ist, dass man keine lokalen Proxylisten vorhalten muss. Man setzt einen Request ab und bekommt IP-Adressen, die man dann verwendet. [Luminati](https://luminati.io/?affiliate=ref_5ee711e0c7669177ab29ff24) ist ein solcher Dienst, den ich allerdings nur kurz verwendet habe.

Das ist viel eleganter als die Lösung vorher hat jedoch einen Nachteil. Du setzt einen Request ab, um IP-Adressen zu erhalten, die du dann für den eigentlichen Request verwende. Ich mache also zwei Requests statt einem. Codetechnisch erfordert das zwar ganz ein wenig Boilerplatecode, der allerdings überschaubar ist.

```python
import requests

# Api call to get Proxy
proxy = requests.get(f"https://luminati.io/api/get_proxy/key={api_key}").text

# use proxy for the request
r = requests.get(url, proxies={"http": proxy})

```


### Blackbox Call zur Zieladresse

Ein viel besserer Ansatz ist, wenn du den verwendeten Proxy gar nicht erst in der deiner Logik handeln musst, weil du dem API-Provider die Ziel-Url übermittlest und dieser den Aufruf abarbeitet. Wenn der Provider dann noch in der Lage ist Seiten mit JavaScript Code über einen Headless Browsern zu rendern, dann kannst du dich voll auf die Extraktion der Daten konzentrieren. 
Du sparst enorm viel Zeit. Lange Zeit habe ich nach einer solchen API gesucht. Schliesslich bin ich fündig geworden:  [ScraperAPI](https://www.scraperapi.com?fpr=jens78) bietet genau die Features, die ich immer gesucht habe.

```python
import requests

# Scraper Api url template
SCRAPER_API_URL = "http://api.scraperapi.com?api_key={api_key}&url={url}"

# target url
url = "https://somesitetoscrape.com"

# parsed request url
scraper_url = SCRAPER_API_URL.format(api_key=api_key, url=url)

# fetch target url
r = requests.get(scraper_url)

```
