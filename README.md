## Program pro výpočet výsledků přeboru škol

Automaticky spočítá body pro jednotlivá školní družstva
Program pracuje s výsledky z aplikace MeOS exportovanými ve formátu OE2010 ("Kramer")

### Použití
1. Nainstalovat Python verze 3 nebo vyšší (https://www.python.org/), při instalaci zaškrtnout možnost "Add Python 3.x to PATH".
2. Z *MeOS* exportovat výsledky do CSV ve formátu OE2010 bez mezičasů.
3. Pro jednoduchost stáhnout soubor prebor_skol.py do stejné složky s výsledky.
4. Spustit příkazovou řádku ve složce se souborem **prebor_skol.py**.
5. Příkazem ```prebor_skol.py -f "cesta/k/souboru/s/vysledky.csv"``` spustit program
6. Pokud je vše ok, vytvoří se ve složce s programem soubor **vysledky_skoly.txt** a soubor vysledky_body.csv s bodovými zisky jednotlivců
