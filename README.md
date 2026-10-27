# Gasteinertal Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

<img src="https://raw.githubusercontent.com/trollsoft7/gasteinertal-homeassistant/main/custom_components/gasteinertal/brand/icon.png" alt="Gasteinertal Icon" width="180" />

Home Assistant Custom Integration für Live-Daten aus dem Gasteinertal:

- Wasserstand der Gasteiner Ache in Bad Hofgastein
- Lufttemperatur auf der Schlossalm / Gastein Berg
- 13 Live-Webcams aus dem Feriengebiet

## Entitäten

### `sensor.wasserstand_gasteiner_ache`
- Quelle: https://www.salzburg.gv.at/wasser/hydro/grafiken/data.json
- Wert: `values.W["15m.Cmd.WiskiWeb"].v`
- Station: `Bad Hofgastein`
- Einheit: `cm`

### `sensor.temperatur_schlossalm`
- Bezeichnung: Temperatur Schlossalm
- Quelle: https://www.salzburg.gv.at/lawine/Station.js
- Wert: `measuredData.values.LT`
- Station: `badhofgastein_schlossalm`
- Einheit: `°C`

### `sensor.temperatur_bad_gastein`
- Quelle: [GeoSphere Austria Stationsdaten](https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-10min)
- Station: Bad Gastein, 1092 m, Stations-ID `7`
- Messwert: Lufttemperatur in 2 m Höhe (`tl`)
- Einheit: `°C`

### `sensor.niederschlag_letzte_10_min_bad_gastein`
- Quelle: [GeoSphere Austria Stationsdaten](https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-10min)
- Station: Bad Gastein, 1092 m, Stations-ID `7`
- Messwert: Niederschlagssumme der letzten 10 Minuten (`rr`)
- Einheit: `mm`

### `sensor.niederschlag_seit_jahresbeginn_bad_gastein`
- Quelle: [GeoSphere Austria tägliche Stationsdaten](https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1d)
- Station: Bad Gastein, 1092 m, Stations-ID `7`
- Messwert: Summe der verfügbaren Tages-Niederschlagswerte (`rr`) seit Jahresanfang
- Einheit: `mm`
- Attribut `fehlende_tageswerte`: Anzahl der fehlenden/ungültigen Tageswerte, die nicht in die Summe eingehen

Die GeoSphere-Messwerte werden alle zehn Minuten aktualisiert. Der 10-Minuten-Sensor zeigt die Niederschlagssumme dieses Intervalls. Der Jahressensor summiert die verfügbaren täglichen Niederschlagssummen seit Jahresbeginn; fehlende oder ungültige Tageswerte werden ausgelassen und über das Attribut `fehlende_tageswerte` ausgewiesen.

### Wetterwarnungen

Die drei `binary_sensor.wetterwarnung_heute_*` zeigen an, ob auf der jeweiligen Gemeindeseite für heute mindestens eine Warnstufe ausgegeben wird. `on` bedeutet, dass heute irgendwann eine Warnung gilt; die Attribute `warnstufe` (`0` bis `3`) und `warnfarbe` (`green`, `yellow`, `orange`, `red`) zeigen die höchste Tagesstufe.

- Bad Gastein: http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/badgastein/
- Bad Hofgastein: http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/bad_hofgastein/
- Dorfgastein: http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/dorfgastein/

Die Warnungsseiten sind derzeit nur über HTTP erreichbar; Home Assistant fragt sie daher unverschlüsselt ab. Die Integration zeigt den höchsten Warnlevel des heutigen Tages an, nicht ausschließlich eine Warnung, die genau zum aktuellen Zeitpunkt aktiv ist.

### Webcams

Alle Kameras sind im Gasteinertal. Die Bild-URLs stammen von Gasteinertal.com:

