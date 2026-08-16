from typing import List, Dict, Any

# A predefined competency mapping for common roles.
# Each role maps to a list of required skills with a priority level.
# Priorities: "Critical", "High", "Moderate", "Low"
COMPETENCY_MAPPING = {
    "Data Scientist": {
        "Python": "Critical",
        "Machine Learning": "Critical",
        "SQL": "High",
        "Statistics": "High",
        "Data Visualization": "Moderate",
        "Deep Learning": "Moderate",
        "NLP": "Low"
    },
    "Software Engineer": {
        "Python": "Critical",
        "Java": "Critical",
        "Data Structures": "Critical",
        "Algorithms": "High",
        "Git": "High",
        "System Design": "Moderate",
        "SQL": "Moderate"
    },
    "Web Developer": {
        "HTML": "Critical",
        "CSS": "Critical",
        "JavaScript": "Critical",
        "React": "High",
        "Node.js": "High",
        "Git": "Moderate",
        "SQL": "Moderate"
    },
    "Data Analyst": {
        "SQL": "Critical",
        "Excel": "Critical",
        "Python": "High",
        "Tableau": "High",
        "Data Cleaning": "Moderate",
        "Statistics": "Moderate"
    },
    "DevOps Engineer": {
        "Linux": "Critical",
        "Docker": "Critical",
        "Kubernetes": "High",
        "CI/CD": "High",
        "AWS": "High",
        "Python": "Moderate",
        "Bash": "Moderate"
    }
}

# A generic fallback if the role isn't explicitly mapped
DEFAULT_COMPETENCIES = {
    "Communication": "Critical",
    "Problem Solving": "Critical",
    "Project Management": "High",
    "Agile": "Moderate"
}

def get_required_skills(role: str) -> Dict[str, str]:
    """Return the required skills and priorities for a given role."""
    # Find a matching role (case-insensitive and partial match)
    for key, skills in COMPETENCY_MAPPING.items():
        if key.lower() in role.lower() or role.lower() in key.lower():
            return skills
    return DEFAULT_COMPETENCIES

def get_actionable_suggestion(skill: str, priority: str, role: str) -> str:
    """Generate a specific improvement suggestion based on the missing skill."""
    suggestions = {
        "Python": f"Take an advanced Python course focusing on {role} applications. Practice on LeetCode or Kaggle.",
        "SQL": "Practice complex SQL queries involving window functions and CTEs on platforms like HackerRank.",
        "Machine Learning": "Build end-to-end ML projects (e.g., predicting housing prices) and deploy them.",
        "Deep Learning": "Learn PyTorch or TensorFlow and implement a basic neural network for image or text classification.",
        "React": "Create a portfolio website or a complex single-page application to demonstrate state management.",
        "Java": "Build a scalable backend API using Spring Boot to showcase enterprise-level skills.",
        "Docker": "Containerize a small web application and write a multi-stage Dockerfile.",
        "Kubernetes": "Set up a local Minikube cluster and deploy a microservices architecture."
    }
    
    default_suggestion = f"Identify top resources or courses online to build foundational knowledge in {skill}. Start a small side project to apply it practically."
    return suggestions.get(skill, default_suggestion)

def analyze_skill_gap(candidate_skills: List[str], predicted_role: str) -> Dict[str, Any]:
    """
    Compare candidate skills with required skills for the role.
    Categorize gaps and provide suggestions.
    """
    # Normalize candidate skills to lower case for comparison
    candidate_skills_lower = [s.lower().strip() for s in candidate_skills]
    
    required_skills = get_required_skills(predicted_role)
    
    matched_skills = []
    missing_skills = []
    priority_gaps = []
    
    total_score = 0
    max_score = 0
    
    priority_weights = {
        "Critical": 4,
        "High": 3,
        "Moderate": 2,
        "Low": 1
    }
    
    for req_skill, priority in required_skills.items():
        weight = priority_weights.get(priority, 1)
        max_score += weight
        
        # Check if required skill is in candidate's skills
        # Doing a basic substring match to account for slight variations (e.g. "React.js" vs "React")
        is_matched = any(req_skill.lower() in cs or cs in req_skill.lower() for cs in candidate_skills_lower)
        
        if is_matched:
            matched_skills.append({"skill": req_skill, "priority": priority})
            total_score += weight
        else:
            missing_skills.append({"skill": req_skill, "priority": priority})
            if priority in ["Critical", "High"]:
                priority_gaps.append({
                    "skill": req_skill, 
                    "priority": priority,
                    "suggestion": get_actionable_suggestion(req_skill, priority, predicted_role)
                })
                
    match_percentage = 0
    if max_score > 0:
        match_percentage = round((total_score / max_score) * 100, 2)
        
    return {
        "predicted_role": predicted_role,
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "priority_gaps": priority_gaps
    }
