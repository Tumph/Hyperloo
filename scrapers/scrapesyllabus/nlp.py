import spacy
from spacy.training.example import Example
import random
# Load a blank English model
nlp = spacy.blank("en")

# Add a text classification pipeline
textcat = nlp.add_pipe("textcat")

# Add labels
textcat.add_label("SYLLABUS")
textcat.add_label("NOT_SYLLABUS")

# Training data
TRAIN_DATA = [
    ("Homework 1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Homework 2", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Homework 3", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Homework 4", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Homework 5", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Assignment 1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Assignment 2", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Assignment 3", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Project 1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Project 2", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Project 3", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Quiz 1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Quiz 2", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Quiz 3", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Quiz 4", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Quiz 5", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Midterm Review", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Midterm Review Session", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Final Review", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Final Review Session", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lecture Notes", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lecture Slides", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Tutorial 1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Tutorial 2", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Tutorial 3", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Tutorial 4", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Tutorial 5", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Policies", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Grading Criteria", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Office Hours", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Instructor's Contact Information", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lecture Video", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lecture Audio", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Discussion Forum", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Weekly Announcements", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Discussion Board Post", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Extra Credit Assignment", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Group Project", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Group Presentation", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Student Feedback Form", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Research Paper", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Peer Review", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Peer Evaluation", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Semester Project", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Semester Report", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Survey", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Grade Distribution", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Schedule of Classes", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Calendar", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Prerequisites", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Syllabus Overview", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Instructor's Bio", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course FAQs", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lecture Time and Location", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Class Participation", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Schedule Changes", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Resources", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Electric Charges & Forces", {"cats": {"SYLLABUS": 1.0}}),
    ("Electric Field (1)", {"cats": {"SYLLABUS": 1.0}}),
    ("Electric Field & Capacitors", {"cats": {"SYLLABUS": 1.0}}),
    ("Gauss’s Law", {"cats": {"SYLLABUS": 1.0}}),
    ("Electrostatic Potential", {"cats": {"SYLLABUS": 1.0}}),
    ("Electric Field & Potential", {"cats": {"SYLLABUS": 1.0}}),
    ("Current & Resistance", {"cats": {"SYLLABUS": 1.0}}),
    ("Magnetic Field", {"cats": {"SYLLABUS": 1.0}}),
    ("Ampere’s Law", {"cats": {"SYLLABUS": 1.0}}),
    ("Electromagnetic Induction", {"cats": {"SYLLABUS": 1.0}}),
    ("Inductors", {"cats": {"SYLLABUS": 1.0}}),
    ("Electromagnetic Fields & Waves", {"cats": {"SYLLABUS": 1.0}}),
    ("Conic Sections", {"cats": {"SYLLABUS": 1.0}}),
    ("Composition of Functions, Inverses and Symmetry", {"cats": {"SYLLABUS": 1.0}}),
    ("Piecewise-Defined and Heaviside Functions", {"cats": {"SYLLABUS": 1.0}}),
    ("Inequalities", {"cats": {"SYLLABUS": 1.0}}),
    ("Partial Fractions", {"cats": {"SYLLABUS": 1.0}}),
    ("Trigonometric, Hyperbolic and Inverse Trig Functions", {"cats": {"SYLLABUS": 1.0}}),
    ("Working with Sines & Cosines", {"cats": {"SYLLABUS": 1.0}}),
    ("Sequences", {"cats": {"SYLLABUS": 1.0}}),
    ("Limits and Proving Limits", {"cats": {"SYLLABUS": 1.0}}),
    ("Continuity", {"cats": {"SYLLABUS": 1.0}}),
    ("IVT/EVT", {"cats": {"SYLLABUS": 1.0}}),
    ("Differentiation Rules, Implicit / Logarithmic Differentiation, Derivatives on Inverse Functions", {"cats": {"SYLLABUS": 1.0}}),
    ("Local/Global Extreme & Optimization Problems", {"cats": {"SYLLABUS": 1.0}}),
    ("Curve Sketching", {"cats": {"SYLLABUS": 1.0}}),
    ("Intro to Integration, Riemann Sums", {"cats": {"SYLLABUS": 1.0}}),
    ("The Definite Integral", {"cats": {"SYLLABUS": 1.0}}),
    ("FTC1 & FTC2", {"cats": {"SYLLABUS": 1.0}}),
    ("Indefinite Integrals", {"cats": {"SYLLABUS": 1.0}}),
    ("Method of Substitution", {"cats": {"SYLLABUS": 1.0}}),
    ("Integration by Parts (IBP)", {"cats": {"SYLLABUS": 1.0}}),
    ("Areas between Curves, Average Values", {"cats": {"SYLLABUS": 1.0}}),
    ("Trig Substitutions", {"cats": {"SYLLABUS": 1.0}}),
    ("Integration of Rational Functions", {"cats": {"SYLLABUS": 1.0}}),
    ("Arc Length, Surface Area and Volume of Revolution", {"cats": {"SYLLABUS": 1.0}}),
    ("Improper Integrals", {"cats": {"SYLLABUS": 1.0}}),
    ("Polar Coordinates, Areas and Arc Length in Polar Coordinates", {"cats": {"SYLLABUS": 1.0}}),
    ("Labs", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lab 1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lab 2", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lab 3", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lab 4", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Midterm", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Final", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Laptop/Computer access to LEARN", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("1- R.D. Knight, 'Physics for Scientists & Engineers,' 5th edition, Pearson, 2023", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp. 2-9", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §1.2.3, 2.2, 2.4", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp 11-26", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §1.1.5, 7.5", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp 26-54", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §1.3, 2.6, 2.7, 9.1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp 82-90", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §5.1, 5.3, 5.4, 5.5", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp 91-106", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §5.2, 5.6, 5.7, 6.1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp 107–118", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §6.2, 6.3, 7.1", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp 119-136", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §7.3, 7.4, 8.2, 8.4", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp 136-154", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §7.5, 8.3, 8.7, 8.8", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes, pp 156-173", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Guichard §7.7, 11.1, 11.2, 11.3", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Notes by David Harmsworth", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Calculus - Early Transcendentals by D. Guichard", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Posted on LEARN", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Fundamentals of Digital Logic with VHDL Design, 4th Ed.– Brown and Vranesic", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Recommended", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Print (Login): $109.95; E-Text (Vitalsource): $98.23 for lifetime and $70.17 for 180 days", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Labs (see Note #1 below)", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Midterm (see Note #2 below)", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Final (see Note #3 below)", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course introduction and overview", {"cats": {"SYLLABUS": 1.0}}),
    ("1.1 Vectors in Rn", {"cats": {"SYLLABUS": 1.0}}),
    ("1.2 Linear Combinations", {"cats": {"SYLLABUS": 1.0}}),
    ("1.3 The Norm and the Dot Product", {"cats": {"SYLLABUS": 1.0}}),
    ("1.4 Vector Equations of Lines and Planes", {"cats": {"SYLLABUS": 1.0}}),
    ("1.5 The Cross Product in R3", {"cats": {"SYLLABUS": 1.0}}),
    ("1.6 The Scalar Equation of Planes in R3", {"cats": {"SYLLABUS": 1.0}}),
    ("1.7 Projections", {"cats": {"SYLLABUS": 1.0}}),
    ("2.1 Introduction and Terminology", {"cats": {"SYLLABUS": 1.0}}),
    ("2.2 Solving Systems of Linear Equations", {"cats": {"SYLLABUS": 1.0}}),
    ("2.3 Rank", {"cats": {"SYLLABUS": 1.0}}),
    ("2.4 Homogeneous Systems of Linear Equations", {"cats": {"SYLLABUS": 1.0}}),
    ("3.1 Matrix Algebra", {"cats": {"SYLLABUS": 1.0}}),
    ("3.2 The Matrix-Vector Product", {"cats": {"SYLLABUS": 1.0}}),
    ("3.3 The Matrix Equation Ax=b", {"cats": {"SYLLABUS": 1.0}}),
    ("3.4 Matrix Multiplication", {"cats": {"SYLLABUS": 1.0}}),
    ("3.5 Matrix Inverses", {"cats": {"SYLLABUS": 1.0}}),
    ("4.1 Spanning Sets", {"cats": {"SYLLABUS": 1.0}}),
    ("4.2 Geometry of Spanning Sets", {"cats": {"SYLLABUS": 1.0}}),
    ("4.3 Linear Dependence and Linear Independence", {"cats": {"SYLLABUS": 1.0}}),
    ("4.4 Subspaces of Rn", {"cats": {"SYLLABUS": 1.0}}),
    ("4.5 Bases and Dimension", {"cats": {"SYLLABUS": 1.0}}),
    ("4.6 Fundamental Subspaces of a Matrix", {"cats": {"SYLLABUS": 1.0}}),
    ("5.1 Matrix Transformations and Linear Transformations", {"cats": {"SYLLABUS": 1.0}}),
    ("5.3 Operations on Linear Transformations", {"cats": {"SYLLABUS": 1.0}}),
    ("5.4 Inverses of Linear Transformations", {"cats": {"SYLLABUS": 1.0}}),
    ("5.5 The Kernel and the Range", {"cats": {"SYLLABUS": 1.0}}),
    ("6.1 Determinants and Invertibility", {"cats": {"SYLLABUS": 1.0}}),
    ("6.2 Elementary Row and Column Operations", {"cats": {"SYLLABUS": 1.0}}),
    ("6.3 Properties of Determinants", {"cats": {"SYLLABUS": 1.0}}),
    ("7.1 Basic Operations", {"cats": {"SYLLABUS": 1.0}}),
    ("7.2 Conjugate and Modulus", {"cats": {"SYLLABUS": 1.0}}),
    ("7.3 Polar Form", {"cats": {"SYLLABUS": 1.0}}),
    ("7.4 Complex Polynomials", {"cats": {"SYLLABUS": 1.0}}),
    ("7.5 Complex nth Roots", {"cats": {"SYLLABUS": 1.0}}),
    ("8.1 Introduction", {"cats": {"SYLLABUS": 1.0}}),
    ("8.2 Computing Eigenvalues and Eigenvectors", {"cats": {"SYLLABUS": 1.0}}),
    ("8.3 Eigenspaces", {"cats": {"SYLLABUS": 1.0}}),
    ("8.4 Diagonalization", {"cats": {"SYLLABUS": 1.0}}),
    ("8.5 Powers of Matrices", {"cats": {"SYLLABUS": 1.0}}),
    ("Additional topics at the discretion of the instructor (as time permits)", {"cats": {"SYLLABUS": 1.0}}),
    ("Linear Algebra for Engineering Fall 2024 Course Notes", {"cats": {"SYLLABUS": 1.0}}),
    ("Required text provided on LEARN", {"cats": {"SYLLABUS": 1.0}}),
    ("Linear Algebra with Applications by Keith Nicholson", {"cats": {"SYLLABUS": 1.0}}),
    ("Optional text provided on LEARN", {"cats": {"SYLLABUS": 1.0}}),
    ("Midterm", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Midterm", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Tentative Course Schedule", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Major Topic*", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Introduction & Review", {"cats": {"SYLLABUS": 1.0}}),
    ("Frequency Response", {"cats": {"SYLLABUS": 1.0}}),
    ("Operational Amplifiers", {"cats": {"SYLLABUS": 1.0}}),
    ("Operational Amplifiers", {"cats": {"SYLLABUS": 1.0}}),
    ("Introduction", {"cats": {"SYLLABUS": 1.0}}),
    ("Diodes", {"cats": {"SYLLABUS": 1.0}}),
    ("Diodes", {"cats": {"SYLLABUS": 1.0}}),
    ("Op Amps", {"cats": {"SYLLABUS": 1.0}}),
    ("Step Response", {"cats": {"SYLLABUS": 1.0}}),
    ("Step Response", {"cats": {"SYLLABUS": 1.0}}),
    ("Frequency Response", {"cats": {"SYLLABUS": 1.0}}),
    ("MOSFET Introduction & DC Analysis", {"cats": {"SYLLABUS": 1.0}}),
    ("MOSFET Amplifiers", {"cats": {"SYLLABUS": 1.0}}),
    ("Diodes", {"cats": {"SYLLABUS": 1.0}}),
    ("MOSFET Amplifiers", {"cats": {"SYLLABUS": 1.0}}),
    ("CMOS Logic", {"cats": {"SYLLABUS": 1.0}}),
    ("Applied Linear Systems", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Calculus for Electrical Engineering", {"cats": {"SYLLABUS": 1.0}}),
    ("Circuit Theorems and Techniques", {"cats": {"SYLLABUS": 1.0}}),
    ("Nonlinear Dynamics in Electrical Circuits", {"cats": {"SYLLABUS": 1.0}}),
    ("Control System Stability Analysis", {"cats": {"SYLLABUS": 1.0}}),
    ("Quantum Computing Algorithms", {"cats": {"SYLLABUS": 1.0}}),
    ("Biomolecular Engineering", {"cats": {"SYLLABUS": 1.0}}),
    ("Solid-State Physics of Semiconductor Devices", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Materials for Nanoelectronics", {"cats": {"SYLLABUS": 1.0}}),
    ("Computational Fluid Dynamics for Aerospace", {"cats": {"SYLLABUS": 1.0}}),
    ("Finite Element Analysis in Structural Engineering", {"cats": {"SYLLABUS": 1.0}}),
    ("Geomechanics and Rock Fracture Mechanics", {"cats": {"SYLLABUS": 1.0}}),
    ("Biomedical Signal Processing", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Image Processing for Computer Vision", {"cats": {"SYLLABUS": 1.0}}),
    ("Microfabrication for MEMS Devices", {"cats": {"SYLLABUS": 1.0}}),
    ("Wireless Communication Systems and Design", {"cats": {"SYLLABUS": 1.0}}),
    ("Thermal Transport in Nanomaterials", {"cats": {"SYLLABUS": 1.0}}),
    ("Multi-Agent Systems in Artificial Intelligence", {"cats": {"SYLLABUS": 1.0}}),
    ("Deep Learning for Robotics", {"cats": {"SYLLABUS": 1.0}}),
    ("Optical Metrology in Material Characterization", {"cats": {"SYLLABUS": 1.0}}),
    ("Bioinformatics Algorithms", {"cats": {"SYLLABUS": 1.0}}),
    ("Embedded Systems for IoT Applications", {"cats": {"SYLLABUS": 1.0}}),
    ("Data Analytics for Healthcare", {"cats": {"SYLLABUS": 1.0}}),
    ("Electromagnetic Wave Propagation", {"cats": {"SYLLABUS": 1.0}}),
    ("Robotic Manipulation and Grasping", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Signal Processing for Communication Systems", {"cats": {"SYLLABUS": 1.0}}),
    ("High-Energy Particle Physics", {"cats": {"SYLLABUS": 1.0}}),
    ("Structural Optimization Methods", {"cats": {"SYLLABUS": 1.0}}),
    ("Bioelectromagnetics", {"cats": {"SYLLABUS": 1.0}}),
    ("Quantum Cryptography and Security", {"cats": {"SYLLABUS": 1.0}}),
    ("Fluid-Structure Interaction in Biomechanics", {"cats": {"SYLLABUS": 1.0}}),
    ("Applied Cryptography in Computer Networks", {"cats": {"SYLLABUS": 1.0}}),
    ("High-Performance Computing for Computational Chemistry", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Algorithms in Machine Learning", {"cats": {"SYLLABUS": 1.0}}),
    ("Computational Neuroscience", {"cats": {"SYLLABUS": 1.0}}),
    ("Power Electronics for Electric Vehicles", {"cats": {"SYLLABUS": 1.0}}),
    ("Computational Geometry and Computer Graphics", {"cats": {"SYLLABUS": 1.0}}),
    ("Nanophotonics and Plasmonics", {"cats": {"SYLLABUS": 1.0}}),
    ("Computational Biology and Systems Biology", {"cats": {"SYLLABUS": 1.0}}),
    ("Space Robotics and Autonomous Navigation", {"cats": {"SYLLABUS": 1.0}}),
    ("Analog and Digital Communication Theory", {"cats": {"SYLLABUS": 1.0}}),
    ("Hydrodynamics of Coastal Systems", {"cats": {"SYLLABUS": 1.0}}),
    ("Electrochemical Energy Storage Systems", {"cats": {"SYLLABUS": 1.0}}),
    ("Geospatial Data Analysis for Engineering", {"cats": {"SYLLABUS": 1.0}}),
    ("Acoustics and Vibration in Mechanical Systems", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Network Security", {"cats": {"SYLLABUS": 1.0}}),
    ("Climate Change Modeling and Simulations", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Microbial Biotechnology", {"cats": {"SYLLABUS": 1.0}}),
    ("Robust Control in Autonomous Systems", {"cats": {"SYLLABUS": 1.0}}),
    ("High-Performance Computing in Fluid Mechanics", {"cats": {"SYLLABUS": 1.0}}),
    ("Photovoltaic Systems Design and Analysis", {"cats": {"SYLLABUS": 1.0}}),
    ("Optoelectronics and Quantum Dots", {"cats": {"SYLLABUS": 1.0}}),
    ("Cellular and Molecular Neuroscience", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Robotics for Manufacturing", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Computational Physics", {"cats": {"SYLLABUS": 1.0}}),
    ("Biodegradable Polymers for Biomedical Applications", {"cats": {"SYLLABUS": 1.0}}),
    ("Computer Vision for Autonomous Vehicles", {"cats": {"SYLLABUS": 1.0}}),
    ("Quantum Optics and Information Processing", {"cats": {"SYLLABUS": 1.0}}),
    ("Bioengineering of Smart Materials", {"cats": {"SYLLABUS": 1.0}}),
    ("Thermodynamics of Complex Systems", {"cats": {"SYLLABUS": 1.0}}),
    ("Advanced Heat Transfer Techniques", {"cats": {"SYLLABUS": 1.0}}),
]


random.shuffle(TRAIN_DATA)
train_size = int(0.8 * len(TRAIN_DATA))  # 80% for training
train_data = TRAIN_DATA[:train_size]
test_data = TRAIN_DATA[train_size:]

# Initialize the model
nlp.initialize()

# Convert training data into spaCy Example format
train_examples = []
for text, annotations in train_data:
    doc = nlp.make_doc(text)  # Create a spaCy Doc
    example = Example.from_dict(doc, annotations)  # Create an Example
    train_examples.append(example)

# Training loop
for i in range(25):  # Train for 20 epochs
    losses = {}
    nlp.update(train_examples, drop=0.2, losses=losses)
    print(f"Losses at iteration {i}: {losses}")

# Save the model
nlp.to_disk("syllabus_classifier2")

nlp = spacy.load("syllabus_classifier2")
test_examples = []
for text, annotations in test_data:
    doc = nlp.make_doc(text)  # Create a spaCy Doc
    example = Example.from_dict(doc, annotations)  # Create an Example
    test_examples.append(example)

# Evaluate the model
correct = 0
for example in test_examples:
    doc = nlp(example.text)  # Get the predicted doc
    predict = 0# 0 is syllabus
    if(doc.cats["SYLLABUS"]<0.5):
        predict = 1
    actual = 0
    if "NOT" in str(example.reference.cats):
        actual = 1
    if actual == predict:  # Compare the predicted and true categories
        correct += 1

accuracy = correct / len(test_examples)
print(f"Accuracy on test data: {accuracy}")



#nlp = spacy.load("syllabus_classifier")
text = "Operational Amplifiers"
doc = nlp(text)
print(doc.cats)  # Output classification scores
