import spacy
import re
from nltk.stem import WordNetLemmatizer

# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

# Initialize WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

wks=['fruit','price','today','tommorow','cost','value','farmer','field']
def preprocess_sentence(sentence):
    # Remove possessive markers
    sentence = re.sub(r"(\w+)'s\b", r"\1", sentence)
    return sentence

def extract_keyword(sentence):
    # Preprocess the sentence
    sentence = preprocess_sentence(sentence)
    print(sentence)
    # Extract keywords using spaCy
    doc = nlp(sentence)
    keywords = []
    for token in doc:
        # Lemmatize the token (convert to lowercase and then to its root form)
        lemma = lemmatizer.lemmatize(token.text.lower())
        # Check if the lemmatized token is in the crop list
        # if token.text=="millet": keywords.append(token.text.capitalize())

        if token.pos_ == ("NOUN" or "PROPN") and lemma not in wks:
            keywords.append(token.text.capitalize())
    return keywords

