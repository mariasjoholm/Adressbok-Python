
from datetime import datetime      #Datetime för datumsvalidering
from email.utils import parseaddr  # Hjälpfunktion för att dela upp och kontrollera e-postadresser
import sys                         # Ger tillgång till systemfunktioner, t.ex. avsluta programmet med sys.exit()
import time                        # Tidshantering, t.ex. pauser med time.sleep()
#import difflib                    # För att få bästa matchningen på strängar
from util.util_fuzz import best_match   # importera fuzzy funktion från util_fuzzy (bästa strängträff)
#from tabulate import tabulate      # Kräver att installera "pip install tabulate" innan man kör koden 



#Testpersoner:
contacts = [
    {"first_name": "Anna",  "last_name": "Jonsson"},
    {"first_name": "Maria", "last_name": "Sjöholm"},
    {"first_name": "Maria", "last_name": "Vestman"},
    {"first_name": "Oscar", "last_name": "Haikola"}
]

#contacts = [] #tom lista med objekt som används för inkörning utan testpersoner, vid använding:  kommentera bort testpersonerna. 

# Skriva in information om kontakt, input finns bara i terminalen 
def check_value(value: str):
    # Istället för input('first name: ) osv, utan använder metoden istället
    value = input(value).strip()
    while not value:
        print('Du glömde skriva in något\n')
        value = input(value).strip()
    return value

# Validerar datum 
def check_date(value):
    date = input(value).strip()
    while date != '':
        try:
            dt = datetime.strptime(date, '%Y:%m:%d')
            return dt.strftime('%Y:%m:%d')
        except ValueError:
            print('Skriv datum som YYYY:MM:DD\n')
            date = input(value).strip()
    return ''

#Validerar email: Att det finns ett snabel a samt en ändelse efteråt. 
def is_valid_email(email: str) -> bool:
    return '@' in parseaddr(email)[1]

# lägger till kontakter
def add_yes_or_no():
    svar = input('Do you want to add contact? yes or no?: ').strip().lower()
    while True:
        if svar == 'yes':
            return True
        elif svar == 'no':
            return False
        else:
            print('You have to write and answer')
            svar = input(
                'Do you want to add contact? yes or no?: ').strip().lower()


def add_contact():
    print('Welcome to add your new contacts information')
    print('\n')
    # varabler med metoden check_value
    first_name = check_value('First name: ')
    last_name = input('Last name: ')
    telephone = input('Telephonenumber: ')

    while not telephone.isdigit() and telephone != '':
        print('Du måste ange mobilnummer med siffror om du ska skriva ett telefonnummer')
        telephone = input('Telephonenumber: ')
    adress = input('Adress:')
    email = input('Email adress: ').strip()

    while not is_valid_email(email) and email != '':
        print('You must write an valid email adress. Write no to not writing an email\n')
        if email == 'no': 
           email = ''
        else: 
          email = input('Email adress: ').strip()
          
    birthday = check_date(
        'Birthday date with year,mouth and day 0000:00:00 : ')
    information = input('Information: ')
    print('\n')

    person = {
        'first_name': first_name,
        'last_name': last_name,
        'telephone': telephone,
        'adress': adress,
        'email': email,
        'birthday': birthday,
        'information': information
    }

    print(f""" 
    Namn: {person['first_name']} {person[last_name]}
    Telefon: {person['telephone']}
    Adress: {person['adress']}
    Epost: {person['email']}
    Födelsedag: {person['birthday']}
    Info: {person['information']}""")

    # Här avgörs om kontakten ska sparas i listan
    if add_yes_or_no():
        contacts.append(person)
        print('Your new contact is added to your contacts\n')
        main()
    else:
        print('Your contact is not saved.\n')
        main()

# Sök efter en kontakt
def search_contact():
    # Om inga kontakter, tillbaka till menyn direkt
    if not contacts:
        print('There is no contact to find you will return to main menu')
        return main()

    # Förbered en lista med fulla namn (samma ordning som contacts)
    names = [f"{p.get('first_name', '')} {p.get('last_name', '')}".strip()
             for p in contacts]

    while True:
        # Hämta söksträng från användaren
        query = input(
            'Write first name and last name of the contact to find: ').strip()

        # Hitta bästa träffen (eller None)
        hit = best_match(query, names, cutoff=82)

        if hit:
            # Plocka ut index och presentera originalnamnet snyggt 
            match_str, score, idx = hit
            person = contacts[idx]
            pretty = f"{person.get('first_name', '').strip()} {person.get('last_name', '').strip()}".strip(
            ) or match_str
            print(f'Found: {pretty}')
            # Fråga om vi ska söka igen
            while True:
                confirm = input(
                    'Do you want to search a new name? yes or no: ').strip().lower()
                if confirm == 'yes':
                    break
                elif confirm == 'no':
                    print('Back to main menu')
                    return main()
                else:
                    print('Please answer yes or no')
        else:
            # Ingen träff – fråga om ny sökning
            while True:
                again = input(
                    'Name not found, try again? yes or no: ').strip().lower()
                if again == 'yes':
                    break
                elif again == 'no':
                    print('Back to main menu')
                    return main()
                else:
                    print('Please answer yes or no')

