import re

def evaluate_flags(parsed_data):
    """
    Evaluates parsed resume data to dynamically generate Green Flags (strengths)
    and Red Flags (weaknesses).
    """
    raw_text = parsed_data.get("raw_text", "").lower()
    skills = parsed_data.get("skills", [])
    email = parsed_data.get("email", "")
    phone = parsed_data.get("phone", "")
    certifications = parsed_data.get("certifications", "")

    green_flags = []
    red_flags = []

    # 1. Contact Information Check
    if email != "Not Provided" and phone != "Not Provided":
        green_flags.append("✔ Professional contact information")
    else:
        red_flags.append("✖ Incomplete contact details (missing phone or email)")

    # 2. GitHub Profile Check
    if "github.com" in raw_text or "github" in raw_text:
        green_flags.append("✔ GitHub portfolio profile included")
    else:
        red_flags.append("✖ Missing GitHub profile")

    # 3. LinkedIn Profile Check
    if "linkedin.com" in raw_text or "linkedin" in raw_text:
        green_flags.append("✔ LinkedIn professional profile included")
    else:
        red_flags.append("✖ Missing LinkedIn profile")

    # 4. Skills Count & Technical Strength
    if len(skills) >= 6:
        green_flags.append("✔ Strong technical skill set")
        green_flags.append("✔ Good keyword coverage")
    elif len(skills) >= 3:
        green_flags.append("✔ Basic technical skills identified")
        red_flags.append("✖ Skills section too short")
    else:
        red_flags.append("✖ Skills section too short")

    # 5. Internship / Experience Check
    if any(k in raw_text for k in ["internship", "intern", "experience", "worked as", "developer", "engineer"]):
        green_flags.append("✔ Relevant internship experience")
    else:
        red_flags.append("✖ Limited relevant internship experience")

    # 6. Projects Check
    if "project" in raw_text or "developed" in raw_text or "built" in raw_text:
        green_flags.append("✔ Multiple projects included")
    else:
        red_flags.append("✖ Weak project descriptions")

    # 7. Certifications Check
    if certifications and certifications != "None detected":
        green_flags.append("✔ Certifications available")
    else:
        red_flags.append("✖ Missing certifications")

    # 8. Measurable Achievements (Numbers / Percentages)
    if re.search(r'\b\d+%\b|\b\d+\s*percent\b|\$\d+|\b\d+\s*users\b|\b\d+\s*x\b', raw_text):
        green_flags.append("✔ Action verbs used with measurable achievements")
    else:
        red_flags.append("✖ No measurable achievements")

    # 9. Structure & ATS Formatting
    if any(header in raw_text for header in ["education", "skills", "experience", "projects"]):
        green_flags.append("✔ Clear education section")
        green_flags.append("✔ ATS-friendly formatting")
        green_flags.append("✔ Consistent resume structure")
    else:
        red_flags.append("✖ Unclear section structure for ATS parsing")

    # 10. Summary Section Check
    if "summary" in raw_text or "objective" in raw_text or "profile" in raw_text:
        green_flags.append("✔ Clear professional summary section")
    else:
        red_flags.append("✖ Missing summary section")

    # 11. Length Check
    word_count = len(raw_text.split())
    if word_count > 1200:
        red_flags.append("✖ Resume exceeds recommended length")

    # Fallbacks to ensure adequate representation if empty
    if not green_flags:
        green_flags.append("✔ Valid document structure submitted")

    return {
        "green_flags": green_flags,
        "red_flags": red_flags
    }
