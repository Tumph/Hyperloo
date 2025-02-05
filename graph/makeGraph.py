import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
print("d")
course1_description = preprocess_text("Basic electromagnetic theory; magnetic circuits; electric circuit elements; DC circuit analysis; first-order transient response; AC circuit analysis; Diodes; Transistors: regions of operation, single-transistor amplifiers")
course2_description = preprocess_text("The diversity of invertebrate animals will be explored in this class. Topics covered in lectures and laboratory will include reproduction, development, life history, feeding, locomotion, and behaviour.")


course1_embedding = model.encode(course1_description)
course2_embedding = model.encode(course2_description)

similarity = cosine_similarity([course1_embedding], [course2_embedding])
print(f"Similarity between courses: {similarity[0][0]}")