# visa alla kontakter
def all_contacts():
    if not contacts:
        print('No contacts yet.\n')
        main()
    # enumerate är en inbyggd Python funktion som låter mig
    for index, kontaktObject in enumerate(contacts, 1):
        # loopa över en samling och samtidigt få ett löpnummer (index).
        print(f'{index}. Namn: {kontaktObject.get('first_name', '')} {kontaktObject.get('last_name', '')} '
              f'| Tel: {kontaktObject.get('telephone', '') or '-'} '
              f'| Email: {kontaktObject.get('email', '') or '-'} '
              f'| Adress: {kontaktObject.get('adress', '') or '-'} '
              f'| Birthday: {kontaktObject.get('birthday', '') or '-'} '
              f'| Info: {kontaktObject.get('information', '') or '-'}')
    print('\n')

    svar_igen = input(
        'Do you want to go to the menu yes or no?').strip().lower()

    while svar_igen != 'yes' and svar_igen != 'no':
        print('yes or no please')
        svar_igen = input('Answer:').strip().lower()
    if svar_igen == 'yes':
        main()
    else:
        print('Bye bye!')
        return
    
# Radera en kontakt 
def remove_contact():
    if not contacts:
        print('There is no contact to delete')
        return main()

    while True:
        delete_req = input(
            'Write first name and last name of the contact to delete: ').strip().lower()
        # Bygg lista med fulla namn i samma ordning som contacts
        name_list = [f"{p.get('first_name', '')} {p.get('last_name', '')}{p.get('information', '')}".strip().lower()
                     for p in contacts]

        # Ny matchning med best_match (kort och enkel) 
        hit = best_match(delete_req, name_list, cutoff=82)
        if hit:
            match_name, _, match_id = hit
        else:
            match_id = None

        if match_id is not None:
            # Visa namn snyggt från contacts istället för normaliserat
            person = contacts[match_id]
            pretty_name = f"{person.get('first_name','').strip()} {person.get('last_name','').strip()}".strip() or match_name
            print(f'Found: {pretty_name}')
            # Fråga tills vi får yes eller no
            while True:
                confirm = input('Delete this contact? yes or no: ').strip().lower()
                if confirm == 'yes':
                    contacts.pop(match_id)
                    print(f'{pretty_name} was deleted.\n')
                    return main()
                elif confirm == 'no':
                    print('Contact is not deleted, going back to main menu')
                    return main()
                else:
                    print('Please answer yes or no')
        else:
            # Namn hittades inte: fråga tills vi får yes/no
            while True:
                no_name = input('Name not found, try again? yes or no: ').strip().lower()
                if no_name == 'yes':
                    break  # gå upp och fråga efter namn igen
                elif no_name == 'no':
                    print('Contact is not deleted, going back to main menu')
                    return main()
                else:
                    print('Please answer yes or no')



# visa menyn funktion
def show_menu():
    print('Welcome to your adressbook!\n')
    print(
        '1)Search for contact\n'

        '2)Add new contact\n'

        '3)Remove an contact\n'

        '4)Show all contacts\n'

        '5)Show all birthdays in one month\n'

        '0)Close the adress book\n'
    )

# main
def main():
    show_menu()
    val = input('what can i help you with?\nAnswer: ')
    match val:
        case '1':
            print('Search for contact')
            search_contact()

        case '2':
            print('Add new contact')
            add_contact()

        case '3':
            print('Edit or Remove an contact')
            remove_contact()

        case '4':
            print('Show all contacts')
            all_contacts()

        case '5':
            print('Show all birthdays in one month')

        case '0':
            print('Closing the adress book')
            for i in range(3):
                time.sleep(1)
                print('.', end='', flush=True)
            sys.exit(0)

main()
