# Gasteinertal Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

<img src="https://raw.githubusercontent.com/trollsoft7/gasteinertal-homeassistant/main/assets/gasteinertal-icon.svg" alt="Gasteinertal Icon" width="180" />

Home Assistant Custom Integration für Live-Daten aus dem Gasteinertal:

- Wasserstand der Gasteiner Ache in Bad Hofgastein
- Lufttemperatur auf der Schlossalm / Gastein Berg
- 5 Live-Webcams aus dem Feriengebiet

## Entitäten

### `sensor.wasserstand_gasteiner_ache`
- Quelle: https://www.salzburg.gv.at/wasser/hydro/grafiken/data.json
- Wert: `values.W["15m.Cmd.WiskiWeb"].v`
- Station: `Bad Hofgastein`
- Einheit: `cm`

### `sensor.temperatur_gastein_berg`
- Quelle: https://www.salzburg.gv.at/lawine/Station.js
- Wert: `measuredData.values.LT`
- Station: `badhofgastein_schlossalm`
- Einheit: `°C`

### Webcams
- Bad Hofgastein
- Haitzingalm
- Kühhager
- Bad Gastein
- Sportgastein

## Woher kommen die Daten?

Die Daten stammen direkt aus den offiziellen öffentlichen Quellen des Landes
Salzburg und der Region Gasteinertal:

- Wasserstand: Salzburg Wasser / Hydro
- Bergtemperatur: Lawinenlage / Stationen Salzburg
- Webcams: gasteinertal.com

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

## Lizenz

MIT (oder nach Wunsch anpassen).
