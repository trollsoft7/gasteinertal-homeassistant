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

- Wasserstand: Salzburg Wasser / Hydro
- Bergtemperatur: Lawinenlage / Stationen Salzburg
- Webcams: gasteinertal.com

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
