# Create a TextCategorizer component
# config = Config({"exclusive_classes": True, "architecture": "simple_cnn"})
# textcat = nlp.add_pipe("textcat", config=config)

# # Add labels
# textcat.add_label("SYLLABUS")
# textcat.add_label("NOT_SYLLABUS")

# # Convert training data into spaCy format
# examples = [Example(nlp.make_doc(text), annotations) for text, annotations in TRAIN_DATA]

# # Training loop
# optimizer = nlp.initialize()
# for i in range(10):  # Train for 10 epochs
#     losses = {}
#     nlp.update(examples, drop=0.2, losses=losses)
#     print(f"Losses at iteration {i}: {losses}")

# # Save the model
# nlp.to_disk("syllabus_classifier")
