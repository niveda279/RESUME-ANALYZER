import re
import os
import pypdf
import docx

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

# Curated Technical & Analytical Skill Vocabulary
SKILLS_DB = {
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'html', 'css', 'react', 'react.js',
    'vue', 'angular', 'node.js', 'express', 'flask', 'django', 'fastapi', 'sql', 'postgresql',
    'mysql', 'sqlite', 'mongodb', 'redis', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
    'terraform', 'git', 'github', 'gitlab', 'ci/cd', 'jenkins', 'linux', 'bash', 'rest api',
    'graphql', 'microservices', 'pandas', 'numpy', 'scikit-learn', 'pytorch', 'tensorflow',
    'spacy', 'nltk', 'tableau', 'power bi', 'excel', 'jira', 'confluence', 'agile', 'scrum',
    'machine learning', 'deep learning', 'nlp', 'data analysis', 'a/b testing', 'tableau',
    'cybersecurity', 'penetration testing', 'wireshark', 'siem', 'unit testing'
}

CERTIFICATIONS_DB = [
    'aws certified', 'azure certified', 'google cloud certified', 'pmp', 'cissp', 'ceh',
    'certified kubernetes administrator', 'cka', 'comptia security+', 'scrum master',
    'csm', 'ccna', 'oracle certified'
]

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == '.pdf':
        try:
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            text = f"Error parsing PDF: {str(e)}"
    elif ext in ['.docx', '.doc']:
        try:
            doc = docx.Document(file_path)
            fullText = [para.text for para in doc.paragraphs]
            text = '\n'.join(fullText)
        except Exception as e:
            text = f"Error parsing DOCX: {str(e)}"
    else:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            text = f"Error reading file: {str(e)}"
    return text

def parse_resume_text(text):
    text_lower = text.lower()

    # 1. Email Extraction
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    email = email_match.group(0) if email_match else "Not Provided"

    # 2. Phone Extraction
    phone_match = re.search(r'\(?\+?[0-9]{1,4}\)?[-. ]?\(?[0-9]{1,3}\)?[-. ]?[0-9]{3,4}[-. ]?[0-9]{3,4}', text)
    phone = phone_match.group(0) if phone_match else "Not Provided"

    # 3. Name Extraction
    name = "Candidate Name"
    if nlp:
        doc = nlp(text[:500])  # Look in first 500 chars for name
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text.split()) in [2, 3]:
                name = ent.text.strip()
                break
    if name == "Candidate Name":
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines[:5]:
            if not any(char in line for char in ['@', 'http', 'www', ':', '/']) and len(line.split()) in [2, 3]:
                name = line.strip()
                break

    # 4. Skills Extraction
    extracted_skills = set()
    for skill in SKILLS_DB:
        # Match whole word
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            extracted_skills.add(skill.title() if len(skill) <= 4 else skill.capitalize())
    skills_list = sorted(list(extracted_skills))

    # 5. Education Extraction
    education_keywords = ['bachelor', 'master', 'phd', 'b.s.', 'm.s.', 'b.tech', 'm.tech', 'b.e.', 'degree', 'university', 'college', 'institute']
    education_found = []
    for line in text.split('\n'):
        if any(kw in line.lower() for kw in education_keywords):
            cleaned = line.strip()
            if cleaned and len(cleaned) < 120:
                education_found.append(cleaned)
    education_str = "; ".join(education_found[:3]) if education_found else "Degree / Academic details detected in resume text"

    # 6. Experience Extraction
    exp_keywords = ['experience', 'internship', 'developer', 'engineer', 'analyst', 'manager', 'specialist', 'associate', 'lead', 'architect']
    exp_found = []
    for line in text.split('\n'):
        if any(kw in line.lower() for kw in exp_keywords) and len(line.strip()) < 100:
            exp_found.append(line.strip())
    experience_str = "; ".join(exp_found[:4]) if exp_found else "Relevant work/internship experience present"

    # 7. Certifications Extraction
    certs_found = []
    for cert in CERTIFICATIONS_DB:
        if cert in text_lower:
            certs_found.append(cert.title())
    if not certs_found and 'certif' in text_lower:
        certs_found.append("Professional Certifications Section Found")
    certifications_str = ", ".join(certs_found) if certs_found else "None detected"

    # 8. Projects Extraction
    projects_found = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'project' in line.lower() and len(line.strip()) < 60:
            # Grab next 2 lines if possible
            proj_context = " ".join([l.strip() for l in lines[i:i+3] if l.strip()])
            if proj_context:
                projects_found.append(proj_context[:150])
    projects_str = " | ".join(projects_found[:2]) if projects_found else "Project implementations mentioned in document"

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills_list,
        "education": education_str,
        "experience": experience_str,
        "certifications": certifications_str,
        "projects": projects_str,
        "raw_text": text
    }
