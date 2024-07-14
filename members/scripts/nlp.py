import spacy

# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

def extract_keyword(sentence):
    # Extract keywords using spaCy
    doc = nlp(sentence)
    keywords = []
    for token in doc:
        if token.pos_ == "NOUN" and not any(word in token.text.lower() for word in ["price","today","today's","cost", "value","fruit","fruits"]):
            keywords.append(token.text)
    return keywords

