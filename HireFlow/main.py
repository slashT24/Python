import os
import csv
from resume_parser import extract_text_from_pdf
from text_preprocessing import clean_text, clean_text_for_skills
from matcher import calculate_match, extract_skills

# --- Paths ---
resume_folder = "sample_resumes/"
job_path = "job_description.txt"
skills_path = "skills.txt"

# --- Load job description ---
with open(job_path, "r", encoding="utf-8") as f:
    job_text = f.read()

# --- Load skills list ---
with open(skills_path, "r", encoding="utf-8") as f:
    skills_list = [line.strip() for line in f.readlines()]

# --- Clean job text ---
job_clean_for_tfidf = clean_text(job_text)
job_clean_for_skills = clean_text_for_skills(job_text)

print(job_clean_for_tfidf)
print('-----------------------')
print(job_clean_for_skills)
print('-----------------------')
# --- Store results ---
resume_results = []

# --- Loop through resumes ---
for resume_file in os.listdir(resume_folder):
    if resume_file.endswith(".pdf"):
        resume_path = os.path.join(resume_folder, resume_file)
        resume_text = extract_text_from_pdf(resume_path)
        
        # Clean separately for TF-IDF and skills
        resume_clean_tfidf = clean_text(resume_text)
        resume_clean_skills = clean_text_for_skills(resume_text)

        print(resume_clean_tfidf)
        print('-----------------------')
        print(resume_clean_skills)
        
        # --- Calculate match score ---
        score = calculate_match(resume_clean_tfidf, job_clean_for_tfidf)
        
        # --- Extract skills ---
        resume_skills = extract_skills(resume_clean_skills, skills_list, threshold=80)
        
        # --- Determine matched and missing skills ---
        matched_skills = list(set(resume_skills) & set(skills_list))
        missing_skills = list(set(skills_list) - set(resume_skills))
        
        resume_results.append({
            "file": resume_file,
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

# --- Sort by score descending ---
resume_results = sorted(resume_results, key=lambda x: x["score"], reverse=True)

# --- Display results ---
print("📄 Resume Ranking")
print("----------------------")
for idx, r in enumerate(resume_results, 1):
    print(f"{idx}. {r['file']}")
    print(f"   Match Score: {r['score']}%")
    print(f"   Matched Skills: {', '.join(r['matched_skills']) if r['matched_skills'] else 'None'}")
    print(f"   Missing Skills: {', '.join(r['missing_skills']) if r['missing_skills'] else 'None'}\n")

# --- Export CSV ---
def export_to_csv(results, filename="resume_ranking.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Resume File", "Match Score (%)", "Matched Skills", "Missing Skills"])
        for r in results:
            writer.writerow([
                r["file"],
                r["score"],
                ", ".join(r["matched_skills"]) if r["matched_skills"] else "None",
                ", ".join(r["missing_skills"]) if r["missing_skills"] else "None"
            ])
    print(f"✅ Results exported to '{filename}'")

export_to_csv(resume_results)