| Kamera | Live-Bild | Kameraseite |
| --- | --- | --- |
| Bad Hofgastein | [JPEG](https://www.gasteinertal.com/webcam/badhofgastein/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/badhofgastein.html) |
| Haitzingalm | [JPEG](https://www.gasteinertal.com/webcam/haitzingalm/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/haitzingalm.html) |
| Kühhager | [JPEG](https://www.gasteinertal.com/webcam/kuehhager/current/1200.jpg) | [Fulseck](https://www.gasteinertal.com/webcam/fulseck.html) |
| Bad Gastein | [JPEG](https://www.gasteinertal.com/webcam/badgastein/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/badgastein.html) |
| Sportgastein | [JPEG](https://www.gasteinertal.com/webcam/sportgastein/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/sportgastein-nassfeld.html) |
| Sportgastein Siglitztal | [JPEG](https://www.gasteinertal.com/webcam/sportgastein2/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/sportgastein-siglitztal.html) |
| Bad Gastein Zentrum | [JPEG](https://www.gasteinertal.com/webcam/badgastein2/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/badgastein2.html) |
| Schlossalm Snowcam | [JPEG](https://camhost1.gasteinertal.com/webcam/snowcam/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/snowcam.html) |
| Golfplatz Bad Gastein | [JPEG](https://www.gasteinertal.com/webcam/golfgastein/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/golf.html) |
| Wasserfall Bad Gastein | [JPEG](https://www.gasteinertal.com/webcam/wasserfall/current/816.jpg) | [Webcam](https://www.gasteinertal.com/webcam/wasserfall-badgastein.html) |
| Jungeralm Stubnerkogel | [JPEG](https://www.gasteinertal.com/webcam/jungeralm.jpg) | [Webcam](https://www.gasteinertal.com/webcam/jungeralm.html) |
| Dorfgastein Talabfahrt | [JPEG](https://camhost1.gasteinertal.com/webcam/hauserbauer/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/dorfgastein-hauserbauer.html) |
| Angertal Skizentrum | [JPEG](https://www.gasteinertal.com/webcam/angertal/current/1200.jpg) | [Webcam](https://www.gasteinertal.com/webcam/angertal.html) |

## Woher kommen die Daten?

Die Daten stammen direkt aus den offiziellen öffentlichen Quellen des Landes
Salzburg und der Region Gasteinertal:

- Wasserstand: [Salzburg Wasser / Hydro](https://www.salzburg.gv.at/wasser/hydro/grafiken/data.json)
- Temperatur Schlossalm: [Salzburger Lawinenlagebericht / Station.js](https://www.salzburg.gv.at/lawine/Station.js)
- Temperatur und Niederschlag Bad Gastein: [GeoSphere Austria Data Hub, 10-Minuten-Stationsdaten](https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-10min)
- Wetterwarnungen: [ZAMG-Warnseiten Bad Gastein](http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/badgastein/), [Bad Hofgastein](http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/bad_hofgastein/) und [Dorfgastein](http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/dorfgastein/)
- Webcams: [gasteinertal.com](https://www.gasteinertal.com/webcam/)

Die Nutzung der Integration erfolgt auf eigene Verantwortung. Verfügbarkeit,
Aktualität und Richtigkeit der externen Daten können nicht garantiert werden.

## Installation (HACS-konform)

1. HACS in Home Assistant öffnen.
2. Unter "Integrationen" nach `Gasteinertal` suchen.
3. Die Integration installieren.
4. Home Assistant neu starten.
5. In `Einstellungen → Geräte & Dienste → Integration hinzufügen` die
   Integration `Gasteinertal` hinzufügen.

Alternative manuell:

1. `custom_components/gasteinertal` in dein Home-Assistant-Verzeichnis kopieren.
2. Home Assistant neu starten.
3. Integration hinzufügen.

## HACS-Repository-Status

Dieses Repository ist als HACS-kompatible Custom Integration aufgebaut:

- `hacs.json` vorhanden
- `custom_components/gasteinertal/manifest.json` vorhanden
- Ordnerstruktur entspricht dem HACS-Standard
- Home Assistant Branding liegt in `custom_components/gasteinertal/brand/` und benötigt Home Assistant 2026.3 oder neuer

## Lizenz

MIT (oder nach Wunsch anpassen).
