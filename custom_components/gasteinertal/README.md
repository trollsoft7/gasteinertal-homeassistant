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

## Webcams

Die Integration bietet die folgenden Webcam-Ansichten an:

- Bad Hofgastein
- Haitzingalm
- Kühhager
- Bad Gastein
- Sportgastein

Quellen:

- https://www.gasteinertal.com/webcam/badhofgastein/current/1200.jpg
- https://www.gasteinertal.com/webcam/haitzingalm/current/1200.jpg
- https://www.gasteinertal.com/webcam/kuehhager/current/1200.jpg
- https://www.gasteinertal.com/webcam/badgastein/current/1200.jpg
- https://www.gasteinertal.com/webcam/sportgastein/current/1200.jpg

## Nutzung

Nach dem Kopieren in `custom_components/gasteinertal` und einem Neustart von Home Assistant erscheint die Integration unter `Einstellungen → Geräte & Dienste → Integration hinzufügen`.
