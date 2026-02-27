
# Adressbok i Python

Detta är en kontaktapplikation utvecklad i Python med Streamlit. Applikationen gör det möjligt att skapa, redigera, ta bort, söka och spara kontakter med JSON som lagringsformat.

## Översikt

Projektet visar hur man kan strukturera en mindre Python applikation med tydlig uppdelning mellan användargränssnitt, validering, lagring och sökfunktion.

Användargränssnittet är byggt med Streamlit. Kontaktdata lagras lokalt i en JSON fil. Födelsedatum hanteras genom att konverteras mellan datatypen datetime.date och ISO format när data sparas och laddas.

## Funktioner

Applikationen innehåller stöd för att lägga till nya kontakter, redigera befintliga kontakter samt ta bort kontakter. Det finns även en sökfunktion som använder flera nivåer av matchning för att öka träffsäkerheten.

Validering sker vid inmatning av förnamn, telefonnummer, e postadress och födelsedatum. Födelsedatum är frivilligt men om det anges måste det vara ett datum före dagens datum.

Kontaktdata sparas permanent i en JSON fil vilket gör att informationen finns kvar när applikationen startas om.

## Söklogik

Sökningen sker stegvis.

1. Exakt matchning
2. Prefixmatchning per ord
3. Delsträngsmatchning per ord
4. Fuzzy matchning vid icke exakta lösningar, baserad på jämförelse med hjälp av `difflib`

Denna struktur gör att sökningen både är flexibel och tillförlitlig.

## Projektstruktur

Projektet består av följande delar.

### Filer i rotmappen

`app.py` innehåller huvudapplikationen och användargränssnittet.  
`storage_json.py` ansvarar för att läsa och skriva JSON samt konvertera datum.  
`validation.py` innehåller logik för inmatningskontroll.  
`test_contacts.py` innehåller initial testdata.  
`style.css` innehåller anpassad styling.  
`contacts.json` skapas automatiskt och lagrar sparade kontakter.

### Mappar

`util` innehåller `util_fuzz.py` som ansvarar för fuzzy sökning.  
`Images` innehåller applikationens headerbild.

### Återställning av testkontakter

Om du vill återställa den ursprungliga testdatan stoppar du applikationen och tar bort filen contacts.json. När applikationen startas igen skapas en ny fil automatiskt med testkontakter.

## Installation och körning

### Klona repositoryt

Se till att klona repositoryt med url 

### Skapa och aktivera virtuell miljö
python -m venv .venv
.\.venv\Scripts\Activate.ps1

### Installera beroenden
pip install streamlit

### Starta applikationen
python -m streamlit run app.py
