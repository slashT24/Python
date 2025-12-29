# 📄 HireFlow- Resume Screening AI (Python)

An AI-based Resume Screening system built using Python that automatically ranks resumes against a job description and identifies matched and missing skills.

This project demonstrates practical usage of NLP techniques like TF-IDF, cosine similarity, and fuzzy matching for real-world HR tech applications.

---

## 🚀 Features

- Reads multiple PDF resumes
- Calculates resume–job match score using TF-IDF & cosine similarity
- Extracts skills accurately from resumes
- Handles:
  - Short skills (Java, SQL, AWS, ML)
  - Long skills (Machine Learning, Data Analysis)
  - PDF line breaks and formatting issues
- Ranks resumes based on relevance
- Exports results to CSV
- Console-based (easy to extend to web apps)

---

## 🛠️ Tech Stack

- Python 3
- scikit-learn
- PyPDF2
- fuzzywuzzy
- Regular Expressions

