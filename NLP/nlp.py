import spacy
from spacy.training.example import Example
import random

# Load a blank English model
nlp = spacy.blank("en")

currentModelName = "syllabus_classifierv3"

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
    ("""Turnitin.com: Text matching software (Turnitin®) may be used to screen assignments in this course.
        Turnitin® is used to verify that all materials and sources in assignments are documented. Students'
        submissions are stored on a U.S. server, therefore students must be given an alternative (e.g.,
        scaffolded assignment or annotated bibliography), if they are concerned about their privacy and/or security.
        Students will be given due notice, in the first week of the term and/or at the time assignment details are provided,
        about arrangements and alternatives for the use of Turnitin in this course.
    It is the responsibility of the student to notify the instructor if they, in the
    first week of term or at the time assignment details are provided, wish to submit
    alternate assignment.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Academic integrity: In order to maintain a culture of academic integrity, members of the University of Waterloo
        community are expected to promote honesty, trust, fairness, respect and responsibility. [Check the Office of Academic
        Integrity for more information.]
    Grievance: A student who believes that a decision affecting some aspect of their university life has been unfair or unreasonable
    may have grounds for initiating a grievance. Read Policy 70, Student Petitions and Grievances, Section 4. When in doubt,
    please be certain to contact the department’s administrative assistant who will provide further assistance.
    Discipline: A student is expected to know what constitutes academic integrity to avoid committing an academic offence,
    and to take responsibility for their actions. [Check the Office of Academic Integrity for more information.] A student
    who is unsure whether an action constitutes an offence, or who needs help in learning how to avoid offences (e.g., plagiarism,
    cheating) or about “rules” for group work/collaboration should seek guidance from the course instructor, academic advisor, or the
    undergraduate associate dean. For information on categories of offences and types of penalties, students should refer to Policy 71,
    Student Discipline. For typical penalties, check Guidelines for the Assessment of Penalties.
    Appeals: A decision made or penalty imposed under Policy 70, Student Petitions and Grievances (other than a petition) or Policy 71,
    Student Discipline may be appealed if there is a ground. A student who believes they have a ground for an appeal should refer to Policy 72,
    Student Appeals.
    Note for students with disabilities: AccessAbility Services, located in Needles Hall, Room 1401, collaborates with all academic
    departments to arrange appropriate accommodations for students with disabilities without compromising the academic integrity of the curriculum.
    If you require academic accommodations to lessen the impact of your disability, please register with AccessAbility Services at the beginning of each academic term.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Introduction to Data Analytics Process: From Spreadsheets to R and Python 1st Edition", {"cats": {"SYLLABUS": 1.0}}),
    ("Title / Name", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Notes / Comments", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Note: Any prices provided in course outlines are best estimates based on recent online prices and do not include shipping or taxes. Prices may vary between retailers.", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Content WeekDat(s)Chapter - TopicHomeworkDue", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("DateTimeWeek 1Jan-601 - Course IntroductionHomework", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Data Management", {"cats": {"SYLLABUS": 1.0}}),
    ("Homework h4w01Jan-107:00-8:20 pmWeek 3Jan-17 - Jan-2003 - Big Picture -", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Descriptive Analytics", {"cats": {"SYLLABUS": 1.0}}),
    ("Homework h4w02Jan-177:00-8:20 pmWeek 4Jan-24 - Jan-2704 - ",  {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Segment Analysis", {"cats": {"SYLLABUS": 1.0}}),
    ("Diagnostic Analysis", {"cats": {"SYLLABUS": 1.0}}),
    ("CRISP with R", {"cats": {"SYLLABUS": 1.0}}),
    ("Each of the School of Accounting and Finance’s Program Level learning outcomes identifies a knowledge, skill or value of a financial professional. These outcomes are organized into seven areas as reflected in the chart below. They reflect the integration of all areas. All outcomes are also developed through experiential learning.This course’s learning outcomes map to the Program Level learning outcomes as follows:Intended Learning OutcomesBy the end of the course, you will be able to:", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Introduction to Data Analytics Process: From Spreadsheets to R and Python 1st Edition", {"cats": {"SYLLABUS": 1.0}}),
    ("Title / Name", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Notes / Comments", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Note: Any prices provided in course outlines are best estimates based on recent online prices and do not include shipping or taxes. Prices may vary between retailers.", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Content WeekDat(s)Chapter - TopicHomeworkDue", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("DateTimeWeek 1Jan-601 - Course IntroductionHomework", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Data Management", {"cats": {"SYLLABUS": 1.0}}),
    ("Homework h4w01Jan-107:00-8:20 pmWeek 3Jan-17 - Jan-2003", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Territorial acknowledgement: The University of Waterloo acknowledges that much of our work takes place on the traditional territory of the Attawandaron (Neutral), Anishinaabeg (Ă-nĭsh’-ē-naw-bā or Mississaugas) and Haudenosaunee (Hō-dĕ-nō-shō’-nē or Iroquois) peoples. Our main campus is situated on the Haldimand Tract, the land granted to the Six Nations (Mohawk, Cayuga, Onondaga, Oneida, Seneca and Tuscarora) that includes six miles on each side of the Grand River. Our active work toward reconciliation takes place across our campuses through research, learning, teaching, and community building, and is coordinated within the Office of Indigenous Relations (and here).""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Inclusive teaching-learning spaces: The University of Waterloo values the diverse and intersectional identities of its students, faculty, and staff. The University regards equity and diversity as an integral part of academic excellence and is committed to accessibility for all. We consider our classrooms, online learning, and community spaces to be places where we all will be treated with respect, dignity, and consideration. We welcome individuals of all ages, backgrounds, beliefs, ethnicities, genders, gender identities, gender expressions, national origins, religious affiliations, sexual orientations, ability – and other visible and nonvisible differences. We are all expected to contribute to a respectful, welcoming, and inclusive teaching- learning environment. Any member of the campus community who has experienced discrimination at the University is encouraged to seek guidance from the Office of Equity, Diversity, Inclusion and Anti-racism (EDI-R) via email at equity@uwaterloo.ca. Sexual Violence Prevention and Response Office (SVPRO), supports students at uWaterloo who have experienced, or have been impacted by, sexual violence and gender-based violence. This includes those who experienced harm, those who are supporting others who experienced harm. SVPRO can be contacted at svpro@uwaterloo.ca""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""You should be prepared to show your work. To demonstrate your learning, you should keep your rough notes, including research notes, brainstorming, and drafting notes. You may be asked to submit these notes along with earlier drafts of their work, either through saved drafts or saved versions of a document. If the use of GenAI is suspected where not permitted, you may be asked to meet with your instructor or teaching assistant (TA) to provide explanations to support the submitted material as being your original work. Through this process, if you have not sufficiently supported your work, academic misconduct allegations may be brought to the Associate Dean.

    In addition, you should be aware that the legal/copyright status of generative AI inputs and outputs is unclear. More information is available from the Copyright Advisory Committee: https://uwaterloo.ca/copyright-at-waterloo/teaching/generative-artificial-intelligence

    Students are encouraged to reach out to campus supports if they need help with their coursework including:

    Student Success Office for help with skills like notetaking and time management
    Writing and Communication Centre for assignments with writing or presentations
    AccessAbility Services for documented accommodations
    Library for research-based assignments""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Generative artificial intelligence: This course includes the independent development and practice of specific skills, such as software design and development. Therefore, the use of Generative artificial intelligence (GenAI) trained using large language models (LLM) or other methods to produce text, images, music, or code, like Chat GPT, DALL-E, or GitHub CoPilot, is not permitted in this class. Unauthorized use in this course, such as running course materials through GenAI or using GenAI to complete a course assessment is considered a violation of Policy 71 (plagiarism or unauthorized aids or assistance). Work produced with the assistance of GenAI tools does not represent the author’s original work and is therefore in violation of the fundamental values of academic integrity including honesty, trust, respect, fairness, responsibility and courage (ICAI, n.d.).""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Supremacy of the final examination grade: Any project or mid-term examination grade will be replaced by the grade on the final examination if the grade on the final examination is higher than the grade for a specific project or the mid-term examination. For example, if nothing is submitted throughout the term, your grade on the final-examination will be your final grade. This policy, however, will not be applied if a grade on a project or the mid-term examination is the result of a Policy 71 investigation.

    Extensions: There will be no extensions granted in this course. If any component of this course is missed, the missing grade will be automatically replaced by the final examination grade as described in the previous point.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Student notice of recording: It is not anticipated that any part of this course will be recorded; however, in the event of another lockdown, it may be appropriate to record activities such as tutorials. Activities for this course involve recording, in partial fulfillment of the course learning outcomes.  You will receive notification of recording via the Learning Management System (LEARN). Some technologies may also provide a recording indicator. Recordings will be managed according to the University records classification scheme, WatClass, and will be securely destroyed when no longer needed by the University. Your personal information is protected in accordance with the Freedom of Information and Protection of Privacy Act, as well as University policies and guidelines and may be subject to disclosure where required by law.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Assignment Screening
    MOSS: Source-code matching software (MOSS) may be used to screen assignments in this course. MOSS is used to verify that all source code in projects is not plagiarized from peers either from this offering or previous offerings of this course. Students' submissions are stored on a server in the United States of America at Stanford University for a period not exceeding one month, therefore students will be given an alternative of having the instructor personally investigate the similarity of their submissions with those of others students.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Each of the five projects are due on a Tuesday at 10:00 pm (22:00):
        Project 1    September 24
        Project 2    October 8
        Project 3    November 5
        Project 4    November 19
        Project 5    December 3 (last day of classes)

    Texts / Materials
    Title / Name	Notes / Comments	Required
    Course web site	https://ece.uwaterloo.ca/~ece150/	No
    Student Assessment
    Component	Value
    Final examination	F out of 100.
    Mid-term examination	M out of 100.
    Projects	Five projects, P1, P2, P3, P4 and P5, each out of 100.
    Let E = ¾F + ¼M be your examination weighted average.

    Let P = ⅕(P1 + P2 + P3 + P4 + P5) be your project average.

    If E ≥ 60, your grade is ⅔E + ⅓P.
    If E ≤ 40, your grade is E; that is, your projects do not count.
    If 40 < E < 60, your grade is E(P − E)/60 + (5E − 2P)/3; that is, the weight of your projects increases linearly from 0% to 33⅓% as your examination weighted average increases from 40 to 60.

    Projects are due at 10:00 p.m. in the day that they are marked as due (see the Tentative Course Schedule above). No late projects will be accepted.

    The mid-term examination will be held on Thursday, October 24, during the 8:30 a.m. to 10:30 a.m time slot. Seating for the mid-term examinations will be arranged through Odyssey. Students will be spread through E7 5343, E7 5353, RCH 110, RCH 204, RCH 302, STC 0010 and STC 0040.

    The final examination will be scheduled by the Registrar's Office, which will post on its website.  Seating for the final examinations will be arranged through Odyssey.

    Source code for Projects be submitted through the Marmoset""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Literal data; identifies; local variables and initialization and assignment thereof; arithmetic, comparison and logical operators; and conditional (if) statements.", {"cats": {"SYLLABUS": 1.0}}),
    ("Assignment operators; for-loops and while loops; scope of local variables; break statements; the structured programming theorem; and the call stack.", {"cats": {"SYLLABUS": 1.0}}),
    ("Libraries and function calls; writing functions; assertions; code-development strategies; writing tests and comments; and logging.", {"cats": {"SYLLABUS": 1.0}}),
    ("Debugging; binary and hexadecimal numbers; integer data types; bitwise and bit-shift operators; floating-point data types; constant variables; and the default value of parameters.", {"cats": {"SYLLABUS": 1.0}}),
    ("The structured programming theorem; the call stack; and the stack frame.", {"cats": {"SYLLABUS": 1.0}}),
    ("Reference variables, pass by reference and aliases; arrays; main memory; the call stack; and C-style strings.", {"cats": {"SYLLABUS": 1.0}}),
    ("Addresses and pointers; dynamic memory allocation including that of arrays; lifetime of dynamically allocated memory; problems with pointers; and protecting pointers with const.", {"cats": {"SYLLABUS": 1.0}}),
    ("Solving problems recursively; the class data structure; namespaces; and functions on objects.", {"cats": {"SYLLABUS": 1.0}}),
    ("Instruct computers to carry out operational tasks using the C++ language.", {"cats": {"SYLLABUS": 1.0}}),
    ("""Tentative Course Schedule
    Each full course at the University of Waterloo consists of 36 lectures spread over nominally twelve weeks of classes. These twelve weeks do not include the autumnal and winter reading weeks. If there are holidays throughout the term, there will be make-up lectures at the end of the term. For example, if the holiday was on a Friday and the make-up lecture is on a Monday, then that Monday will follow a Friday schedule. Also, the Department of Electrical and Computer Engineering cancels classes during mid-term week and, instead, offers make-up lectures. Thus, the make-up lectures before the mid-term week will speed the progression through the course material, and after mid-term week, we will be initially a lecture or two behind, but then as subsequent make-up lectures occur, we will catch up once again with the schedule below. The schedule below is "tentative" and not intended to reflect exactly what topics are covered in which week of the course.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Programming fundamentals, language syntax, simple data types, control constructs, functions, parameter passing, recursion, classes, arrays and lists, list traversals, introduction to searching and sorting algorithms, basic object-oriented design, polymorphism and inheritance, simple testing and debugging strategies, pointers and references, basic memory management.", {"cats": {"SYLLABUS": 1.0}}),
    ("""
        Thursdays, 10:30 to 1:30 except for the block 11:30 to 1:00 on September 12, October 10 and November 14 due to a departmental meeting
        Thursdays, 3:30 to 5:30, although if no one is in my office after 5:00, the instructor reserves the right to go home early
        Please note, this is for both courses Douglas teaches, so some hours may overlap with your courses. Students in Douglas's section have priority, but students in the other sections will have their questions answered, as well. Alternatively, you can call him or talk to him after class, or just drop by his office.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""
        Version
        Latest
        Class Schedule
        Instructor & TA (Teaching Assistant) Information
        Course Description
        Learning Outcomes
        Tentative Course Schedule
        Texts / Materials
        Student Assessment
        Assignment Screening
        Notice of Recording
        Administrative Policy
        University Policy
        Browse Outlines
        Log Out
        Fundamentals of Programming Fall 2024
        ECE 150
        Published Sep 13, 2024""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course Description", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Learning Outcomes", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Tentative Course Schedule", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Texts / Materials", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Student Assessment", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Assignment Screening", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Notice of Recording", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Administrative Policy", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("University Policy", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Browse Outlines", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Log Out", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Print / Save PDF
    Class Schedule
    Course	Meet Days	Meet Time	Location	Instructor(s)
    CS 240 201 [TST]	Thursday -
    Thursday
    Feb 27
    04:30PM - 06:20PM
    O. Veksler
    oveksler@uwaterloo.ca
    K. Anderson
    karen.anderson@uwaterloo.ca
    CS 240 001 [LEC]	Tuesday, Thursday -
    Tue, Thu
    Jan 6 - Apr 4
    10:00AM - 11:20AM	RCH 112
    O. Veksler
    oveksler@uwaterloo.ca
    CS 240 002 [LEC]	Tuesday, Thursday -
    Tue, Thu
    Jan 6 - Apr 4
    11:30AM - 12:50PM	RCH 112
    O. Veksler
    oveksler@uwaterloo.ca
    CS 240 101 [TUT]	Fridays -
    Fridays
    Jan 6 - Apr 4
    10:30AM - 11:20AM	MC 4040
    CS 240 102 [TUT]	Fridays -
    Fridays
    Jan 6 - Apr 4
    11:30AM - 12:20PM	MC 4040
    CS 240 103 [TUT]	Fridays -
    Fridays
    Jan 6 - Apr 4
    01:30PM - 02:20PM	MC 4058
    schedule data automatically refreshed daily
    Instructor & TA (Teaching Assistant) Information
    Instructor: Olga Veksler
    Office:	DC 2321.
    Office Hours:	Tuesdays   1:30pm - 2:30pm   In person and Online on MS Teams

    Lectures:	RCH 112   10:00am - 11:20am   Tuesdays and Thursdays
    RCH 112   11:30am - 12:50pm   Tuesdays and Thursdays
    Email:	oveksler@uwaterloo.ca
    Instructional Support Assistant (ISA): Michael Wong
    Office:	MC 4065
    Tutorials:	MC 4058   1:30pm - 2:20pm   Fridays

    Consulting Hours:	Mondays   1:30pm - 3:00pm
    Tuesdays   8:30am - 10:00am
    Thursdays   3:30pm - 4:30pm   Online on MS Teams
    Fridays   3:00pm - 4:00pm

    Additional consulting hours, in-person or online, are available by appointment (email the course account).
    Email:	cs240@uwaterloo.ca
    Instructional Support Assistant (ISA): Taebin Kim
    Office:	N/A
    Tutorials:	N/A
    Consulting Hours:	N/A
    Email:	cs240@uwaterloo.ca
    Instructional Support Assistant (ISA): Tom Iagovet
    Office:	MC 4065
    Tutorials:	N/A
    Consulting Hours:	Mondays   10:00am - 11:00am
    Fridays   9:30am - 10:30am

    All of Tom's consulting hours are in-person in MC 4065.
    Additional consulting hours, in-person or online, are available by appointment (email the course account).
    Email:	cs240@uwaterloo.ca
    Instructional Apprentice (IA): Prashanth Arun
    Office:	MC 4065
    Tutorials:	MC 4040   11:30am - 12:20am   Fridays

    Consulting Hours:	Fridays   2:00pm - 3:00pm

    Email:	cs240@uwaterloo.ca
    Instructional Apprentice (IA): Matthew Regehr
    Office:	N/A
    Tutorials:	MC 4040   10:30am - 11:20am   Fridays

    Consulting Hours:	N/A

    Email:	cs240@uwaterloo.ca
    Instructional Support Coordinator: Karen Anderson
    Office:	MC 4010
    Office Hours:	Email to set up an appointment
    Email:	kaanders@uwaterloo.ca
    Points of Contact for Common Student Questions
    Note: If you decide to e-mail the course staff, you must use your uwaterloo Quest e-mail account (WatIAM/Quest userID @uwaterloo.ca); otherwise we cannot verify who you are and are limited on what we can accept and respond to.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""The course will be graded on a scale of 0-100, with 100 being the highest possible grade. The following grading scale will be used:

    Assignments: 100% of the points will be assigned for assignments. Assignments will be graded on a scale of 0-100, with 100% being the highest possible grade. The following grading scale will be used:

    Assignments: 100% of the points will be assigned for assignments. Assignments will be graded on a scale of 0-100, with 100% being the highest possible grade. The following grading scale will be used:""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""The course will be graded on a scale of 0-100, with 100 being the highest possible grade. The following grading scale will be used:

    Assignments: 100% of the points will be assigned for assignments. Assignments will be graded on a scale of 0-100, with 100% being the highest possible grade. The following grading scale""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Help Topic	Contact
    Assignment, Missed Deadline:	We do not accept late or emailed assignments. The last files submitted before the deadline will be marked (submit early and often, even if not finished).
    If deadline is missed due to illness or other valid, verifiable reason, see Missed Work Due To Illness below.
    Assignment Marking Error:	Re-mark request, due within 10 days of release of marks on Crowdmark. See Mark Appeals instructions on Course info.
    Course Website Error:	Email CS240 ISAs
    CS240 Handouts Error:	CS240 instructors - email or check consulting hours below.
    CS240 Textbook Error:	Email Prof. Biedl (include screenshot or version-date and line number)
    Enrollment:	If Quest won't let you enroll or switch LEC or TUT sections without a permission/override number: Instructors and course staff are unable to help you -- you must see a CS academic advisor.
    Exam Seat (Midterms & Final):	Assigned seating will be available to view via Odyssey by the time of assessment
    General Course Help:	CS240 ISAs or instructors - check office hours below.
    Midterm Remarks:	See Re-mark Request instructions on Course info (the same instructions apply for Midterms with the email subject updated accordingly).
    Missed Work Due To Illness/Valid, Verifiable Reason (Assignments, Exams):	Assignments, midterms, final exam: Validation required (for MATH students see MATH VIF and all others, see Verification of Illness Services at https://uwaterloo.ca/campus-wellness/health-services/student-medical-clinic. In all cases, substitute Karen Anderson (CS 240 ISC) for references to instructor.
    AccessAbility Services (AAS) exam accommodation forms (request to write at AAS):	Submit to AAS at least 3 weeks before exam.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Introduction to widely used and effective methods of data organization, focusing on data structures, their algorithms, and the performance of these algorithms. Specific topics include priority queues, sorting, dictionaries, data structures for text processing.", {"cats": {"SYLLABUS": 1.0}}),
    ("""Course Description
    CS 240:""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""
        View requirements for CS 240

        Revised (December 11, 2013)""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Analyze, apply, and use various data structures and data-management techniques in a variety of applications
    Perform rigorous complexity analyses of simple algorithms and data structures, which includes writing correct mathematical proofs on inductively-defined structures and solving simple recurrence relations
    Compare different data-structuring techniques from the point of view of time, memory requirements, etc.
    Select a good data structure to solve a specific algorithmic problem
    Apply data structures correctly and efficiently in one or more high-level programming languages, including C++""", {"cats": {"SYLLABUS": 1.0}}),
    ("""Logistics
    Audience
    2B Computer Science students
    Normally available
    Fall, Winter, and Spring
    Related courses
    Predecessors: CS 245 (logic) or SE 212; CS 246 or 247 (programming); any of STAT 206, 230, 240 (probability)
    Successors: Most third-year CS major courses
    Conflicts: Other courses that seriously consider efficiency and correctness of fundamental data structures and their algorithms
    For official details, see the UW calendar.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Software/hardware used", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("UNIX, C++", {"cats": {"SYLLABUS": 1.0}}),
    ("""Typical reference(s)
    R. Sedgewick, """, {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Algorithms in C", {"cats": {"SYLLABUS": 1.0}}),
    (""", 3rd ed, Parts 1-4. Addison Wesley
    Required preparation
    At the start of the course, students should be able to""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Define and explain order notation; perform complexity analyses of simple algorithms
    Define "abstract data type" or ADT; explain the utility of this concept
    Perform basic computations of discrete probability and expectation
    Use mathematical induction on recursively defined structures, including finding simple errors in inductive arguments
    Prove simple properties of program fragments correct through the use of pre-conditions and post-conditions for loops and recursive calls""", {"cats": {"SYLLABUS": 1.0}}),
    ("""Design, implement, test, and debug C++ programs to solve problems requiring hundreds of lines of code
    Define the ADTs for stacks and queues; write efficient implementations in C/C++
    Describe tree structures, including binary search trees and multi-way trees; use these structures in C/C++ programs
    Describe basic sorting algorithms (including Quicksort) and implement them in C/C++
    Explain the notion of a hash table (students don't have to describe the algorithms or their efficiency)""", {"cats": {"SYLLABUS": 1.0}}),
    ("""Perform rigorous asymptotic analyses of simple algorithms and express the result using order notation; compare algorithms based on their asymptotic complexity; and prove formal results involving order notation
    Apply the priority-queue ADT to solve various application problems, implement a priority queue using heaps, and analyze the complexity of common implementations of heap operations
    Develop best-, worst- and average-case analyses of sorting algorithms, including Quicksort, and explain the ramifications of these analyses in practice; explain the basic principles of randomized algorithms and their potential advantages, specifically in the case of Quicksort; explain the difference between comparison-based sorting and non-comparison-based sorting algorithms, and when and why the latter may run faster; and apply sorting-based techniques to algorithmic problems, such as elimination of duplicates
    Develop bounded-height search trees that accommodate efficient (i.e., O(log n)) implementations of search, insert, and delete; evaluate which search tree techniques are best suited to various application scenarios (e.g., B-trees are useful for large-scale data structures stored in external memory)
    Explain the advantages and disadvantages of various hashing techniques; identify the best hashing techniques to use in a particular application scenario; and recognize when hashing techniques are preferable to other dictionary implementations
    Design data structures for real-world data (where keys are often inherently multidimensional) in such a way that common operations (including range search) can be implemented efficiently
    Design special data structures that can efficiently store and process words and strings, and select and apply a suitable technique for data compression in a specific application scenario""", {"cats": {"SYLLABUS": 1.0}}),
    ("""Basic computer model: the random-access machine
    Runtime of an algorithm: worst-case, best-case, and average-case
    Asymptotic analysis, order notation, growth rates, and complexity
    Stacks, queues, and priority queues (3 hours)
    Review of stacks and queues
    Priority queue ADT and simple implementations
    Heaps and Heapsort
    Using heaps to solve the selection problem
    Sorting and analysis of randomized algorithms (5 hours)
    Quicksort (non-randomized): worst-case, best-case, and average-case complexity
    Randomized quicksort and its analysis; application to selection and its analysis
    Lower bound on comparison-based sorting
    Non-comparison-based sorting algorithms (e.g., Counting Sort and Radix Sort)
    Search trees (5 hours)
    Dictionary ADT and simple implementations
    Binary search trees (insert and delete operations and analysis)
    Balanced search trees (insert and delete operations and analysis; instructors will normally choose two or more AVL trees, 2-3 trees, red-black trees, etc.)
    2-3-4 trees and B-trees (search, insert, and delete operations and analysis)
    Hashing (5 hours)
    Key-indexed search, simple hash functions
    Collision resolution: chaining and open addressing
    Complexity of search, insertion, and deletion
    Extendible hashing
    Range search and multidimensional dictionaries (5 hours)
    Range search in a binary search tree
    Data structures for orthogonal range search: quad trees, Kd-trees, range trees
    Algorithms and data structures for text processing (8 hours)
    Dictionaries for text strings: radix trees, tries, compressed tries, suffix tries
    String matching algorithms: brute force, finite automata, the Knuth-Morris-Pratt algorithm
    Text compression: Huffman codes, Lempel-Ziv B, Burrows-Wheeler Transform (BWT)""", {"cats": {"SYLLABUS": 1.0}}),
    ("""Learning Outcomes
    By the end of this course students should be able to:
    See Course Description above.
    Tentative Course Schedule
    Lectures are held every Tuesday and Thursday throughout the term. Students are asked to attend their assigned lecture section, as seating in the classroom is limited.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""
        Lecture slides will appear on this page. Sometimes these include animations/overlays, in case of which there will be both a Display version (with them) and a Print version (omitting them, but otherwise the same content).

        The individual chapters of the course notes are available from the protected files area. If you want further reading, a list of textbooks that cover the topics of the course well are listed below, and specific relevant areas are listed with each module.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Winter 2025 Slides
    The slides for each module will be posted as the term progresses.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Module #	Topic	Slides	Readings", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Module 0	Administrivia	M0.pdf", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Lecture_Slides.pdf 	None", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Module 1	",  {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Introduction and Asymptotic Analysis",  {"cats": {"SYLLABUS": 1.0}}),
    ("Lecture_Slides.pdf 	None", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("	M1.pdf", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Course notes Chapter 1",  {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Optional: Course notes Appendix A-B if you need a refresher.
    Optional: Goodrich & Tamassia   1.1, 1.2, 1.3
    Optional: Sedgewick    8.2, 8.3""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Priority Queues",  {"cats": {"SYLLABUS": 1.0}}),
    ("""Option 1:

    20% - 6 assignments
    30% - 2 midterm exams
    50% - final exam
    Option 2:

    10% - 6 assignments
    20% - 2 midterm exams
    70% - final exam""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Student Assessment
    There is no defined grading scheme for this course.
    Your final mark will be the best result from the following two grading schemes:""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""by S.T. Thornton and J.B. Marion

    Brooks/Cole, Cengage Learning c 2004

    (e-textbook $74.95) ISBN: 978-0-357-88612-0

    (hardcopy $257.95) ISBN-13: 978-0-534-40896-1""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Newtonian dynamics of particles and systems of particles. Oscillations. Gravity and the central force problem. Lorentz transformations and relativistic dynamics.", {"cats": {"SYLLABUS": 1.0}}),
    ("""Print / Save PDF
    Class Schedule
    Course	Meet Days	Meet Time	Location	Instructor(s)
    PHYS 263 001 [LEC]	Monday, Wednesday, Friday -
    Mon, Wed, Fri
    Jan 6 - Apr 4
    08:30AM - 09:20AM	AL 211
    M. Matsen
    mark.matsen@uwaterloo.ca
    schedule data automatically refreshed daily
    Instructor & TA (Teaching Assistant) Information
    Instructor: Mark Matsen""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("""Active and passive circuit elements, Kirchhoff's laws, mesh and nodal circuit analysis, principle of superposition; step response of first and second order networks; sinusoidal steady state analysis using complex impedance phasors; input-output relationships, transfer functions and frequency response of linear systems; operational amplifiers, operational amplifier circuits using negative or positive feedback; diodes, operational amplifier circuits using diodes; analog signal detection, conditioning and conversion systems; transducers, difference and instrumentation amplifiers, active filters, A/D and D/A conversion.""", {"cats": {"SYLLABUS": 1.0}}),
    ("In this course, students will gain an overall understanding and processes, including",  {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("sources of errors, involved in obtaining electrical analog measurements and digitally acquiring these measurements.",  {"cats": {"SYLLABUS": 1.0}}),
    ("voltage, current, resistance, capacitance, and inductance", {"cats": {"SYLLABUS": 1.0}}),
    ("The course will be graded on a scale of 0-100, with 100 being the highest possible grade. The following grading scale will be used:",  {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("techniques for analyzing simple circuits when driven by direct or alternating power sources", {"cats": {"SYLLABUS": 1.0}}),
    ("filters, transducers, pulse width modulation",  {"cats": {"SYLLABUS": 1.0}}),
    ("""Email Policy: Microsoft Teams group chat window and email are the best way to get in touch with the instructor or TA. When sending an email, remember the following: 1. Emails should be sent from your official UW email account. 2. Put SYDE 292 in the email subject line followed by a brief description of the email subject. For example, ‘SYDE 292: Question concerning ….”. 3. Sign your email with your first and last name and your student number. 4. Emails should contain professional and respectful language. 5. While we will do our best to respond to your emails as soon as possible, allow couple of hours (excluding weekends) for a response to your email. 6. If your question or concern requires a complex answer or warrants a discussion, the instructor or teaching assistant may suggest a face-to-face or e-meeting.""", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Instructor's Contact Information", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Fundamentals of Active and Passive Circuit Elements", {"cats": {"SYLLABUS": 1.0}}),
    ("Schematics, Sources, and Resistive Circuits", {"cats": {"SYLLABUS": 1.0}}),
    ("Makeup Lecture during tutorial time: Monday September 9 at 1:30pm in RCH 211", {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("4	Sept 23 – 27",  {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Circuit Analysis Techniques and Drills", {"cats": {"SYLLABUS": 1.0}}),
    ("Schematics, Sources, and Resistive Circuits Continued",{"cats": {"SYLLABUS": 1.0}}),
    ("Kirchhoff’s Current and Voltage Laws", {"cats": {"SYLLABUS": 1.0}}),
    ("""Sentence: [section 4-6]
    3	Sept 16 – 20""",  {"cats": {"NOT_SYLLABUS": 1.0}}),
    ("Capacitors in Time Domain and their Natural and Step Response", {"cats": {"SYLLABUS": 1.0}}),
    ("Source Transforms and Thevenin/Norton Equivalents", {"cats": {"SYLLABUS": 1.0}}),
    ("Circuit Analysis Techniques and Drills Continued", {"cats": {"SYLLABUS": 1.0}}),
    ("""Sentence: [section 4,5] &  Ch.4 [section 1-8]
    Assessment 1 due September 27
    5	Oct 30 – Oct 4""",  {"cats": {"NOT_SYLLABUS": 1.0}})
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
nlp.to_disk(currentModelName)


nlp = spacy.load(currentModelName)
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



nlp = spacy.load(currentModelName)
text = "Operational Amplifiers"
doc = nlp(text)
print(doc.cats)  # Output classification scores
