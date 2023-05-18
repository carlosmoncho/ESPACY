from flask import Flask, render_template, request
import spacy
from langdetect import detect

app = Flask(__name__)

@app.route("/")
def login():
    return render_template('index.html')

@app.route("/process",  methods = ["GET", "POST"])
def users():
    results = []
    num_of_results = 0
    if request.method == 'POST':
        rawtext = request.form["rawtext"]
        lang = detect(rawtext)

        if lang == "en":
            nlp = spacy.load("en_core_web_sm")
        elif lang == "es":
            nlp = spacy.load("es_core_news_sm")
        else:
            nlp = spacy.load("en_core_web_sm")

        taskoption = request.form["taskoption"]
        if taskoption == "organization":
            labels = ["ORG"] if lang == "en" else ["ORG"]
        elif taskoption == "person":
            labels = ["PERSON"] if lang == "en" else ["PER"]
        elif taskoption == "date":
            labels = ["DATE"] if lang == "en" else ["DATE"]
        elif taskoption == "money":
            labels = ["MONEY"] if lang == "en" else ["MONEY"]
        elif taskoption == "location":
            labels = ["GPE"] if lang == "en" else ["LOC"]
        else:
            labels = ["ORG", "PERSON", "DATE", "MONEY", "GPE"] if lang == "en" else ["ORG", "PER", "DATE", "MONEY", "LOC"]
        
        doc = nlp(rawtext)
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
        results = [ent.text for ent in doc.ents if ent.label_ in labels]
        num_of_results = len(results)
    return render_template('index.html', results=results, num_of_results=num_of_results)

if __name__ == '__main__':
    app.run(debug = True)
