import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

course1_description = preprocess_text("CS 137 provides an introduction to fundamental programming principles for first-year Software Engineering students. Topics include: procedures and parameter passing, arrays and structures, recursion, sorting, pointers and simple dynamic structures, space and time analysis of designs, and design methodologies.")
course2_description = preprocess_text("Analysis of linear circuits. Voltage, current, resistance, capacitance, inductance, voltage source, current source, dependent sources, Ohm's Law, Kirchhoff's Laws, nodal analysis, mesh analysis, circuit transformations, operational amplifier circuits, time response, sinusoidal steady-state response. Preparing for, conducting, and reporting of laboratory experiments.")


course1_embedding = model.encode(course1_description)
course2_embedding = model.encode(course2_description)

similarity = cosine_similarity([course1_embedding], [course2_embedding])
print(f"Similarity between courses: {similarity[0][0]}")
