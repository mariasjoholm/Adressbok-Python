#Funktion för att validera formuläret 
import streamlit as st             #
from datetime import date          # för att kunna ha födelsedatum som datatyp för testpersonerna 
from email.utils import parseaddr  # Hjälpfunktion för att dela upp och kontrollera e-postadresser 

#Validerar email: Att det finns ett snabel a samt en ändelse efteråt. 
def is_valid_email(email: str) -> bool:
    return email == "" or '@' in parseaddr(email)[1]
def is_valid_telephone(phoneNumber: str)->bool: 
    if not phoneNumber: 
        return True
    try:
        if phoneNumber.startswith('+'): 
            int(phoneNumber[1:])
        else: 
            int (phoneNumber)
        return True
    except ValueError:
        return False
    
def validate_contact(firstName:str, telephone:str,email:str, birthday)->bool: 
    valid = True
    if not firstName or len(firstName)<2:
        st.error('You must write a first name with at least two characters')
        valid = False
    if not is_valid_telephone(telephone):
        st.error('Telephone number can only contain digits and optional + first')
        valid = False
    if not is_valid_email(email):
        st.error('You must write a valid email address')
        valid = False
    if birthday is not None and birthday >= date.today():
        st.error ("The birthday cannot be today or after today")
        valid = False
    return valid