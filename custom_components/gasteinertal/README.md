# Gasteinertal

Home Assistant Custom Integration für Live-Daten aus dem Gasteinertal.

## Sensoren

### Wasserstand Gasteiner Ache
- Entity: `sensor.wasserstand_gasteiner_ache`
- Datenquelle: https://www.salzburg.gv.at/wasser/hydro/grafiken/data.json
- Wert: `values.W["15m.Cmd.WiskiWeb"].v`
- Einheit: `cm`
- Station: `Bad Hofgastein`

### Temperatur Schlossalm
- Entity: `sensor.temperatur_schlossalm`
- Datenquelle: https://www.salzburg.gv.at/lawine/Station.js
- Wert: `measuredData.values.LT`
- Einheit: `°C`
- Station: `badhofgastein_schlossalm`

### Temperatur Bad Gastein
- Entity: `sensor.temperatur_bad_gastein`
- Datenquelle: https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-10min
- Station: Bad Gastein, 1092 m, Stations-ID `7`
- Messwert: Lufttemperatur in 2 m Höhe (`tl`)
- Einheit: `°C`

### Niederschlag letzte 10 Min Bad Gastein
- Entity: `sensor.niederschlag_letzte_10_min_bad_gastein`
- Datenquelle: https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-10min
- Station: Bad Gastein, 1092 m, Stations-ID `7`
- Messwert: Niederschlagssumme des 10-Minuten-Intervalls (`rr`)
- Einheit: `mm`

### Niederschlag seit Jahresbeginn Bad Gastein
- Entity: `sensor.niederschlag_seit_jahresbeginn_bad_gastein`
- Datenquelle: https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1d
- Station: Bad Gastein, 1092 m, Stations-ID `7`
- Messwert: Summe der verfügbaren täglichen Niederschlagswerte (`rr`) seit Jahresanfang
- Einheit: `mm`
- Attribut `fehlende_tageswerte` zählt fehlende oder ungültige Tageswerte, die nicht mit aufsummiert werden.

## Wetterwarnungen

Die `binary_sensor.wetterwarnung_heute_*` zeigen an, ob es für den jeweiligen
Ort heute mindestens eine Warnung gibt. Attribute enthalten die höchste
Tages-Warnstufe (`0` bis `3`) und deren Farbe. Ein aktiver Sensor bedeutet
nicht zwingend, dass die Warnung gerade jetzt gilt.

- Bad Gastein: http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/badgastein/
- Bad Hofgastein: http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/bad_hofgastein/
- Dorfgastein: http://warnungen.zamg.at/html/de/heute/alle/at/salzburg/sankt_johann_im_pongau/dorfgastein/

Die ZAMG-Seiten sind derzeit nur per HTTP erreichbar; Warnungsabfragen erfolgen
daher unverschlüsselt.

## Webcams

Die Integration bietet 13 Webcam-Ansichten an. Alle Kameras liegen im
Gasteinertal:

| Kamera | Live-Bild | Kameraseite |
| --- | --- | --- |
| Bad Hofgastein | https://www.gasteinertal.com/webcam/badhofgastein/current/1200.jpg | https://www.gasteinertal.com/webcam/badhofgastein.html |
| Haitzingalm | https://www.gasteinertal.com/webcam/haitzingalm/current/1200.jpg | https://www.gasteinertal.com/webcam/haitzingalm.html |
| Kühhager | https://www.gasteinertal.com/webcam/kuehhager/current/1200.jpg | https://www.gasteinertal.com/webcam/fulseck.html |
| Bad Gastein | https://www.gasteinertal.com/webcam/badgastein/current/1200.jpg | https://www.gasteinertal.com/webcam/badgastein.html |
| Sportgastein | https://www.gasteinertal.com/webcam/sportgastein/current/1200.jpg | https://www.gasteinertal.com/webcam/sportgastein-nassfeld.html |
| Sportgastein Siglitztal | https://www.gasteinertal.com/webcam/sportgastein2/current/1200.jpg | https://www.gasteinertal.com/webcam/sportgastein-siglitztal.html |
| Bad Gastein Zentrum | https://www.gasteinertal.com/webcam/badgastein2/current/1200.jpg | https://www.gasteinertal.com/webcam/badgastein2.html |
| Schlossalm Snowcam | https://camhost1.gasteinertal.com/webcam/snowcam/current/1200.jpg | https://www.gasteinertal.com/webcam/snowcam.html |
| Golfplatz Bad Gastein | https://www.gasteinertal.com/webcam/golfgastein/current/1200.jpg | https://www.gasteinertal.com/webcam/golf.html |
| Wasserfall Bad Gastein | https://www.gasteinertal.com/webcam/wasserfall/current/816.jpg | https://www.gasteinertal.com/webcam/wasserfall-badgastein.html |
| Jungeralm Stubnerkogel | https://www.gasteinertal.com/webcam/jungeralm.jpg | https://www.gasteinertal.com/webcam/jungeralm.html |
| Dorfgastein Talabfahrt | https://camhost1.gasteinertal.com/webcam/hauserbauer/current/1200.jpg | https://www.gasteinertal.com/webcam/dorfgastein-hauserbauer.html |
| Angertal Skizentrum | https://www.gasteinertal.com/webcam/angertal/current/1200.jpg | https://www.gasteinertal.com/webcam/angertal.html |

## Nutzung

Nach dem Kopieren in `custom_components/gasteinertal` und einem Neustart von Home Assistant erscheint die Integration unter `Einstellungen → Geräte & Dienste → Integration hinzufügen`.

Die Nutzung erfolgt auf eigene Verantwortung. Aktualität, Richtigkeit und
Verfügbarkeit der externen Datenquellen können nicht garantiert werden.
