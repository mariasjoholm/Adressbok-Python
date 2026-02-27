import json
from datetime import date 

#Tar emot en dictionary(en kontakt i detta fall) returnerar en ny dictionary som kan sparas som JSON 
def to_json(person:dict)-> dict:

    #Kopierar en dictionary så vi inte ändrar orginalet och hämtar birthday direkt från dictionary
    personCopy = person.copy()
    getBirthday = personCopy.get("birthday")
    
    # Om birthday är ett date-object så görs det om till JSON eftersom JSON inte kan spara date object
    # Alltså gör vi om det till text (YYYY-MM-DD)
    if isinstance(getBirthday, date):
        personCopy['birthday'] = getBirthday.isoformat()
    else:
        personCopy['birthday'] = None
        
    return personCopy
    
# Gör om en JSON laddad kontakt till Pythonformat igen
def to_python(person:dict)->dict: 
    #    När vi laddar från JSON är birthday text. Här gör vi om den till ett riktigt date objekt igen.
    personCopy = person.copy()
    getBirthday = personCopy.get('birthday')
    
    if isinstance(getBirthday,str) and getBirthday:
        personCopy['birthday'] = date.fromisoformat(getBirthday)
    else: 
        personCopy['birthday'] = None
    
    return personCopy

#Läser hela JSON filen path returnerar en lista med contacts 
def load_contacts_json(path: str)->list[dict]:
    try:
        with open(path,'r',encoding='utf-8') as file: 
            data = json.load(file)
    #Om det inte finns en lista returnera en tom lista 
        if not isinstance(data,list): 
            return []
        
        # Gör om varje kontakt från JSON-format till Python-format
        return [to_python(personCopy) for personCopy in data]
    
    # Hantera file not found och filen är tom eller trasig 
    except FileNotFoundError: 
        return[]
    
    except json.JSONDecodeError: 
        return []
    
#Sparar alla kontakter till JSON filen, detta tar emot en lista med dictionarys(kontakter) och skriver över json filen med nya värden 
def save_contacts_json(path:str, contacts:list[dict])->None: 

    data = [to_json(personCopy) for personCopy in contacts]
    with open(path,'w',encoding='utf-8')as file: 
        json.dump(data,file,ensure_ascii=False,indent=2)
    