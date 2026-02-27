"""
För att använda programmet: 
1) Installera streamlit i mappen, om detta är redan gjort skippa till steg 2 

2)Aktivera virtuell miljö
Skriv detta i powershell i mappen: 
.\.venv\Scripts\Activate.ps1

3) Starta appen
Skriv sedan detta i powershell i mappen: 
python -m streamlit run app.py
"""
from contacts.test_contacts import test_contacts # Importera testkontakter 
import streamlit as st                  # Används för 
from util.util_fuzz import best_match   # Importera fuzzy funktion från util_fuzzy, bästa strängträff
from validation import validate_contact # Importera valideringsfunktionen
from storage_json import load_contacts_json, save_contacts_json
from datetime import date 

#filen för sparade kontakter 
contacts_file = 'contacts/contacts.json'

#importera style.css 
def style(path):
    with open(path) as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)  
style("style.css")

# Skapas bara första gången appen körs
if "contacts" not in st.session_state:
    
    saved = load_contacts_json(contacts_file)
    #Starta med testkontakter 
    if saved:
        st.session_state.contacts = saved
    #starta med testkontakter och skapa JSON filen direkt
    else:
        st.session_state.contacts = test_contacts.copy()
        save_contacts_json(contacts_file, st.session_state.contacts)

# Används för tillfälligt bekräftelsemeddelande
if "saved_msg" not in st.session_state:
    st.session_state.saved_msg = ""
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

contacts = st.session_state.contacts

#----- Header------------------------------------------------------------------------------- 
#Bild & titel 
st.image("Images/Orange.png", use_container_width=True)
st.title('Address book')

#----- Tabs------------------------------------------------------------------------------- 
tab_showAll, tab_addContact, tab_searchContact = st.tabs(['show all contacts','add contact', 'search'])
#Redigera en kontakt 
def edit_contact(index):
    person = st.session_state.contacts[index]

    st.markdown("#### Edit contact")
    # date_input kan inte få None i value, så vi ger den ett datum om birthday saknas
    default_birthday = person["birthday"] if person["birthday"] is not None else date.today()

    with st.form(f"editContact_form_{index}", clear_on_submit=False):
        editFirstname = st.text_input("Förnamn *", value=person["firstName"]).strip()
        editLastname = st.text_input("Efternamn", value=person["lastName"]).strip()
        editTelephone = st.text_input("Telephone number", value=person["telephone"]).strip()
        editAdress = st.text_input("Adress", value=person["adress"]).strip()
        editEmail = st.text_input("Email address", value=person["email"]).strip()

        editBirthday = st.date_input("Add birthday", value=default_birthday)
        noBirthday = st.checkbox(
            "No birthday",
            value=person["birthday"] is None,
            key=f"no_birthday_{index}"
        )
        if noBirthday:
            editBirthday = None

        editInfo = st.text_input("Information", value=person["info"]).strip()

        colA, colB = st.columns(2)
        with colA:
            cancel = st.form_submit_button("Cancel",use_container_width = True, type = "primary")
        with colB:
            save = st.form_submit_button("Save",use_container_width = True)

    if cancel:
        st.session_state.edit_index = None
        st.rerun()

    if save:
        if validate_contact(editFirstname,editTelephone,editEmail, editBirthday):
            st.session_state.contacts[index] = {
                "firstName": editFirstname,
                "lastName": editLastname,
                "telephone": editTelephone,
                "adress": editAdress,
                "email": editEmail,
                "birthday": editBirthday,
                "info": editInfo,
            }
            #spara 
            save_contacts_json(contacts_file, st.session_state.contacts)

            st.session_state.edit_index = None
            st.session_state.saved_msg = "Contact updated"
            st.rerun()

#Visa alla kontakter 
with tab_showAll: 
    if not contacts: 
      st.info("No contacts")
    else: 
        for index, person in enumerate(contacts):
            column1,column2 =st.columns([6,1])

            with column1:
                st.write(f"### {person['firstName']} {person['lastName']}")
                st.write(f"**Telefon:** {person['telephone']}")
                st.write(f"**Adress:** {person['adress']}")
                st.write(f"**E-post:** {person['email']}")
                st.write(f"**Födelsedag:** {person['birthday']}")
                st.write(f"**Information:** {person['info']}")
            if st.session_state.edit_index == index:
                edit_contact(index)

            st.divider()
            
            with column2:
                if st.button('**Remove**', key= f'delete{index}', use_container_width = True):
                    st.session_state.contacts.pop(index)
                    #spara 
                    save_contacts_json(contacts_file, st.session_state.contacts)
                    st.rerun() 
                if st.button('**Edit**', key= f'edit{index}', use_container_width = True):
                    st.session_state.edit_index =index
                    st.rerun()                               
    
# Lägg till ny kontakt
with tab_addContact: 
    if st.session_state.saved_msg:
        st.success(st.session_state.saved_msg)
        st.session_state.saved_msg = ""

    with st.form('addContact_form',clear_on_submit=True):
        firstName = st.text_input('Förnamn *').strip()
        lastName = st.text_input('Efternamn').strip()
        telephone = st.text_input('Telephone number').strip()
        adress = st.text_input('Adress').strip()
        email = st.text_input('Email address').strip()
        birthday = st.date_input('Add birthday', value= None)
        noBirthday = st.checkbox('No birthday and any selected date will be removed')
        if noBirthday: 
            birthday = None
        info = st.text_input('Information').strip()
        save = st.form_submit_button("Save")
    if save: 
        if validate_contact(firstName,telephone,email, birthday):
            st.session_state.contacts.append({
                'firstName': firstName, 
                'lastName': lastName, 
                'telephone': telephone,
                "adress": adress,
                "email": email,
                "birthday": birthday,
                "info": info})
            #spara 
            save_contacts_json(contacts_file, st.session_state.contacts) 
            # Sparar bekräftelsemeddelande och startar om appen
            st.session_state.saved_msg = "Kontakt sparad"
            st.rerun()

#Sök efter en kontakt 
with tab_searchContact:
    query = st.text_input('Search name in contactlist')
    search = st.button('Search')
    if search: 
        if not query.strip():
            st.error("Write something to search for a contact")
        else: 
            #lista för namn i sökningen
            names = [
                f"{person['firstName']} {person['lastName']}".strip()
                for person in contacts
            ]
            hit = best_match(query,names, cutoff=82)
            if hit:
                match, score, index = hit
                person = contacts[index]
                st.success(f"Contact found!")

                st.write(f"**Förnamn:** {person['firstName']}")
                st.write(f"**Efternamn:** {person['lastName']}")
                st.write(f"**Telefon:** {person['telephone']}")
                st.write(f"**Adress:** {person['adress']}")
                st.write(f"**E-post:** {person['email']}")
                st.write(f"**Födelsedag:** {person['birthday']}")
                st.write(f"**Info:** {person['info']}")
            else: 
                st.error('No contact found')