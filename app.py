import streamlit as st
import re
import spacy
import pickle
from bs4 import BeautifulSoup


# Load the model from the .pkl file
with open("ner_model.pkl1", "rb") as f:
    loaded_model = pickle.load(f)

# Load the spaCy NER model
nlp = loaded_model

def extract_entities(text):
    # Preprocess the text
    # text = re.sub("\n", " ", text)
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()

    # print(text)

    # Create a spaCy doc
    doc = nlp(text)
    
    # Extract entities and labels
    entity = []
    label = []
    for ent in doc.ents:
        entity.append(ent.text)
        label.append(ent.label_)
    
    # Zip the entities and labels into a dictionary
    extracted_entities = dict(zip(label, entity))
    
    result = {
            "contactInfo": {
                "customer": "",
                "contact" : "",
                "phone" : "",
                "email" : ""
            },
            "origin": {
                "city": "",
                "state" : "",
                "zipcode" : "",
                "country" : ""
            },
            "destination": {
                "city": "",
                "state" : "",
                "zipcode" : "",
                "country" : ""
            },
            "commodity" : "",
            "dimensions" : "",
            "weight" : "",
            "class" : "",
            "shipDate" : "",
            "notes" : ""
        }
    
    # Fill the extracted entities into the result dictionary
    if 'CONTACT' in extracted_entities:
        result['contactInfo']['contact'] = extracted_entities['CONTACT']
    if 'CUSTOMER' in extracted_entities:
        result['contactInfo']['customer'] = extracted_entities['CUSTOMER']
    if 'PHONE' in extracted_entities:
        result['contactInfo']['phone'] = extracted_entities['PHONE']
    if 'EMAIL' in extracted_entities:
        result['contactInfo']['email'] = extracted_entities['EMAIL']
    if 'OCITY' and "DCITY" in extracted_entities:
        if 'OCITY'in extracted_entities:
            result['origin']['city'] = extracted_entities['OCITY']
        else:
            result['destination']['city'] = extracted_entities['DCITY']
    if 'DATE' in extracted_entities:
        result['shipDate'] = extracted_entities['DATE']
    
    return result

st.title("Named Entity Recognition App")
text = st.text_area("Enter your text here", "")
if st.button("Extract"):
    entities = extract_entities(text)
    st.write("Extracted entities:", entities)
