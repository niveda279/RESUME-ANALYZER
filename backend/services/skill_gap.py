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
    },
    "Business Analyst": {
        "SQL": "Critical",
        "Jira": "Critical",
        "Requirements Gathering": "High",
        "Agile": "High",
        "Excel": "High",
        "UML": "Moderate",
        "User Stories": "Moderate"
    },
    "ML Engineer": {
        "Python": "Critical",
        "PyTorch": "Critical",
        "TensorFlow": "Critical",
        "Scikit-Learn": "High",
        "Docker": "High",
        "MLOps": "Moderate",
        "MLflow": "Moderate"
    },
    "Product Manager": {
        "Product Roadmap": "Critical",
        "User Research": "Critical",
        "Agile": "High",
        "Jira": "High",
        "Figma": "Moderate",
        "Product Strategy": "Moderate"
    },
    "Cyber Security Specialist": {
        "Network Security": "Critical",
        "Penetration Testing": "Critical",
        "SIEM": "High",
        "Wireshark": "High",
        "Firewalls": "High",
        "Cryptography": "Moderate",
        "Vulnerability Assessment": "Moderate"
    },
    "Cloud Architect": {
        "AWS": "Critical",
        "Azure": "Critical",
        "Terraform": "High",
        "Kubernetes": "High",
        "CloudFormation": "High",
        "Microservices": "Moderate",
        "Serverless": "Moderate"
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
        "Kubernetes": "Set up a local Minikube cluster and deploy a microservices architecture.",
        "PyTorch": "Take the PyTorch Deep Learning course. Build and train neural nets for computer vision or NLP.",
        "TensorFlow": "Complete the TensorFlow Developer Certificate course and build standard models.",
        "Scikit-Learn": "Build machine learning pipelines using Scikit-Learn for preprocessing, classifier training, and validation.",
        "MLOps": "Familiarize yourself with MLOps concepts like model registry, CI/CD for ML, and drift monitoring.",
        "MLflow": "Learn how to use MLflow to track experiments, log model parameters, and register trained models.",
        "Jira": "Learn how to manage backlogs, set up sprints, and write developer tasks and bugs in Jira.",
        "Agile": "Get certified in Scrum/Agile (e.g. PSM I) or learn Agile lifecycle management workflows.",
        "Requirements Gathering": "Practice interviewing stakeholders, cataloging requirements, and mapping specifications.",
        "Excel": "Complete an advanced Excel training course covering pivot tables, INDEX-MATCH, and macros.",
        "UML": "Draw system logic mappings, activity flows, and class definitions using UML diagram standards.",
        "User Stories": "Practice writing high-quality User Stories with detailed User Value statements and Acceptance Criteria.",
        "Product Roadmap": "Read product management case studies, define MVPs, and practice roadmapping with tools like Productboard.",
        "User Research": "Learn user interview techniques, survey design, and how to analyze qualitative user feedback.",
        "Figma": "Learn core Figma features including autolayout, components, and interactive prototypes for design design.",
        "Product Strategy": "Understand metrics frameworks like North Star, and study strategy templates (e.g., SWOT, Lean Canvas).",
        "Network Security": "Study CompTIA Security+ materials, firewall configurations, and secure networking architectures.",
        "Penetration Testing": "Register on HackTheBox or TryHackMe, and practice attacking simulated vulnerabilities using Metasploit.",
        "SIEM": "Learn how to collect and analyze security logs using open platform systems like Splunk or ELK Stack.",
        "Wireshark": "Practice capturing networks packets, inspecting headers, and filtering traffic sequences on Wireshark.",
        "Firewalls": "Configure firewalls policies, rule evaluation chains, and intrusion prevention setups.",
        "Cryptography": "Understand cryptographic concepts such as symmetric/asymmetric encryption, hashing, and TLS certs.",
        "Vulnerability Assessment": "Learn how to scan ports and analyze configurations using networks scanners like Nessus.",
        "AWS": "Study for the AWS Certified Solutions Architect Associate exam, deploying EC2, RDS, VPC, and S3 resources.",
        "Azure": "Study for Azure Solutions Architect certifications and deploy virtual machines, storage, and AKS.",
        "Terraform": "Write Infrastructure as Code configurations to deploy cloud resources in AWS or Azure.",
        "CloudFormation": "Learn how to write JSON/YAML CloudFormation templates to provision standard AWS architectures.",
        "Microservices": "Understand microservice design patterns (e.g., API gateway, CQRS) and backend communications (REST, gRPC, queues).",
        "Serverless": "Build serverless microservices using AWS Lambda, API Gateway, and DynamoDB."
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
