import spacy
from tqdm import tqdm

currentmodel = "syllabus_classifierv3"

def classify_text_from_file(file_path):
    # Load the trained model for classification
    nlp_classifier = spacy.load(f'./{currentmodel}')

    # Load a model for sentence segmentation (e.g., en_core_web_sm)
    nlp_segmenter = spacy.load('en_core_web_sm')

    with open(file_path, 'r') as file:
        text = file.read()

    # Segment the text into sentences
    doc_segmented = nlp_segmenter(text)

    # Iterate over sentences and classify them
    for sentence in tqdm(list(doc_segmented.sents), desc="Processing Sentences"):
        # Classify the sentence using the classifier model
        sentence_doc = nlp_classifier(sentence.text)

        # Print sentence and its classification scores
        print(f"Sentence: {sentence.text}")
        print(f"Classification Scores: {sentence_doc.cats}")
        print("\n---\n")

# Example usage
classify_text_from_file('example.txt')
