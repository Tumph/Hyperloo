import spacy
from tqdm import tqdm

currentmodel = "syllabus_classifierv3"

def chunker(file_path):
    nlp_classifier = spacy.load(f'./{currentmodel}')
    nlp = spacy.load("en_core_web_lg")

    nlp.disable_pipes(["ner", "tagger", "parser", "attribute_ruler", "lemmatizer"])
    nlp.enable_pipe("senter")


    with open(file_path, 'r') as file:
        text = file.read()

    max_length = nlp.max_length
    texts = [text[i:i+max_length] for i in range(0, len(text), max_length)]

    sentences = []

    truesyllabus = []

    for doc in tqdm(nlp.pipe(texts), desc="Processing Text"):
        sentences.extend([sent.text.strip() for sent in doc.sents if sent.text.strip()])

    final_sentences = []
    for sentence in sentences:
        sub_sentences = sentence.split('\n')
        final_sentences.extend([s.strip() for s in sub_sentences if s.strip()])

    for sentence in tqdm(final_sentences, desc="Classifying Sentences"):
        sentence_doc = nlp_classifier(sentence)
        print(f"Sentence: {sentence}")
        print(f"Classification Scores: {sentence_doc.cats}")
        print("\n---\n")

    for sentence in final_sentences:
        sentence_doc = nlp_classifier(sentence)
        if sentence_doc.cats.get('SYLLABUS', 0) > 0.9:
            truesyllabus.append(sentence)

    print(len(truesyllabus))
    print(truesyllabus)




# Example usage
chunker('example.txt')
