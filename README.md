# 🧩 CSV to JSON Converter

Malý Python nástroj pro převod CSV souborů do formátu JSON s možností výběru konkrétních sloupců.

## 🛠 Co program umí

- Načíst CSV soubor z adresáře `./CSVs`
- Automaticky detekovat správné kódování (např. `utf-8`, `cp1250` atd.)
- Vypsat náhled a názvy sloupců
- Nechat uživatele vybrat, které sloupce chce převést
- Odfiltrovat chybějící data (prázdné řádky)
- Uložit výstup jako JSON do `./JSONs/result.json`
- Všechno s přehledným výstupem díky knihovně [`rich`](https://github.com/Textualize/rich)

## ▶️ Jak spustit

1. Ujisti se, že máš složky `CSVs` a `JSONs` ve stejné úrovni jako skript.
2. Nahraj svůj `.csv` soubor do složky `CSVs`
3. Spusť program:

```bash
python csv_to_json.py
```

4. Zadej název souboru (bez `.csv`) a pak vyber sloupce oddělené čárkou.

## 🧩 Ukázka použití

```text
Enter CSV file name (without .csv): users
✅ Loaded successfully using encoding: cp1250
seznam sloupcu: ['Jméno', 'Příjmení', 'Email', 'Věk']

Enter selected columns: Jméno, Email
💾 Uloženo do /cesta/k/JSONs/result.json
```

## 🐍 Požadavky

- Python 3.10+
- Knihovny: `pandas`, `rich`

Instalace:

```bash
pip install pandas rich
```

## 📁 Struktura složek

```
.
├── csv_to_json.py
├── CSVs/
│   └── users.csv
├── JSONs/
│   └── result.json
```

## ✅ Výhody

- Funguje s různými kódováními CSV (včetně češtiny)
- Jednoduché použití
- Rychlá konverze pro potřeby analýzy nebo migrace dat

