from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
import re

def calculate_match(resume_text, job_text):
    """
    Calculate overall similarity match score between resume and job description
    using TF-IDF vectorization and cosine similarity.
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(similarity[0][0] * 100, 2)

def extract_skills(text, skills_list, threshold=80, debug=False):
    """
    Robust skill extraction with optional debug output:
    - Normalize text and skills for comparison
    - Try whole-phrase (word-boundary) match first
    - Then check that all words in the skill appear in the text (order independent)
    - Fallback: fuzzy partial ratio against the text
    Returns skills in their original casing as provided in skills_list.
    """
    text = text.replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    text_lower = text.lower()

    if debug:
        print("[extract_skills] normalized text:", text_lower)

    found_skills = []
    for skill in skills_list:
        skill_clean = skill.strip()
        if not skill_clean:
            if debug:
                print(f"[extract_skills] skipping empty skill entry")
            continue
        skill_lower = skill_clean.lower()

        if debug:
            print(f"[extract_skills] checking skill: '{skill_clean}' (normalized: '{skill_lower}')")

        # Short skills (<=3) use whole-word match
        if len(skill_lower) <= 3:
            if re.search(rf'\b{re.escape(skill_lower)}\b', text_lower):
                if debug:
                    print(f"[extract_skills] matched (short whole-word): {skill_clean}")
                found_skills.append(skill_clean)
            else:
                if debug:
                    print(f"[extract_skills] no match (short whole-word) for: {skill_clean}")
            continue

        # First try exact whole-phrase match (case-insensitive)
        if re.search(rf'\b{re.escape(skill_lower)}\b', text_lower):
            if debug:
                print(f"[extract_skills] matched (whole-phrase): {skill_clean}")
            found_skills.append(skill_clean)
            continue

        # Next, check that all words in the skill appear somewhere in the text (order independent)
        skill_words = [w for w in re.findall(r"\w+", skill_lower) if w]
        if skill_words and all(w in text_lower for w in skill_words):
            if debug:
                print(f"[extract_skills] matched (all words present): {skill_clean}")
            found_skills.append(skill_clean)
            continue

        # Fallback: fuzzy partial ratio (skill vs. text) which can find substrings
        score = fuzz.partial_ratio(skill_lower, text_lower)
        if debug:
            print(f"[extract_skills] fuzzy score for '{skill_clean}': {score}")
        if score >= threshold:
            if debug:
                print(f"[extract_skills] matched (fuzzy): {skill_clean} (score={score})")
            found_skills.append(skill_clean)
        else:
            if debug:
                print(f"[extract_skills] no match for: {skill_clean}")

    return found_skills
