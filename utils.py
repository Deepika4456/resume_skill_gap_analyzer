import PyPDF2
import re

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file with error handling."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            except:
                continue
        if not text or text.strip() == "":
            raise Exception("No text could be extracted from PDF")
        return text
    except Exception as e:
        raise Exception(f"Failed to extract PDF: {str(e)}")

# Load skills from file
def load_skills():
    """Load skills from skills.txt file."""
    try:
        with open("skills.txt", "r") as file:
            skills = [skill.strip().lower() for skill in file.readlines() if skill.strip()]
        return skills
    except FileNotFoundError:
        raise Exception("skills.txt file not found. Please create it with a list of skills.")

def match_skills(text, skills_list):
    """
    Match skills in text with case-insensitive matching.
    Uses word boundary detection for accuracy.
    """
    if not text or not skills_list:
        return []
    
    # Normalize text: convert to lowercase
    text_lower = text.lower()
    
    present_skills = []
    # Sort skills by length descending to match longer phrases first
    sorted_skills = sorted(set(skills_list), key=lambda x: len(x), reverse=True)
    
    for skill in sorted_skills:
        skill_lower = skill.strip().lower()
        if not skill_lower or len(skill_lower) < 2:
            continue
        
        try:
            # Use word boundary regex with IGNORECASE flag for reliable matching
            # This ensures we match whole words/phrases, case-insensitive
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                present_skills.append(skill_lower)
        except:
            # Fallback to simple substring if regex fails
            if skill_lower in text_lower:
                present_skills.append(skill_lower)
    
    return sorted(list(set(present_skills)))

# Categorize score
def categorize_score(score):
    """Categorize match score into levels."""
    if score >= 80:
        return "🟢 Strong Match"
    elif score >= 60:
        return "🟡 Moderate Match"
    elif score >= 40:
        return "🟠 Fair Match"
    else:
        return "🔴 Weak Match"
