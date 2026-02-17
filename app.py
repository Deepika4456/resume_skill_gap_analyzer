import streamlit as st
from utils import extract_text_from_pdf, load_skills, match_skills, categorize_score
from datetime import datetime

st.set_page_config(page_title="Resume Skill Gap Analyzer", layout="wide", initial_sidebar_state="expanded")

st.title("🚀 Resume Skill Gap Analyzer")
st.markdown("#### Analyze your resume against job descriptions and identify skill gaps")

with st.sidebar:
    st.header("⚙️ Settings")
    show_details = st.checkbox("Show Detailed Analysis", value=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Resume")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    st.subheader("📋 Job Description")
    job_description = st.text_area("Paste Job Description Here", height=200)

if resume_file and job_description:
    try:
        with st.spinner("Processing resume and job description..."):
            resume_text = extract_text_from_pdf(resume_file)
            jd_text = job_description

            skills_list = load_skills()

            if not resume_text.strip():
                st.error("❌ Could not extract text from resume. Please ensure it's a valid PDF.")
            else:
                resume_skills = match_skills(resume_text, skills_list)
                jd_skills = match_skills(jd_text, skills_list)
            
                with st.expander("🔍 Debug Info - Click to expand"):
                    st.write(f"**Total skills in database:** {len(skills_list)}")
                    st.write(f"**Resume text length:** {len(resume_text)} characters")
                    st.write(f"**Job Description text length:** {len(jd_text)} characters")
                    st.write(f"**Skills detected in Resume:** {len(resume_skills)}")
                    st.write(f"**Skills detected in JD:** {len(jd_skills)}")
                    
                   
                    st.write("**First 50 skills in database:**")
                    st.write(", ".join(skills_list[:50]))
                    
                    st.write("---")
                    st.write("**Manual Skill Tester:**")
                    test_skill = st.text_input("Enter a skill name to test if it's detected:")
                    if test_skill:
                        test_skill_lower = test_skill.lower()
                        in_resume = test_skill_lower in resume_text.lower()
                        in_jd = test_skill_lower in jd_text.lower()
                        in_database = test_skill_lower in skills_list
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            status = "✅" if in_resume else "❌"
                            st.write(f"{status} In Resume: {in_resume}")
                        with col2:
                            status = "✅" if in_jd else "❌"
                            st.write(f"{status} In JD: {in_jd}")
                        with col3:
                            status = "✅" if in_database else "❌"
                            st.write(f"{status} In Database: {in_database}")
                    
                    st.write("---")
                    st.write(f"**Resume text preview (first 300 chars):**")
                    st.text(resume_text[:300])

                if len(jd_skills) == 0:
                    st.warning("⚠️ No skills detected in job description. Make sure to mention specific skills like Python, Java, SQL, etc.")

                missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))
                extra_skills = sorted(list(set(resume_skills) - set(jd_skills)))
                matched_skills = sorted(list(set(resume_skills) & set(jd_skills)))

                match_percent = int((len(matched_skills) / len(jd_skills)) * 100) if jd_skills else 0
                match_category = categorize_score(match_percent)

                st.success("✅ Analysis Complete!")
                st.markdown("---")

                st.header("📊 Resume Match Score")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Match Score", f"{match_percent}%")
                with col2:
                    st.metric("Matched Skills", len(matched_skills))
                with col3:
                    st.metric("Missing Skills", len(missing_skills))
                with col4:
                    st.metric("Extra Skills", len(extra_skills))
                st.progress(match_percent / 100)
                st.markdown(f"**Overall Evaluation:** {match_category}")
                st.markdown("---")

                if show_details:
                    st.header("📌 Detailed Analysis")
                    
                    tab1, tab2, tab3, tab4, tab5 = st.tabs(["✅ Matched", "❌ Missing", "➕ Extra", "📋 JD Skills", "📝 Resume Skills"])
                    
                    with tab1:
                        if matched_skills:
                            st.write(f"**Found {len(matched_skills)} matching skills:**")
                            cols = st.columns(3)
                            for idx, skill in enumerate(matched_skills):
                                with cols[idx % 3]:
                                    st.write(f"✓ {skill}")
                        else:
                            st.warning("⚠️ No matching skills found. Review job description and resume.")
                    
                    with tab2:
                        if missing_skills:
                            st.write(f"**⚠️ {len(missing_skills)} skills to learn:**")
                            for i, skill in enumerate(missing_skills, 1):
                                st.write(f"{i}. **{skill}**")
                        else:
                            st.success("🎉 Perfect! You have all required skills!")
                    
                    with tab3:
                        if extra_skills:
                            st.write(f"**🌟 {len(extra_skills)} bonus skills you possess:**")
                            cols = st.columns(3)
                            for idx, skill in enumerate(extra_skills):
                                with cols[idx % 3]:
                                    st.write(f"★ {skill}")
                        else:
                            st.info("No extra skills beyond job requirements.")
                    
                    with tab4:
                        st.write(f"**All {len(jd_skills)} skills required in JD:**")
                        if jd_skills:
                            for skill in jd_skills:
                                st.write(f"• **{skill}**")
                        else:
                            st.warning("⚠️ No skills detected. Please add skill names to the job description.")
                    
                    with tab5:
                        st.write(f"**All {len(resume_skills)} skills found in Resume:**")
                        if resume_skills:
                            for skill in resume_skills:
                                st.write(f"• **{skill}**")
                        else:
                            st.warning("⚠️ No skills detected in resume.")
                st.markdown("---")
                st.subheader("💾 Export Results")
                
                export_text = f"""
Resume Skill Gap Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

MATCH SCORE: {match_percent}%
EVALUATION: {match_category}

MATCHED SKILLS ({len(matched_skills)}):
{', '.join(matched_skills) if matched_skills else 'None'}

MISSING SKILLS ({len(missing_skills)}):
{', '.join(missing_skills) if missing_skills else 'None'}

EXTRA SKILLS ({len(extra_skills)}):
{', '.join(extra_skills) if extra_skills else 'None'}

JD REQUIRED SKILLS ({len(jd_skills)}):
{', '.join(jd_skills) if jd_skills else 'None'}

RESUME FOUND SKILLS ({len(resume_skills)}):
{', '.join(resume_skills) if resume_skills else 'None'}
"""
                st.text(export_text)
                st.download_button(
                    label="Download as Text",
                    data=export_text,
                    file_name="skill_analysis.txt",
                    mime="text/plain"
                )

    except Exception as e:
        st.error(f"❌ Error processing files: {str(e)}")

else:
    st.info("👆 Please upload a resume and paste a job description to get started.")

